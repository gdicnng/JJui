# -*- coding: utf_8_sig-*-
import os
import sys
import subprocess

from jjui.save_pickle import save as save_pickle
from jjui.read_pickle import read as read_pickle
from jjui import ui_configure_file


# 临时文件路径
# 相对于上层文件夹，主函数的位置
temp_file_name          = os.path.join(os.curdir,".jjui","cache_data_1.bin")
    #dict_keys(['mame_version', 'set_data', 'dict_data'])
temp_file_name_gamelist = os.path.join(os.curdir,".jjui","cache_data_2_gamelist.bin") # 游戏列表 数据
temp_file_name_available= os.path.join(os.curdir,".jjui","cache_available.bin") # 拥有列表 数据
translation_file_name =   os.path.join(os.curdir,".jjui","translation.txt")
ini_file              =   os.path.join(os.curdir,".jjui","jjui.ini")
xml_file              =   os.path.join(os.curdir,".jjui","roms.xml")
available_hide_file   =   os.path.join(os.curdir,".jjui","hide_list.txt")
export_text_file      =   os.path.join(os.curdir,".jjui","out.txt")
    # 导出
    
docs_html_index_file     = os.path.join(os.curdir,".jjui","docs","index.html")


image_path_icon_for_jjui = os.path.join(os.curdir,"jjui","images","for-icon.png")
image_path_no_image      = os.path.join(os.curdir,"jjui","images","no_image.png")
image_path_icon_black    = os.path.join(os.curdir,"jjui","images","black.png")
image_path_icon_red      = os.path.join(os.curdir,"jjui","images","red.png")
image_path_icon_yellow   = os.path.join(os.curdir,"jjui","images","yellow.png")
image_path_icon_green    = os.path.join(os.curdir,"jjui","images","green.png")
image_path_zhifubao      = os.path.join(os.curdir,"jjui","images","zhifubao.png")
image_path_weixin        = os.path.join(os.curdir,"jjui","images","weixin.png")



# 临时文件夹 
temp_folders = os.path.join(os.curdir,".jjui")
# 如果不存在，创建 目录
if os.path.exists(temp_folders):
    pass
else:
    os.makedirs(temp_folders)
# 如果存在同名文件，删除后，创建 目录
if os.path.isfile(temp_folders):
    os.remove(temp_folders)
    os.makedirs(temp_folders)


# 游戏列表
# 读取哪些
# 列，标准。配置文件中 设置的 读取 列 的范围，要在这其中
columns = ("name","translation","year","sourcefile","manufacturer","description","cloneof","romof","status","savestate")

index_translation = {   'all_set':'所有列表',
                        'available_set':'拥有列表',
                        'unavailable_set':'未拥有列表',
                        'parent_set':'主版本',
                        'clone_set':'副版本',                        
                        
                        'bios':'bios',
                        'device':'device',
                        'mechanical':'mechanical',
                        'softwarelist':'software list',
                        'chd':'chd',
                        'sample':'sample',
                        
                        'year':'年代',
                        'manufacturer':'厂商',
                        'sourcefile':'源代码', 
                        'status':'模拟状态'  ,
                        'savestate'         :"存盘状态",
                        'dump'              :"dump 问题",
                        'sound channels'    :"声音 通道",
                        'chip cpu'          :"芯片 cpu",
                        'chip audio'        :"芯片 audio",
                        'input players'     :"输入 玩家",
                        'input control'     :"输入 控制",
                        'display type'      :"显示 种类",
                        'display refresh'   :"显示 刷新率",
                        'display rotate'    :"显示 旋转",
                        'display resolution':"显示 分辨率",

                        #'only_sample_set':'仅需 sample，无需 rom、chd',
                        #'no_roms':'无需 rom、chd',
                        #'no_rom_chd_sample':'无需 rom、chd、sample',
                    }

index_order = ( 'all_set',
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
                'display type',
                'display refresh',
                'display rotate',
                'display resolution',

                )
index_level_3 = ('sourcefile',)

columns_translation = {  
        # "#0":"",
        "name":"缩写",
        "year":"年代",
        "sourcefile":"源代码",
        "manufacturer":"厂商",
        "cloneof":"主版本",
        "translation":"游戏名(译)",
        "description":"游戏名英文",
        "status":"模拟状态",
        "savestate":"存档状态",
        }


# 读取 jjui.ini
ini_data ={} # 默认值
try: # 读取
    ini_data = ui_configure_file.read_ini( ini_file )
except:
    pass

# 在下面 ini_default 中使用
columns_width = {  
        "#0":55,
        "name":120,
        "year":50,
        "sourcefile":80,
        "manufacturer":100,
        "cloneof":80,
        "translation":300,
        "description":300,
        "status":50,
        "savestate":50,
        }


