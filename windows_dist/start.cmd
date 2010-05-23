@echo off
call local.env\Scripts\activate.bat
start /min show.cmd
paster serve production.ini