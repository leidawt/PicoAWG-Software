@REM NOTE: To reduce package size, we only compile PicoAWG.py and picoawg_driver.py into PicoAWG.exe, the other dependences (e.g. *.png numpy, matplotlib) are not included.
nuitka --disable-console --follow-import-to=picoawg_driver  --nofollow-imports --output-dir=dist --windows-icon-from-ico=./icon.ico  --remove-output PicoAWG.py

xcopy /y .\dist\PicoAWG.exe .\