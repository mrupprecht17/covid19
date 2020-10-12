@echo off
set directory="C:\Users\Michael\OneDrive - California Institute of Technology\Documents\musings, et cetera\COVID-19"
echo downloading data...
py -3.7 %directory%\IL_data_scraper_current_date_matcher_(overwrite_protected).py
pause
echo formatting data to json...
py -3.7 %directory%\IL_data_stripper_current_date.py
pause
echo converting json to csv...
py -3.7 %directory%\IL_data_converter_current_date.py
pause
echo importing csv to excel...
wscript %directory%\macro_runner.vbs
pause
