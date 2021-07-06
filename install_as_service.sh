#!/bin/bash
set -e
set -u

if [[ "$(whoami)" != "root" ]]; then
	echo "This installation must be run as root" 1>&2
	exit 1
fi

INTERVALL=1000
ADD_DATE_TO_LOGFILE=1
USER='user'

helpFuntion()
{
    echo ""
    echo "Usage: sudo ./install_as_service.sh -l <log_file_location> -i <intervall in ms> -a <1 or 0>"
    echo "example: sudo ./install_as_service.sh --l /home/tegrastats_log.json --i 1000, --a 1"
    echo "-l: logfile location eg myfile.json"
    echo "-i: intervall in mS"
    echo "-a: Add date to log_file, if set to true, a datepart will be added to the filename each time the service starts, eg myfile.json will be myfile-2021-01-01 10:59:01.json"
    echo "-u: set 'user' name for the default user"
    
}
pip3 install .
while getopts l:i:a:u: flag
do
    case "${flag}" in
        l ) LOG_FILE=${OPTARG};;
        i ) INTERVALL=${OPTARG};;
        a ) ADD_DATE_TO_LOGFILE=${OPTARG};;
        u ) USER=${OPTARG};;
        ? ) helpFuntion;;
    esac
done
echo "file: $LOG_FILE";
echo "intervall: $INTERVALL mS"
echo "add_date_to_logfile: $ADD_DATE_TO_LOGFILE"
echo "user: $USER"

sed -i "/.*ExecStart=.*/c\ExecStart=/home/$USER/.local/bin/tegrastatsjson --log_file $LOG_FILE --interval ${INTERVALL} --add_date_to_logfile ${ADD_DATE_TO_LOGFILE}" tegrastatsjsond.service
sed -i "/.*User=.*/c\User=$USER" tegrastatsjsond.service

cp tegrastatsjsond.service /etc/systemd/system
systemctl daemon-reload
systemctl start tegrastatsjsond.service
systemctl enable tegrastatsjsond.service

