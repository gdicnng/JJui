# -*- coding: utf_8_sig-*-
import os
import sys
import re
import codecs

from . import global_variable
# from .global_static import columns

# 在下面 ini_default 中使用
columns_width = {  
        "#0":55,
        #"name":120,
        "#id":120,
        "year":50,
        "sourcefile":80,
        "manufacturer":100,
        "cloneof":80,
        "translation":300,
        "description":300,
        "status":50,
        "savestate":50,
        }

gamelist_columns_to_show_1=("#id","translation","year","sourcefile","manufacturer",)
gamelist_columns_to_show_2=("#id","description","year","sourcefile","manufacturer",)
gamelist_columns_to_show_3=("#id","translation","description","year","sourcefile","manufacturer","cloneof","status","savestate")

if global_variable.gamelist_type == "softwarelist":
    columns_width = {  
            "#0":55,
            "#id":120,
            "xml":120,
            "name":120,
            "year":50,
            #"sourcefile":80,
            "publisher":100,
            "cloneof":80,
            "translation":300,
            "description":300,
            "alt_title"  :300,
            "supported":50,
            #"savestate":50,
            }
    gamelist_columns_to_show_1=("xml","name","translation","alt_title","year","publisher",)
    gamelist_columns_to_show_2=("xml","name","description","alt_title","year","publisher",)
    gamelist_columns_to_show_3=("xml","name","translation","description","alt_title","year","publisher","cloneof","supported","#id")

# return temp_dict
# 读取文本，尚未校验
def read_ini( ini_file_name ):
    
    temp_dict = {}
    
    text_file = open( ini_file_name , 'rt',encoding='utf_8_sig')
    lines = text_file.readlines()
    text_file.close()
    
    #temp_srt = r'^\s*(\S+)\s+(\S+)\s*$' # 值有空格，这个不行
    temp_str = r'^\s*(\S+)\s+(\S.*?)\s*$'
        # 选项 值
            # 选项没有空格 \S+
            # 值，有空格 (\S.*?)\s*
    p=re.compile(temp_str)
    
    #temp_srt_2 = r'^(")(.+)(")$'
    #先不管这个
        # 选项 值，
        # 值 为路径的话，里面有空格
        # sanp "xxx\ yyy"
        # "xxx\ yyy"
        # 去掉 引号
    #p2=re.compile(temp_srt_2)
    
    #count = 0
    for line in lines:
        str_1 = ''
        str_2 = ''
        m=p.search(line)
        if m:
            str_1 = m.group(1)
            str_2 = m.group(2)
            #m2 = p2.search(m.group(2))
            #if m2:
            #    str_2 = m2.group(2)
            temp_dict[str_1] = str_2
    return temp_dict

# return 无
def write_ini(ini_file_name,ini_dict,order = None):
    
    # order 顺序
        # keys 组成的 list 或 tuple
    # 因为
        # 新版本的 dict 会保持 原有的 顺序
        # 但老版本的 dict 不会保持 原有的 顺序

    with open(ini_file_name, 'wt',encoding='utf_8_sig') as text_file:
    
        length=29 
        # 文字左对齐长度 
        # 之后再加一个空格
        
        if order == None:
            for x in sorted( ini_dict.keys() ):
                print( x.ljust(length) , end='',file = text_file )
                print( " "         ,     end='',file = text_file )# 增加一个空格，万一长度超了也不影响
                print( ini_dict[x] ,            file = text_file )

        else:
            for x in order:
                if x in ini_dict:
                    print( x.ljust(length) , end='',file = text_file )
                    print( " "         ,     end='',file = text_file )# 增加一个空格，万一长度超了也不影响
                    print( ini_dict[x] ,            file = text_file )
            for x in sorted( ini_dict.keys() ):
                if x not in order:
                    print( x.ljust(length) , end='',file = text_file )
                    print( " "         ,     end='',file = text_file )# 增加一个空格，万一长度超了也不影响
                    print( ini_dict[x] ,            file = text_file )



