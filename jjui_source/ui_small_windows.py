# -*- coding: utf_8_sig-*-
#import os
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from . import misc
from . import global_variable
from . import global_static_key_word_translation
from . import global_static_filepath as the_files
from .ui_misc import  misc_funcs
from . import save_pickle 
from . import ui__text_with_scrollbar
from . import extra_command

# 搜索范围，选择 列
def window_for_gamelist_set_search_columns():
    # global_static_key_word_translation.columns_translation {}
    # global_variable.columns []
    # global_variable.columns_index {}
    
    # 这个是 搜索 范围
    # global_variable.search_columns_set
    
    root = global_variable.root_window
    
    translation_dict = global_static_key_word_translation.columns_translation
    
    window = tk.Toplevel()
    #window.geometry( "400x300" )
    window.resizable(width=True, height=True)
    window.title(_("搜索范围"))
    checkbuttons={}
    checkbuttons_variable={}
    
    def for_ok_button():
        print()
        
        is_empty = True
        for the_id in sorted(  global_variable.columns + ["#id",]  ):
            if checkbuttons_variable[the_id].get():
                is_empty = False
                break
        
        if is_empty:
            text = _("搜索范围，至少要选一项")
            messagebox.showwarning(message=text)
        
        else:
            # 大小写
            global_variable.search_ignorecase = ignore_case.get()
            
            # 列范围 （全部列 + id 列）
            global_variable.search_columns_set.clear()
            for the_id in sorted(  global_variable.columns + ["#id",]  ):
                if checkbuttons_variable[the_id].get():
                    global_variable.search_columns_set.add( the_id )
            
            print()
            for x in sorted(global_variable.search_columns_set):
                print(x)
            window.destroy()
    
    n=0
    ok_button = ttk.Button(window,text="OK",command=for_ok_button)
    ok_button.grid(row=n,sticky=tk.W)
    n+=1
    
    ignore_case = tk.IntVar()
    if global_variable.search_ignorecase:
        ignore_case.set(1)
    else:
        ignore_case.set(0)

    ttk.Checkbutton(window, text=_("忽略大小写"),variable=ignore_case).grid(row=n,sticky=tk.W)
    n+=1
    
    ttk.Separator(window,orient=tk.HORIZONTAL).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    ttk.Label(window,text=_("搜索范围(按列)")).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    
    ttk.Separator(window,orient=tk.HORIZONTAL).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    for the_id in sorted(  global_variable.columns + ["#id",]  ):
        
        checkbuttons_variable[the_id] = tk.IntVar()
        
        if the_id in global_variable.search_columns_set:
            checkbuttons_variable[the_id].set(1)
        else:
            checkbuttons_variable[the_id].set(0)
        
        if the_id in translation_dict:
            text = translation_dict[the_id]
        else:
            text = the_id
        
        checkbuttons[the_id] = ttk.Checkbutton(window, text=text,variable=checkbuttons_variable[the_id])
        checkbuttons[the_id].grid(row=n,sticky=tk.W)
        n+=1
        
    window.lift(root)
    window.transient(root)
    
    window.wait_window()

# 非窗口
# 目录 重新 发送信号，列表刷新
def request_for_index_info(jump_to_available=False):
    
    # 内空变化了，比如 过滤 功能时，需要 取消掉 记录
    # table  重置 记录
    global_variable.the_showing_table.new_var_remember_last_index_data = None
    
    if jump_to_available:
        global_variable.root_window.event_generate('<<RequestForAvailableGameList>>')
    else:
        # 从目录 读取 数据
        global_variable.root_window.event_generate('<<RequestForIndexInfo>>')

