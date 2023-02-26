# -*- coding: utf_8_sig-*-
#import sys
import os
import sys
import re


# gamelist_type="mame" #  "softwarelist"

import tkinter as tk
from tkinter import ttk

from . import global_variable
from . import global_static_filepath as the_files
from . import global_static

from .ui_toplevel_window_mame_initial    import Toplevel_Window as initial_window
from .ui_toplevel_window_mame_initial_sl import Toplevel_Window as initial_window_sl

from .read_pickle import read as read_pickle

# from . import read_user_config
from . import ui_themes
from . import ui_high_dpi

from .ui_misc import  misc_funcs # import 在后边，有些变量值，之前，还没有赋值


# 因为 global_variable 赋值
# 有些 import 最好放在后边

# from . import ui_main_window as main_window
    # 这个 到 最后 import ，因为 global_variable 有些常用变量还没有赋值


"""
    
    # ttk.Treeview 颜色 bug
    
    # ui
        # themes 第三方主题
        # themes 第三方主题 ，微调
    
    # 初始化窗口
        # 检查临时数据文件，没有的话，
            # 打开一个小窗口 让用户选择 模拟器
            # 初始化，从 mame 读取数据，生成数据文件
    # 主窗口
        # 检查临时数据文件，有的话，
            # 打开主 ui 主窗口
    
"""

# bug fix
# Treeview 颜色 bug ，版本 tkinter 8.6.9
def fixed_map(option,style):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
      elm[:2] != ('!disabled', '!selected')]

def gamelist_data_file_exist():
    
    the_file_path = the_files.file_pickle_gamelist_data
    
    flag = False
    
    if os.path.isfile( the_file_path ):
        flag = True
    else:
        flag = False
    
    #print("if file exist")
    #print(the_file_path)
    #print(flag)
    
    return flag