use_shell_or_not_in_subprocess = False
the_mame_path = os.path.join(os.curdir,"mame.exe")
if sys.platform.lower().startswith('win'):
    use_shell_or_not_in_subprocess = True
else:
    the_mame_path = "mame"
    
# jjui.ini 默认值
ini_temp = [ 
    ("mame_path",the_mame_path ), # .\mame.exe
    
    ("mame_working_directory",""),# subprocess.Popen() 函数中，cwd=
    ("use_shell",use_shell_or_not_in_subprocess ),# Ture False , # subprocess.Popen() 函数中，window 中用 True
    
    
    ("size","800x600"),
    
    ("theme",""),
    


    
    # ("unavailable_character","-"),#√×
    
    ("font"               ,""  ),
    ("font_size"          ,0   ),    
    ("gamelist_font"      ,""  ),
    ("gamelist_font_size" ,0   ),
    ("text_font"          ,""  ),
    ("text_font_size"     ,0   ),    
    ("text_2_font"        ,""  ),
    ("text_2_font_size"   ,0   ),
    ("others_font"        ,""  ),
    ("others_font_size"   ,0   ),       
    
    ("row_height"         ,0),
    ("icon_size",16),
    
    ("tk_scaling_use_flag",0), # 0 , 1 ,ttk.Checkbutton  
    ("tk_scaling_number",0),
    
    ("colour_bg","grey90" ), #
    ("colour_panedwindow_bg","grey50" ), #    
    ("use_available_game_mark",0 ), # 是否使用 标记
    ("available_game_mark","√" ),# 拥有游戏，标记
    
    #"use_background_flag",0,
    
    ("pos1",150),# 分隔线位置，目录｜游戏列表
    ("pos2",600),# 分隔线位置 ，游戏列表｜周边
    ("pos3",250),# 分隔线位置  ，图片1｜图片2
    
    ("extra_tab_index",0),
    
    ("gamelist_columns",("name","translation","description","year","sourcefile","manufacturer","cloneof","status","savestate")  ),
    
    ("gamelist_columns_to_show_1",("name","translation","year","sourcefile","manufacturer",)    ),
    
    ("gamelist_columns_to_show_2",("name","description","year","sourcefile","manufacturer",)    ),
    
    ("gamelist_columns_width",columns_width),
    
    ("extra_image_chooser_index",1),
    ("extra_image_chooser_2_index",0),
    ("extra_text_chooser_index",2),
    ("extra_command_type_chooser_index",0),
    
    ("extra_image_usezip",1),# 0 , 1 ,ttk.Checkbutton    
    ("extra_image_usezip_2",1),# 0 , 1 ,ttk.Checkbutton    
 
    ("index_be_chosen",''),  # 暂时，初始化为 空
    #"index_set_remembered",set(),  # 有上面一项就够了
    
    ("gamelist_group_mark",True), 
    ("gamelist_sorted_by",''),
        #   'name'
        #   还是 设为 空比较好，万一 别人不选 'name' 这一组呢
        # 不能用数字，数字容易超。因为使用了三组，每组显示 列数目 不一样
        # 用 自己设定的 列 ID 
    ("gamelist_sorted_reverse",False),
    
    ("filter",[]),

    # # ##################### # #
    
    ("folders_path",os.path.join(os.curdir,"folders") ),#r".\folders"

    ("snap_path"   ,os.path.join(os.curdir,"snap")    ),  #r".\snap"
    ("titles_path" ,os.path.join(os.curdir,"titles")  ), #r".\titles"
    ("flyers_path" ,os.path.join(os.curdir,"flyers")  ),#r".\flyers"
    
    ("cabinets_path"  ,os.path.join(os.curdir,"cabinets")   ),#r".\cabinets"
    ("cpanel_path"    ,os.path.join(os.curdir,"cpanel")     ),#r".\cpanel"
    ("devices_path"   ,os.path.join(os.curdir,"devices")    ),#r".\devices"
    ("marquees_path"  ,os.path.join(os.curdir,"marquees")   ),#r".\marquees"
    ("pcb_path"       ,os.path.join(os.curdir,"pcb")        ),#r".\pcb"
    ("artpreview_path",os.path.join(os.curdir,"artpreview") ),#r".\artpreview"
    ("bosses_path"    ,os.path.join(os.curdir,"bosses")     ),#r".\bosses"
    ("ends_path"      ,os.path.join(os.curdir,"ends")       ),#r".\ends"
    ("gameover_path"  ,os.path.join(os.curdir,"gameover")   ),#r".\gameover"
    ("howto_path"     ,os.path.join(os.curdir,"howto")      ),#,r".\howto"
    ("logo_path"      ,os.path.join(os.curdir,"logo")       ),#r".\logo"
    ("scores_path"    ,os.path.join(os.curdir,"scores")     ),#r".\scores"
    ("select_path"    ,os.path.join(os.curdir,"select")     ),#r".\select"
    ("versus_path"    ,os.path.join(os.curdir,"versus")     ),#r".\versus"
    ("warning_path"   ,os.path.join(os.curdir,"warning")    ),#r".\warning"
    
    ("snap.zip_path"   ,os.path.join(os.curdir,"snap.zip")   ),#r".\snap.zip"
    ("titles.zip_path" ,os.path.join(os.curdir,"titles.zip") ),#r".\titles.zip"
    ("flyers.zip_path" ,os.path.join(os.curdir,"flyers.zip") ),#r".\flyers.zip"
    
    ("cabinets.zip_path"  ,os.path.join(os.curdir,"cabinets.zip")   ),#r".\cabinets.zip"
    ("cpanel.zip_path"    ,os.path.join(os.curdir,"cpanel.zip")     ),#r".\cpanel.zip"
    ("devices.zip_path"   ,os.path.join(os.curdir,"devices.zip")    ),#r".\devices.zip"
    ("marquees.zip_path"  ,os.path.join(os.curdir,"marquees.zip")   ),#r".\marquees.zip"
    ("pcb.zip_path"       ,os.path.join(os.curdir,"pcb.zip")        ),#r".\pcb.zip"
    ("artpreview.zip_path",os.path.join(os.curdir,"artpreview.zip") ),#r".\artpreview.zip"
    ("bosses.zip_path"    ,os.path.join(os.curdir,"bosses.zip")     ),#r".\bosses.zip"
    ("ends.zip_path"      ,os.path.join(os.curdir,"ends.zip")       ),#r".\ends.zip"
    ("gameover.zip_path"  ,os.path.join(os.curdir,"gameover.zip")   ),#r".\gameover.zip"
    ("howto.zip_path"     ,os.path.join(os.curdir,"howto.zip")      ),#,r".\howto.zip"
    ("logo.zip_path"      ,os.path.join(os.curdir,"logo.zip")       ),#r".\logo.zip"
    ("scores.zip_path"    ,os.path.join(os.curdir,"scores.zip")     ),#r".\scores.zip"
    ("select.zip_path"    ,os.path.join(os.curdir,"select.zip")     ),#r".\select.zip"
    ("versus.zip_path"    ,os.path.join(os.curdir,"versus.zip")     ),#r".\versus.zip"
    ("warning.zip_path"   ,os.path.join(os.curdir,"warning.zip")    ),#r".\warning.zip"
    
    ("history.xml_path"        ,os.path.join(os.curdir,"history.xml")         ),#.\history.xml
    ("history.dat_path"        ,os.path.join(os.curdir,"history.dat")         ),#.\history.dat
    ("command.dat_path"        ,os.path.join(os.curdir,"command.dat")         ),#.\command.dat
    ("command_english.dat_path",os.path.join(os.curdir,"command_english.dat") ),#.\command_english.dat
    ("mameinfo.dat_path"       ,os.path.join(os.curdir,"mameinfo.dat")        ),#.\mameinfo.dat
    ("messinfo.dat_path"       ,os.path.join(os.curdir,"messinfo.dat")        ),#.\messinfo.dat
    ("gameinit.dat_path"       ,os.path.join(os.curdir,"gameinit.dat")        ),#.\gameinit.dat
    ("sysinfo.dat_path"        ,os.path.join(os.curdir,"sysinfo.dat")         ),#.\sysinfo.dat
]

