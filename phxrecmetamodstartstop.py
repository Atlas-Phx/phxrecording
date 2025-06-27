# Author: Phoenix Geohysics Ltd.
# Creation: 2024-08-19

import phxrecording as rec
import argparse as ap
import os

def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise ap.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
    
def out_path(path):
    if os.path.isdir(os.path.dirname(path)):
        return path
    else:
        raise ap.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

if __name__ == "__main__":
    parser = ap.ArgumentParser(description='Tool to modify start and/or stop time in Phoenix recmeta json file.')
    parser.add_argument('-i, --infile', dest='inpath', type=file_path,
                        help='Specify recmeta file path, required')
    parser.add_argument('-o, --outfile', dest='outpath', type=out_path,
                        help='Specify output json file path, required')
    parser.add_argument('-s, --start', dest='start', type=int, default=0,
                        help='New recording start time in unix timestamp')
    parser.add_argument('-e, --stop', dest='stop', type=int, default=0,
                        help='New recording stop time in unix timestamp')
    args = parser.parse_args()

    if not args.inpath:
        print("You have to specify input json file path!")
    elif not args.outpath:
        print("You have to specify output json file path!")
    else:
        print(rec.recmetafile_changestartstop(args.inpath, args.outpath, args.start, args.stop))