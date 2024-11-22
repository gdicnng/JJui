# -*- coding: utf-8 -*-
"""
    Text_container ：
    
        --------------------------
        |  种类选择器  | 使用目录 |
        |-------------------------|
        |    子目分类             |
        |------------------------|
        |                        |
        |    内容                |
        |                        |
        |    ( Text_area )       |
        |                        |
        |                        |
        |                        |
        |                        |
        --------------------------
    
"""
import sys
import os
#import time

import tkinter as tk
import tkinter.ttk as ttk

#from PIL import Image, ImageTk

#from . import global_static_filepath as the_files
from . import global_static
from . import global_static_key_word_translation 
from . import global_variable
from . import global_static_filepath as the_files

from . import extra_read_history_xml
from . import extra_mameinfo_dat
from . import extra_history_dat
from . import extra_gameinit_dat
from . import extra_command
from . import extra_command_english

from . import read_pickle


text_types          = global_static.extra_text_types
text_types_2        = global_static.extra_text_types_2
    # ("snap","titles","flyers",......)
key_word_translation   = global_static_key_word_translation.extra_text_types_translation
key_word_translation_2 = global_static_key_word_translation.extra_text_types_2_translation


# 变量前缀
# self.new_ui_
# self.new_var_
# self.new_func_

# 鼠标右击 ，mac 似乎不一样
if sys.platform.startswith('darwin'): # macos
    event_mouse_right_click   = r'<Button-2>'
    event_mouse_right_release = r'<ButtonRelease-2>'
else:
    event_mouse_right_click   = r'<Button-3>'
    event_mouse_right_release = r'<ButtonRelease-3>'


class Text_area(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_ui()
        self.new_func_ui_popup_menu()
        self.new_func_bindings()
        
        
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        self.new_ui_text = tk.Text(
                    parent,
                    borderwidth        = 0,
                    highlightthickness = 0,
                    takefocus = False,
                    undo      = False,
                    maxundo   = 1,
                    state     = tk.DISABLED,
                    wrap      = "char",
                    )
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_text.yview)
        
        self.new_ui_text.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        
        self.new_ui_text.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        self.new_ui_scrollbar_v.grid(row=0,column=1,sticky=tk.N+tk.S,)
        
        parent.rowconfigure(1, weight=0)
        
        #
        
        self.new_ui_scrollbar_h = ttk.Scrollbar( parent, orient=tk.HORIZONTAL , command=self.new_ui_text.xview)
            
        self.new_ui_text.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
            
        #self.new_ui_scrollbar_h.grid(row=1,column=0,columnspan=2,sticky=(tk.W,tk.E))
        
        ""
    
    def new_func_ui_popup_menu(self,):
        # 右键菜单
        self.new_ui_index_popup_menu = tk.Menu(self.new_ui_text, tearoff=0)
        
        self.new_ui_index_popup_menu.add_command(label=_("不换行"),
                command = self.new_func_wrap_by_none
                )
        
        self.new_ui_index_popup_menu.add_command(label=_("以词换行"),
                command = self.new_func_wrap_by_word
                )
        
        self.new_ui_index_popup_menu.add_command(label=_("以字符换行"),
                command = self.new_func_wrap_by_char
                )
        
        #self.new_ui_index_popup_menu.add_command(label=_("显示横向进度条"),
        #        command = self.new_func_show_scrollbar_h
        #        )
        #
        #self.new_ui_index_popup_menu.add_command(label=_("关闭横向进度条"),
        #        command = self.new_func_close_scrollbar_h
        #        )
        
        ""
    
    def new_func_bindings(self,):
        ""
        # 右键菜单
        if sys.platform.startswith('linux'):
            self.new_ui_text.bind(event_mouse_right_release,self.new_func_bindings_right_click_to_show_menu)
        else:
            self.new_ui_text.bind(event_mouse_right_click,self.new_func_bindings_right_click_to_show_menu)

    
    def new_func_bindings_right_click_to_show_menu(self,event):
        if sys.platform.startswith('linux'):
            # 鼠标 右击 释放时
            # 如果不在 范围内
            if event.widget is not event.widget.winfo_containing(event.x_root, event.y_root,):
                return
        
        self.new_ui_index_popup_menu.tk_popup(event.x_root, event.y_root)


    def new_func_insert_string(self,a_string='',tags=None):
        self.new_ui_text.configure(state="normal")
        
        if tags is None:
            self.new_ui_text.insert(tk.END,a_string)
        else:
            self.new_ui_text.insert(tk.END,a_string,tags=tags)
        
        self.new_ui_text.configure(state="disabled")

    def new_func_wrap_by_none(self,):
        self.new_ui_text.configure(wrap="none")
        
        self.new_func_show_scrollbar_h()
    
    def new_func_wrap_by_char(self,):
        self.new_ui_text.configure(wrap="char")
        
        self.new_func_close_scrollbar_h()
    
    def new_func_wrap_by_word(self,):
        self.new_ui_text.configure(wrap="word")
        
        self.new_func_close_scrollbar_h()
    
    def new_func_show_scrollbar_h(self,):
        if not self.new_ui_scrollbar_h.winfo_ismapped():
            self.new_ui_scrollbar_h.grid(row=1,column=0,columnspan=2,sticky=tk.W+tk.E,)
    
    def new_func_close_scrollbar_h(self,):
        if self.new_ui_scrollbar_h.winfo_ismapped():
            self.new_ui_scrollbar_h.grid_forget()




