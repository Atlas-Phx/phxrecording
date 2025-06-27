# ********************** Script requirements **********************
# - Python 3.10 or later installed and made callable from commandline (added to PATH)
# - Note: python-is-python3 is also required so "python" command works.

# ********************** Usage **********************
# - Specify recording folder full path, target folder path, start unix timestamp, stop unix timestamp in sequance
# - The paths should not end with /

#!/bin/bash

if [ $# -ne 4 ]
then
  echo "Usage: $0 [recording folder full path] [target folder path] [start unix timestamp] [stop unix timestamp]"
  exit
fi

# Input vars
SOURCE_PATH=$1
DEST_FOLDER=$2
NEW_START=$3
NEW_STOP=$4

# 1. Make the new folder with new recording ID
PHXRECORDING_PATH=$(realpath "$0")
PHXRECORDING_FOLDER_PATH=$(dirname "$PHXRECORDING_PATH")
SOURCE_REC_ID=${SOURCE_PATH##*/}
INSTRUMENT_ID=${SOURCE_REC_ID:0:5}
REC_FOLDER_NAME=$(python $PHXRECORDING_FOLDER_PATH/phxrecid.py -i $INSTRUMENT_ID -s $NEW_START)
echo New recording name: $REC_FOLDER_NAME
DEST_PATH=$DEST_FOLDER/$REC_FOLDER_NAME
mkdir $DEST_PATH

# 2. Modify and copy new recmeta.json
echo Copying recmeta...
python $PHXRECORDING_FOLDER_PATH/phxrecmetamodstartstop.py -i $SOURCE_PATH/recmeta.json -o $DEST_PATH/recmeta.json -s $NEW_START -e $NEW_STOP
echo Done.

# 3. Modify and copy new stats binary file
echo Making new stats...
ORG_START=$(python $PHXRECORDING_FOLDER_PATH/phxrecstart.py -i $SOURCE_PATH)
START_MIN=$((($NEW_START-$ORG_START)/60))
STOP_MIN=$((($NEW_STOP-$ORG_START)/60))
python $PHXRECORDING_FOLDER_PATH/phxstatsfile/phxstatsshrink.py -i $SOURCE_PATH/stats -o $DEST_PATH/stats -s $START_MIN -e $STOP_MIN
echo Done.

# 4. Copy other needed files
echo Copying data files....
#  4.1 Create needed folders
cd $SOURCE_PATH
CHAN_FOLDERs=`ls -d ./*/`
for eachname in $CHAN_FOLDERs
do
   mkdir $DEST_PATH/$(basename $eachname)
done
#  4.2 Copy files
FILE_LIST=$(python $PHXRECORDING_FOLDER_PATH/phxrecshrinkfilelist.py -i $SOURCE_PATH/ -s $NEW_START -e $NEW_STOP)
for eachname in $FILE_LIST
do
   cp $SOURCE_PATH/$eachname $DEST_PATH/$eachname
done
python $PHXRECORDING_FOLDER_PATH/phxrecshrinkfinish.py -i $SOURCE_PATH/ -o $DEST_PATH/ -s $NEW_START -e $NEW_STOP
echo Done.
echo New recording created at $DEST_PATH