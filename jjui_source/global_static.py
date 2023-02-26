# -*- coding: utf_8_sig-*-
#import os
#import sys
#import re

from . import global_variable

version_string=r"JJui (v.2.1.01 test)"
title_string = _(r"MAME 街机游戏列表显示器")
if global_variable.gamelist_type == "softwarelist":
    title_string= _(r"MAME Software List(软件列表)")

# 游戏列表
# 读取哪些
# 列，标准。配置文件中 设置的 读取 列 的范围，要在这其中
#   好像没用了
columns = (
        "name",
        "translation",
        "year",
        "sourcefile",
        "manufacturer",
        "description",
        "cloneof",
        "romof",
        "status",
        "savestate",
)



index_order = ( 
        'all_set',
        'available_set',
        'unavailable_set',
        'parent_set',
        'clone_set',
        
        'bios',
        'device',
        
        'chd',
        'sample',
        
        'mechanical',
        
        'softwarelist',
        
        #'no_roms',
        #'only_sample_set',
        #'no_rom_chd_sample',
        
        'year',
        'manufacturer',
        'sourcefile',
        'status',
        'savestate',
        'dump',
        'sound channels',
        
        'chip cpu',
        'chip audio',
        
        'input players',
        'input control',
        'display number',
        'display type',
        'display refresh',
        'display rotate',
        'display resolution',

                )

if global_variable.gamelist_type == "softwarelist":
    index_order = ( 
            'all_set',
            'available_set',
            'unavailable_set',
            'parent_set',
            'clone_set',
            
            'xml',
            'year',
            'publisher',
            'supported',
            
            
                )



# ui ,extra ，图片的选项
extra_image_types = (
        r"snap",
        r"titles",
        r"flyers",
        
        r"cabinets",
        r"cpanel",
        r"devices",
        r"marquees",
        r"pcb",
        r"artpreview",
        r"bosses",
        r"ends",
        r"gameover",
        r"howto",
        r"logo",
        r"scores",
        r"select",
        r"versus",
        r"warning",
        r"other_image_1",
        r"other_image_2",
        r"other_image_3",
                            )

# ui ,extra ，text 的选项
#   同类型 history.dat sysinfo.dat
#   同类型 mameinfo.dat messinfo.dat
extra_text_types =  (
        "history.xml",
        "history.dat",
        "mameinfo.dat",
        "messinfo.dat",
        "gameinit.dat",
        "sysinfo.dat",
        )
if global_variable.gamelist_type == "softwarelist":
    extra_text_types =  (
            "history.xml",
            "history.dat"
            )

# ui ,extra ，文档，第二类，出招表
extra_text_types_2 =  (
        "command.dat",
        "command_english.dat",
        )

if __name__ =="__main__":
    
    
    pass