# Author: Phoenix Geohysics Ltd.
# Creation: 2024-07-22

# Global Constants
## The mode of operation; 0 = normal, 1 = debug.
DEBUG = 0
## Structure sizes in bytes
MHEADER_SIZE = 16
HEADER_SIZE = 32
PAYLOAD_SIZE = 17
## JSON field names
JSON_NAME_VERSION = "version"
JSON_NAME_NUMCHAN = "numchannels"
JSON_NAME_RECID = "recordingid"
JSON_NAME_DURATION_MIN = "duration(min)"
JSON_NAME_ERROR = "error"
JSON_NAME_TEMPRETURE = "tempreture"
JSON_NAME_BATTERY_MV = "battery(mV)"
JSON_NAME_ID = "id"
JSON_NAME_MINVAL = "minvalue"
JSON_NAME_MAXVAL = "maxvalue"
JSON_NAME_AVGVAL = "avgvalue"
JSON_NAME_SAT_COUNT = "saturationcount"
JSON_NAME_MISF_COUNT = "missingframecount"
JSON_NAME_CHAN_STATS = "channelstats"
JSON_NAME_PER_MIN_STATS = "perminstats"

import json, struct, datetime

# Util function
def extractinfo(stat_bin):
    """! Extract essential information (file version, recording ID, number of channels, duration) from stat file binary

    @param stat_bin bytearray of the stat file
    """
    data_dict = {}
    file_version = stat_bin[1]
    data_dict[JSON_NAME_VERSION] = file_version

    instrument_id = stat_bin[2:10].decode().replace('\u0000', '')
    start_time_bin = bytes(stat_bin[10:14])
    start_time = struct.unpack('I', start_time_bin)[0]
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d-%H%M%S")
    data_dict[JSON_NAME_RECID] = instrument_id + "_" + start_time_str

    num_channels = stat_bin[14]
    data_dict[JSON_NAME_NUMCHAN] = num_channels

    num_stat_units = (len(stat_bin) - MHEADER_SIZE) / (HEADER_SIZE + PAYLOAD_SIZE * num_channels) 
    data_dict[JSON_NAME_DURATION_MIN] = int(num_stat_units)
    return data_dict

# Header info function
def getstatsinfo(filepath):
    """! Read binary stats file from a local path and return a dictionary of header data
    Note: This function will return the total duration of the stat file.

    @param filepath the path to the stats binary file
    """
    try:
        with open(filepath, "rb") as file:
            stat_bin = bytearray(file.read())
    except (IOError, OSError) as e:
        return {JSON_NAME_ERROR:e}
    
    if stat_bin[0]!=0x16:
        if DEBUG:
            print("File " + filepath + " is not a phoenix stats file!")
        return {JSON_NAME_ERROR:"File " + filepath + " is not a phoenix stats file!"}
    
    if stat_bin[1]!=0x01:
        if DEBUG:
            print("File " + filepath + " version " + stat_bin[1] + " is not supported!")
        return {JSON_NAME_ERROR:"File " + filepath + " version " + stat_bin[1] + " is not supported!"}
    
    data_dict = extractinfo(stat_bin)
    return data_dict

# Major data extraction function
def getstatsdata(filepath, start=0, stop=0):
    """! Read binary stats file from a local path and return a dictionary of desired data
    Note: This function renturns the duration that the resulting file contains, in case of specified start and stop, this
          duration will be different with the original stat file.

    @param filepath the path to the stats binary file
    @param start the start minute from the begining to begin reading the stat data
    @param stop the end minute from the begining to end the reading, resulting data will include the stop minute.
    """
    if stop < start:
        if DEBUG:
            print("Invalid start and stop time: " + str(start) + " " + str(stop))
        return {JSON_NAME_ERROR:"Invalid start and stop time: " + str(start) + " " + str(stop)}

    with open(filepath, "rb") as file:
        stat_bin = bytearray(file.read())
    if stat_bin[0]!=0x16:
        if DEBUG:
            print("File " + filepath + " is not a phoenix stats file!")
        return {JSON_NAME_ERROR:"File " + filepath + " is not a phoenix stats file!"}
    
    if stat_bin[1]!=0x01:
        if DEBUG:
            print("File " + filepath + " version " + stat_bin[1] + " is not supported!")
        return {JSON_NAME_ERROR:"File " + filepath + " version " + stat_bin[1] + " is not supported!"}
    
    data_dict = extractinfo(stat_bin)
    if stop > data_dict[JSON_NAME_DURATION_MIN]:
        if DEBUG:
            print("Invalid stop time: " + str(stop))
        return {JSON_NAME_ERROR:"Invalid stop time: " + str(stop)}

    stats_block_size = HEADER_SIZE + PAYLOAD_SIZE * data_dict[JSON_NAME_NUMCHAN]
    data_array = []
    if stop == 0:
        stop = data_dict[JSON_NAME_DURATION_MIN]
    else:
        data_dict[JSON_NAME_DURATION_MIN] = stop - start
    for i in range(start, stop):
        data_position = MHEADER_SIZE + stats_block_size * i + (HEADER_SIZE - 4)
        per_min_dict = {}
        per_min_dict[JSON_NAME_TEMPRETURE] = stat_bin[data_position]
        battery_bin = bytes(stat_bin[data_position + 1 : data_position + 3])
        per_min_dict[JSON_NAME_BATTERY_MV] = struct.unpack('H', battery_bin)[0]
        channel_array = []
        for j in range(data_dict[JSON_NAME_NUMCHAN]):
            data_position_j = MHEADER_SIZE + stats_block_size * i + HEADER_SIZE + PAYLOAD_SIZE * j
            id=stat_bin[data_position_j]
            channel_dict = {JSON_NAME_ID:id}
            minv_bin = bytes(stat_bin[data_position_j + 1 : data_position_j + 5])
            channel_dict[JSON_NAME_MINVAL] = struct.unpack('f', minv_bin)[0]
            maxv_bin = bytes(stat_bin[data_position_j + 5 : data_position_j + 9])
            channel_dict[JSON_NAME_MAXVAL] = struct.unpack('f', maxv_bin)[0]
            avgv_bin = bytes(stat_bin[data_position_j + 9 : data_position_j + 13])
            channel_dict[JSON_NAME_AVGVAL] = struct.unpack('f', avgv_bin)[0]
            sat_bin = bytes(stat_bin[data_position_j + 13 : data_position_j + 15])
            channel_dict[JSON_NAME_SAT_COUNT] = struct.unpack('H', sat_bin)[0]
            mf_bin = bytes(stat_bin[data_position_j + 15 : data_position_j + 17])
            channel_dict[JSON_NAME_MISF_COUNT] = struct.unpack('H', mf_bin)[0]
            channel_array.append(channel_dict)
            #print("j "+str(j)+" "+str(id)+"  "+str(333))
        per_min_dict[JSON_NAME_CHAN_STATS] = channel_array
        data_array.append(per_min_dict)
    data_dict[JSON_NAME_PER_MIN_STATS] = data_array
    return data_dict