# ini_default
#       jjui.ini 中的默认值设置
# return(ini_order,ini_default)
def get_configure_file_default_value( ):
    """
    # return(ini_order,ini_default)
    """

    the_mame_path = os.path.join(os.curdir,"mame.exe")
    use_shell_or_not_in_subprocess = False
    
    if sys.platform.lower().startswith('win'):
        use_shell_or_not_in_subprocess = True
    else:
        the_mame_path = "mame"
    
    if global_variable.gamelist_type == "softwarelist":
    
        #snap_path      = os.path.join(os.curdir,"snap")
        #titles_path    = os.path.join(os.curdir,"titles")
        
        snap_zip_path  =os.path.join(os.curdir,"snap_sl.zip")
        titles_zip_path=os.path.join(os.curdir,"titles_sl.zip")
    
    
    else:
        #snap_path      = os.path.join(os.curdir,"snap")
        #titles_path    = os.path.join(os.curdir,"titles")
        
        snap_zip_path  =os.path.join(os.curdir,"snap.zip")
        titles_zip_path=os.path.join(os.curdir,"titles.zip")
    
    # jjui.ini 默认值 ，初始
    #   之后改为：
    #   ini_order       list 保存顺序
    #   ini_default     dict 方便使用
    ini_temp = [ 
        ("mame_path",the_mame_path ), # .\mame.exe
        
        ("mame_working_directory",""),# subprocess.Popen() 函数中，cwd=
        
        ("use_shell",use_shell_or_not_in_subprocess ),
        # Ture False , 
        # subprocess.Popen() 函数中，windows 中用 True
        
        ("high_dpi",0 ),
        
        ("encoding","" ),
        
        ("size","800x600"),
        ("zoomed",False),
        # normal, iconic, withdrawn, icon, or (Windows and Mac OS X only) zoomed. 
        # normal, zoomed. 
        
        ("theme",""), 
        
        ("ui_language",""), # ??
        
        ("locale_name",""), # locale.setlocale(locale.LC_COLLATE,locale="???")
        ("use_locale_sort",False), # locale.strxfrm()
        
        ("keep_track_of_the_select_item",        False),
        # 分类列表切换时，总是尝试定位选中项

        ("gamelist_level",        1),
            # 1，列表 仅一层
            # 2，列表 两层，总是展开，不能收起
            # 3，列表，两层，总是收起，手动点击展开
        
        
        ("gamelist_columns_to_show_1",gamelist_columns_to_show_1  ),
        
        ("gamelist_columns_to_show_2",gamelist_columns_to_show_2  ),

        ("gamelist_columns_to_show_3",gamelist_columns_to_show_3  ),
        
        ("gamelist_columns_width",columns_width),
        
        
        # ("unavailable_character","-"),#√×
        
        
        
        ("use_colour_flag",1 ), #
        ("foreground","black" ), #
        ("background","grey90" ), 
        ("selectforeground","white" ), #
        ("selectbackground","LightBlue4" ), 
        # cadet blue ,CadetBlue,CadetBlue3,CadetBlue4,
        # DodgerBlue4
        # LightBlue4
        # LightSkyBlue4
        # SkyBlue3 SkyBlue4
        # SteelBlue3 SteelBlue4
        ("background_for_panedwindow","grey50" ), #

         
        
        ("gamelist_font"      ,""  ),
        ("gamelist_font_size" ,0   ),
        ("gamelist_header_font"      ,""  ),
        ("gamelist_header_font_size" ,0   ),
        ("text_font"          ,""         ),
        ("text_font_size"     ,0          ),
        ("text_2_font"        ,""         ),
        ("text_2_font_size"   ,0          ),
        #("menu_font"          ,""           ),
        #("menu_font_size"     ,0            ),
        #("label_font"         ,""          ),
        #("label_font_size"    ,0           ),
        ("others_font"        ,""         ),
        ("others_font_size"   ,0          ),
        
        ("row_height"            ,0),
        ("row_height_for_header" ,0),
        #("row_height_for_text"   ,0),
        
        ("icon_size",16),
        
        ("tk_scaling_use_flag",0), # 0 , 1 ,ttk.Checkbutton  
        ("tk_scaling_number",0),
        

        #("use_available_game_mark",0 ), # 是否使用 标记
        #("available_game_mark","√" ),# 拥有游戏，标记
        ("unavailable_mark",False ), # 标记未拥有游戏，图标 - 号
        
        
        ("pos1",150),# 分隔线位置，目录｜游戏列表
        ("pos2",600),# 分隔线位置 ，游戏列表｜周边
        ("pos3",250),# 分隔线位置  ，图片1｜图片2
        
        
        ("extra_delay_time",    50),
        ("extra_delay_time_use_flag",1),# menu 中，初始化时，检验 0,1,
        
        ("extra_tab_index",0),

        ("extra_image_chooser_index",1),
        ("extra_image_chooser_2_index",0),
        ("extra_text_chooser_index",2),
        ("extra_command_type_chooser_index",0),
        
        ("extra_image_usezip",1),# 0 , 1 ,ttk.Checkbutton    
        ("extra_image_usezip_2",1),# 0 , 1 ,ttk.Checkbutton    
        ("extra_text_use_index_1",1),# 0 , 1 ,ttk.Checkbutton    
        ("extra_text_use_index_2",1),# 0 , 1 ,ttk.Checkbutton            
     
        ("index_be_chosen",''),  # 暂时，初始化为 空
        ("game_be_chosen",''),  # 暂时，初始化为 空
        #"index_set_remembered",set(),  # 有上面一项就够了
        

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
        ("other_image_1_path"   ,os.path.join(os.curdir,"other_image_1")    ),#r".\warning"
        ("other_image_2_path"   ,os.path.join(os.curdir,"other_image_2")    ),#r".\warning"
        ("other_image_3_path"   ,os.path.join(os.curdir,"other_image_3")    ),#r".\warning"
        
        ("snap.zip_path"   ,snap_zip_path   ),
        ("titles.zip_path" ,titles_zip_path ),
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
        ("other_image_1.zip_path"   ,os.path.join(os.curdir,"other_image_1.zip")    ),
        ("other_image_2.zip_path"   ,os.path.join(os.curdir,"other_image_2.zip")    ),
        ("other_image_3.zip_path"   ,os.path.join(os.curdir,"other_image_3.zip")    ),
        
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

    #print("")
    #print("ini_temp")
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
    #print("")
    
    return(ini_order,ini_default) # list   dict


# 读取 jjui.ini
#   并校验，部分数据校验
# ini_data
def get_configure_file_value( file_name ):
    ini_data ={} # 初始
    try: # 读取
        ini_data = read_ini( file_name )
    except:
        ini_data ={} 
    
    ini_order,ini_default=get_configure_file_default_value()



    # 部分 数据校验
    
    # ("encoding","" ),
    if "encoding" in ini_data:
        if ini_data["encoding"]:
            try :
                codecs.lookup(ini_data["encoding"])
            except:
                ini_data["encoding"]=ini_default["encoding"]
    
    # "tk_scaling_number" 大于0, 默认值为0 不修改
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
    for x in (
        #"gamelist_group_mark",
        "gamelist_sorted_reverse",
        "use_shell",
        "zoomed",
        "unavailable_mark",
        "use_locale_sort",
        "keep_track_of_the_select_item",
        ):
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
    # 不限范围
    for x in (
              #"font_size",
              "gamelist_font_size",
              "gamelist_header_font_size",
              "text_font_size",
              "text_2_font_size",
              #"menu_font_size",
              #"label_font_size",
              "others_font_size",
              "high_dpi",
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
                    pass
                else:
                    ini_data[x] = ini_default[x]  
    
  
    # int 类型的数据
    # >=0
    for x in (  "gamelist_level",
                "pos1","pos2","pos3",
                
                "extra_delay_time",
                "extra_tab_index",

                
                "extra_delay_time_use_flag",
                
              "row_height",
              "row_height_for_header",
              #"row_height_for_text",
              "icon_size",
              
              "tk_scaling_use_flag", # 选转为整数，用的时候，校验一下范围
              "use_colour_flag", # 选转为整数，用的时候，校验一下范围
              
              
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
    for x in ("gamelist_columns_to_show_1","gamelist_columns_to_show_2","gamelist_columns_to_show_3"):
        if x in ini_data:
            # 字符 转为 tuple
            if type( ini_data[x] ) == str : # 字符串，从 ini 文件中读取的值
                try:
                    ini_data[x] = eval( ini_data[x] )
                except:
                    pass
            #if type( ini_data[x] ) == tuple:
            #    # 与标准数据比较 columns
            #    temp_list = []
            #    for y in ini_data[x]:
            #        if y in columns:
            #            if y not in temp_list:
            #                temp_list.append(y)
            #    ini_data[x] = tuple(temp_list)

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
                    if type( ini_data[x][y] ) != int:
                        ini_data[x][y] = ini_default[x][y] # 数据 不是整数 读取默认值
                    elif ini_data[x][y] <=0:
                        ini_data[x][y] = ini_default[x][y] # 数据 小于0 读取默认值
            else: 
                ini_data[x] = ini_default[x]

    # "filter":类型为  list ,
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
            print('\t',end='')
            print(x,end='')
            print('\t',end='')
            print(ini_data[x])
    for x in ini_data:
        if x not in ini_order:
            print('\t',end='')
            print(x,end='')
            print('\t',end='')
            print(ini_data[x])
    
    return ini_data


if __name__ =="__main__":
    
    
    #ini_order,ini_default = get_configure_file_default_value()
    #print()
    #for x in ini_order:
    #    print(x)
    #
    #print()
    #for k,v in ini_default.items():
    #    print(k,"\t",end="")
    #    print(v)
    
    #ini_file=r"d:\temp\_s\tkinter\jjui2\.jjui\jjui.ini"
    ini_file=r".jjui\jjui.ini"
    temp_dict = read_ini(ini_file)
    number=0
    for k,v in temp_dict.items():
        print(number)
        print(k,v)
        number+=1