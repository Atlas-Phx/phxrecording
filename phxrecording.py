# Author: Phoenix Geohysics Ltd.
# Creation: 2024-08-15

# Global Constants
## The mode of operation; 0 = normal, 1 = debug.
DEBUG = 1
## JSON tags
JSON_NAME_RECSTATS = "rec_status"
JSON_NAME_ACQ = "acqtime"
JSON_NAME_START = "start"
JSON_NAME_STOP = "stop"

# Lib Dependencies
import json, struct, datetime, zoneinfo, os, math, fnmatch
from pathlib import Path

def getrecid(instid, starttime):
    """! Generate recording ID from instrument ID and start time

    @param instid Instrument ID, normally is 5 digits interger
    @param starttime The start time of the recording, unix timestamp integer
    @return Phoenix recording ID calculated from the given instrument ID and start time
    """

    start_time_str = datetime.datetime.fromtimestamp(starttime, zoneinfo.ZoneInfo("UTC")).strftime("%Y-%m-%d-%H%M%S")
    rec_id = str(instid) + "_" + start_time_str
    if len(rec_id) == 23:
        return rec_id
    else:
        return "Error: invalid result:" + rec_id

def recmeta_changestartstop(recmetajson, start=0, stop=0):
    """! Change start and/or stop time in Phoenix recmeta.json

    @param recmetajson The recmeta.json input in form of string
    @param start The new start time of the recording, unix timestamp integer
    @param stop The new stop time of the recording, unix timestamp integer
    @return The changed recmeta string
    """
    recmetajson[JSON_NAME_RECSTATS] = "completed"
    if start == 0:
        start = recmetajson[JSON_NAME_START]
    if stop == 0:
        stop = recmetajson[JSON_NAME_STOP]
    if stop > start:
        recmetajson[JSON_NAME_ACQ] = stop - start
        if start > 1325394000: # If it is later than 2012 (basic check if the number making sense)
            recmetajson[JSON_NAME_START] = start
        else:
            if DEBUG: print("start time", start, "seems wrong(earlier than 2012)")
        if stop > 1325394000:
            recmetajson[JSON_NAME_STOP] = stop
        else:
            if DEBUG: print("start time", start, "seems wrong(earlier than 2012)")
    else:
        if DEBUG: print("start time is later than stop time!")

    return recmetajson

def recmetafile_getstarttimestamp(rjfilepath):
    """! Get start time from recmeta json file

    @param rjfilepath The recmeta.json input file path
    @return Unix timestamp of start time
    """
    try:
        with open(rjfilepath, "rb") as file:
            json_file = file.read()
        rj = json.loads(json_file)
    except (IOError, OSError) as e:
        if DEBUG:
            print(e)
        return 0
    return rj[JSON_NAME_START]

def recmetafile_changestartstop(rjfilepath, savepath, start=0, stop=0):
    """! Change the recmeta stop and start time and then save to another location

    @param rjfilepath The recmeta.json input file path
    @param savepath Targeting save path of the new recmeta.json file
    @param start The new start time of the recording, unix timestamp integer
    @param stop The new stop time of the recording, unix timestamp integer
    @return How many bytes written to the targeting place
    """
    try:
        with open(rjfilepath, "rb") as file:
            json_file = file.read()
        rj = json.loads(json_file)
    except (IOError, OSError) as e:
        if DEBUG:
            print(e)
        return 0
    
    recmeta_json = recmeta_changestartstop(rj, start, stop)

    try:
        with open(savepath, "w") as file:
            return file.write(json.dumps(recmeta_json, indent="\t"))
    except (IOError, OSError) as e:
        if DEBUG:
            print(e)
        return 0
    
def datafile_modrecid(filepath, starttime):
    """! Change recording ID(start time unix timestamp) in time series data file header

    @param filepath The absolute path to the data file
    @param starttime The start time of the recording, unix timestamp integer
    @return Error message or number of bytes written
    """
    try:
        with open(filepath, "rb") as file:
            data_file = file.read()
        bin_arr = bytearray(data_file)
        struct.pack_into('I', bin_arr, 20, starttime)
        with open(filepath, 'wb') as file:
            return file.write(bytes(bin_arr))
    except (IOError, OSError) as e:
        if DEBUG:
            print(e)
        return e

