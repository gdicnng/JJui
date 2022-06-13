﻿# -*- coding: utf_8_sig-*-
import sys
import os
import tkinter as tk
from tkinter import ttk 

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

from . import global_variable
from . import global_static_key_word_translation as key_word_translation
from . import global_static

from .ui_frames          import MainFrame
from .ui_menubar         import MenuBar
from .ui_toolbar         import ToolBar
from .ui_index           import GameIndex 
from .ui_statesbar       import StatesBar 


#from .ui_game_list_table_1_level import GameList
from .ui_game_list_table_1_level import GameList
from .ui_game_list_table_2_level import GameList as GameList_2
from .ui_game_list_table_2_level_collapse import GameList as GameList_3

from .ui_extra           import Extra
from .ui_statesbar       import StatesBar

from . import folders_search 
from . import folders_read 
from .ui_misc import  misc_funcs



from .read_pickle import read as read_pickle

configure_data = global_variable.user_configure_data

# style
def change_menubutton(style):
    
    layout_2=[
        ('Menubutton.border', {'sticky': 'nswe', 'children': [
         ('Menubutton.focus', {'sticky': 'nswe', 'children': [
          ('Menubutton.padding', {'expand': '1', 'sticky': 'we', 'children': [
           ('Menubutton.label', {'side': 'left', 'sticky': ''})]})]})]})
                ]
    
    # 去掉箭头
    style.layout('TMenubutton',layout_2)


# test ,will be deleted
def show_childrens(window):
    # w.winfo_children()
    # w.winfo_class()
    print()
    print("find children windows")
    print()
    
    # 查找
    result=[]
    def find_childen(window):
        for child in window.winfo_children():
            result.append(child)
            find_childen(child)
    find_childen(window)
    
    # 结果
    if result : 
        for x in result:
            print(x)
            #print(type(x))
        
    print()
    print("find children windows result")
    print("total numbers : {}".format(len(result)))


# 读取外部目录数据
def get_external_index_data(folders_path):
    # 分类列表文件  
    ini_files = {} # 初始化
        # keys,为 （相对/绝对）路径 + 文件名 ，
        # values ，为 文件名，不含路径
    # 分类列表，具体信息
    external_index_data = {} # 初始化
        # keys,为 （相对/绝对）路径 + 文件名 ，
        # values ，为 为一个 {}
            # keys,为子分类名，
            # values,为，分类游戏，集合 ,后来 转为 list 格式了
    # 查找 文件
    for x in folders_path.split(';') :
        if global_variable.gamelist_type == "softwarelist":
            ini_files.update( folders_search.search_ini( x ,file_extension=".sl_ini") )
        else:
            ini_files.update( folders_search.search_ini( x ) )
    
    # 计算分类列表 具体信息
    for x in ini_files:
        temp = folders_read.read_folder_ini_3(x) ## 
        if temp==None:
            # 格式错误，只检查了个别错误
            pass
        else: 
            external_index_data[x] = {} # 初始化
            external_index_data[x] = temp  
    
    return external_index_data

# 游戏列表界面，建立
def add_game_list( 
            gamelist_table_type,
            parent_window ,
            game_list_data,
            external_index,
            configure_data,
            ):
        
        gamelist_window = gamelist_table_type( parent_window, )
        gamelist_window.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
        
        # 添加数据
        gamelist_window.new_func_feed_data(game_list_data,external_index)
        # 添加数据，所有列范围
        gamelist_window.new_func_set_all_columns( columns = global_variable.columns )
        # 添加数据，列宽度
        gamelist_window.new_func_set_column_width( **configure_data["gamelist_columns_width"] )
        # 添加数据，要显示的 列
        gamelist_window.new_func_set_columns_to_show( columns = configure_data["gamelist_columns_to_show_1"] )
        # 添加数据，列标题 翻译
        gamelist_window.new_func_header_set_column_translation( key_word_translation.columns_translation )
        
        return gamelist_window



