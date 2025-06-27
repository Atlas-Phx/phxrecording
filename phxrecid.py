# Author: Phoenix Geohysics Ltd.
# Creation: 2024-08-15

import phxrecording as phrec
import argparse as ap

if __name__ == "__main__":
    parser = ap.ArgumentParser(description='Get the Phoenix recording ID from the instrument ID and start timestamp.')
    parser.add_argument('-i, --id', dest='id', type=int,
                        help='Specify instrument id, required')
    parser.add_argument('-s, --start', dest='start', type=int,
                        help='Starting time of the recording in unix time stamp, required')
    args = parser.parse_args()

    if not args.id:
        print("You have to specify instrument id!")
    elif not args.start:
        print("You have to specify start time!")
    else:
        print(phrec.getrecid(args.id, args.start))