::ping a client, log it with time stamp and display on dos shell as well
::creates log files like "ping-log-192.168.xx.xx.log"
::use for long term testing, to see at which time network problem occurred
::unix tee for windows and related dlls must be in the same folder of batch file
::http://gnuwin32.sourceforge.net/packages/coreutils.htm
::ping with time stamp from batch file
::https://stackoverflow.com/a/24907186
::one idea to inspect resulting log file
::import log to excel, use formula and make a plot of column
::=IF(ISNUMBER(SEARCH("timed"; B1));1;0)
::if there is a big, continuous block of 1's means, ping lost for a while (Request timed out)
::however, it is observed that this method is not good because wireless clients in dense environment may not response in time
::in this case many drops appears in above method, instead use given python script to parse log file to find count of occurrences
::emrea, Nov 2021

@echo off

::ip to be ping
set ip=192.168.1.101

::seperator for time stamp and ping response prints
set sep=-


echo ----------------------------------------
echo Start to ping %ip%
echo ----------------------------------------
echo.

::ping -t %ip%|tee.exe ping-log-%ip%.log
::ping -t %ip%|cmd /q /v /c "(pause&pause)>nul & for /l %%a in () do (set /p "data=" && echo(!time! !data!|tee.exe -a ping-log-%ip%.log)&ping -n 2 localhost>nul"
::ping -t %ip%|cmd /q /v /c "(pause&pause)>nul & for /l %%a in () do (set /p "data=" && echo(!time! !data!|tee.exe -a ping-log-%ip%.log)&sleep 1"
::ping -t %ip%|cmd /q /v /c "(pause&pause)>nul & for /l %%a in () do (set /p "data=" && echo(!date! !time!-!data!|tee.exe -a ping-log-%ip%.log)"

::this prints out whole response in one line, but first char of "Reply", "Request" is consumed by pause and it prints "eply" "equest" etc, however it doesn't matter for purpose
ping -t %ip%|cmd /q /v /c "(pause&pause)>nul & for /l %%a in () do (set /p "data=" && echo(!date! !time!%sep%!data!|tee.exe -a ping-log-%ip%.log)&pause>nul"