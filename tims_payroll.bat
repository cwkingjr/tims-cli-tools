@echo off
set app=tims_payroll.exe
echo Invoking %app% --input-path "%1"
echo Please wait for the spreadsheets to be written to your Documents folder.
echo When done, %app% will print info about the files being written.
%HOMEDRIVE%%HOMEPATH%\.local\bin\%app% --input-path "%1"
pause