del use_shell_or_not_in_subprocess
del the_mame_path

ini_order=[]
for x in ini_temp:
    ini_order.append(x[0])

ini_default={}

print("")
print("ini_temp")
for x in ini_temp:
    if type(x) ==  tuple:
        if len(x) == 2:
            ini_default[ x[0] ] = x[1]
        else:
            print(x)
            print("tuple,wrong length,not 2")
    else:
        print(x)
        print("wrong type,not tuple")
print("")


# 部分 数据校验
# 
# 整数，或 浮点数
for x in ("tk_scaling_number",):
    if x in ini_data:
        # 字符 转为 int 或 float
        if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
            try:
                ini_data[x] = eval( ini_data[x] )
            except:
                pass
        
        # 如果 转换 失败，则 读取默认值
        if x in ini_default:
            if type( ini_data[x] ) == int :
                pass
            elif type( ini_data[x] ) == float :
                pass
            else:
                ini_data[x] = ini_default[x]
        
        if ini_data[x] <= 0.01:
            ini_data[x] = 0

# bool 类型的数据
for x in ("gamelist_group_mark","gamelist_sorted_reverse","use_shell",):
    if x in ini_data:
        # 字符 转为 bool
        if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
            try:
                ini_data[x] = eval( ini_data[x] )
            except:
                pass
        # 如果 转换 失败，则 读取默认值
        if x in ini_default:
            if type( ini_data[x] ) == bool :
                pass
            else:
                ini_data[x] = ini_default[x]