class Text_container(ttk.Frame):
    
    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "extra_text_1"
        
        self.new_var_virtual_event_name_CurrentGame=r'<<CurrentGame>>'
            # 不在这里用这个了
        
        self.new_var_remember_text_type = None
        
        self.new_func_ui()
        self.new_func_bindings()
        self.new_func_initialize()
        
    def new_func_ui(self,):
        parent = self
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=0)
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        # 第一行 选择栏
        self.new_var_string_for_text_chooser = tk.StringVar()
        self.new_ui_text_chooser = ttk.Combobox( parent ,takefocus=False,textvariable=self.new_var_string_for_text_chooser,state="readonly")
        self.new_ui_text_chooser.grid(row=0 , column=0 , sticky=tk.W+tk.N+tk.E,)
        #self.new_ui_text_chooser.grid(row=0 , column=0 ,columnspan=2, sticky=(tk.W,tk.N,tk.E,),)
        
        # 第一行 标记 ：创建目录 
        self.new_var_index_flag = tk.IntVar()
        self.new_ui_index_checkbutton = ttk.Checkbutton( parent ,
                takefocus=False,
                text=_("用目录"),
                variable=self.new_var_index_flag,
                )
        self.new_ui_index_checkbutton.grid(row=0 , column=1 , sticky=tk.N+tk.E, )
        
        
        # 第二行 选择栏 2
        self.new_var_string_for_chooser_2 = tk.StringVar()
        self.new_ui_chooser_2 = ttk.Combobox( parent ,takefocus=False,textvariable=self.new_var_string_for_chooser_2,state="readonly")
        self.new_ui_chooser_2.grid(row=1 , column=0 , columnspan=2,sticky=tk.W+tk.N+tk.E,)
        
        
        # 第三行 文本显示区
        self.new_ui_text_area = Text_area(parent)
        self.new_ui_text_area.grid(row=2 , column=0 ,columnspan=2, sticky=tk.W+tk.N+tk.E+tk.S,)
    
    #### ??
    def new_func_bindings(self,):
        self.new_ui_text_chooser.bind(r"<<ComboboxSelected>>",self.new_func_for_virtual_event_of_combobox)
        
        #self.bind_all(self.new_var_virtual_event_name_CurrentGame,self.new_func_bindings_receive_virtual_event,"+")
            # 不在这里用这个
        ""
    
    def new_func_for_virtual_event_of_combobox(self,event):
        print()
        print("<<ComboboxSelected>>")
        
        item_id = global_variable.current_item
        
        self.new_func_show( item_id )
        
    
    def new_func_initialize(self,):
        
        self.new_ui_chooser_2.grid_forget()
        
        # 记录
        global_variable.Combobox_chooser_text_1 = self.new_ui_text_chooser
        
        global_variable.tkint_flag_for_text_index_1 = self.new_var_index_flag
        self.new_var_index_flag.set( global_variable.user_configure_data["extra_text_use_index_1"] )
        
        # 记录 
        global_variable.tk_text_1 = self.new_ui_text_area.new_ui_text
        
        # text tag bind
        self.new_ui_text_area.new_ui_text.tag_bind(
                "mameinfo_find_sourcefile", 
                "<ButtonPress-1>",
                self.new_func_tag_binding_mameinfo_dat_find_source_use_index,
                )
        self.new_ui_text_area.new_ui_text.tag_config(
                "mameinfo_find_sourcefile", 
                underline=True,
                )
        
        
        
        temp=[]
        for x in text_types:
            if x in key_word_translation:
                temp.append(key_word_translation[x])
            else:
                temp.append(x)
        self.new_ui_text_chooser["values"]= temp
        
        try: # 读取配置文件中 记录的 index
            n = global_variable.user_configure_data["extra_text_chooser_index"] 
            if n < len(text_types):
                pass
            else:
                n=0
            self.new_ui_text_chooser.set( temp[n] )
        except:
            self.new_ui_text_chooser.set( temp[0] )
        
        self.new_func_get_info_from_choice()# 初始数据读取
    
    def new_func_insert_string(self,a_string = "",tags=None):
        self.new_ui_text_area.new_ui_text.configure(state="normal")
        
        self.new_ui_text_area.new_ui_text.insert(tk.END,a_string,tags)
        
        self.new_ui_text_area.new_ui_text.configure(state="disabled")
    
    def new_func_insert_list_of_string(self,list_of_string = None,tags=None):
        if list_of_string is None: 
            list_of_string = []
        
        self.new_ui_text_area.new_ui_text.configure(state="normal")
        
        for a_string in list_of_string:
            self.new_ui_text_area.new_ui_text.insert(tk.END,a_string,tags)
        
        self.new_ui_text_area.new_ui_text.configure(state="disabled")
        
    
    def new_func_clear_chooer(self,):
        self.new_ui_chooser_2["values"]=("",)
        self.new_ui_chooser_2.set("") 
    
    def new_func_clear_content(self,):
        self.new_ui_text_area.new_ui_text.configure(state="normal")
        
        # 再 清理文本
        self.new_ui_text_area.new_ui_text.delete('1.0',tk.END)
        
        self.new_ui_text_area.new_ui_text.configure(state="disabled")

    # ??
    def new_func_get_info_from_choice(self,):

        number_index = self.new_ui_text_chooser.current()
        
        
        text_type = text_types[number_index]
        
        #
        self.new_var_remember_text_type = text_type
    

    # 用这个
    def new_func_show(self,item_id,clear_text=True):
        
        self.new_ui_chooser_2["values"] = ()
        
        if item_id != global_variable.current_item : return 
        
        if item_id is None:
            print("None ,return")
            return
        
        # 清理选择框
        self.new_func_clear_chooer()
        
        # 清理文本区
        if clear_text:
            self.new_func_clear_content()
        
        if self.new_ui_text_area.winfo_viewable():
            #if self.new_var_index_flag.get():
            
            # 是否创建目录 加速
            
            n = self.new_ui_text_chooser.current()
            temp = text_types[n]
            
            
            if global_variable.gamelist_type == "softwarelist":
                if temp == "history.xml":
                    self.new_func_show_history_xml(item_id)
                elif temp in ("history.dat","sysinfo.dat",):
                    self.new_func_show_history_dat(temp,item_id)
                else:
                    print("not for softwarelist")
                    return
            else:
                if temp == "history.xml":
                    self.new_func_show_history_xml(item_id)
                elif temp in ("mameinfo.dat","messinfo.dat",):
                    self.new_func_show_mameinfo_dat(temp,item_id)
                elif temp in ("history.dat","sysinfo.dat",):
                    self.new_func_show_history_dat(temp,item_id)
                elif temp in ("gameinit.dat",):
                    #show_gameinit_dat(self,type,game_name)
                    self.new_func_show_gameinit_dat(temp, item_id)
    
    ##########################
    
    # history.xml 
    #   no index
    def new_func_show_history_xml_not_use_index(self,game_name):

        path = global_variable.user_configure_data["history.xml_path"]
        path = path.replace(r'"',"") # 去掉双引号
        
        if not os.path.isfile(path) : return
        
        if game_name != global_variable.current_item : return
        
        new_text = ''
        
        def get_content(path,game_name):
            if global_variable.gamelist_type == "softwarelist":
                text = extra_read_history_xml.getinfo(path,game_name,the_type = "softwarelist")
            else:
                text = extra_read_history_xml.getinfo(path,game_name)
            return text
            
        new_text = get_content(path,game_name)
        
        if not new_text : return 
        
        if game_name == global_variable.current_item :
                self.new_func_insert_string(new_text)
    
    # history.xml 
    #   index
    def new_func_show_history_xml_use_index(self,game_name):
        path = global_variable.user_configure_data["history.xml_path"]
        path = path.replace(r'"',"") # 去掉双引号
    
        if not os.path.isfile(path) : 
            print("file is missing,return")
            return    
    
        # 如果还没有读取目录，读取目录
        if not global_variable.extra_index_for_histroty_xml:
            if os.path.isfile(the_files.file_pickle_extra_index_history_xml):
                try:
                    global_variable.extra_index_for_histroty_xml = read_pickle.read(the_files.file_pickle_extra_index_history_xml)
                except:
                    global_variable.extra_index_for_histroty_xml = {}
        
        if global_variable.extra_index_for_histroty_xml:
            index_dict = global_variable.extra_index_for_histroty_xml
            
            #####################
            # 添加主版本
            parent_flag = False
            if game_name in index_dict: 
                the_index = index_dict[game_name]
            else:
                if game_name in global_variable.dict_data["clone_to_parent"]:
                    parent_name = global_variable.dict_data["clone_to_parent"][game_name]
                    if parent_name not in index_dict:
                        print("item id ,not in index,")
                        print("parent id ,not in index,too ,return")
                        return
                    else:
                        self.new_func_insert_string(_("主版本为：")+parent_name + "\n"+ "\n")
                        parent_index = index_dict[parent_name]
                        parent_flag = True
                else:
                    print("item id not in index,return")
                    return
                        
            
            
            if parent_flag:
                print("id:{}".format(parent_name))
                print("index:{}".format(parent_index))
            else:
                print("id:{}".format(game_name))
                print("index:{}".format(the_index))
            
            
            if game_name != global_variable.current_item : return
        
            new_text = ''
        
            def get_content(path,game_name,the_index):
                if global_variable.gamelist_type == "softwarelist":
                    text = extra_read_history_xml.getinfo_by_index(path,game_name,the_index=the_index,the_type = "softwarelist")
                else:
                    text = extra_read_history_xml.getinfo_by_index(path,game_name,the_index=the_index)
                return text
            
            if parent_flag:
                new_text = get_content(path,parent_name,parent_index)
            else:
                new_text = get_content(path,game_name,the_index)
            
            if not new_text : return 
            
            if game_name == global_variable.current_item :
                    self.new_func_insert_string(new_text)
    
    # history.xml
    def new_func_show_history_xml(self,game_name):
        
        if self.new_var_index_flag.get():
            self.new_func_show_history_xml_use_index(game_name)
        else:
            self.new_func_show_history_xml_not_use_index(game_name)
    
    ###############################
    
    # ("history.dat","sysinfo.dat",)
    #   no index
    def new_func_show_history_dat_not_use_index(self,data_type,game_name):

        data_type =  data_type + "_path" # "history.dat_path"
        
        path = global_variable.user_configure_data[ data_type ]
        path = path.replace(r'"',"") # 去掉双引号 
        
        if os.path.isfile(path):
        
            new_text = []
        
            if game_name == global_variable.current_item:
                text = None
                text = extra_history_dat.get_content_by_file_name(path,game_name,global_variable.gamelist_type)
                if text is not None:
                    new_text = text
        
            # if new_text == '':
            #     if game_name == self.tree.focus():
            #         # 再找主版本
            #         print("try parent")
            #         if game_name in self.data['dict_data']['clone_to_parent']:
            #             parent_name = self.data['dict_data']['clone_to_parent'][game_name]
            #             text = extra_history_dat.get_content_by_file_name(path,parent_name)
            #             if text is not None:
            #                 new_text = text

            if game_name == global_variable.current_item:
                #for x in new_text:
                #    self.new_func_insert_string(x)
                self.new_func_insert_list_of_string(new_text)

    # ("history.dat","sysinfo.dat",)
    #   index
    def new_func_show_history_dat_use_index(self,data_type,game_name):
        
        #data_type =  data_type + "_path" # "history.dat_path"
        
        path = global_variable.user_configure_data[ data_type + "_path" ]
        path = path.replace(r'"',"") # 去掉双引号 
        
        if not os.path.isfile(path) : 
            print("file is missing,return")
            return    
        # 如果还没有读取目录，读取目录
        if data_type == "history.dat":
            print("history.dat")
            if not global_variable.extra_index_for_histroty_dat:
                if os.path.isfile(the_files.file_pickle_extra_index_history_dat):
                    try:
                        global_variable.extra_index_for_histroty_dat = read_pickle.read(the_files.file_pickle_extra_index_history_dat)
                    except:
                        global_variable.extra_index_for_histroty_dat = {}
            
            index_dict = global_variable.extra_index_for_histroty_dat
        
        elif data_type == "sysinfo.dat":
            #print("sysinfo.dat")
            if not global_variable.extra_index_for_sysinfo_dat:
                if os.path.isfile(the_files.file_pickle_extra_index_sysinfo_dat):
                    try:
                        global_variable.extra_index_for_sysinfo_dat = read_pickle.read(the_files.file_pickle_extra_index_sysinfo_dat)
                    except:
                        global_variable.extra_index_for_sysinfo_dat = {}
            
            index_dict = global_variable.extra_index_for_sysinfo_dat
        

        if not index_dict : 

            print("no index,return")
            return
        

        
        #####################
        # 添加主版本
        parent_flag = False
        if game_name in index_dict: 
            the_index = index_dict[game_name]
        else:
            if game_name in global_variable.dict_data["clone_to_parent"]:
                parent_name = global_variable.dict_data["clone_to_parent"][game_name]
                if parent_name not in index_dict:
                    print("item id ,not in index,")
                    print("parent id ,not in index,too ,return")
                    return
                else:
                    self.new_func_insert_string(_("主版本为：")+parent_name + "\n"+ "\n")
                    parent_index = index_dict[parent_name]
                    parent_flag = True
                    
                
            else:
                print("item id not in index,return")
                return
            
        
        new_text = []
        
        if game_name == global_variable.current_item:
            
            text = None
            
            if parent_flag:
                text = extra_history_dat.get_content_by_file_name_by_index(
                        path,parent_name,the_index=parent_index,the_type=global_variable.gamelist_type)
            else:
                text = extra_history_dat.get_content_by_file_name_by_index(
                        path,game_name,the_index=the_index,the_type=global_variable.gamelist_type)


            

        
            if text is not None:
                new_text = text
        
        #if game_name == global_variable.current_item:
            #for x in new_text:
            #    self.new_func_insert_string(x)
            self.new_func_insert_list_of_string(new_text)

    # ("history.dat","sysinfo.dat",)
    def new_func_show_history_dat(self,data_type,game_name):
        if self.new_var_index_flag.get():
            self.new_func_show_history_dat_use_index(data_type,game_name)
        else:
            self.new_func_show_history_dat_not_use_index(data_type,game_name)

    ################################
    
    # ("mameinfo.dat","messinfo.dat",)
    def new_func_show_mameinfo_dat_not_use_index(self,data_type,game_name,flag_is_game=True,the_source=None):
        # flag_is_game
            # 是游戏名
            # 是驱动名

        #data_type =   data_type + "_path"
        # path = self.ini_data[ "mameinfo.dat_path" ]
        # path = self.ini_data[ "messinfo.dat_path" ]
        path = global_variable.user_configure_data[ data_type + "_path" ]
        
        path = path.replace(r'"',"") # 去掉双引号 
        
        print(path)
        
        if not os.path.isfile(path): 
            print("file missing ,return")
            return
        
        new_text = [] # 记录该游戏的文档,读取内容后，是 []  ，
        
        if flag_is_game:
            if game_name != global_variable.current_item: 
                return
        
        if flag_is_game:
            text = extra_mameinfo_dat.get_content_by_file_name(path,game_name)
        else:
            text = extra_mameinfo_dat.get_content_by_file_name(path,the_source)
        
        
        if flag_is_game:
            if game_name != global_variable.current_item: 
                return
        
        if text is not None:
            new_text = text
        
        #for x in new_text:
        #    self.new_func_insert_string(x)
        self.new_func_insert_list_of_string(new_text)
        
        
        if flag_is_game:
            try:
                game_info = global_variable.machine_dict[game_name]
                sourcefile = game_info[ global_variable.columns_index["sourcefile"] ]
            except:
                sourcefile = None
                
            if sourcefile is None:
                return
                
            the_tk_text = self.new_ui_text_area.new_ui_text
                    
            def for_button():
                #print(sourcefile)
                
                # 清理
                the_tk_text.configure(state="normal")
                the_tk_text.delete('1.0',tk.END)
                the_tk_text.configure(state="disabled")
                
                #data_type,game_name,flag_is_game=True,the_source=None):
                self.new_func_show_mameinfo_dat_not_use_index(data_type,game_name,flag_is_game=False,the_source=sourcefile)
            
            def make_a_button():
                b = ttk.Button(the_tk_text,text=sourcefile,command=for_button)
                return b
            
            
            the_tk_text.configure(state="normal")
            
            the_tk_text.insert(tk.END,"\n")
            
            the_tk_text.window_create(
                    tk.END,
                    create=make_a_button,
                    )
            
            the_tk_text.configure(state="disabled")
    
    # ("mameinfo.dat","messinfo.dat",)
    def new_func_show_mameinfo_dat_use_index(self,data_type,game_name,flag_is_game=True,the_source=None):
        # flag_is_game
            # 是游戏名
            # 是驱动名
        
        #data_type =  data_type + "_path" # "history.dat_path"
        
        path = global_variable.user_configure_data[ data_type + "_path" ]
        path = path.replace(r'"',"") # 去掉双引号 
        
        if not os.path.isfile(path) : 
            print("file is missing,return")
            return
    
        print("",)
        print("use index",)
        print(data_type)
        print(game_name)
        
        
        # 如果还没有读取目录，读取目录
        if data_type == "mameinfo.dat":
            print("mameinfo.dat")
            if not global_variable.extra_index_for_mameinfo_dat:
                if os.path.isfile(the_files.file_pickle_extra_index_mameinfo_dat):
                    try:
                        global_variable.extra_index_for_mameinfo_dat = read_pickle.read(the_files.file_pickle_extra_index_mameinfo_dat)
                    except:
                        global_variable.extra_index_for_mameinfo_dat = {}
            
            index_dict = global_variable.extra_index_for_mameinfo_dat
        
        elif data_type == "messinfo.dat":
            #print("messinfo.dat")
            if not global_variable.extra_index_for_messinfo_dat:
                if os.path.isfile(the_files.file_pickle_extra_index_messinfo_dat):
                    try:
                        global_variable.extra_index_for_messinfo_dat = read_pickle.read(the_files.file_pickle_extra_index_messinfo_dat)
                    except:
                        global_variable.extra_index_for_messinfo_dat = {}
            
            index_dict = global_variable.extra_index_for_messinfo_dat
        
        else:return
        
        if not index_dict : 
            print("no index,return")
            return
        
        ########################
        # 添加驱动
        ########################
        # 如果是 game_name ，增加一个 按扭跳转到 驱动
        # 如果是 驱动名 ，下面就不需要了
        if flag_is_game :
            if game_name in global_variable.machine_dict:
                try:
                    game_info = global_variable.machine_dict[game_name]
                    sourcefile = game_info[ global_variable.columns_index["sourcefile"] ]
                except:
                    sourcefile = None
                
                if sourcefile:
                    
                    # 新的驱动 文件夹/sourcefile
                    #   取 sourcefile 的值
                    # 这样原来的也仍然有效
                    if sourcefile not in index_dict:
                        if "/" in sourcefile:
                            temp_string=sourcefile.split("/")[-1]
                            if temp_string:
                                sourcefile = temp_string
                    
                    # 之前的代码
                    if sourcefile in index_dict:
                        #the_index = index_dict[sourcefile]
                        
                        the_tk_text = self.new_ui_text_area.new_ui_text
                        
                        the_tk_text.configure(state="normal")
                        the_tk_text.insert(tk.END,"\n")
                        the_tk_text.insert(tk.END,sourcefile,("mameinfo_find_sourcefile",))
                        the_tk_text.insert(tk.END,"\n")
                        the_tk_text.insert(tk.END,"\n")
                        the_tk_text.configure(state="disabled")
        
        ###############################
        # 添加主版本
        ###############################
        
        parent_flag = False
        
        if flag_is_game:
            if game_name in index_dict: 
                the_index = index_dict[game_name]
            else:
                print("item id not in index")
                
                if game_name not in global_variable.dict_data["clone_to_parent"]:
                    print("no parent,return")
                    return
                else:
                    parent_name = global_variable.dict_data["clone_to_parent"][game_name]
                    
                    if parent_name not in index_dict:
                        print("parent id ,not in index,too ,return")
                        return
                    else:
                        self.new_func_insert_string(_("主版本为：")+parent_name + "\n" + "\n")
                        parent_index = index_dict[parent_name]
                        parent_flag = True
        
        else:
            if the_source in index_dict: 
                the_index = index_dict[the_source]
            else:
                print("source id not in index,return")
                return
            
            
        
        
        new_text = []
        
        if flag_is_game:
            if game_name != global_variable.current_item:
                return
            
            if parent_flag:
                text = extra_mameinfo_dat.get_content_by_file_name_by_index(path,parent_name,the_index=parent_index)
            else:
                text = extra_mameinfo_dat.get_content_by_file_name_by_index(path,game_name,the_index=the_index)
        else:
            
            text = extra_mameinfo_dat.get_content_by_file_name_by_index(path,the_source,the_index=the_index)
            

        
        if text is not None:
            new_text = text
        

        #for x in new_text:
        #    self.new_func_insert_string(x)
        self.new_func_insert_list_of_string(new_text)
    
    # mameinfo find source
    def new_func_tag_binding_mameinfo_dat_find_source_use_index(self,event):
        print()
        print("mameinfo.dat find source use index")
        
        n = self.new_ui_text_chooser.current()
        data_type = text_types[n]
        print(data_type)
        
        index_start = self.new_ui_text_area.new_ui_text.index("current linestart")
        index_end   = self.new_ui_text_area.new_ui_text.index("current lineend")
        
        #print(index_start)
        #print(index_end)
        
        # tag.first tag.last
        #index_start = self.new_ui_text_area.new_ui_text.index("command_find_parent.first")
        #index_end   = self.new_ui_text_area.new_ui_text.index("command_find_parent.last")
            # 如果有多个 相同的 tag ，找到的第一个 和 最后一个，
        
        # 算了，让 tag 内容，占一整行吧，这样好处理点
        
        source_name = self.new_ui_text_area.new_ui_text.get(index_start,index_end)
        print(source_name)
        source_name = source_name.rstrip("\r\n") # 不知道它，会不会包含 换行符号
        
        print(source_name)
        
        # 获得文本数据后，再清理
        
        # 清理文本区
        self.new_func_clear_content()
        
        # 清理选择框
        self.new_func_clear_chooer()
        
        game_name = None # 弄个假的
        self.new_func_show_mameinfo_dat_use_index(data_type,game_name,flag_is_game=False,the_source=source_name)
    
    # ("mameinfo.dat","messinfo.dat",)
    def new_func_show_mameinfo_dat(self,data_type,game_name):
        if self.new_var_index_flag.get():
            self.new_func_show_mameinfo_dat_use_index(data_type,game_name)
        else:
            self.new_func_show_mameinfo_dat_not_use_index(data_type,game_name)

    ##############################
    
    # ("gameinit.dat",)
    def new_func_show_gameinit_dat_not_use_index(self,data_type,game_name):
        
        data_type =  data_type + "_path" # "gameinit.dat_path"
        
        path = global_variable.user_configure_data[ data_type ]
        path = path.replace(r'"',"") # 去掉双引号 
        
        if os.path.isfile(path):
        
            new_text = []
        
            if game_name == global_variable.current_item:
                text = extra_gameinit_dat.get_content_by_file_name(path,game_name)
                if text is not None:
                    new_text = text
                    
            # 主版本 ？，算了，不管
            
            if game_name == global_variable.current_item:
                #for x in new_text:
                #    self.new_func_insert_string(x)
                self.new_func_insert_list_of_string(new_text)

    # ("gameinit.dat",)
    def new_func_show_gameinit_dat_use_index(self,data_type,game_name):
        # 如果还没有读取目录，读取目录
        # gameinit.dat

        print("gameinit.dat")
        if not global_variable.extra_index_for_gameinit_dat:
            if os.path.isfile(the_files.file_pickle_extra_index_gameinit_dat):
                try:
                    global_variable.extra_index_for_gameinit_dat = read_pickle.read(the_files.file_pickle_extra_index_gameinit_dat)
                except:
                    global_variable.extra_index_for_gameinit_dat = {}
        
        index_dict = global_variable.extra_index_for_gameinit_dat
        
        if not index_dict : 
            print("no index,return")
            return
        
        data_type =  data_type + "_path" # "history.dat_path"
        
        path = global_variable.user_configure_data[ data_type ]
        path = path.replace(r'"',"") # 去掉双引号 
        
        if not os.path.isfile(path) : 
            print("file is missing,return")
            return
        
        if game_name not in index_dict: 
            print("item id not in index,return")
            return
        
        the_index = index_dict[game_name]
        
        new_text = []
        
        if game_name == global_variable.current_item:
            
            text = extra_gameinit_dat.get_content_by_file_name_use_index(path,game_name,the_index=the_index)
        
            if text is not None:
                new_text = text
        
        #if game_name == global_variable.current_item:
            #for x in new_text:
            #    self.new_func_insert_string(x)
            self.new_func_insert_list_of_string(new_text)

    # ("gameinit.dat",)
    def new_func_show_gameinit_dat(self,data_type,game_name):
        if self.new_var_index_flag.get():
            self.new_func_show_gameinit_dat_use_index(data_type,game_name)
        else:
            self.new_func_show_gameinit_dat_not_use_index(data_type,game_name)




