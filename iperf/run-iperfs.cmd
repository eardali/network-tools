::run iperf3 for multiple times
::max time duration is 86400 which is 24 hours
::perform successive runs for several days for long term stability tests
::put this script in iperf3 folder, cd to iperf3 dir and run from dos cli
::redirects output to a file, put iperf params, round# and start time stamp to the file name
::ie iperf3-c192.168.1.26-i1-t90-P4-round3-20220416-180245.txt
::emrea, Apr 2022
::add delay params, June 2023

@echo off
setlocal EnableDelayedExpansion

::how may rounds want to run
set round=2
::set iperf params
set iperf_args=-c192.168.1.26 -i1 -t10 -P4
::how long wait before start iperf, secs
set delay=30
::how long wait between rounds, secs
set roundDelay=10

::remove spaces to use it in file name
::output file name like iperf3-args-roundx.txt
set file_name=%iperf_args: =%

echo.
echo %round% rounds will be run with iperf3 params: %iperf_args%
echo %delay% seconds will be waited before start
echo %roundDelay% seconds will be waited between rounds
echo.

::wait predefined time
timeout /t %delay% /nobreak>nul

for /L %%x in (1, 1, %round%) do (
for /f "tokens=2-7 delims=.:,/ " %%a in ("!DATE! !TIME!") do set DateNtime=%%c%%b%%a-%%d%%e%%f
echo Round %%x starts at !DateNtime!
iperf3 %iperf_args%>iperf3%file_name%-round%%x-!DateNtime!.txt
::wait a bit before next round
timeout /t %roundDelay% /nobreak>nul
)

endlocal
::pause