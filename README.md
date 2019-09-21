# Src_Automatic-Test_Controller
1. 更改C:\Users\hc\AppData\Local\Programs\Python\Python36\Lib\site-packages\barcode\writer.py的第54行
2. FONT = os.path.join(PATH, 'DejaVuSansMono.ttf')
    FONT = ".\\DejaVuSansMono.ttf"
3. 这个是barcode要用的字体，否则打包的程序用条形码生成不了