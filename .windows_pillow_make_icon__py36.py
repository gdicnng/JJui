import sys
from PIL import Image

if sys.version_info < (3, 6):
    pass

else:
    logo = Image.open(r"jjui_source\images\for-icon.png")
     
    logo.save("jjui.ico",format='ICO')


    logo = Image.open(r"jjui_source\images\for-icon-2.png")
     
    logo.save("jjui_sl.ico",format='ICO')