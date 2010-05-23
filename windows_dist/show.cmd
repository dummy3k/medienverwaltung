@echo off
echo Waiting...
ping -n 5 localhost > %temp%\null
del %temp%\null

start http://localhost:5000/
exit