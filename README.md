# TegrastatsJson



## Install

there are two options for installaion, one is for manual start and stop and the other creates a service that is always started at 

# Install manual startup
pip install git+https://github.com/dangraf/tegrastatsjson

to start loggin, just type
tegrastatsjson --log_file your_logfile.json --interval 1000

# Install as a service
1. git clone https://github.com/dangraf/tegrastatsjson
1. cd tegrastatsjson
1. pip install .
1. sudo /.install_as_service.sh -l your_logfile.json -i 1000 -a 1 -u jetson

The switches for the logging is:
- -l : path to your log file
- -i : Interval in ms
- -u : user, the username that is used when logging into your jetson platform
- -a : Add date to log_file, if set to 0, all samples will be saved in the same log-file. But if set to 1, a datepart will be added to the filename creating a separate log each time the service starts. eg **sudo /.install_as_service.sh -l your_logfile.json -a 1** will create the file **your_logfile-2021-01-01 10:59:01.json** where the date part is when the service started

# Time spent for running the script
I've timed the parsing part (the heavy part) on a jetson AGX Xavier and it takes around 140us to execute when running in  30W mode on 4 cores
