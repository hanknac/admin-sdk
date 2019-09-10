#! /bin/bash
cd /home/[YOUR-USERNAME]/admin-sdk
export date=`date`
echo $date
python3 members.py --group group@xyz.com
