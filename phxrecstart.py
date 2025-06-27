# Author: Phoenix Geohysics Ltd.
# Creation: 2024-08-16

import phxrecording as phrec
import argparse as ap
import os

def file_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise ap.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

if __name__ == "__main__":
    parser = ap.ArgumentParser(description='A getter to get start time unix timestamp.')
    parser.add_argument('-i, --infile', dest='inpath', type=file_path,
                        help='Specify the recording path, required')
    args = parser.parse_args()

    if not args.inpath:
        print("You have to specify input stats file path!")
    else:
        print(phrec.recmetafile_getstarttimestamp(os.path.join(args.inpath,"recmeta.json")))