def shrink_sourcefilelist(recpath, start, stop):
    """! Get a path list(relative path) of all the files required to copy for a shrinked recording

    @param recpath The absolute path to the source recording
    @param start The start time of the targeting recording, unix timestamp integer
    @param stop The stop time of the targeting recording, unix timestamp integer
    @return An array of file paths relative to the source recording path(no slash at the begining)
    """
    filelist = ["backend.log","executor.log","kern.pri","config.json","recmeta.json.bak"]
    subfolders = [ f.path for f in os.scandir(recpath) if f.is_dir() ]

    # Find all unique file extensions 
    file_extensions = set()
    for file in os.listdir(subfolders[0]):
        file_extensions.add(file.split('.')[-1])

    # Add the needed data files
    org_starttime = recmetafile_getstarttimestamp(os.path.join(recpath, "recmeta.json"))
    start_offset = start - org_starttime
    start_seq = math.floor(start_offset / 360) # 6min of data each file
    seq_len = math.floor((stop - start) / 360)
    for folder in subfolders:
        localfilelist = os.listdir(folder)
        if len(localfilelist) > 0:
            basename = Path(localfilelist[0]).stem[:17]
            for i in range(seq_len):
                for ext in file_extensions:
                    filename = (basename + f'{format(start_seq+i+1,"x"):0>8}' + '.' ).upper()
                    filename += ext
                    filelist.append(os.path.join(folder[-1], filename))
    return filelist

def shrink_destfilerename(recpath, destpath, start, stop):
    """! Rename the copied files after shrink to match the naming rules of a Phoenix recording.

    @param recpath The absolute path to the source recording
    @param destpath The absolute path to the destination recording
    @param start The start time of the targeting recording, unix timestamp integer
    @param stop The stop time of the targeting recording, unix timestamp integer
    @return Error message or finished message
    """
    subfolders = [ f.path for f in os.scandir(recpath) if f.is_dir() ]

    # Find all unique file extensions 
    file_extensions = set()
    for file in os.listdir(subfolders[0]):
        file_extensions.add(file.split('.')[-1])

    # Add the needed data files
    org_starttime = recmetafile_getstarttimestamp(os.path.join(recpath, "recmeta.json"))
    start_offset = start - org_starttime
    start_seq = int(start_offset / 360) # 6min of data each file
    seq_len = int((stop - start) / 360)
    for folder in subfolders:
        localfilelist = os.listdir(folder)
        os.chdir(os.path.join(destpath, folder[-1]))
        if len(localfilelist) > 0:
            basename = Path(localfilelist[0]).stem[:17]
            for i in range(seq_len):
                for ext in file_extensions:
                    srcfilename = (basename + f'{format(start_seq+i+1,"x"):0>8}' + '.').upper() 
                    srcfilename += ext
                    destfilename = (basename.replace(format(org_starttime, 'x').upper(), format(start, 'x')) + f'{format(i+1,"x"):0>8}' + '.').upper()
                    destfilename += ext                    
                    os.rename(srcfilename, destfilename)
    return "Rename finished."

def shrink_moddatafilerecid(destpath, start):
    """! Change all the necessary files' recording ID(start time unix timestamp) in time series data file header

    @param destpath The absolute path to the destination folder
    @param start The start time of the targeting recording, unix timestamp integer
    @return Number of files modified
    """
    subfolders = [ f.path for f in os.scandir(destpath) if f.is_dir() ]
    first_filepath = ""
    file_count = 0
    for folder in subfolders:
        found = False
        for root, dirs, files in os.walk(os.path.join(destpath,folder[-1])):
            for name in files:
                if fnmatch.fnmatch(name, "*00000001*"): #Only need the first file
                    found = True
                    first_filepath = os.path.join(root, name)
                    break
        if found: 
            datafile_modrecid(first_filepath, start)
            file_count += 1
    print(file_count, "files modified.")
    return 