# 游戏列表 全局 过滤 
def window_for_gamelist_filter():
    ###
    # global_variable
    ###
    
    root = global_variable.root_window
    
    window = tk.Toplevel()
    
    window.resizable(width=True, height=True)
    
    #size = "400x300" 
    #window.geometry(size)
    
    window.title(_("全局过滤"))
    
    window.lift()
    window.transient(root)
    
    translation_dict = {
        "parent":_("主版"),
        "clone":_("克隆版"),
        "driver status good"        :_("模拟状态 good"),
        "driver status imperfect"   :_("模拟状态 imperfect"),
        "driver status preliminary" :_("模拟状态 preliminary"),
    }
    
    
    all_set_list = ["parent","clone",]
    
    if global_variable.gamelist_type == "mame" :
        if misc.get_id_list_from_internal_index("bios"):
            all_set_list.append( "bios")
        if misc.get_id_list_from_internal_index("device"):
            all_set_list.append( "device")
        if misc.get_id_list_from_internal_index("mechanical"):
            all_set_list.append( "mechanical")
        #chd
        if misc.get_id_list_from_internal_index("chd"):
            all_set_list.append( "chd")
        #softwarelist
        if misc.get_id_list_from_internal_index("softwarelist"):
            all_set_list.append( "softwarelist")
        # status
        # driver status good
        # driver status imperfect
        # driver status preliminary
        if misc.get_id_list_from_internal_index("status","good"):
            all_set_list.append( "driver status good")
        if misc.get_id_list_from_internal_index("status","imperfect"):
            all_set_list.append( "driver status imperfect")
        if misc.get_id_list_from_internal_index("status","preliminary"):
            all_set_list.append( "driver status preliminary")
        # driver savestate supported
        # driver savestate unsupported
        # nodump
        # baddump
    elif global_variable.gamelist_type == "softwarelist" :
        # supported
        if misc.get_id_list_from_internal_index("supported","yes"):
            all_set_list.append( "supported yes")
        if misc.get_id_list_from_internal_index("supported","partial"):
            all_set_list.append( "supported partial")
        if misc.get_id_list_from_internal_index("supported","no"):
            all_set_list.append( "supported no")
    
    tk_int_dict = {}
    


    def for_ok_button():
        print()
        #
        #global_variable.filter_set
        temp_set = set()
        global_variable.filter_list.clear()
        for the_key in tk_int_dict:
            print(the_key,tk_int_dict[the_key].get())
            if tk_int_dict[the_key].get():
                global_variable.filter_list.add(the_key)# 记录
                if global_variable.gamelist_type == "mame" :
                    if the_key =="parent":
                        temp_set.update( global_variable.set_data["parent_set"] )
                    elif the_key =="clone":
                        temp_set.update( global_variable.set_data["clone_set"] )
                    # bios
                    # device
                    # mechanical
                    # chd
                    # softwarelist
                    elif the_key in ("bios","device","mechanical","chd","softwarelist",):
                        temp_set.update( misc.get_id_list_from_internal_index(the_key) )
                    # driver status good
                    # driver status imperfect
                    # driver status preliminary
                    elif the_key in ("driver status good","driver status imperfect","driver status preliminary",):
                        #id_1 = "status"
                        id_2 = the_key.split(" ")[-1]
                        temp_set.update( misc.get_id_list_from_internal_index("status",id_2) ) 
                elif global_variable.gamelist_type == "softwarelist" :
                    if the_key =="parent":
                        temp_set.update( global_variable.set_data["parent_set"] )
                        
                    elif the_key =="clone":
                        temp_set.update( global_variable.set_data["clone_set"] )
                    elif the_key in ("supported yes","supported partial","supported no"):
                        #id_1 = "supported"
                        id_2 = the_key.split(" ",1)[1]
                        temp_set.update( misc.get_id_list_from_internal_index("supported",id_2) ) 
                    
        global_variable.filter_set = temp_set
        if not global_variable.filter_set:
            print("")
            print("choose nothing")
        
        #
        request_for_index_info()
        
        window.destroy()

    n = 0
    button=ttk.Button(window,text=_("确认"),command=for_ok_button)
    button.grid(row=n,column=0,sticky=tk.W+tk.N,)
    n+=1

    ttk.Label(window,text=_("选择不想显示的种类"),).grid(row=n,column=0,sticky=tk.W+tk.N)
    n+=1
    
    ttk.Label(window,text=_("有些种类，一起选，可能游戏列表就空了"),).grid(row=n,column=0,sticky=tk.W+tk.N)
    n+=1
    
    ttk.Label(window,text=_("程序关闭后，此选项不会被保存"),).grid(row=n,column=0,sticky=tk.W+tk.N)
    n+=1
    
    for the_key in all_set_list:
        tk_int_dict[the_key]=tk.IntVar()
        
        if the_key in global_variable.filter_list:
            tk_int_dict[the_key].set(1) 
        else:
            tk_int_dict[the_key].set(0) # 默认都不选
        
        if the_key in translation_dict:
            text = translation_dict[the_key]
        else:
            text = the_key
        
        ttk.Checkbutton(window, text=text,variable= tk_int_dict[the_key] ).grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
    
    
    
    ttk.Sizegrip(window).grid(row=n,column=0,sticky=tk.E+tk.S)
    window.rowconfigure(n, weight=1)
    window.columnconfigure(0, weight=1)
    n+=1
    
    
    window.wait_window()