def main(game_list_data):
    root  = global_variable.root_window
    style = ttk.Style()
    
    # 读取外部目录
    external_index=get_external_index_data(configure_data["folders_path"])
    
    # 记录
    global_variable.external_index = external_index
    
    # 记录
    # 外部目录中，可编辑的文件
    for x in external_index:
        if os.access(x,os.W_OK):
            global_variable.external_index_files_editable.add(x)
    #print()
    #print()
    #print(global_variable.external_index_files_editable)
    
    
    root.rowconfigure(0, weight=1)#
    root.columnconfigure(0, weight=1)
    
    # 标题更新
    title_string = root.title()
    title_string = title_string + game_list_data["mame_version"]
    root.title(title_string)


    
    
    # ttk.Menubutton 去掉箭头
    change_menubutton(style)
    
    main_frame = MainFrame(root)
    main_frame.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    # 记录 PanedWindow ，方便获得分隔线 位置
    global_variable.PanedWindow = main_frame.frame_middle


    # ui menu bar
    ui_menubar = MenuBar(main_frame.frame_menu)
    ui_menubar.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    
    # ui tool bar
    ui_toolbar = ToolBar(main_frame.frame_top)
    ui_toolbar.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    
    # ui game index
    ui_index = GameIndex(main_frame.middle_1)
    ui_index.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    # 添加 内部目录数据
    #
    print(global_static.index_order)
    ui_index.new_func_index_set_content_internal(
        game_list_data["internal_index"] ,
        translation_dict = key_word_translation.index_translation,
        index_order      = global_static.index_order,
        )
    
    # 添加 外部目录数据
    ui_index.new_func_index_set_content_external_ini(external_index)
    
    # ui game list
    # 三种 列表，添加
    gamelist_table_1 = add_game_list ( 
            GameList,
            main_frame.middle_2,
            game_list_data,
            external_index ,
            configure_data,
            )
    gamelist_table_2 = add_game_list ( 
            GameList_2,
            main_frame.middle_2,
            game_list_data,
            external_index ,
            configure_data,
            )
    gamelist_table_2_collapse = add_game_list ( 
            GameList_3,
            main_frame.middle_2,
            game_list_data,
            external_index ,
            configure_data,
            )
    # 置顶一种
    if configure_data["gamelist_level"] == 2:
        gamelist_table_2.new_func_show_gamelist_again()
    elif configure_data["gamelist_level"] == 3:
        gamelist_table_2_collapse.new_func_show_gamelist_again()
    else:# 默认 1
        gamelist_table_1.new_func_show_gamelist_again()
    
    # 记录
    global_variable.all_tables.append(gamelist_table_1)
    global_variable.all_tables.append(gamelist_table_2)
    global_variable.all_tables.append(gamelist_table_2_collapse)


    # ui extra area
    ui_extra = Extra(main_frame.middle_3)
    ui_extra.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    # 记录，方便之后　获得　分隔线　位置
    global_variable.Notebook_for_extra       = ui_extra.new_ui_notebook
    #global_variable.Combobox_chooser_image_1 = 
    #global_variable.Combobox_chooser_image_2 = 
    global_variable.PanedWindow_2            = ui_extra.new_ui_extra_image_panedwindow
    
    # ui states bar
    ui_statesbar = StatesBar(main_frame.frame_bottom)
    ui_statesbar.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    
    total_number = len(game_list_data["machine_dict"])
    ui_statesbar.new_ui_label_total_number.configure(text=_("总数量：")+str(total_number)+" . ")



    # 接收，列表切换信号，1层列表、2层列表、2层列表（可收缩）
    # 直接，换一个列表
    # <<GamelistChangeGroupMode>>
    def virtual_event_receive_for_change_gamelist_group_mode(event):
        """ 
            从置顶列表中，读取 列宽设置、列标题显示范围设置
            
            把选中列表置顶
                （记忆置顶的 列表，在列表 new_func_show_gamelist_again() 中弄）
            bind ,重新 bind 一下
            清空另外两列表
            目录信号重新发一下，以刷新列表
            
        """
        print()
        print("virtual event receive")
        print("<<GamelistChangeGroupMode>>")
        
        ### 从置顶列表中，读取 列宽设置、列标题显示范围设置
        top_table = global_variable.the_showing_table
        print(top_table)
        
        if top_table is not None:
            columns_width = top_table.new_func_get_column_width()
            columns_to_show = top_table.new_func_get_columns_to_show()
            print(columns_width)
            print(columns_to_show)
            
        
        ### 把选中列表置顶
        
        # 1 ,2 ,3 
        temp = configure_data["gamelist_level"]
        
        if temp not in (1,2,3) : temp=1
        
        temp = temp + 1
        
        if temp > 3: temp = 1
        
        configure_data["gamelist_level"] = temp
        
        print(temp)
        print(configure_data["gamelist_level"])
        
        def clear_other_table(the_table):
            for table in (gamelist_table_1,gamelist_table_2,gamelist_table_2_collapse):
                if table is not the_table:
                    table.new_func_hide_gamelist() 
                    print("")
                    print("table clear:")
                    print(table)
        
        
        def show_the_chosen_table(the_table):
            
            clear_other_table(the_table) # 清理
            
            the_table.new_func_show_gamelist_again()
            
            
            root.event_generate('<<RequestForIndexInfo>>')
            # 目录重新发个信号
            # 反正 index 数据没变，重新发个信号就行；就是搜索状态打断了
            
            # 列宽度
            if type(columns_width) == dict:
                the_table.new_func_set_column_width(**columns_width)
            
            # 列范围
            if columns_to_show:
                the_table.new_func_set_columns_to_show(columns_to_show)
            
            
            #the_table.new_func_refresh_all()
            the_table.new_func_table_reload_the_game_list()
            
        if temp==2 :
            show_the_chosen_table(gamelist_table_2)
        elif temp==3:
            show_the_chosen_table(gamelist_table_2_collapse)
        else   :# temp==1
            show_the_chosen_table(gamelist_table_1)
    # 接收，列表 列项目 切换：1组、2组、3组
    # 1组、2组 方便 中英文 切换显示；
    # 第3组，显示整体
    # <<GameListChangeColumnsToShow>>
    def virtual_event_receive_for_change_gamelist_change_columns(event):
        print("")
        print("")
        print("")
        print("virtual event receive")
        print("<<GameListChangeColumnsToShow>>")
        
        ### 从置顶列表中，读取 列宽设置、列标题显示范围设置
        top_table = global_variable.the_showing_table
        
        # 读取计数
        temp = global_variable.column_group_counter
        if temp not in (1,2,3) : temp = 1
        temp += 1
        if temp not in (1,2,3) : temp = 1
        global_variable.column_group_counter = temp
        
        print(temp)
        
        # 根据计数，切换列表
        if temp == 2:
            columns = configure_data["gamelist_columns_to_show_2"]
            top_table.new_func_set_columns_to_show( columns )
            print(columns)
        elif temp == 3:
            columns = configure_data["gamelist_columns_to_show_3"]
            top_table.new_func_set_columns_to_show( columns )
            print(columns)
        else:# temp == 1
            columns = configure_data["gamelist_columns_to_show_1"]
            top_table.new_func_set_columns_to_show( columns )
            print(columns)
        
        # 刷新
        top_table.new_func_refresh_all()
    # wip 
    # 还需要一个 列表 1，2，3 组，选择的 功能，小窗口
    

    def some_bindings():
        root.bind('<<GamelistChangeGroupMode>>',virtual_event_receive_for_change_gamelist_group_mode)
        root.bind('<<GameListChangeColumnsToShow>>',virtual_event_receive_for_change_gamelist_change_columns)
        
        root.bind('<Control-KeyPress-t>',lambda event : show_childrens(root))
        root.bind('<Control-KeyPress-T>',lambda event : show_childrens(root))
    
        root.bind("<<StartGame>>",misc_funcs.start_game)
        root.bind("<<MameShowInfo>>",misc_funcs.mame_show_info)
    some_bindings()
    
    
    ############
    # ui 初始，设置 配置文件中的 位置、选项
    def ui_initial():
        
        root.deiconify()
        
        # 窗口大小
        #root.update()
        if configure_data["size"] != "" :
            try:
                root.geometry( configure_data["size"] )
            except:
                pass
        #root.update()

        # 分隔线位置，初始时，根据配置文件，设置一下
        root.update() # 前边不放一个 updata ，就没有效果 ？？？？
        
        # 初始时，分隔线,重置位置
        main_frame.frame_middle.sashpos(0,configure_data["pos1"])
        main_frame.frame_middle.sashpos(1,configure_data["pos2"])
        # 还有周边一个分隔线
        ui_extra.new_ui_extra_image_panedwindow.sashpos(0,configure_data["pos3"])
        #root.update()
    
        # 周边，notebook，选择
        try:
            ui_extra.new_ui_notebook.select( configure_data["extra_tab_index"] )
        except:
            pass
        
        # 初始化，两个 周边 图片 选择条，在 ui 部分已设置
        # 初始化，两个 周边 图片 zip 选择，在 ui 部分已设置
        
        
    ui_initial()
    
    
    misc_funcs.use_user_configure_row_height()
    misc_funcs.use_user_configure_row_height_for_header()
    misc_funcs.use_user_configure_icon_width()
    
    # 字体初始化
    misc_funcs.font_initial()
    
    # 测试
    #misc_funcs.find_widget('Canvas')
    
    #颜色
    misc_funcs.use_user_configure_colours()
    
    root.protocol("WM_DELETE_WINDOW", misc_funcs.exit_2)