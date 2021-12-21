pyinstaller -D -w --hidden-import=PyQt5.sip main.py
xcopy .\icon dist\main\icon /E /Y /I
xcopy .\background dist\main\background /E /Y /I
xcopy .\report dist\main\report /E /Y /I
xcopy .\code_image dist\main\code_image /E /Y /I
copy DejaVuSansMono.ttf dist\main /Y
copy courR14.pbm dist\main /Y
copy courR14.pil dist\main /Y
copy config.json dist\main /Y
xcopy .\postek_q8 dist\main\postek_q8 /E /Y /I
pause