class Text_container_2(Text_container):
    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "extra_text_2"
    
    
    def new_func_initialize(self,):
        
        # 记录
        global_variable.Combobox_chooser_text_2 = self.new_ui_text_chooser
        
        global_variable.tkint_flag_for_text_index_2 = self.new_var_index_flag
        self.new_var_index_flag.set( global_variable.user_configure_data["extra_text_use_index_2"] )
        
        # 记录 
        global_variable.tk_text_2 = self.new_ui_text_area.new_ui_text
        
        # 没用上了
        ## text tag bind
        #self.new_ui_text_area.new_ui_text.tag_bind(
        #        "command_find_parent", 
        #        "<ButtonPress-1>",
        #        self.new_func_tag_binding_command_dat_find_parent_use_index,
        #        )
        #self.new_ui_text_area.new_ui_text.tag_config(
        #        "command_find_parent", 
        #        underline=True
        #        )
        
        #print()
        #print(text_types_2)
        #print(key_word_translation_2)
        temp=[]
        for x in text_types_2:
            if x in key_word_translation_2:
                temp.append(key_word_translation_2[x])
            else:
                temp.append(x)
        self.new_ui_text_chooser["values"]= temp
        #print(temp)
        
        try: # 读取配置文件中 记录的 index
            n = global_variable.user_configure_data["extra_command_type_chooser_index"] 
            if n < len(text_types_2):
                pass
            else:
                n=0
            self.new_ui_text_chooser.set( temp[n] )
        except:
            self.new_ui_text_chooser.set( temp[0] )
        
        self.new_func_get_info_from_choice()# 初始数据读取
    
    def new_func_bindings(self,):
        super().new_func_bindings()
        self.new_ui_chooser_2.bind("<<ComboboxSelected>>",self.new_func_binding_command_index_choose) 
    
    # 用这个
    def new_func_show(self,item_id):
        
        print("text 2")
        
        if item_id != global_variable.current_item : return 
        
        if item_id is None:
            print("None ,return")
            return
        
        # 清理选择框
        self.new_func_clear_chooer()
        
        # 清理文本区
        self.new_func_clear_content()
        
        if self.new_ui_text_area.winfo_viewable():
            #if self.new_var_index_flag.get():
            
            # 是否创建目录 加速
            
            n = self.new_ui_text_chooser.current()
            temp = text_types_2[n]
            
            self.new_func_show_command_dat(temp,item_id)
    
    def new_func_show_command_dat_not_use_index(self,data_type,game_name):
    
        print("show command")
        
        
        path = data_type + "_path" # "command.dat_path"
        path = global_variable.user_configure_data[path]
        path = path.replace(r'"',"") # 去掉双引号 
        
        print(path)
        
        if not os.path.isfile(path):
            #self.new_ui_chooser_2["values"]=("",)
            #self.new_ui_chooser_2.set("")
            return 0 
            # 如果，文档，不存在，直接退出函数
        
        # 初始化
        try:
            self.new_var_command_content
        except:
            self.new_var_command_content =  None 

        # 读取内容
        
        # 中文版，英文版 ，格式不同
        

        if data_type == "command.dat":
            self.new_var_command_content = extra_command.get_content_by_file_name( path,game_name )
        elif data_type == "command_english.dat":
            self.new_var_command_content = extra_command_english.get_content_by_file_name( path,game_name )

        
        
        if self.new_var_command_content is None:
            self.new_ui_chooser_2["values"]=("",)
            self.new_ui_chooser_2.set("") 
        elif len(self.new_var_command_content) <= 1:
            #print(r"<=1")
            self.new_ui_chooser_2["values"]=(_("全部"),)
            self.new_ui_chooser_2.set( _("全部") ) 
            for x in self.new_var_command_content:
                #for y in self.new_var_command_content[x]:
                #    self.new_func_insert_string( y)
                self.new_func_insert_list_of_string(  self.new_var_command_content[x]  )
        else:
            #print(r">1")
            index = []
            index.append( _("全部") )
            for x in self.new_var_command_content:
                # 提取 每一段 第一行，做为小标题
                try:
                    index.append( self.new_var_command_content[x][0].rstrip('\r\n') )
                except:
                    index.append("")
            self.new_ui_chooser_2["values"]=index
            self.new_ui_chooser_2.set( _("全部") ) 
            
            for x in self.new_var_command_content:
                #for y in self.new_var_command_content[x]:
                #    self.new_func_insert_string( y)
                self.new_func_insert_list_of_string(  self.new_var_command_content[x]  )
    
    #"command.dat",
    #"command_english.dat",
    def new_func_show_command_dat_use_index(self,data_type,game_name,):
        
        #data_type =  data_type + "_path" # "history.dat_path"
        path = global_variable.user_configure_data[ data_type + "_path" ]
        path = path.replace(r'"',"") # 去掉双引号 
        
        if not os.path.isfile(path) : 
            print("file is missing,return")
            return
        
        # 如果还没有读取目录，读取目录
        if data_type == "command.dat":
            print("command.dat")
            if not global_variable.extra_index_for_command_dat:
                if os.path.isfile(the_files.file_pickle_extra_index_command_dat):
                    try:
                        global_variable.extra_index_for_command_dat = read_pickle.read(the_files.file_pickle_extra_index_command_dat)
                    except:
                        global_variable.extra_index_for_command_dat = {}
            
            index_dict = global_variable.extra_index_for_command_dat
        
        elif data_type == "command_english.dat":
            print("command_english.dat")
            if not global_variable.extra_index_for_command_english_dat:
                if os.path.isfile(the_files.file_pickle_extra_index_command_english_dat):
                    try:
                        global_variable.extra_index_for_command_english_dat = read_pickle.read(the_files.file_pickle_extra_index_command_english_dat)
                    except:
                        global_variable.extra_index_for_command_english_dat = {}
            
            index_dict = global_variable.extra_index_for_command_english_dat
        
        if not index_dict : 
            print("no index,return")
            return
        
        if game_name not in index_dict: 
            print("item id not in index")
            #return # 是否 还需要添加主版本按钮
            if game_name in global_variable.dict_data["clone_to_parent"]:
                
                parent_name = global_variable.dict_data["clone_to_parent"][game_name]
                
                print("parent id in index")
                
                if parent_name in index_dict:
                    #the_tk_text = self.new_ui_text_area.new_ui_text
                    #the_tk_text.configure(state="normal")
                    #
                    #the_tk_text.insert(tk.END,"\n")
                    #the_tk_text.insert(tk.END,parent_name,("command_find_parent",))
                    #the_tk_text.insert(tk.END,"\n")
                    #    # 让内容，占一整行，方便提取文本值
                    #the_tk_text.configure(state="disabled")
                    self.new_func_show_command_dat_use_index(data_type,parent_name)
                    return
                    
                else:
                    print("parent id not in index,return")
                    return
            else:
                print("return")
                return
            
            return
        
        the_index = index_dict[game_name]
        
        # 初始化
        try:
            self.new_var_command_content
        except:
            self.new_var_command_content =  None 

        # 读取内容
        
        # 中文版，英文版 ，格式不同
        
        try:
            if data_type == "command.dat":
                #print("A")
                self.new_var_command_content = extra_command.get_content_by_file_name_use_index( path,game_name,the_index )
            elif data_type == "command_english.dat":
                #print("B")
                self.new_var_command_content = extra_command_english.get_content_by_file_name_use_index( path,game_name,the_index )
        except:
            self.new_var_command_content =  None 
        
        
        if self.new_var_command_content is None:
            self.new_ui_chooser_2["values"]=("",)
            self.new_ui_chooser_2.set("") 
        elif len(self.new_var_command_content) <= 1:
            #print(r"<=1")
            self.new_ui_chooser_2["values"]=(_("全部"),)
            self.new_ui_chooser_2.set( _("全部") ) 
            for x in self.new_var_command_content:
                #for y in self.new_var_command_content[x]:
                #    self.new_func_insert_string( y)
                self.new_func_insert_list_of_string( self.new_var_command_content[x] )
        else:
            #print(r">1")
            index = []
            index.append( _("全部") )
            for x in self.new_var_command_content:
                # 提取 每一段 第一行，做为小标题
                try:
                    index.append( self.new_var_command_content[x][0].rstrip("\r\n") )
                except:
                    index.append("")
            self.new_ui_chooser_2["values"]=index
            self.new_ui_chooser_2.set( _("全部") ) 
            
            for x in self.new_var_command_content:
                #for y in self.new_var_command_content[x]:
                #    self.new_func_insert_string( y)
                self.new_func_insert_list_of_string( self.new_var_command_content[x] )
    
    def new_func_show_command_dat(self,data_type,game_name):
        if self.new_var_index_flag.get():
            self.new_func_show_command_dat_use_index(data_type,game_name)
        else:
            self.new_func_show_command_dat_not_use_index(data_type,game_name)
    
    def new_func_binding_command_index_choose(self,event):

        try:
            self.new_var_command_content
        except:
            self.new_func_clear_content() 
            # 清空内容
            
            return 0 
            # 如果还没有 数据 记录
            # 退出函数
        
        if self.new_var_command_content is None:
            self.new_func_clear_content() 
            # 清空内容
            
            return 0 
            # 退出函数
        
        
        n = self.new_ui_chooser_2.current()
        
        if n==0:
            self.new_func_clear_content() 
            try:
                for x in self.new_var_command_content:
                    #for y in self.new_var_command_content[x]:
                    #    self.new_func_insert_string( y)
                    self.new_func_insert_list_of_string(self.new_var_command_content[x])
            except:
                pass
        else:
            self.new_func_clear_content() 
            try:
                #for x in self.new_var_command_content[n]:
                #    self.new_func_insert_string( x)
                self.new_func_insert_list_of_string(self.new_var_command_content[n])
            except:
                pass
    
    # 没用上了，直接导入 主版本 文档
    def new_func_tag_binding_command_dat_find_parent_use_index(self,event):
        print()
        print("command.dat find parent use index")
        
        
        
        index_start = self.new_ui_text_area.new_ui_text.index("current linestart")
        index_end   = self.new_ui_text_area.new_ui_text.index("current lineend")
        
        print(index_start)
        print(index_end)
        
        # tag.first tag.last
        #index_start = self.new_ui_text_area.new_ui_text.index("command_find_parent.first")
        #index_end   = self.new_ui_text_area.new_ui_text.index("command_find_parent.last")
            # 如果有多个 相同的 tag ，找到的第一个 和 最后一个，
        
        # 算了，让 tag 内容，占一整行吧
        
        parent_name = self.new_ui_text_area.new_ui_text.get(index_start,index_end)
        print(parent_name)
        parent_name = parent_name.rstrip("\r\n") # 不知道它，会不会包含 换行符号
        
        print(parent_name)
        
        # 获得文本数据后，再清理
        
        # 清理文本区
        self.new_func_clear_content()
        
        # 清理选择框
        self.new_func_clear_chooer()        
        
        n = self.new_ui_text_chooser.current()
        data_type = text_types_2[n]
        print(data_type)
        
        self.new_func_show_command_dat_use_index( data_type,parent_name, )

if __name__ == "__main__" :
    
    root=tk.Tk()
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    

    
    #a=Text_with_scrollbar(root)
    a=Text_container(root)
    a.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S))
    
    
    for x in range(10):
        a.new_func_insert_string("test "*30+"\n")     
    
    for x in range(1000):
        a.new_func_insert_string(str(x) + " : "+"test\n") 
    
    root.mainloop()