# JSON output Wrapper
def tojson(filepath, start=0, stop=0):
    """! Read binary stats file and then return json with needed information.

    @param filepath the path to the stats binary file
    @param start the start minute from the begining to begin reading the stat data
    @param stop the end minute from the begining to end the reading, resulting data will include the stop minute.
    """
    # get data
    data = getstatsdata(filepath, start, stop)    
    return json.dumps(data)

# JSON file writer
def tojsonfile(infilepath, outfilepath, start=0, stop=0):
    """! Read binary stats file and then output json file with needed information.

    @param infilepath the path to the stats binary file
    @param outfilepath the path to the output JSON file
    @param start the start minute from the begining to begin reading the stat data
    @param stop the end minute from the begining to end the reading, resulting data will include the stop minute.

    """
    # get data
    data = tojson(infilepath, start, stop)

    # put to json file
    try:
        with open(outfilepath, 'w') as file:
            return file.write(data)
    except (IOError, OSError) as e:
        return {JSON_NAME_ERROR:e}

# File shrinker
def shrinkto(infilepath, outfilepath, start=0, stop=0):
    """! Read binary stats file and then output shrinked binary file with new start and stop. If start time changed, new 
    recording ID will be generated.

    @param infilepath the path to the stats binary file
    @param outfilepath the path to the output binary file
    @param start the start minute from the begining to begin reading the new stat file
    @param stop the end minute from the begining to end the reading, resulting data will include the stop minute.

    @return number of bytes wrote or error message
    """
    # Check input
    if stop != 0 and stop < start:
        if DEBUG:
            print("Invalid start and stop time: " + str(start) + " " + str(stop))
        return 0
    try:
        with open(infilepath, "rb") as file:
            stat_bin = file.read()
    except (IOError, OSError) as e:
        if DEBUG:
            print("error: " + e)
        return e

    if start == stop == 0:
        if DEBUG:
            print("start and stop time both 0, copy file without changing")
        try:
            with open(outfilepath, 'wb') as file:
                return file.write(stat_bin)
        except (IOError, OSError) as e:
            if DEBUG:
                print("error: " + e)
            return e

    if DEBUG:
        print("Params checking finished. Begin to generate new file...")

    # Read data info
    data_info = extractinfo(bytearray(stat_bin))
    if not start==0:
        if stop == 0:
            data_info[JSON_NAME_DURATION_MIN] -= start
        else:
            data_info[JSON_NAME_DURATION_MIN] = stop - start + 1
    elif not stop == 0:
        data_info[JSON_NAME_DURATION_MIN] -= data_info[JSON_NAME_DURATION_MIN] - stop - 1
    
    if data_info[JSON_NAME_DURATION_MIN] == 0:
        if DEBUG:
            print("Unexpected 0 length duration")
        return 0
    
    if DEBUG:
        print("Generating new stats for", data_info[JSON_NAME_NUMCHAN], "Channels, duration", data_info[JSON_NAME_DURATION_MIN])
    stat_bin_arr = bytearray(stat_bin)
    result_array = stat_bin_arr[0:MHEADER_SIZE]

    # Need to write new start time if changed
    if start > 0:
        start_time_unix = struct.unpack_from('I', stat_bin, 10)[0]
        start_time_unix += 60 * start
        struct.pack_into('I', result_array, 10, start_time_unix)
        if DEBUG:
            print("New start time written:", struct.unpack('I', bytes(result_array[10:14]))[0])

    # Pick the data needed
    start_offset = 0
    data_block_size = HEADER_SIZE + data_info[JSON_NAME_NUMCHAN] * PAYLOAD_SIZE
    if start > 0:
        start_offset = data_block_size * (start - 1)

    stop_offset = data_block_size * (data_info[JSON_NAME_DURATION_MIN] - 1)
    if stop > 0:
        stop_offset = data_block_size * (stop - 1)
    
    current_offset = start_offset
    while current_offset <= stop_offset:
        result_array.extend(stat_bin_arr[(current_offset+MHEADER_SIZE):(current_offset+MHEADER_SIZE+data_block_size)])
        current_offset += data_block_size
    if DEBUG:
        print("Extracted", (len(result_array)-MHEADER_SIZE)/data_block_size, "min of data")

    try:
        with open(outfilepath, 'wb') as file:
            return file.write(bytes(result_array))
    except (IOError, OSError) as e:
        if DEBUG:
            print("error: " + e)
        return e