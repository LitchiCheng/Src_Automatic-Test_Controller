pyinstaller -D -w --hidden-import=PyQt5.sip main.py
xcopy .\icon dist\main\icon /E /Y /I
xcopy .\background dist\main\background /E /Y /I
xcopy .\report dist\main\report /E /Y /I
xcopy .\code_image dist\main\code_image /E /Y /I
copy DejaVuSansMono.ttf dist\main /Y
pause