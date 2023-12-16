# -*- coding: utf_8_sig-*-
# import sys
import os
import time
import tkinter as tk
# from tkinter import ttk

from . import global_variable
from . import global_static_key_word_translation as key_word_translation
from . import global_static

from .ui_frames          import MainFrame
from .ui_menubar         import MenuBar
from .ui_toolbar         import ToolBar
from .ui_index           import GameIndex 

#from .ui_game_list_table_1_level import GameList
from .ui_game_list_table_1_level import GameList
from .ui_game_list_table_2_level import GameList as GameList_2
from .ui_game_list_table_2_level_collapse import GameList as GameList_3
#GameList_3 = GameList

from .ui_extra           import Extra
from .ui_statesbar       import StatesBar

from .                   import ui_small_windows # 显示 运行参数列表 小窗口

from . import folders_search 
from . import folders_read 
from .ui_misc import  misc_funcs


# from .read_pickle import read as read_pickle

# 读取外部目录数据
    # sl  and  mame
def get_external_index_data(folders_path):
    
    # 去掉 双引号
    folders_path = folders_path.replace(r'"',"")

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
    
    if ini_files:
        # 字符过滤一下，节省一点空间
        folders_read.all_dict={ game_id:game_id for game_id in global_variable.set_data["all_set"] }
        
        # 计算分类列表 具体信息
        for x in ini_files:
            temp = folders_read.read_folder_ini(x) ## 
            if temp is None:
                # 格式错误，只检查了个别错误
                pass
            else: 
                external_index_data[x] = temp  
        
        folders_read.all_dict={} # 清理
    
    return external_index_data


# 读取外部目录数据，只读目录，
#   sl 
#       by xml
#       .xml_ini
#
#   mame
#       by source
#       .source_ini
def get_external_read_only_index_data(folders_path,file_extension):
    
    # 去掉 双引号
    folders_path = folders_path.replace(r'"',"")

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
        ini_files.update( folders_search.search_ini( x ,file_extension=file_extension) )
    
    
    # 计算分类列表 具体信息
    for x in ini_files:
        temp = folders_read.read_folder_ini(x) ## 
        if temp==None:
            # 格式错误，只检查了个别错误
            pass
        else: 
            #external_index_data[x] = {} 
            external_index_data[x] = temp  
    
    return external_index_data






