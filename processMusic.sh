#! /bin/bash

# Script to move all files from ~/Downloads/music to ~/Music/New\ Music/mmddyy
# where mmddyy is the current date
# Consider automating with a cron job daily

cd ~/Downloads/music
# if [ ls -A ]; then
mkdir -p ~/Music/New\ Music/$( date +%m%d%y )
# fi
mv ~/Downloads/music/* ~/Music/New\ Music/$( date +%m%d%y )
#done
mpc --no-status update
