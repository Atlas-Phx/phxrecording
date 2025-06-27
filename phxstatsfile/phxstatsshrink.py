# Author: Phoenix Geohysics Ltd.
# Creation: 2024-08-14

import phxstatsfile as stats
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
    parser = ap.ArgumentParser(description='A shrinker that could pick a subset of minutes from Phoenix stats binary and spawn a new binary.')
    parser.add_argument('-i, --infile', dest='inpath', type=file_path,
                        help='Specify stats file path, required')
    parser.add_argument('-o, --outfile', dest='outpath', type=out_path,
                        help='Specify output json file path, required')
    parser.add_argument('-s, --startmin', dest='start', type=int, default=0,
                        help='Starting point of the output data, how many minutes from the recording start')
    parser.add_argument('-e, --stopmin', dest='stop', type=int, default=0,
                        help='Stop point of the output data, how many minutes from the recording start')
    args = parser.parse_args()

    if not args.inpath:
        print("You have to specify input stats file path!")
    elif not args.outpath:
        print("You have to specify output stats file path!")
    else:
        print(stats.shrinkto(args.inpath, args.outpath, args.start, args.stop))