# 游戏列表界面，建立
def add_game_list( 
            gamelist_table_type,
            parent_window ,
            game_list_data,
            external_index,
            
            ):
            # global_variable.user_configure_data,
    gamelist_window = gamelist_table_type( parent_window, )
    gamelist_window.grid(row=0,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
    
    # 添加数据
    gamelist_window.new_func_feed_data(game_list_data,external_index)
    # 添加数据，所有列范围
    gamelist_window.new_func_set_all_columns( columns = global_variable.columns + ["#id",] ) # 增加 id 一列
    # 添加数据，列宽度
    gamelist_window.new_func_set_column_width( **global_variable.user_configure_data["gamelist_columns_width"] )
    # 添加数据，要显示的 列
    gamelist_window.new_func_set_columns_to_show( columns = global_variable.user_configure_data["gamelist_columns_to_show_1"] )
    # 添加数据，列标题 翻译
    gamelist_window.new_func_header_set_column_translation( key_word_translation.columns_translation )
    # 图标列
    gamelist_window.new_func_set_icon_column_index_in_header( global_variable.icon_column_index )
    
    return gamelist_window

def hide_other_table():
    
    # global_variable.the_showing_table 记录在 列表 new_func_show_gamelist_again 函数
    current_table = global_variable.the_showing_table
    
    for table in global_variable.all_tables:
        if table is not current_table:
            if table.winfo_ismapped():
                table.grid_remove()


def main(game_list_data,root,style):
    
    # 读取外部目录
    print()
    print("reading data from external index")
    time_external_0=time.time()
    external_index=get_external_index_data(global_variable.user_configure_data["folders_path"])
    print("time:",time.time()-time_external_0)
    del time_external_0
    # 记录
    global_variable.external_index = external_index
    
    # 读取外部目录 ,只读目录，
    # sl 部分，按 xml 分类
    if global_variable.gamelist_type == "softwarelist":
        print()
        print("reading data from external index ,SL only by xml")
        external_index_by_xml=get_external_read_only_index_data(global_variable.user_configure_data["folders_path"],".xml_ini")
        # 记录
        global_variable.external_index_sl_by_xml = external_index_by_xml
    # mame 部分按 source 分类
    elif global_variable.gamelist_type == "mame":
        print()
        print("reading data from external index ,mame only by source")
        external_index_by_source=get_external_read_only_index_data(global_variable.user_configure_data["folders_path"],".source_ini")
        # 记录
        global_variable.external_index_by_source = external_index_by_source
    
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
    
    main_frame = MainFrame(root)
    main_frame.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
    # 记录 PanedWindow ，方便获得分隔线 位置
    global_variable.PanedWindow = main_frame.frame_middle


    # ui menu bar
    ui_menubar = MenuBar(main_frame.frame_menu)
    ui_menubar.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
    
    # ui tool bar
    ui_toolbar = ToolBar(main_frame.frame_top)
    ui_toolbar.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
    
    
    # ui game index
    ui_index = GameIndex(main_frame.middle_1)
    ui_index.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
    # 记录
    global_variable.the_index = ui_index
    # 添加 内部目录数据
    #
    print("")
    print("index_order")
    print(global_static.index_order)
    ui_index.new_func_index_set_content_internal(
        game_list_data["internal_index"] ,
        translation_dict = key_word_translation.index_translation,
        index_order      = global_static.index_order,
        )
    
    # 添加 外部目录数据
    ui_index.new_func_index_set_content_external_ini(external_index)
    
    # 读取外部目录 ,只读目录，
    # 仅 sl 添加的功能
    if global_variable.gamelist_type == "softwarelist":
        ui_index.new_func_index_set_content_external_xml_ini(external_index_by_xml)
    # 仅 mame 部分
    elif global_variable.gamelist_type == "mame":
        ui_index.new_func_index_set_content_external_source_ini(external_index_by_source)
    

    
    
    # ui game list
    # 三种 列表，添加
    gamelist_table_1 = add_game_list ( 
            GameList,
            main_frame.middle_2,
            game_list_data,
            external_index ,
            #global_variable.user_configure_data,
            )
    gamelist_table_2 = add_game_list ( 
            GameList_2,
            main_frame.middle_2,
            game_list_data,
            external_index ,
            #global_variable.user_configure_data,
            )
    gamelist_table_2_collapse = add_game_list ( 
            GameList_3,
            main_frame.middle_2,
            game_list_data,
            external_index ,
            #global_variable.user_configure_data,
            )
    # 置顶一种
    if global_variable.user_configure_data["gamelist_level"] == 2:
        gamelist_table_2.new_func_show_gamelist_again()
    elif global_variable.user_configure_data["gamelist_level"] == 3:
        gamelist_table_2_collapse.new_func_show_gamelist_again()
    else:# 默认 1
        gamelist_table_1.new_func_show_gamelist_again()
    # 记录
    global_variable.all_tables.append(gamelist_table_1)
    global_variable.all_tables.append(gamelist_table_2)
    global_variable.all_tables.append(gamelist_table_2_collapse)


    # ui extra area
    ui_extra = Extra(main_frame.middle_3)
    ui_extra.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
    # 记录，方便之后　获得　分隔线　位置
    global_variable.Notebook_for_extra       = ui_extra.new_ui_notebook
    #global_variable.Combobox_chooser_image_1 = 
    #global_variable.Combobox_chooser_image_2 = 
    global_variable.PanedWindow_2            = ui_extra.new_ui_extra_image_panedwindow
    
    # ui states bar
    ui_statesbar = StatesBar(main_frame.frame_bottom)
    ui_statesbar.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
    
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
            隐藏其它列表
            目录信号重新发一下，以刷新列表
            
        """
        print()
        print("virtual event receive")
        print("<<GamelistChangeGroupMode>>")
        
        ### 从置顶列表中，读取 列宽设置、列标题显示范围设置
        top_table = global_variable.the_showing_table
        print(top_table)
        
        item_id = None
        if top_table is not None:
            columns_width   = top_table.new_func_get_column_width()
            columns_to_show = top_table.new_func_get_columns_to_show()

            item_id         = top_table.new_var_remember_select_row_id
            selected_items  = top_table.new_var_remember_selected_items

            # 多选模式
            multi_select_mode = top_table.new_var_tk_gamelist_multi_select_mode.get() # tk.IntVar
            sort_key     = top_table.new_var_data_holder.sort_key
            sort_reverse = top_table.new_var_data_holder.sort_reverse
            
            print(columns_width)
            print(columns_to_show)
            
        
        ### 把选中列表置顶
        
        # 1 ,2 ,3 
        temp = global_variable.user_configure_data["gamelist_level"]
        
        if temp not in (1,2,3) : temp=1
        
        temp = temp + 1
        
        if temp > 3: temp = 1
        
        global_variable.user_configure_data["gamelist_level"] = temp
        
        print(temp)
        print(global_variable.user_configure_data["gamelist_level"])
        
        def clear_other_table(the_table):
            for table in (gamelist_table_1,gamelist_table_2,gamelist_table_2_collapse):
                if table is not the_table:
                    table.new_func_hide_gamelist() 
                    print("")
                    print("table clear:")
                    print(table)
        
        def show_the_chosen_table(the_table):
            
            # 显示
            if not the_table.winfo_ismapped():
                the_table.grid()
            the_table.new_func_show_gamelist_again()
            
            clear_other_table(the_table) # 清理
            
            # 隐藏 其它
            hide_other_table()
            
            the_table.new_var_remember_select_row_id   = item_id # 当前项
            the_table.new_var_remember_selected_items  = selected_items # 所有选中项
            the_table.new_var_data_holder.sort_key     = sort_key
            the_table.new_var_data_holder.sort_reverse = sort_reverse
            # if item_id is not None:
            #     the_table.new_var_remember_selected_items.add(item_id)
            #           
            # 多选模式记录
            if multi_select_mode != the_table.new_var_tk_gamelist_multi_select_mode.get():
                the_table.new_var_tk_gamelist_multi_select_mode.set(multi_select_mode) # 多选模式，记录
                the_table.new_func_multi_select_mode_bind() # 多选模式，切换

            print()
            print(item_id)
            
            root.event_generate('<<RequestForIndexInfo>>')
            # 目录重新发个信号
            # 反正 index 数据没变，重新发个信号就行；就是搜索状态打断了
            
            # 列宽度
            if type(columns_width) == dict:
                the_table.new_func_set_column_width(**columns_width)
            
            # 列范围 
            #if columns_to_show: #非空，不管了
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
            columns = global_variable.user_configure_data["gamelist_columns_to_show_2"]
            top_table.new_func_set_columns_to_show( columns )
            print(columns)
        elif temp == 3:
            columns = global_variable.user_configure_data["gamelist_columns_to_show_3"]
            top_table.new_func_set_columns_to_show( columns )
            print(columns)
        else:# temp == 1
            columns = global_variable.user_configure_data["gamelist_columns_to_show_1"]
            top_table.new_func_set_columns_to_show( columns )
            print(columns)
        
        # 刷新
        top_table.new_func_refresh_all()
    # wip 
    # 还需要一个 列表 1，2，3 组，选择的 功能，小窗口
    

    ##################
    ##################
    ##################
    
    
    def just_for_test(event):
        table=global_variable.the_showing_table
        print()
        print("table")
        print(table)
        
        parent = table.winfo_parent()
        parent = root.nametowidget(parent)
        print()
        print("table's parent")
        print(parent)
        
        print()
        print("parent's other child")
        child_list = parent.winfo_children()
        for child in child_list :
            print()
            
            if child is table:
                print("the currnet table")
                
            print(child)
            print("is maped ?")
            if child.winfo_ismapped():
                print("mapped")
            else:
                print("not mapped")
    
        
        
    
    def some_bindings():
        root.bind('<<GamelistChangeGroupMode>>',virtual_event_receive_for_change_gamelist_group_mode)
        
        root.bind('<<GameListChangeColumnsToShow>>',virtual_event_receive_for_change_gamelist_change_columns)
        
        root.bind("<<StartGame>>",misc_funcs.start_game)
        root.bind("<<MameShowInfo>>",misc_funcs.mame_show_info)
        
        root.bind("<Control-KeyPress-t>",just_for_test)
        
        root.bind("<KeyPress-F1>",ui_small_windows.show_command_list)

    
    some_bindings()
    
    
    ##################
    ##################
    ##################
    
    # sl 模式，隐藏出招表
    # 放在 下边 那些 初始内容，前边
    if global_variable.gamelist_type == "softwarelist":
        ui_extra.new_ui_notebook.hide(2)
    
    ############
    # ui 初始，设置 配置文件中的 位置、选项
    def ui_initial():
        
        root.deiconify()
        
        # 窗口大小
        #root.update()
        if global_variable.user_configure_data["size"] != "" :
            try:
                root.geometry( global_variable.user_configure_data["size"] )
            except:
                pass
        #root.update()
        
        # 窗口最大化，初始
        if global_variable.user_configure_data["zoomed"]:
            root.wm_state("zoomed")
        else:
            pass
        
        # 周边图片区 分隔线
        # 分隔线位置，初始时，根据配置文件，设置一下
        root.update() # 前边不放一个 update ，就没有效果 ？？？？
        
        # 周边一个分隔线
        ui_extra.new_ui_extra_image_panedwindow.sashpos(0,global_variable.user_configure_data["pos3"])
        #root.update()
        
        root.update()
        
        # 周边，notebook，选择
        #   因为默认先显示的 图片区
        #   先调整 图片分隔线 位置，再选择 周边 区域
        #   图片区，能见的时候，调整分隔线，似乎才有用
        try:
            ui_extra.new_ui_notebook.select( global_variable.user_configure_data["extra_tab_index"] )
        except:
            pass
        # 初始化，两个 周边 图片 选择条，在 ui 部分已设置
        # 初始化，两个 周边 图片 zip 选择，在 ui 部分已设置
        
        
        misc_funcs.use_user_configure_row_height()
        misc_funcs.use_user_configure_row_height_for_header()
        misc_funcs.use_user_configure_icon_width()
        
        # 字体初始化
        misc_funcs.font_initial()
        
        # 测试
        #misc_funcs.find_widget('Canvas')
        
        #颜色
        if global_variable.user_configure_data["use_colour_flag"]:
            misc_funcs.use_user_configure_colours()
        
        

        
        root.update()
        # 初始时，分隔线,重置位置
        main_frame.frame_middle.sashpos(0,global_variable.user_configure_data["pos1"])
        main_frame.frame_middle.sashpos(1,global_variable.user_configure_data["pos2"])
        
    ui_initial()
    
    

    
    table = global_variable.the_showing_table
    # 上次记录的游戏
    game_name = global_variable.user_configure_data["game_be_chosen"]
    if game_name:
        if game_name in global_variable.set_data["all_set"]:
            table.new_var_remember_select_row_id = game_name
            table.new_var_remember_selected_items.add(game_name)
    # 排序 使用 记录值
    table.new_var_data_holder.sort_key  = global_variable.user_configure_data["gamelist_sorted_by"]
    table.new_var_data_holder.sort_reverse =global_variable.user_configure_data["gamelist_sorted_reverse"]
    # 目录 选择 上一次的记录
    root.update() # 不然,index 的 Treeview 部件，定位不准            
    global_variable.the_index.new_func_index_initial_select( global_variable.user_configure_data["index_be_chosen"] )

    # 初始化 拥有列表 过滤选项 
    # 在 ui_main.py 中过滤的
    
    #隐藏 其它 两个列表
    # 放在 update 之后，不然 还没有 map 好
    hide_other_table()
    
    root.protocol("WM_DELETE_WINDOW", misc_funcs.exit_2)