# 拥有列表 过滤
def window_for_gamelist_available_filter():
    
    user_configure=global_variable.user_configure_data
    
    window = tk.Toplevel()
    
    window.resizable(width=True, height=True)
    
    size = "400x300" 
    window.geometry(size)
    
    window.title(_("拥有列表过滤"))
    
    window.lift()
    window.transient(global_variable.root_window)
    
    the_level_1_list = ["bios","mechanical","device","chd","softwarelist"]
    
    
    def for_ok_button():
        
        temp = set(user_configure["filter"])
        
        for the_key in tk_int_dict:
            if tk_int_dict[the_key].get():
                temp.add(the_key)
            else:
                temp.discard(the_key)
        
        user_configure["filter"].clear()
        user_configure["filter"].extend( temp ) 
        
        global_variable.available_filter_set.clear()  # 重置 ，重新计算
        
        for x in user_configure["filter"]:
            if x in the_level_1_list:
                global_variable.available_filter_set.update( misc.get_id_list_from_internal_index(x) )
        
        print("available gamelist filter list")
        print( user_configure["filter"] )
        
        # 
        request_for_index_info(jump_to_available=True)
        
        window.destroy()
    
    
    tk_int_dict = {}
    for the_key in the_level_1_list:
        tk_int_dict[the_key] = tk.IntVar()
    
    n=0
    
    for the_key in tk_int_dict:
        if the_key in user_configure["filter"]:
            tk_int_dict[the_key].set(1)
        else:
            tk_int_dict[the_key].set(0)
        
        if misc.get_id_list_from_internal_index(the_key):
            temp  = ttk.Checkbutton(window, text=the_key,variable=tk_int_dict[the_key])
            temp.grid(row=n,column=0,sticky=tk.W+tk.N,)
            n+=1
    
    button=ttk.Button(window,text=_("确认"),command=for_ok_button)
    button.grid(row=n,column=0,sticky=tk.W+tk.N,)
    n+=1
    
    window.wait_window()


