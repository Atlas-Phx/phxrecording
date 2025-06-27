# Author: Phoenix Geohysics Ltd.
# Creation: 2024-08-22

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
                        help='Specify the source recording path, required')
    parser.add_argument('-o, --outfile', dest='outpath', type=file_path,
                        help='Specify the destination recording path, required')
    parser.add_argument('-s, --start', dest='start', type=int, default=0,
                        help='New recording start time in unix timestamp')
    parser.add_argument('-e, --stop', dest='stop', type=int, default=0,
                        help='New recording stop time in unix timestamp')
    args = parser.parse_args()

    if not args.inpath:
        print("You have to specify input stats file path!")
    else:
        print(phrec.shrink_destfilerename(args.inpath, args.outpath, args.start, args.stop))
        phrec.shrink_moddatafilerecid(args.outpath, args.start)