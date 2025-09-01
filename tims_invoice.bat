@echo off
set app=tims_invoice.exe
echo Invoking %app% "%1"
echo Please wait for the spreadsheet to be transformed
echo When done, %app% will print the location of the transformed file
%HOMEDRIVE%%HOMEPATH%\.local\bin\%app% "%1"
pause