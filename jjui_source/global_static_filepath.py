# -*- coding: utf_8_sig-*-
import os
#import sys
#import string

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
folder_language = os.path.join(folder_source_file,"ui_translation" )

# 导入内容，多的话，导出到文件夹
# 比如，导出内置目录
folder_export    =   os.path.join(folder_temporary,"out")

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
# 所有列表，需要隐藏的
file_txt_hide_gamelist_available   =   os.path.join(folder_temporary ,"hide_list.txt")
file_txt_hide_gamelist_all         =   os.path.join(folder_temporary ,"hide_list_all.txt")
if global_variable.gamelist_type == "softwarelist":
    file_txt_hide_gamelist_available   =   os.path.join(folder_temporary ,"hide_list_sl.txt")
    file_txt_hide_gamelist_all         =   os.path.join(folder_temporary ,"hide_list_all_sl.txt")


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
if global_variable.gamelist_type == "softwarelist":
    image_path_icon_main     = os.path.join(folder_images,"for-icon-2.png")
image_path_image_no      = os.path.join(folder_images,"no_image.png")

image_path_icon_black    = os.path.join(folder_images,"black.png")
image_path_icon_red      = os.path.join(folder_images,"red.png")
image_path_icon_yellow   = os.path.join(folder_images,"yellow.png")
image_path_icon_green    = os.path.join(folder_images,"green.png")
image_path_icon_not_have = os.path.join(folder_images,"not_have.png")

image_path_zhifubao      = os.path.join(folder_images,"zhifubao.png")
image_path_weixin        = os.path.join(folder_images,"weixin.png")

image_path_icon_plus     = os.path.join(folder_images,"plus.xbm")
image_path_icon_minus    = os.path.join(folder_images,"minus.xbm")


emulator_configure_folder    = os.path.join(folder_temporary,"emu")
emulator_configure_folder_sl = os.path.join(folder_temporary,"emu_sl")
emulator_configure_folder_by_source    = os.path.join(folder_temporary,"emu_source") # mame 源代码分类

file_pickle_extra_index_history_xml = os.path.join(folder_temporary ,"cache_index_history_xml.bin") 
if global_variable.gamelist_type == "softwarelist":
    file_pickle_extra_index_history_xml = os.path.join(folder_temporary ,"cache_index_history_xml_sl.bin") 

# ("history.dat","sysinfo.dat",)
file_pickle_extra_index_history_dat = os.path.join(folder_temporary ,"cache_index_history_dat.bin") 
file_pickle_extra_index_sysinfo_dat = os.path.join(folder_temporary ,"cache_index_sysinfo_dat.bin") 
if global_variable.gamelist_type == "softwarelist":
    file_pickle_extra_index_history_dat = os.path.join(folder_temporary ,"cache_index_history_dat_sl.bin") 

#("mameinfo.dat","messinfo.dat",)
file_pickle_extra_index_mameinfo_dat = os.path.join(folder_temporary ,"cache_index_mameinfo_dat.bin") 
file_pickle_extra_index_messinfo_dat = os.path.join(folder_temporary ,"cache_index_messinfo_dat.bin") 

#"command.dat",
#"command_english.dat",
file_pickle_extra_index_command_dat = os.path.join(folder_temporary ,"cache_index_command_dat.bin") 
file_pickle_extra_index_command_english_dat = os.path.join(folder_temporary ,"cache_index_command_english_dat.bin") 

# "gameinit.dat",
file_pickle_extra_index_gameinit_dat = os.path.join(folder_temporary ,"cache_index_gameinit_dat.bin") 


# # command.dat 图片
# if global_variable.gamelist_type == "mame":
#     
#     folder_command_image=os.path.join(folder_images,"command")
# 
#     command_image_file_path_dict = {}
#     # key 用原始字符
#     # value 为 图片路径
#     #
#     # A = os.path.join(folder_command_image,"A")
#     # ......
#     # Z = os.path.join(folder_command_image,"Z")
# 
#     # string.ascii_uppercase
#     # 大写字母 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     for a_char in string.ascii_uppercase:
#         # @A-button 文件名 A.png
#         # @Z-button 文件名 Z.png
#         k = r"@" + a_char + r"-button"
#         v = os.path.join( folder_command_image , a_char + ".png" )
#         command_image_file_path_dict[k]=v
# 
#     # 方向
#     # command_image_file_path_dict[k]=v
#     command_image_file_path_dict[r"_1"] = os.path.join( folder_command_image , r"_1" + ".png" ),
#     command_image_file_path_dict[r"_2"] = os.path.join( folder_command_image , r"_2" + ".png" ),
#     command_image_file_path_dict[r"_3"] = os.path.join( folder_command_image , r"_3" + ".png" ),
#     command_image_file_path_dict[r"_4"] = os.path.join( folder_command_image , r"_4" + ".png" ),
#     command_image_file_path_dict[r"_5"] = os.path.join( folder_command_image , r"_5" + ".png" ), # gbk  ??? ############### ☉☉⊕⊕
#     command_image_file_path_dict[r"_6"] = os.path.join( folder_command_image , r"_6" + ".png" ),
#     command_image_file_path_dict[r"_7"] = os.path.join( folder_command_image , r"_7" + ".png" ),
#     command_image_file_path_dict[r"_8"] = os.path.join( folder_command_image , r"_8" + ".png" ),
#     command_image_file_path_dict[r"_9"] = os.path.join( folder_command_image , r"_9" + ".png" ),
# 
#     # 其它

if __name__ == "__main__" :
    # locals()
    # or
    # dir()
    
    temp = locals()
    #print()
    #print(temp)
    
    the_keys=sorted(temp.keys())
    #print()
    #print( the_keys )
    
    print()
    for x in the_keys:
        if x.startswith("_"):
            pass
        elif type(temp[x])==str:
            print(x.ljust(45),end="")
            print(' ',end='')
            print(temp[x])
    
    print()
    if "command_image_file_path_dict" in temp:
        for k,v in sorted( temp["command_image_file_path_dict"].items() ):
                    print(k,"\t",v)
    
    print()
    print("end")