# int 类型的数据
# >=0
for x in ("pos1","pos2","pos3",

          "extra_tab_index",

          "font_size",
          "gamelist_font_size",
          "text_font_size",
          "text_2_font_size",
          "others_font_size",
          
          "row_height",
          "icon_size",
          
          "tk_scaling_use_flag",
          "use_available_game_mark",
          
          #"use_background_flag",
          
          "extra_image_usezip","extra_image_usezip_2",
          
          "extra_image_chooser_index",
          "extra_image_chooser_2_index",
          "extra_text_chooser_index",
          "extra_command_type_chooser_index",
          ):
    if x in ini_data:
        # 字符 转为 int
        if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
            try:
                ini_data[x] = eval( ini_data[x] )
                ini_data[x] = int( ini_data[x] )
            except:
                pass
        # 如果 转换 失败，则 读取默认值
        if x in ini_default:
            if type( ini_data[x] ) == int :
                if ini_data[x] >= 0: # 还不能是负数
                    pass
                else :
                    ini_data[x] = ini_default[x]
            else:
                ini_data[x] = ini_default[x]
# columns 列表 columns
# tuple
for x in ("gamelist_columns","gamelist_columns_to_show_1","gamelist_columns_to_show_2"):
    if x in ini_data:
        # 字符 转为 tuple
        if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
            try:
                ini_data[x] = eval( ini_data[x] )
            except:
                pass
        if type( ini_data[x] ) == tuple:
            # 与标准数据比较 columns
            temp_list = []
            for y in ini_data[x]:
                if y in columns:
                    if y not in temp_list:
                        temp_list.append(y)
            ini_data[x] = tuple(temp_list)
        # 如果 转换 失败，则 读取默认值
        if x in ini_default:
            if type( ini_data[x] ) == tuple :
                pass
            else:
                ini_data[x] = ini_default[x]
# gamelist_columns_width 
# dict
# values 宽度为 整数
for x in ("gamelist_columns_width",):
    if x in ini_data:
        if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
            try:
                ini_data[x] = eval( ini_data[x] )
            except:
                pass
                
        if type( ini_data[x] ) == dict :# 比较类型
            
            temp = columns_width.keys() # 标准项目
            
            for y in ini_data[x]:
                if y in temp:
                    if type( ini_data[x][y] ) != int:
                        ini_data[x][y] = ini_default[x][y] # 数据 不是整数 读取默认值
                else:
                    del ini_data[x][y] # 删除 不需要的 项目
        else: 
            ini_data[x] = ini_default[x]

# 排序标记
# ini_data["gamelist_sorted_by"] ,'name' # 不使用数字，使用 列 id
#   范围：   ini_data["gamelist_columns"]
#       因为用到了 ini_data["gamelist_columns"] ，
#       所以要在 ini_data["gamelist_columns"] 校验之后，再校验此项
#   并且，默认值设置为空字符
ini_default["gamelist_sorted_by"] = ''
x = "gamelist_sorted_by"
if x in ini_data:
    flag = False
    for y in ini_data["gamelist_columns"]:# 用户设置的，所有的 列
        if ini_data[x] == y :
            flag = True
            break
            
    if flag : 
        pass
    else : 
        ini_data[x] = ini_default[x]
        
    del flag
else:
    ini_data[x] = ini_default[x]
del x

# "filter":类型为  list ,（之后使用时，转为 set ,因为空 set ，print 打印出来，格式不一致）
for x in ("filter",):
    if x in ini_data:
        if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
            try:
                ini_data[x] = eval( ini_data[x] )
            except:
                pass
        if type( ini_data[x] ) == list :# 比较类型
            pass
        else: 
            ini_data[x] = ini_default[x]
    else: 
            ini_data[x] = ini_default[x]

# 以上，仅校验 部分 数据


# ini_data 中，没有的项目 ，读取 默认值
temp_dict = {} 
for x in ini_default:
    if x in ini_data : #如果配置文件里有
        temp_dict[x] = ini_data[x]
    else: #如果配置文件里没有
        temp_dict[x] = ini_default[x]

ini_data = temp_dict
del temp_dict

for x in ini_order:
    if x in ini_data:
        print(x,end='')
        print('\t',end='')
        print(ini_data[x])    
for x in ini_data:
    if x not in ini_order:
        print(x,end='')
        print('\t',end='')
        print(ini_data[x])


# 如果不存在，生成 .\.jjui\jjui.ini ,默认值
if not os.path.isfile(ini_file):  
    ui_configure_file.write_ini(ini_file,ini_default)
