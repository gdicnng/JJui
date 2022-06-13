﻿# -*- coding: utf_8_sig-*-
import os
#import sys

from . import global_variable

# 临时文件路径
# 相对路径
#   相对于，主脚本 jjui.pyw 的位置 ，在上层文件夹

#########

#print("查看当前目录")
#print("os.getcwd()")
#print(os.getcwd())

# 源代码文件夹
#   同时存放 
#           图片、
#           UI 翻译 文件、
folder_source_file  = os.path.join(os.curdir,"jjui_source" )

# 临时文件夹 
folder_temporary  = os.path.join(os.curdir,".jjui" )

# ui 翻译文件所在目录
folder_language = os.path.join(folder_source_file,"language" )

# 配置文件
file_ini_configure              =   os.path.join(folder_temporary ,"jjui.ini")
if global_variable.gamelist_type == "softwarelist":
    file_ini_configure           =   os.path.join(folder_temporary ,"jjui_sl.ini")


folder_themes   =      os.path.join(folder_temporary,"themes")

# 数据 存为 pickle 格式
# 如果只用一个文件
file_pickle_gamelist_data = os.path.join(folder_temporary ,"cache_data.bin") 
if global_variable.gamelist_type == "softwarelist":
    file_pickle_gamelist_data = os.path.join(folder_temporary ,"cache_data_sl.bin") 

    # 目录  等
#file_pickle_index    = os.path.join(folder_temporary ,"cache_data_1.bin")
    #dict_keys(['mame_version', 'set_data', 'dict_data'])
    # 游戏列表 数据
#file_pickle_gamelist = os.path.join(folder_temporary ,"cache_data_2_gamelist.bin") 

# 拥有列表 
file_pickle_gamelist_available= os.path.join(folder_temporary ,"cache_available.bin") 
if global_variable.gamelist_type == "softwarelist":
    file_pickle_gamelist_available= os.path.join(folder_temporary ,"cache_available_sl.bin") 

# 拥有列表，需要隐藏的
file_txt_hide_gamelist_available   =   os.path.join(folder_temporary ,"hide_list.txt")
if global_variable.gamelist_type == "softwarelist":
    file_txt_hide_gamelist_available   =   os.path.join(folder_temporary ,"hide_list_sl.txt")

# 游戏列表翻译
# 两个都保留
file_txt_translation_for_gamelist    =   os.path.join(folder_temporary ,"translation.txt")
if global_variable.gamelist_type == "softwarelist":
    file_txt_translation_for_gamelist =   os.path.join(folder_temporary ,"translation_sl.txt")


# sl 的话，下面两个都要
# mame  导出的 roms.xml
file_xml_mame              =   os.path.join(folder_temporary ,"roms.xml")
# mame  导出的 roms_sl.xml
file_xml_mame_softwarelist           =   os.path.join(folder_temporary ,"roms_sl.xml")

# 导出文本，用于导出某个列表中的游戏名缩写
file_txt_export      =   os.path.join(folder_temporary ,"out.txt")
    

# 帮助文档
file_html_index     = os.path.join(folder_temporary ,"docs","index.html")

#图片
folder_images = os.path.join(folder_source_file,"images")

image_path_icon_main     = os.path.join(folder_images,"for-icon.png")
image_path_image_no      = os.path.join(folder_images,"no_image.png")
image_path_icon_black    = os.path.join(folder_images,"black.png")
image_path_icon_red      = os.path.join(folder_images,"red.png")
image_path_icon_yellow   = os.path.join(folder_images,"yellow.png")
image_path_icon_green    = os.path.join(folder_images,"green.png")
image_path_zhifubao      = os.path.join(folder_images,"zhifubao.png")
image_path_weixin        = os.path.join(folder_images,"weixin.png")

image_path_icon_plus     = os.path.join(folder_images,"plus.xbm")
image_path_icon_minus    = os.path.join(folder_images,"minus.xbm")


emulator_configure_folder    = os.path.join(folder_temporary,"emu")
emulator_configure_folder_sl = os.path.join(folder_temporary,"emu_sl")

if __name__ == "__main__" :
    # locals()
    # or
    # dir()
    
    temp =  locals()
    print()
    print(temp)
    
    the_keys=sorted(temp.keys())
    print()
    print( the_keys )
    
    print()
    for x in the_keys:
        if x.startswith("_"):
            pass
        elif x=="os" :# 导入的库
           pass
        elif  x=="temp" or x=="the_keys": # 上面已有的变量
            pass
        else:
            print(x.ljust(45),end="")
            print(' ',end='')
            print(temp[x])
    
    print()