##########
##########
# gamelist ，标题处，右键 菜单 ，选择 显示 哪些 列
# a topleve window 
def header_pop_up_menu_callback_choose_columns():
    # a topleve window 
    # -------------------------------
    # |所有项| 第1组 | 第2组 | all |
    # |  0   |   1   |   2   |  3  |
    # |      |       |       |     |
    # |      |       |       |     |
    # |      |       |       |     |
    # |      |       |       |     |
    # |      |       |       |     |
    # |      |       |       |     |
    # -------------------------------
    #                       确定   |
    # -------------------------------
    
    # global_variable.user_configure_data
        # global_variable.user_configure_data["gamelist_columns_to_show_1"] # 第1组
        # global_variable.user_configure_data["gamelist_columns_to_show_2"] # 第2组
        # global_variable.user_configure_data["gamelist_columns_to_show_3"]           # 第3组
        
        # global_variable.columns + #id  # 第0组 ,所有项
        # "key_word_translation.columns_translation"
    
    # self.menu_call_back_function_save_ini_data()
    key_word_translation = global_static_key_word_translation
    root = global_variable.root_window
    
    window = tk.Toplevel()
    window.resizable(width=True, height=True)
    window.title(_("选择游戏列表显示项目"))
    
    #size = "400x300"
    #window.geometry( size )
         
    window.lift(root)
    window.transient(root)
    #window.grab_set()
    
    
    def add_to(a_treeview):# 第0组，选中项，添加到 另一组
        # no_0
        x = no_0.focus()
        if x:
            if x not in a_treeview.get_children():
                if x in key_word_translation.columns_translation:
                    a_treeview.insert("",'end',iid=x,text=key_word_translation.columns_translation[x])
                else:
                    a_treeview.insert("",'end',iid=x,text=x)
            a_treeview.selection_set( (x,) )
            a_treeview.focus( x )

    def delete_from_a_treeview(a_treeview):# 第1、2、3组，中，删除选中项
        x = a_treeview.focus()
        print(x)
        
        # 记录，删除以后，选中 相邻的项目
        the_next_item = a_treeview.next(x)
        the_prev_item = a_treeview.prev(x)
        
        if x:
            a_treeview.delete( x ) 
        
        # 删除以后，选中 相邻的项目
        if the_next_item:
            a_treeview.selection_set( (the_next_item,) )
            a_treeview.focus( the_next_item )
        elif the_prev_item:
            a_treeview.selection_set( (the_prev_item,) )
            a_treeview.focus( the_prev_item )
    
    def move_up(a_treeview):# 选中项，向上移
        x = a_treeview.focus()
        if a_treeview.prev(x):
            index = a_treeview.index(x)
            a_treeview.move(x,"",index-1)
        
    
    def move_down(a_treeview):# 选中项，向下移
        x = a_treeview.focus()
        if a_treeview.next(x):
            index = a_treeview.index(x)
            a_treeview.move(x,"",index+1)
    
    def button_ok():
    
        print("button_ok")
        
        def get_content(a_treeview):
            
            temp_list = list( a_treeview.get_children() )
            
            temp_list.sort(key=lambda x:a_treeview.index(x),)
            
            return tuple( temp_list )
        
        
        
        print(get_content(no_1))
        print(get_content(no_2))
        print(get_content(no_2))
        
        global_variable.user_configure_data["gamelist_columns_to_show_1"] = get_content(no_1)
        global_variable.user_configure_data["gamelist_columns_to_show_2"] = get_content(no_2)
        global_variable.user_configure_data["gamelist_columns_to_show_3"] = get_content(no_3)
        
        # 标记为第三组，发信号后，切换到第一组
        global_variable.column_group_counter=3
        
        #global_variable.root_window.event_generate(r"<<GameListChangeColumnsToShow>>",)
        root.event_generate(r"<<GameListChangeColumnsToShow>>",)
        
        misc_funcs.save_user_configure()
        
        window.destroy()


    #window.rowconfigure(0,weight=1)
    window.columnconfigure(0,weight=1)
    window.columnconfigure(1,weight=1)
    window.columnconfigure(2,weight=1)
    window.columnconfigure(3,weight=1)
    
    frame0 = ttk.Frame(window,)
    frame1 = ttk.Frame(window,)
    frame2 = ttk.Frame(window,)
    frame3 = ttk.Frame(window,)
    
    
    the_text  =_("第1组，程序一开始显示的内容")
    the_text +="\n"
    the_text +=_("后面的第2组、第3组，主要是为了方便切换显示不同的内容")
    the_text +="\n"
    the_text +=_("不需要的话，可以不用去管 第2组、第3组")

    ttk.Label(window,text=the_text).grid(row=2,column=0,columnspan=4,sticky=tk.W+tk.N,)
    
    button_ok = ttk.Button(window,text=_("确认，确认后跳转到第1组"),command=button_ok)
    button_ok.grid(row=8,column=0,columnspan=4,sticky=(tk.E),)
    
    frame0.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    frame1.grid(row=0,column=1,sticky=tk.W+tk.N+tk.E+tk.S,)
    frame2.grid(row=0,column=2,sticky=tk.W+tk.N+tk.E+tk.S,)
    frame3.grid(row=0,column=3,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    for x in (frame0,frame1,frame2,frame3,):
        #x.rowconfigure(0,weight=1)
        x.columnconfigure(0,weight=1)
    
    h = len( global_variable.columns ) + 1
    if h < 5 : h = 5
    
    # frame0
    ttk.Label(frame0,text=_("内容")).grid(row=0,column=0,sticky=tk.W+tk.N,)
    
    no_0 = ttk.Treeview(frame0,height=h,show="tree",selectmode='browse' )
    no_0.grid(row=1,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    for x in ( ["#id",] + global_variable.columns ):
        if x in key_word_translation.columns_translation:
            no_0.insert("",'end',iid=x,text=key_word_translation.columns_translation[x])
        else:
            no_0.insert("",'end',iid=x,text=x)
    
    button_add_to_1=ttk.Button(frame0,text=_("添加到第1组"),width=-1,command=lambda x=None: add_to(no_1))
    button_add_to_2=ttk.Button(frame0,text=_("添加到第2组"),width=-1,command=lambda x=None: add_to(no_2))
    button_add_to_3=ttk.Button(frame0,text=_("添加到第3组"),width=-1,command=lambda x=None: add_to(no_3))
    
    button_add_to_1.grid()
    button_add_to_2.grid()
    button_add_to_3.grid()
    
    # frame1
    ttk.Label(frame1,text=_("第1组")).grid(row=0,column=0,sticky=tk.W+tk.N,)
    no_1 = ttk.Treeview(frame1,height=h, show="tree" ,selectmode='browse')
    no_1.grid(row=1,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)

    for x in global_variable.user_configure_data["gamelist_columns_to_show_1"]:
        if x in key_word_translation.columns_translation:
            no_1.insert("",'end',iid=x,text=key_word_translation.columns_translation[x])
        else:
            no_1.insert("",'end',iid=x,text=x)
    
    button_delete_from_1=ttk.Button( frame1 ,width=-1,text=_("从第1组移除"),command=lambda x=None:delete_from_a_treeview(no_1))
    button_delete_from_1.grid()
    
    button_move_up_1=ttk.Button( frame1 ,width=-1,text=_("上移"),command=lambda x=None:move_up(no_1))
    button_move_up_1.grid()
    
    button_move_down_1=ttk.Button( frame1 ,width=-1,text=_("下移"),command=lambda x=None:move_down(no_1))
    button_move_down_1.grid()

    # frame2
    ttk.Label(frame2,text=_("第2组")).grid(row=0,column=0,sticky=tk.W+tk.N,)
    no_2 = ttk.Treeview(frame2,height=h, show="tree" ,selectmode='browse')
    no_2.grid(row=1,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)

    for x in global_variable.user_configure_data["gamelist_columns_to_show_2"]:
        if x in key_word_translation.columns_translation:
            no_2.insert("",'end',iid=x,text=key_word_translation.columns_translation[x])
        else:
            no_2.insert("",'end',iid=x,text=x)

    button_delete_from_2=ttk.Button( frame2 ,text=_("从第2组移除"),command=lambda x=None:delete_from_a_treeview(no_2))
    button_delete_from_2.grid()
    
    button_move_up_2=ttk.Button( frame2 ,width=-1,text=_("上移"),command=lambda x=None:move_up(no_2))
    button_move_up_2.grid()
    
    button_move_down_2=ttk.Button( frame2 ,width=-1,text=_("下移"),command=lambda x=None:move_down(no_2))
    button_move_down_2.grid()

    # frame3
    ttk.Label(frame3,text=_("第3组")).grid(row=0,column=0,sticky=tk.W+tk.N,)
    no_3 = ttk.Treeview(frame3,height=h,show="tree" ,selectmode='browse' )
    no_3.grid(row=1,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)

    for x in global_variable.user_configure_data["gamelist_columns_to_show_3"]:
        if x in key_word_translation.columns_translation:
            no_3.insert("",'end',iid=x,text=key_word_translation.columns_translation[x])
        else:
            no_3.insert("",'end',iid=x,text=x)
            
    button_delete_from_3=ttk.Button( frame3 ,text=_("从第3组移除"),command=lambda x=None:delete_from_a_treeview(no_3))
    button_delete_from_3.grid()
    
    button_move_up_3=ttk.Button( frame3 ,width=-1,text=_("上移"),command=lambda x=None:move_up(no_3))
    button_move_up_3.grid()
    
    button_move_down_3=ttk.Button( frame3 ,width=-1,text=_("下移"),command=lambda x=None:move_down(no_3))
    button_move_down_3.grid()
    
    
    window.wait_window()
    ##########
    ##########


################
# 目录 瘦身
#   选择删减内容后，
#       1 目录里 删除 条目，（这个，如果有内容被删了，直接退出，简单点）
#       2 删除内容
#       
def window_for_choose_unwanted_internal_index():
    # global_static_key_word_translation.columns_translation {}
    # global_variable.columns []
    # global_variable.columns_index {}
    
    # 这个是 搜索 范围
    # global_variable.search_columns_set
    
    root = global_variable.root_window
    
    translation_dict = global_static_key_word_translation.index_translation
    
    
    window = tk.Toplevel()
    #window.geometry( "400x300" )
    window.resizable(width=True, height=True)
    window.title(_("内置目录瘦身"))
    window.lift(root)
    window.transient(root)
    ################
    ################
    checkbuttons={}
    checkbuttons_variable={}
    
    def for_ok_button():
        print("for ok button")
        
        delete_list = []
        for the_id in checkbuttons_variable:
            if checkbuttons_variable[the_id].get():
                delete_list.append( the_id )
        
        if delete_list:
            for the_id in delete_list:
                if the_id in global_variable.internal_index:
                    del global_variable.internal_index[the_id]
            
            # 保存
            save_pickle.save(global_variable.all_data , the_files.file_pickle_gamelist_data)
            
            # 退出简单点
            window.destroy()
            sys.exit()
        
        window.destroy()
    
    n=0
    ok_button = ttk.Button(window,text="OK",command=for_ok_button)
    ok_button.grid(row=n,sticky=tk.W)
    n+=1
    
    text = ""
    text += _("选择要删除的项目。")
    text += _("\n")
    text += _("\n")
    text += _("有些项目被删掉的话，列表的过滤功能可能会被影响到一些。")
    text += _("\n")
    text += _("\n")
    text += _("如果有项目被删除，程序修改数据、保存数据后，会关闭。")
    text += _("\n")
    text += _("\n")
    text += _("重新打开程序，查看效果即可。")
    
    ttk.Label(window,text=text).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    ttk.Separator(window,orient=tk.HORIZONTAL).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    not_delete = {"all_set", "clone_set", "parent_set", }
    for the_id in sorted( global_variable.internal_index.keys() ):
        if the_id not in not_delete:
            
            checkbuttons_variable[the_id] = tk.IntVar()
            
            checkbuttons_variable[the_id].set(0)
            
            if the_id in translation_dict:
                text = translation_dict[the_id]
            else:
                text = the_id
        
            checkbuttons[the_id] = ttk.Checkbutton(window, text=text,variable=checkbuttons_variable[the_id])
            checkbuttons[the_id].grid(row=n,sticky=tk.W)
            n+=1
    
    if not checkbuttons_variable:
        ttk.Label(window,text=_("已经没有项目可以删了")).grid(row=n,sticky=tk.W+tk.E)
        n+=1
    
    window.wait_window()
###
# 列表 瘦身 之 删列 （删行 ，不需要 在 窗口里选择）
#   选择删减内容后，
#       删除内容，
#       然后，如果有内容被删了，直接退出，简单点）
def window_for_choose_unwanted_game_list_column():
    print()
    print("window_for_choose_unwanted_game_list_column")
    # global_static_key_word_translation.columns_translation {}
    # global_variable.columns []
    # global_variable.columns_index {}
    
    # 这个是 搜索 范围
    # global_variable.search_columns_set
    
    root = global_variable.root_window
    
    # global_variable.columns
    # global_variable.all_data["columns"]
    # list 格式，这两应该是一样的
    
    columns      = global_variable.all_data["columns"]
    machine_dict = global_variable.all_data["machine_dict"]
    
    translation_dict = global_static_key_word_translation.columns_translation
    
    
    
    window = tk.Toplevel()
    #window.geometry( "400x300" )
    window.resizable(width=True, height=True)
    window.title(_("列表瘦身，删除不需要的列"))
    window.lift(root)
    window.transient(root)
    ################
    ################
    checkbuttons={}
    checkbuttons_variable={}
    
    def for_ok_button():
        print("for ok button")
        
        delete_list = []
        for the_id in checkbuttons_variable:
            if checkbuttons_variable[the_id].get():
                delete_list.append( the_id )
        
        if delete_list:
            
            new_columns    = []
            the_index_list = []
            for the_id in columns:
                if the_id not in delete_list:
                    new_columns.append(the_id)
                    the_index_list.append(columns.index(the_id))
            
            if new_columns:
                # machine_dict
                for item_id in machine_dict:
                    
                    item_info = machine_dict[item_id]
                    
                    new_info = []
                    for the_index in the_index_list:
                        new_info.append( item_info[the_index] )
                    
                    machine_dict[item_id] = new_info
                
                # columns
                # 需要指针功能，不能直接用等号
                columns.clear() 
                columns.extend(new_columns)
            else: # 全删
                for item_id in machine_dict:
                    machine_dict[item_id].clear()
                columns.clear() 
                
            # 保存
            save_pickle.save(global_variable.all_data , the_files.file_pickle_gamelist_data)
            
            # 退出简单点
            window.destroy()
            sys.exit()
                
        
        window.destroy()
    
    n=0
    ok_button = ttk.Button(window,text="OK",command=for_ok_button)
    ok_button.grid(row=n,sticky=tk.W)
    n+=1
    
    text = ""
    text += _("选择要删除的列。")
    text += _("\n")
    text += _("\n")
    text += _("有些列被删掉的话，搜索功能的整体搜索范围会被影响到。")
    text += _("\n")
    text += _("\n")
    text += _("MAME的模拟状态一列，SL的支持一列，影响到图标颜色。")
    text += _("\n")
    text += _("\n")
    text += _("全部都删除的话，没有意义。程序也会出错。")
    text += _("\n")
    text += _("\n")
    text += _("如果有项目被删除，程序修改数据、保存数据后，会关闭。")
    text += _("\n")
    text += _("\n")
    text += _("重新打开程序，查看效果即可。")
    
    ttk.Label(window,text=text).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    ttk.Separator(window,orient=tk.HORIZONTAL).grid(row=n,sticky=tk.W+tk.E)
    n+=1
    
    not_delete = set( ) # 不需要
    for the_id in sorted( columns ):
        if the_id not in not_delete:
            
            checkbuttons_variable[the_id] = tk.IntVar()
            
            checkbuttons_variable[the_id].set(0)
            
            if the_id in translation_dict:
                text = translation_dict[the_id]
            else:
                text = the_id
        
            checkbuttons[the_id] = ttk.Checkbutton(window, text=text,variable=checkbuttons_variable[the_id])
            checkbuttons[the_id].grid(row=n,sticky=tk.W)
            n+=1
    
    if not checkbuttons_variable:
        ttk.Label(window,text=_("已经没有项目可以删了")).grid(row=n,sticky=tk.W+tk.E)
        n+=1
    
    window.wait_window()
    


# 显示 出招表 文字 替换 内容
def window_for_extra_command_character():
    the_title = _("出招表文字替换对照表")
    command_dict = extra_command.replace_dict

    root = global_variable.root_window
    
    window = tk.Toplevel()
    #window.geometry( "400x300" )
    window.resizable(width=True, height=True)
    window.title(the_title)
    window.lift(root)
    window.transient(root)
    window.rowconfigure(0,weight=1)
    window.columnconfigure(0,weight=1)

    text_container = ui__text_with_scrollbar.Text_with_scrollbar(window,horizontal=True,sizegrip=True)
    text_container.grid(row=0,column=0,sticky=tk.NSEW)
    
    # font 与出招表字体相同
    text_container.new_ui_text.configure(font=global_variable.font_text_2)
    
    temp_string  = "出招表 command.dat 原始文件中的一些符号替换，替换为文字"+ "\n"
    temp_string += "替换之后，将出招表显示为完全的文字内容"+ "\n"
    temp_string += "\n"
    temp_string += "主要用的是 GB2312 、GBK 范围中的字符"+ "\n"
    temp_string += "简体中文的电脑用户，这样查看出招表，效果应该还可以"+ "\n"
    temp_string += "其它地区的电脑用户，可能不太方便"+ "\n"
    temp_string += "\n"
    temp_string += "因为是文字内容，显示效果和选择的字体，关系很大"+ "\n"
    temp_string += "jjsnake 的中文出招表，https://www.ppxclub.com/130735-1-1"+ "\n"
    temp_string += "字体可以调整为 楷体、宋体、仿宋 等，"+ "\n"
    temp_string += "显效的效果比较整齐"+ "\n"
    temp_string += "\n"
    temp_string += "\n"
    temp_string +="以下为 替换内容："+ "\n"
    temp_string +="（如果发现有问题，可以跟我说一下）"+ "\n"
    temp_string +="（在低版本 python 上，以下内容可能是乱序显示的）"+ "\n"
    temp_string +="（顺序我就不改了，如果是乱序的，可以复制到文本编辑器上排序一下再查看）"+ "\n"
    temp_string +="\n"
    
    text_container.new_func_insert_string(temp_string)

    for key,value in command_dict.items():
        temp = key.ljust(15,) + " " + value + "\n"
        text_container.new_func_insert_string(temp)

    window.wait_window()


def show_a_text_widget(line_list,title=None):
    if title is None:
        title = "-"

    root = global_variable.root_window
    
    window = tk.Toplevel()
    window.geometry( "400x300" )
    window.resizable(width=True, height=True)
    window.title(title)
    window.lift(root)
    window.transient(root)
    window.rowconfigure(0,weight=1)
    window.columnconfigure(0,weight=1)

    text_container = ui__text_with_scrollbar.Text_with_scrollbar(window,horizontal=True,sizegrip=True)
    text_container.grid(row=0,column=0,sticky=tk.NSEW)
    
    for line in line_list:
        text_container.new_func_insert_string(line)

    window.wait_window()


if __name__ =="__main__":
        
    root = tk.Tk()



    root.mainloop()
    
    ""

