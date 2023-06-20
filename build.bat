python -m nuitka --disable-console --standalone  --nofollow-import-to=numpy --enable-plugin=tk-inter --output-dir=dist --windows-icon-from-ico=./icon.ico --include-data-files=./icon.png=./icon.png  --remove-output PicoAWG.py

@REM xcopy /y .\dist\PicoAWG.exe .\