#########
def main():
    
    root=tk.Tk()
    
    # 记录
    global_variable.root_window = root
    
    # windows 10 high dpi
    ui_high_dpi.main(root,global_variable.user_configure_data["high_dpi"])
    
    # 记录
    num = root.tk.call('tk', 'scaling', )
    global_variable.tk_scaling_number_0 = num
    
    if global_variable.user_configure_data["tk_scaling_number"]:
        try:root.tk.call('tk', 'scaling', global_variable.user_configure_data["tk_scaling_number"])
        except:pass
    
    style=ttk.Style()
    
    ui_themes.main(root,style)
    

    root.iconify() 
    root.withdraw()
    
    
    # bug fix
    # Treeview 颜色 bug ，版本 tkinter 8.6.9
    if root.tk.call('info', 'patchlevel')=="8.6.9":
        print("8.6.9")
        style.map('Treeview', 
                    foreground=fixed_map('foreground',style),
                    background=fixed_map('background',style),
                    )
    # bug fix
    # 放在 style.theme_use("xxxxxx") 后面 ，才有用
    # ？？？？？                   
    
    # 标题 前一段 ；标题 后一段  ，需 读取 mame 版本信息后，再添加
    str_title = global_static.version_string + " - " + global_static.title_string + " - "
    root.title( str_title )
    
    # 图标
    try:
        #root.iconphoto(False, tk.PhotoImage(file= the_files.image_path_icon_main ) )
        root.iconphoto(True, tk.PhotoImage(file= the_files.image_path_icon_main ) )
    except:
        pass
    
    start_from_empty_state = False
    
    
    # 初始化窗口
    # 选择模拟器，读取数据，写入数据到 pickle 文件
    if not gamelist_data_file_exist():
        
        start_from_empty_state = True
        
        if global_variable.gamelist_type == "softwarelist":
            window_for_initial = initial_window_sl()
        else:
            window_for_initial = initial_window()
        
        root.wait_window( window_for_initial )
    
    # 数据 pickle 文件 ，如果没有找到，说明上一步，出问题了，退出
    if not gamelist_data_file_exist():
    
        root.deiconify()
        root.destroy()
        the_file_path = the_files.file_pickle_gamelist_data
        print(" file is missing:\t",end="")
        print(the_file_path)
        print("exit")
        sys.exit(1)
    
    # 数据文件中 的数据
    game_list_data={}
    # 拥有列表文件中 的数据
    available_game_list=set()
    # 然后，打开主窗口
    if gamelist_data_file_exist():
        
        # 如果是 从 初始化 开始的
        # 此处，保存一下配置文件
        if start_from_empty_state:
            misc_funcs.save_user_configure_just_after_initial()
        
        # 数据文件
        main_data_file_path = the_files.file_pickle_gamelist_data
        try:
            game_list_data = read_pickle( main_data_file_path )
        except:
            game_list_data = {}
        
        if game_list_data:
            # global_variable 赋值
            global_variable.all_data       = game_list_data
            global_variable.mame_version   = game_list_data["mame_version"]
            global_variable.columns        = game_list_data["columns"]
            global_variable.machine_dict   = game_list_data["machine_dict"]
            global_variable.dict_data      = game_list_data["dict_data"]
            global_variable.set_data       = game_list_data["set_data"]
            global_variable.internal_index = game_list_data["internal_index"]
            
            #
            global_variable.columns_index = {}
            columns = global_variable.columns
            for index_number in range(len(columns)):
                global_variable.columns_index[columns[index_number]] = index_number
            
            # global_variable.icon_column_index = None # 如果列表被删空了
            # 每个元素中，图标颜色信息的项目
            if global_variable.gamelist_type == "mame":
                global_variable.icon_column_index = global_variable.columns_index.get("status",None)
            elif  global_variable.gamelist_type == "softwarelist":
                global_variable.icon_column_index = global_variable.columns_index.get("supported",None)
            
            # global_variable.search_columns_set = set()
            # 列表，搜索限制，选择 搜索哪些 列
            # 初始化为全部
            global_variable.search_columns_set = set( global_variable.columns + ["#id",] )
            
            print("")
            print("columns")
            print(global_variable.columns)
            print(global_variable.columns_index)
            
        # 拥有列表文件
        # available_game_list_data
        available_file =  the_files.file_pickle_gamelist_available
        try:
            available_game_list_data = read_pickle( available_file )
        except:
            available_game_list_data = set()
        
        
        # 拥有列表，自定义过滤文本
        hide_file = the_files.file_txt_hide_gamelist_available
        available_hide_set = set()
        if os.path.isfile( hide_file ):
            lines=[]
            
            with open(hide_file, 'rt',encoding='utf_8_sig') as text_file :
                lines = text_file.readlines()
            
            temp = []
            #search_str = r'^\s*(\S.*?)\s*$'
            search_str = r'^(.+)$'
            p=re.compile( search_str, )
            
            for line in lines:
                
                line = line.strip()
                
                if not line:
                    continue
                
                m=p.search( line ) 
                if m:
                    temp.append( m.group(1).lower() ) # 转小写
            
            available_hide_set = set(temp) & game_list_data['set_data']['all_set']
            print()
            print("hide_set")
            print( len(available_hide_set) )
            print()
            
            # 记录
            global_variable.available_hide_set = available_hide_set
        
        
        
        
        
        
        # 初始化过滤项
        # 仅 mame ，比如 bios 、devices、机械类 等
        if global_variable.gamelist_type == "softwarelist":
            pass
        else:
            misc_funcs.initial_available_filter_set()
        
        misc_funcs.set_available_gamelist(available_game_list_data,need_save=False)

        #root.deiconify()
        
        
        #######
        from . import ui_main_window as main_window
        
        main_window.main( game_list_data ,root,style)
    
    
    # alt 键：会打断 进度条 ；会跳转到菜单上，麻烦；……
    # 所以重新 bind 一下
    root.bind('<KeyPress-Alt_L>',lambda event : "break")
    root.bind('<KeyPress-Alt_R>',lambda event : "break")
    
    
    root.mainloop()