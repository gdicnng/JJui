# -*- coding: utf_8_sig-*-
import sys
import os
import time
import re
import glob
import subprocess
import threading
import zipfile

import webbrowser

import pickle

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog 
import tkinter.colorchooser

import tkinter.font as tkfont

from PIL import Image, ImageTk


if __name__ != "__main__":
    from jjui import save_pickle
    from jjui import read_pickle
    
    from jjui import folders_read
    from jjui import folders_save
    from jjui import folders_search
    from jjui import ui_configure_file
    
    from jjui import extra_read_history_xml
    from jjui import extra_command
    from jjui import extra_command_english
    from jjui import extra_history_dat
    from jjui import extra_mameinfo_dat
    from jjui import extra_gameinit_dat
    
    import jjui.initial_translation
    
if __name__ == "__main__" :
    import save_pickle
    import read_pickle
    
    import folders_read
    import folders_search
    import ui_configure_file
    import extra_read_history_xml

class MyUi:
    
    def __init__(self , 
                parent ,
                #ini_data,   # 配置文件 jjui.ini
                            # 其中的一些 ui 宽度、高度 等 ，用于 ui 初始化
                            # 用了两个，index 、extra 的宽度
                            
                            # ？？？？
                            # wip
                            # 调到之后，再用???
                            
                #ini_path,   # 配置文件 jjui.ini 路径，用手保存
                data_from_main,
                ttk_style,
                    ):
        
        self.parent = parent
        
        self.style = ttk_style
        
        self.data_from_main = data_from_main
        
        self.ini_data = data_from_main["ini_data"] 
        self.ini_path = data_from_main["ini_path"]
        
        self.image_types = (r"snap",
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
                            ) # ui ,extra ，图片的选项
        self.image_types_translation = {
                        "snap":"截图 snap",
                        "titles":"标题图 titles",
                        "flyers":"海报 flyers",
                        } # ui ,extra ，图片的选项
                        
        self.text_types =  ("history.xml","history.dat","mameinfo.dat","messinfo.dat", "gameinit.dat" , "sysinfo.dat",)# ui ,extra ，text 的选项
        # history.dat sysinfo.dat
        # mameinfo.dat messinfo.dat
        self.text_types_translation = {
                        "history.xml":"历史(xml格式)：history.xml",
                        "history.dat":"历史(dat格式)：history.dat",
                        }
        
        
        self.text_types_2 =  ("command.dat","command_english.dat",)
            # ui ,extra ，文档，第二类，出招表
        self.text_types_2_translation =  {
                        "command.dat":"出招表 中文版 command.dat",
                        "command_english.dat":"出招表 英文版 command_english.dat",
                        }

        # self.ini_files = {}     
            # 在 self.ui_initial_functions_index_content_external() 中赋值
            # 外部 目录 文件
        # self.ini_set_dict = {}  
            # 在 self.ui_initial_functions_index_content_external() 中赋值
            # 外部 目录 文件 读取的数据            
        
        self.parent = parent
        self.parent.rowconfigure(0, weight=0)
        self.parent.rowconfigure(1, weight=1)
        self.parent.rowconfigure(2, weight=0)
        self.parent.columnconfigure(0, weight=1)
        
        # ui 
        self.ui_frames( self.parent )
        self.ui_top_bar( self.frame_top )
        
        self.ui_index(     self.m1 ) 
        self.ui_gamelist(  self.m2 )
        self.ui_extra(     self.m3 )  
         
        self.ui_status_bar( self.frame_bottom )
        self.ui_menu( self.parent )
        # # #
        self.ui_index_pop_up_menu( self.parent )
        self.ui_gamelist_pop_up_menu( self.parent )
        self.ui_gamelist_pop_up_menu_of_heading( self.parent )
        #
        
        #快捷键
        #F5 刷新列表 split
        #self.parent.bind('<Key-F5>',self.menu_call_back_function_gamelist_available_refresh)
        #F6 刷新列表 merged
        #self.parent.bind('<Key-F6>',self.menu_call_back_function_gamelist_available_refresh_2)
        self.parent.bind('<Key-F9>',self.show_current_working_directory)
        self.parent.bind('<Key-F10>',self.get_rompath_from_command_line)
        
        # bindings
        # bindings top
        # 游戏列表 1/2/all
        self.top_button_change.bind('<ButtonPress-1>',self.top_binding_gamelist_change)
        # 游戏列表 分组/不分组
        self.top_button_group.bind('<ButtonPress-1>',self.top_binding_change_group)
        # 游戏列表 定位到
        self.top_button_see.bind('<ButtonPress-1>',  self.top_binding_see_the_game) 
        # 鼠标点击，搜索
        self.top_button_search.bind('<ButtonPress-1>', self.top_binding_search)
        # 回车，搜索
        self.top_entry_search.bind('<Return>',         self.top_binding_search)
        # 正则搜索
        self.top_button_search_re.bind('<ButtonPress-1>', self.top_binding_search_re)
        # 搜索内容，清空
        self.top_button_clear.bind('<ButtonPress-1>',self.top_binding_search_clear)
        # 列表数量
        #self.top_button_count.bind('<ButtonPress-1>',self.count)
        #self.top_button_jump.bind('<ButtonPress-1>',self.gamelist_jump)
        
        # bindings 目录
        # 滚动条
        self.tree_index.bind('<MouseWheel>',    self.index_binding_mousewheel ) 
        # 点击目录，切换游戏列表
        self.tree_index.bind('<ButtonPress-1>', self.index_binding_choose_index_by_click ) 
        # 目录中，按回车键，切换游戏列表
        self.tree_index.bind('<Return>', self.index_binding_choose_index_by_press_return)
        # 按“→”键 ，展开
        self.tree_index.bind('<Right>',  self.index_binding_key_press_right)
        # 右键菜单
        self.tree_index.bind('<ButtonPress-3>',self.index_binding_menu_popup)        
        # 按 空格 键 ，展开、收起，重新 bind
        self.tree_index.bind('<Key-space>',lambda x : self.gamelist_binding_key_press_space(tree=self.tree_index))
        # Home 键，到 开头
        self.tree_index.bind('<Home>',lambda x : self.tree_index.yview(tk.MOVETO,0))
        # End 键，到 结尾
        self.tree_index.bind('<End>', lambda x : self.tree_index.yview(tk.MOVETO,1))         

        # bindings 列表 
        # 1 点击标题 排序
        # 2 点击到图标列 ， 有克隆版本的，展开／关闭 子列表
        self.tree.bind('<ButtonPress-1>',    self.gamelist_binding_click_heading )
        # 游戏列表，选择内容变化时，切换 状态栏、周边内容 的显示
        self.tree.bind('<<TreeviewSelect>>', self.gamelist_binding_selection_change )
        # 滚动条
        self.tree.bind('<MouseWheel>',       self.gamelist_binding_mousewheel )
        # 双击 打开 MAME
        self.tree.bind('<Double-Button-1>',self.gamelist_binding_start_game_by_double_click )
        # 回车 打开 MAME
        self.tree.bind('<Return>',         self.gamelist_binding_start_game_by_press_return )
        # 多选模式，全选快捷键 ，ctrl + A/a
        self.tree.bind('<Control-KeyPress-A>',self.gamelist_binding_select_all)
        self.tree.bind('<Control-KeyPress-a>',self.gamelist_binding_select_all)
        # 按“→”键 ，展开
        self.tree.bind('<Right>',self.gamelist_binding_key_press_right)
        # 鼠标右键，弹出菜单
        self.tree.bind('<ButtonPress-3>',self.gamelist_binding_menu_popup)
        # Home 键，到 开头
        self.tree.bind('<Home>',lambda x : self.tree.yview(tk.MOVETO,0))
        # End 键，到 结尾
        self.tree.bind('<End>', lambda x : self.tree.yview(tk.MOVETO,1))
        # 按 空格 键 ，展开、收起，重新 bind
        self.tree.bind('<Key-space>',lambda x : self.gamelist_binding_key_press_space(tree=self.tree))
        
        
        # bindings extra
        # 周边，切换显示内容
        self.notebook.bind('<<NotebookTabChanged>>',self.extra_binding_notebook_tab_changed) 
        # 拉伸时，图片也变化
        self.extra_image.bind('<Configure>',  self.extra_binding_image_change_size)
        # 拉伸时，图片也变化
        self.extra_image_2.bind('<Configure>',self.extra_binding_image_change_size_2)
        # 选择图片 种类，刷新周边显示
        self.extra_image_chooser.bind("<<ComboboxSelected>>",self.extra_binding_image_type_choose)
        self.extra_image_chooser_2.bind("<<ComboboxSelected>>",self.extra_binding_image_type_choose)
        
        # 选择文档 种类，刷新周边显示。用上边的函数，一样
        self.extra_text_chooser.bind("<<ComboboxSelected>>",self.extra_binding_image_type_choose)
        
        # 选择文档 种类，刷新周边显示。用上边的函数，一样
        self.extra_command_type_chooser.bind("<<ComboboxSelected>>",self.extra_binding_image_type_choose)
        
        # 出招表 的 目录，选择
        self.extra_command_chooser.bind("<<ComboboxSelected>>",self.extra_binding_command_index_choose) 

    # ui 布局
    
    def ui_frames(self, parent):
        self.frame_top     = ttk.Frame( parent , ) # 上
        self.frame_middle  = ttk.PanedWindow(parent,orient=tk.HORIZONTAL)  # 中
        self.frame_bottom  = ttk.Frame( parent,   )# 下

        self.m1 = ttk.Frame( self.frame_middle, )
        self.m2 = ttk.Frame( self.frame_middle, )
        self.m3 = ttk.Frame( self.frame_middle, )
        
        self.frame_top.grid(row=0,column=0,sticky=(tk.W,tk.E,))
        self.frame_middle.grid(row=1,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
        self.frame_bottom.grid(row=2,column=0, sticky=(tk.W,tk.N,tk.E,tk.S))
        
        #self.m1.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S))
        #self.m2.grid(row=0,column=1,sticky=(tk.W,tk.N,tk.E,tk.S))
        #self.m3.grid(row=0,column=2,sticky=(tk.W,tk.N,tk.E,tk.S))
        
        self.frame_middle.add(self.m1,weight=0)
        self.frame_middle.add(self.m2,weight=1)
        self.frame_middle.add(self.m3,weight=0)
            # weight

        ## row/column config
        self.frame_top.rowconfigure(0, weight=0)#
        self.frame_top.columnconfigure(0, weight=0)
        self.frame_top.columnconfigure(1, weight=0)
        self.frame_top.columnconfigure(2, weight=0)
        self.frame_top.columnconfigure(3, weight=0)
        self.frame_top.columnconfigure(4, weight=0)
        self.frame_top.columnconfigure(5, weight=0)
        self.frame_top.columnconfigure(6, weight=0)
        self.frame_top.columnconfigure(7, weight=0)
        self.frame_top.columnconfigure(8, weight=0)
        self.frame_top.columnconfigure(9, weight=0)
        self.frame_top.columnconfigure(10, weight=0)
        self.frame_top.columnconfigure(11, weight=0)
        self.frame_top.columnconfigure(12, weight=0)
        self.frame_top.columnconfigure(13, weight=0)
        self.frame_top.columnconfigure(14, weight=0)
        self.frame_top.columnconfigure(15, weight=1)

        self.frame_bottom.rowconfigure(0, weight=0) #
        self.frame_bottom.columnconfigure(0, weight=0)  
        self.frame_bottom.columnconfigure(1, weight=0)  
        self.frame_bottom.columnconfigure(2, weight=1)  
        self.frame_bottom.columnconfigure(3, weight=0)  
        self.frame_bottom.columnconfigure(4, weight=0)  
        self.frame_bottom.columnconfigure(5, weight=0)  
        self.frame_bottom.columnconfigure(6, weight=0)  

        self.frame_middle.rowconfigure(0, weight=1)
        self.frame_middle.columnconfigure(0, weight=0)  
        self.frame_middle.columnconfigure(1, weight=1)  
        self.frame_middle.columnconfigure(2, weight=0)  
        
        self.m1.rowconfigure(0, weight=1)
        self.m1.columnconfigure(0, weight=1)
        self.m2.rowconfigure(0, weight=1)
        self.m2.columnconfigure(0, weight=1)
        self.m3.rowconfigure(0, weight=1)
        self.m3.columnconfigure(0, weight=1)

    def ui_top_bar(self,parent):
                # w = ttk.Button(parent, option=value, ...)
        self.top_button_change =ttk.Button(parent,takefocus=False,text=r'1/2/3',width=-1)
        self.top_button_change.grid(row=0,column=0,sticky=(tk.W,))
        
        self.top_button_group = ttk.Button(parent,takefocus=False,text=r'分组／不分组',width=-1)
        self.top_button_group.grid(row=0,column=1,sticky=(tk.W,))

        self.top_button_see = ttk.Button(parent,takefocus=False,text=r'定位到',width=-1)
        self.top_button_see.grid(row=0,column=2,sticky=(tk.W,))

        self.top_game_name = tk.StringVar()
        self.top_label_remember = ttk.Label(parent,takefocus=False,anchor=tk.W,width=10,textvariable=self.top_game_name)
        self.top_label_remember.grid(row=0,column=3,sticky=(tk.W,))
        
        self.top_label_search = ttk.Label(parent,takefocus=False,anchor=tk.W,text=r" 搜索栏:")
        self.top_label_search.grid(row=0,column=4,sticky=(tk.W,))
        
        self.top_search_content = tk.StringVar()
        self.top_entry_search = ttk.Entry(parent,takefocus=False,justify=tk.LEFT,textvariable=self.top_search_content )
        self.top_entry_search.grid(row=0,column=5,sticky=(tk.W,))
        
        self.top_button_search = ttk.Button(parent,takefocus=False,text=r'搜索',width=-1)
        self.top_button_search.grid(row=0,column=6,sticky=(tk.W,))
        
        self.top_button_search_re = ttk.Button(parent,takefocus=False,text=r'正则搜索',width=-1)
        self.top_button_search_re.grid(row=0,column=7,sticky=(tk.W,))        
        
        #self.top_button_jump = ttk.Button(parent,text=r'跳转',width=-1)
        #self.top_button_jump.grid(row=0,column=7,sticky=(tk.W,))  

        self.top_button_clear = ttk.Button(parent,takefocus=False,text=r'清空',width=-1)
        self.top_button_clear.grid(row=0,column=8,sticky=(tk.W,))
        
        self.top_button_count = ttk.Button(parent,takefocus=False,text=r'游戏列表数量',width=-1)
        #self.top_button_count.grid(row=0,column=15,sticky=(tk.E,))

    def ui_gamelist(self, parent):
    
        self.tree = ttk.Treeview(parent,selectmode='browse',)
        
        self.gamelist_scrollbar_1 = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.tree.yview)
        
        self.gamelist_scrollbar_2 = ttk.Scrollbar( parent, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=self.gamelist_scrollbar_1.set)
        self.tree.configure(xscrollcommand=self.gamelist_scrollbar_2.set)
        
        self.tree.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.gamelist_scrollbar_1.grid(row=0,column=1,columnspan=2,sticky=(tk.N,tk.S,tk.E))
        self.gamelist_scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E,tk.S))

    
    def ui_index(self, parent):
        
        #width = self.ini_data["width_index"]
        
        self.tree_index = ttk.Treeview(parent,selectmode='browse')
        
        self.index_scrollbar_1 = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.tree_index.yview)
        #self.index_scrollbar_2 = ttk.Scrollbar( parent, orient=tk.HORIZONTAL, command=self.tree_index.xview)
        
        self.tree_index.configure(yscrollcommand=self.index_scrollbar_1.set)
        #self.tree_index.configure(xscrollcommand=self.index_scrollbar_2.set)
        
        self.tree_index.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.index_scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S))

        self.tree_index['columns'] = ("type","others")
        # iid ，用 | 分隔，第一层|第二层|第三层
        #   外部分类的话，
        #       第一层文件名，不会有 | ，
        #       第二层可能会有 |
        #       可以用：
        #       str.split("|",1) ，分隔成 两组
        #   内部分类的话，
        #       第一层自己控制不用 |
        #       第二层，提取数据成生，可能有 | 字符
        #       如果用两层，也一样，
        #
        #       但如果用三层，得用一列记录一下 子 id 
        #       算了，只用两层算了，不整第三层了，
        #       不用记录了
        
        #self.tree_index.column('#0', width= width )
        self.tree_index.heading("#0", text="目录列表")
        
        self.tree_index.heading("#0", text="目录列表")
        self.tree_index.heading("type", text="类型")
        self.tree_index.heading("others", text="其它")
        
        self.tree_index['displaycolumns'] = ()

    def ui_extra(self, parent):
      
        #width = self.ini_data["width_extra"]
        
        # notebook
        self.notebook = ttk.Notebook(parent , takefocus=False,)#width = width
        self.notebook.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)
        
        #self.notebook.state(statespec=("readonly",))
        
        # 图片
        self.extra_f1 = ttk.Frame(self.notebook)  
        self.notebook.add(self.extra_f1, text='图片')
        
        self.extra_f1.columnconfigure(0,weight=1)
        #self.extra_f1.rowconfigure(0,weight=0)        
        self.extra_f1.rowconfigure(0,weight=1)        
        #self.extra_f1.rowconfigure(1,weight=0) 
        #self.extra_f1.rowconfigure(2,weight=1) 

        self.extra_image_panedwindow = ttk.PanedWindow(self.extra_f1,orient=tk.VERTICAL)
        self.extra_image_panedwindow.grid(row=0 , column=0 , sticky=(tk.W,tk.N,tk.E,tk.S))

        self.extra_image_f1 = ttk.Frame(self.extra_image_panedwindow)
        self.extra_image_panedwindow.add(self.extra_image_f1)
        
        self.extra_image_f1.columnconfigure(0,weight=1)
        self.extra_image_f1.rowconfigure(0,weight=0)
        self.extra_image_f1.rowconfigure(1,weight=0)
        self.extra_image_f1.rowconfigure(2,weight=1)
        
        self.extra_image_f2 = ttk.Frame(self.extra_image_panedwindow)
        self.extra_image_panedwindow.add(self.extra_image_f2)
        
        self.extra_image_f2.columnconfigure(0,weight=1)
        self.extra_image_f2.rowconfigure(0,weight=0)
        self.extra_image_f2.rowconfigure(1,weight=0)
        self.extra_image_f2.rowconfigure(2,weight=1)        

        # 图 1
        self.extra_image_str = tk.StringVar()
        self.extra_image_chooser = ttk.Combobox( self.extra_image_f1 ,takefocus=False,textvariable=self.extra_image_str,state="readonly")
        self.extra_image_chooser.grid(row=0 , column=0 , sticky=(tk.W,tk.N,tk.E,),)
        
        # self.image_types
        # self.image_types_translation
        temp=[]
        for x in self.image_types:
            if x in self.image_types_translation:
                temp.append(self.image_types_translation[x])
            else:
                temp.append(x)
        self.extra_image_chooser["values"]= temp
        try: # 读取配置文件中 记录的 index
            n = self.ini_data["extra_image_chooser_index"] 
            if n < len(self.image_types):
                pass
            else:
                n=0
            self.extra_image_chooser.set( temp[n] )
        except:
            self.extra_image_chooser.set( temp[0] )
        del temp
        
        self.extra_image_usezip = tk.IntVar()
        self.extra_image_usezip_checkbutton = ttk.Checkbutton( self.extra_image_f1 , takefocus=False,text="是否使用 zip 中的图片",  variable=self.extra_image_usezip)
        self.extra_image_usezip_checkbutton.grid(row=1 , column=0 , sticky= (tk.W, tk.N, tk.S),) 
        
        self.extra_image = tk.Canvas( self.extra_image_f1 ,highlightthickness = 0, )        
        self.extra_image.grid(row=2 , column=0 , sticky=(tk.W,tk.N,tk.E,tk.S),)  

        # 图2
        self.extra_image_str_2 = tk.StringVar()
        self.extra_image_chooser_2 = ttk.Combobox( self.extra_image_f2 ,takefocus=False,textvariable=self.extra_image_str_2,state="readonly")
        self.extra_image_chooser_2.grid(row=0 , column=0 , sticky=(tk.W,tk.N,tk.E,),)
        
        # self.image_types
        # self.image_types_translation
        temp=[]
        for x in self.image_types:
            if x in self.image_types_translation:
                temp.append(self.image_types_translation[x])
            else:
                temp.append(x)
        self.extra_image_chooser_2["values"]= temp
        try: # 读取配置文件中 记录的 index
            n = self.ini_data["extra_image_chooser_2_index"] 
            if n < len(self.image_types):
                pass
            else:
                n=0
            self.extra_image_chooser_2.set( temp[n] )
        except:
            self.extra_image_chooser_2.set( temp[0] )      
        del temp
        
        self.extra_image_usezip_2 = tk.IntVar()
        self.extra_image_usezip_checkbutton_2 = ttk.Checkbutton( self.extra_image_f2 , takefocus=False,text="是否使用 zip 中的图片",  variable=self.extra_image_usezip_2)
        self.extra_image_usezip_checkbutton_2.grid(row=1 , column=0 , sticky= (tk.W, tk.N, tk.S),) 
        
        self.extra_image_2 = tk.Canvas( self.extra_image_f2 ,highlightthickness = 0, )        
        self.extra_image_2.grid(row=2 , column=0 , sticky=(tk.W,tk.N,tk.E,tk.S),) 

        

     
        # 文档一
        self.extra_f2 = ttk.Frame(self.notebook,)  #增加新选项卡
        self.notebook.add(self.extra_f2, text='文档')  #把新选项卡增加到Notebook 
        self.extra_f2.columnconfigure(0,weight=1)
        self.extra_f2.columnconfigure(1,weight=0)
        self.extra_f2.rowconfigure(0,weight=0)        
        self.extra_f2.rowconfigure(1,weight=1)         
        
        self.extra_text_str = tk.StringVar()
        self.extra_text_chooser = ttk.Combobox( self.extra_f2 ,takefocus=False,textvariable=self.extra_text_str,state="readonly")
        self.extra_text_chooser.grid(row=0 , column=0 , columnspan=2,sticky=(tk.W,tk.N,tk.E,),)# columnspan=2 ，因为有进度条
        
        # self.text_types
        # self.text_types_translation
        temp = []
        for x in self.text_types:
            if x in self.text_types_translation:
                temp.append( self.text_types_translation[x] )
            else:
                temp.append(x)
        self.extra_text_chooser["values"] = temp
        try: # 读取配置文件中 记录的 index
            n = self.ini_data["extra_text_chooser_index"] 
            if n < len(self.text_types):
                pass
            else:
                n=0
            self.extra_text_chooser.set( temp[n] )
        except:
            self.extra_text_chooser.set(temp[0])      
        del temp        
        
        self.extra_text = tk.Text(self.extra_f2,undo=False, takefocus=False, wrap=tk.CHAR)
        self.extra_scrollbar_1 = ttk.Scrollbar( self.extra_f2, orient=tk.VERTICAL, command=self.extra_text.yview)
        
        self.extra_text.configure(yscrollcommand=self.extra_scrollbar_1.set)
        
        self.extra_text.grid(row=1,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.extra_scrollbar_1.grid(row=1,column=1,sticky=(tk.N,tk.E,tk.S))
        
        # 文档二 command.dat
        self.extra_f3 = ttk.Frame(self.notebook,)  #增加新选项卡
        self.notebook.add(self.extra_f3, text='文档2')  #把新选项卡增加到Notebook 
        self.extra_f3.columnconfigure(0,weight=1)
        self.extra_f3.columnconfigure(1,weight=0)
        self.extra_f3.rowconfigure(0,weight=0)        
        self.extra_f3.rowconfigure(1,weight=0)         
        self.extra_f3.rowconfigure(2,weight=1)         
        
        # self.text_types
        
        self.extra_command_type_chooser = ttk.Combobox( self.extra_f3 ,takefocus=False,state="readonly")
        self.extra_command_type_chooser.grid(row=0 , column=0 , columnspan=2,sticky=(tk.W,tk.N,tk.E,),)# columnspan=2 ，因为有进度条
        
        temp = []
        for x in self.text_types_2:
            if x in self.text_types_2_translation:
                temp.append( self.text_types_2_translation[x] )
            else:
                temp.append(x)
        self.extra_command_type_chooser["values"] = temp
        try: # 读取配置文件中 记录的 index
            n = self.ini_data["extra_command_type_chooser_index"] 
            if n < len(self.text_types_2):
                pass
            else:
                n=0
            self.extra_command_type_chooser.set( temp[n] )
        except:
            self.extra_command_type_chooser.set(temp[0])    
        del temp
        
        self.extra_command_str = tk.StringVar()
        self.extra_command_chooser = ttk.Combobox( self.extra_f3 ,takefocus=False, textvariable=self.extra_command_str,state="readonly")
        self.extra_command_chooser.grid(row=1 , column=0 , columnspan=2,sticky=(tk.W,tk.N,tk.E,),)# columnspan=2 ，因为有进度条
        
        #self.extra_command_chooser["values"] = 
        #self.extra_command_chooser.set() 
        
        #
        self.extra_command_text = tk.Text(self.extra_f3,undo=False, takefocus=False, wrap=tk.CHAR)
        self.extra_scrollbar_command_1 = ttk.Scrollbar( self.extra_f3, orient=tk.VERTICAL, command=self.extra_command_text.yview)
        
        self.extra_command_text.configure( yscrollcommand = self.extra_scrollbar_command_1.set )
        
        self.extra_command_text.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.extra_scrollbar_command_1.grid(row=2,column=1,sticky=(tk.N,tk.E,tk.S))        

    def ui_status_bar(self, parent):
    
        self.status_bar_number_total = tk.StringVar()
        self.status_bar_number_total.set('总数量')
        self.status_bar_label_num_total = ttk.Label( parent,anchor=tk.W,textvariable=self.status_bar_number_total)
        self.status_bar_label_num_total.grid(row=0,column=0,sticky=(tk.W,))  

        self.status_bar_number_of_index = tk.StringVar()
        self.status_bar_number_of_index.set('数量')
        self.status_bar_label_num_index = ttk.Label( parent,anchor=tk.W,textvariable=self.status_bar_number_of_index)
        self.status_bar_label_num_index.grid(row=0,column=1,sticky=(tk.W,))  

        self.status_bar_text = tk.StringVar()
        self.status_bar_text.set('状态栏')
        self.status_bar_label = ttk.Label( parent,anchor=tk.W,textvariable=self.status_bar_text)
        self.status_bar_label.grid(row=0,column=2,sticky=(tk.W,tk.N,tk.E,tk.S))
        
        self.status_bar_index_edit_info = tk.StringVar()
        self.status_bar_index_edit_info.set("test")
        self.status_bar_label_index_edit_info = ttk.Label( parent,anchor=tk.W,textvariable=self.status_bar_index_edit_info)
        self.status_bar_label_index_edit_info.grid(row=0,column=3,sticky=(tk.E,tk.S))        
        
        self.sizegrip = ttk.Sizegrip(parent)
        self.sizegrip.grid(row=0,column=99,sticky="se")


    #####
    
    # 菜单
    
    def ui_menu(self,parent):
        self.menu_bar = tk.Menu(parent)
        parent.config(menu=self.menu_bar)
        
        # memu UI
        
        self.menu_ui = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label =r"UI", menu=self.menu_ui)#
        
        self.menu_ui.add_command(label=r"UI ，切换主题，关闭程序，重新打开后生效", command=self.menu_call_back_function_change_theme)

        self.menu_ui.add_separator()
        
        self.menu_ui.add_command(label=r"路径设置", command=self.menu_call_back_function_set_file_path)
        
        self.menu_ui.add_separator()
        
        self.menu_index_tk_scaling_use_flag = tk.IntVar() # default value 0
            # ui_initial_functions_variable_initial 函数中，初始化
        self.menu_ui.add_checkbutton(label=r"启用 tk scaling 缩放（关闭程序，重新打开后生效）", 
                        variable = self.menu_index_tk_scaling_use_flag ,
                        command=self.menu_call_back_function_use_tk_scaling,)
        
        self.menu_ui.add_command(label=r"设置 tk scaling 缩放 值", command=self.menu_call_back_function_set_tk_scaling_number)
        
        
        self.menu_ui.add_separator()
        
        #self.menu_ui.add_command(label="字体／ (游戏列表) 行距", command=self.gamelist_font)
        
        self.menu_ui.add_command( label="列表 行高 设置", command=self.menu_call_back_function_set_row_height )
        self.menu_ui.add_command( label="列表 图标 宽度 设置", command=self.menu_call_back_function_set_icon_size )
        self.menu_ui.add_command( label="列表 字体 设置", command=self.menu_call_back_function_set_gamelist_font )
        self.menu_ui.add_command( label="文档1 字体 设置", command=self.menu_call_back_function_set_text_font )
        self.menu_ui.add_command( label="文档2 字体 设置", command=self.menu_call_back_function_set_text_2_font )
        self.menu_ui.add_command( label="其它 字体 设置", command=self.menu_call_back_function_set_others_font )

        self.menu_ui.add_separator()
        
        self.menu_ui.add_command( label="内置主题背景色", command=self.menu_call_back_function_set_background_of_internal_themes )
        
        self.menu_ui.add_separator()
        
        self.menu_ui.add_command(label=r"保存配置文件", command=self.menu_call_back_function_save_ini_data)
        self.menu_ui.add_command(label=r"保存配置文件、窗口大小", command=self.menu_call_back_function_window_size_save)
        self.menu_ui.add_command(label=r"保存配置文件、窗口大小/位置", command=self.menu_call_back_function_window_size_and_position_save)
        
        #self.menu_font = tk.Menu(self.menu_bar, tearoff=0)
        #self.menu_bar.add_cascade(label="字体", menu=self.menu_font)
        #self.menu_font.add_command(label="游戏列表 字体／行距", command=self.gamelist_font)
        
        # menu index
        
        self.menu_index = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="目录列表", menu=self.menu_index)
        
        self.menu_index_edit_flag = tk.IntVar() # default value 0
        self.menu_index.add_checkbutton(label= "编辑",
                variable = self.menu_index_edit_flag ,
                command = self.donothing)
        self.menu_index.add_command(label="保存",
                command = self.menu_call_back_function_save_index)
        
        self.menu_index.add_command(label="显示目录／显示全部", command=self.menu_call_back_function_index_show_all)
        
        
        
        self.menu_for_gamelist = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="游戏列表", menu=self.menu_for_gamelist)
        
        self.menu_for_gamelist.add_separator()
        self.menu_for_gamelist.add_command(label=r"刷新列表，split/分离模式 (不具体校验文件，只检查有没有压缩包/文件夹)", command=self.menu_call_back_function_gamelist_available_refresh )
        
        self.menu_for_gamelist.add_command(label=r"刷新列表，merged/合并模式 (不具体校验文件，只检查有没有压缩包/文件夹)", command=self.menu_call_back_function_gamelist_available_refresh_2 )
        
        self.menu_for_gamelist.add_command(label=r"以上两项，默认你会整理文件，把存在的文件都整理对了",state=tk.DISABLED, command=self.donothing )
        #
        self.menu_for_gamelist.add_separator()
        
        self.menu_for_gamelist.add_command(label=r"刷新列表，用 mame 整体校验，慢！",command=self.menu_call_back_function_gamelist_available_refresh_audit_by_mame_all )
        
        self.menu_for_gamelist.add_command(label=r"刷新列表，用 mame 逐个校验已拥有文件，特别慢！！！split/分离模式。(如果只有几十个游戏可以试试)",command=self.menu_call_back_function_gamelist_available_refresh_audit_by_mame_one_by_one ) 
        
        self.menu_for_gamelist.add_command(label=r"刷新列表，用 mame 逐个校验已拥有文件，特别慢！！！merged/合并模式。(如果只有几十个游戏可以试试)",command=self.menu_call_back_function_gamelist_available_refresh_audit_by_mame_one_by_one_2 )        
        
        self.menu_for_gamelist.add_separator()
        
        self.menu_gamelist_use_available_game_mark = tk.IntVar()
        self.menu_gamelist_use_available_game_mark.set(self.ini_data["use_available_game_mark"])
        self.menu_for_gamelist.add_checkbutton(label= "是否使用拥有标记(关闭程序重新打开后，生效)",
                variable = self.menu_gamelist_use_available_game_mark ,
                command = self.menu_call_back_function_gamelist_use_available_game_mark)
        self.menu_for_gamelist.add_command(label="拥有列表 过滤", command = self.menu_call_back_function_window_available_filter )
        self.menu_for_gamelist.add_separator()
        self.menu_for_gamelist.add_command(label="游戏列表 导入翻译／更新翻译", command = self.menu_call_back_function_gamelist_load_translation )
        self.menu_for_gamelist.add_separator()
        self.menu_for_gamelist.add_command(label="计算游戏列表 数量", command = self.menu_call_back_function_gamelist_count )
        
        self.menu_about = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="关于", menu=self.menu_about)
        self.menu_about.add_command(label="关于", command=self.menu_call_back_function_window_about)
        
        self.menu_about.add_command(label="打开帮助文档："+self.data_from_main['docs_html_index_file'], command=self.menu_call_back_function_open_html_file)
        
        self.menu_about.add_command(label="如果帮助文档没有正确打开，可以找到文件手动打开", state=tk.DISABLED)        

    # 鼠标右键菜单 ，index
    # 在 bingind 函数中 被调用
    #     def index_binding_menu_popup(self,event):
    def ui_index_pop_up_menu(self,parent):
        self.menu_mouse_index = tk.Menu(self.tree_index, tearoff=0)
        
        self.menu_mouse_index.add_command(label="目录列表，全部收起",
                command = self.index_pop_up_menu_function_hide_level2)
        
                
    # 鼠标右键菜单 ，game list
    # 在 bingind 函数中 被调用
    #     def gamelist_binding_menu_popup(self,event):
    def ui_gamelist_pop_up_menu(self,parent):
        self.menu_mouse = tk.Menu(self.tree, tearoff=0)
        
        self.menu_mouse.add_command(label="运行此游戏",
                command = self.gamelist_pop_up_menu_start_game)
        self.menu_mouse.add_command(label="运行此游戏，不隐藏 UI",
                command = self.gamelist_pop_up_menu_start_game_ui_not_hide)
        self.menu_mouse.add_command(label="运行此游戏，开启多键盘功能" ,
                command=self.gamelist_pop_up_menu_start_game_multikeyboard )
        
        self.menu_mouse.add_separator()
        
        self.menu_mouse.add_command(label="当前列表，全部展开",
                command=self.gamelist_pop_up_menu_show_clone )
        self.menu_mouse.add_command(label="当前列表，全部收起",
                command=self.gamelist_pop_up_menu_hide_clone )
        
        self.menu_mouse.add_separator()
        self.menu_mouse.add_command(label="校验此游戏roms： -verifyroms",
                command=self.gamelist_pop_up_menu_verify_roms )
        self.menu_mouse.add_command(label="校验此游戏samples： -verifysamples",
                command=self.gamelist_pop_up_menu_verify_samples )
        self.menu_mouse.add_command(label="显示此游戏roms校验信息，格式1： -listroms",
                command=self.gamelist_pop_up_menu_list_roms )       
        self.menu_mouse.add_command(label="显示此游戏roms校验信息，格式2，含大量其它信息： -listxml",
                command=self.gamelist_pop_up_menu_list_xml )                  
        
        self.menu_mouse.add_separator()
        
        self.menu_mouse_multi_select_mode_flag = tk.IntVar() # default value 0
        self.menu_mouse.add_checkbutton(label=r"多选模式",
                variable = self.menu_mouse_multi_select_mode_flag ,
                command=self.gamelist_pop_up_menu_select_mode )
        
        self.menu_mouse.add_separator()
        self.menu_mouse.add_command(label=r"导出当前列表内容到 " + self.data_from_main['export_text_file'],
                command=self.gamelist_pop_up_menu_export_gamelist )
        self.menu_mouse.add_command(label=r"导出选中内容到 " + self.data_from_main['export_text_file'],
                command=self.gamelist_pop_up_menu_export_gamelist_select_items )
        
        
        self.menu_mouse.add_separator()
        
        temp_str = "目录修改：从 自定义目录 移除"
        self.menu_mouse.add_command(label = temp_str ,
                command= lambda x=None : self.gamelist_pop_up_menu_delete_from_index( self.tree.selection() ) ,
                )
        # 记录 index
        self.menu_mouse_index_number_1 = self.menu_mouse.index( temp_str )
        del temp_str
        
        temp_str_2 = "目录修改：添加到 自定义目录"
        self.menu_mouse.add_command( label = temp_str_2 ,
                command= lambda x=None : self.gamelist_pop_up_menu_add_to_index( self.tree.selection() ) ,
                )
        self.menu_mouse_index_number_2 = self.menu_mouse.index( temp_str_2 )
        del temp_str_2

        #self.menu_mouse.add_command(label=r"xxxx",command=self.get_gamelist_select_items)
        
        self.menu_mouse.add_separator()
        #self.menu_mouse.add_command(label="未完成1",command=self.donothing)
        #self.menu_mouse.add_command(label="未完成2",command=self.donothing)
    def ui_gamelist_pop_up_menu_of_heading(self,parent):
        self.gamelist_pop_up_menu_of_heading = tk.Menu(self.tree, tearoff=0)
        
        self.gamelist_pop_up_menu_of_heading.add_separator()
        
        self.gamelist_pop_up_menu_of_heading.add_command(label="选择列表显示项目",
                command = self.gamelist_pop_up_menu_of_heading_choose_columns)


    ########
    
    
    # 初始化
    
    # 读取 必要 数据 ,
    # def read_ini_data(self, ini_data,ini_path) :
    #     self.ini_data = ini_data
    #     self.ini_path = ini_path # 保存 ini_data 时需要用路径
    #
    def ui_initial_functions_read_data(self,):
        
        data_file_path      = self.data_from_main["temp_file_name"]
        available_file_path = self.data_from_main["temp_file_name_available"]
        
        # 读取数据
        self.data = read_pickle.read( data_file_path )
        
        # 记录，拥有列表文件路径
        # 刷新游戏列表，需要用
        self.available_gamelist_file_path = available_file_path

        # 拥有列表，读取数据
        #  'available_set'
        self.data['set_data']['available_set'] = set() 
            # 默认值，如果 没有该文件、或 读取失败，
        # 读取 数据 'available_set'
        if os.path.isfile( available_file_path ):
            try:
                self.data['set_data']['available_set'] = read_pickle.read( available_file_path )
            except:
                pass
        
        # 添加未拥有列表
        self.data['set_data']['unavailable_set'] = self.data['set_data']['all_set'] - self.data['set_data']['available_set']

        # mame 版本信息，也在里面。改 ui 标题
        title  = self.parent.title() # 读取原标题
        title += self.data["mame_version"] # 添加版本信息
        self.parent.title( title )
        del title
        
        # 读取之后，正好有一个，总体数字，需要设置
        self.status_bar_number_total.set('总数量：' + str( len(self.data['set_data']['all_set']) ) + r". " )
    # 图片，初始化
    def ui_initial_functions_read_image(self):
        # 读取 绿、红、黄、黑，常用图标
        # no 图片
        # 全局图片 self.image_original 声明
        self.image_no = Image.open( self.data_from_main['image_path_no_image'] )
        self.size_image_no = self.image_no.size
        
        self.image_original = self.image_no
        self.size_original = self.size_image_no
        self.image = ImageTk.PhotoImage(self.image_original)  
        
        self.image_original_2 = self.image_no
        self.size_original_2 = self.size_image_no
        self.image_2 = ImageTk.PhotoImage(self.image_original_2)          
        
        self.image_none=tk.PhotoImage()
        
        self.image_black_original  = Image.open( self.data_from_main['image_path_icon_black'] )
        self.image_green_original  = Image.open( self.data_from_main['image_path_icon_green'] )
        self.image_yellow_original = Image.open( self.data_from_main['image_path_icon_yellow'] )
        self.image_red_original    = Image.open( self.data_from_main['image_path_icon_red'] )

        if self.ini_data["icon_size"] <= 0:
        
            self.image_black  = ImageTk.PhotoImage( self.image_black_original)
            
            self.image_green  = ImageTk.PhotoImage( self.image_green_original)
            
            self.image_yellow = ImageTk.PhotoImage( self.image_yellow_original)
            
            self.image_red    = ImageTk.PhotoImage( self.image_red_original)
        
        else:
            new_size = ( self.ini_data["icon_size"],self.ini_data["icon_size"] )
            
            self.image_black  = ImageTk.PhotoImage( self.image_black_original.resize( new_size,Image.BILINEAR, ))
            
            self.image_green  = ImageTk.PhotoImage( self.image_green_original.resize( new_size,Image.BILINEAR, ))
            
            self.image_yellow = ImageTk.PhotoImage( self.image_yellow_original.resize( new_size,Image.BILINEAR, ))
            
            self.image_red    = ImageTk.PhotoImage( self.image_red_original.resize( new_size,Image.BILINEAR, ))

    
    # 游戏列表，初始化
    def ui_initial_functions_gamelist_initial( self, ):
        
        data_file_name      = self.data_from_main["temp_file_name_gamelist"]
        columns_translation = self.data_from_main["columns_translation"]
        
        time1 = time.time()

        columns = self.ini_data["gamelist_columns"] 
        columns_width = self.ini_data["gamelist_columns_width"]
        # columns_translation
        
        # 读取列：self.ini_data["gamelist_columns"]
            # 这一项，ini_data 中，检查时，已检查多余项目
        # 显示列：self.ini_data["gamelist_columns_to_show_1"]
            # 在 self.tree["columns"] 中，再检查一下，
            # 免得设置时 gamelist_columns_to_show_1 项目 设置的 比 gamelist_columns 还要多
        
        # 列 初始化
        self.tree['columns'] = columns
        
        # 要显示的列，不能超过初始化的列范围
        # 检查多余项目
        def get_columns(old_columns): 
            temp_list = []
            for x in old_columns:
                if x in self.tree["columns"]:
                    temp_list.append(x)
            new_columns = tuple( temp_list )
            return new_columns
        
        # 设置 要显示 哪些列
        self.tree.configure( displaycolumns = get_columns( self.ini_data["gamelist_columns_to_show_1"] ) , )
        
        # '#0' 列，标题、宽度
        if '#0' in columns_translation:
            self.tree.heading("#0", text=columns_translation['#0'] )
        if '#0' in columns_width:
            self.tree.column('#0',width=columns_width['#0'],anchor="w")
        
        # 其它列，标题、宽度、anchor
        for x in self.tree['columns']: # 这里面没有 '#0'
            if x in columns_translation:
                self.tree.heading( x ,text = columns_translation[x])
            if x in columns_width:
                self.tree.column( x , width = columns_width[x] ,anchor="w")
        
        # "#0" 列，不拉伸
        self.tree.column("#0", stretch=False)
        # 其它列，不拉伸
        for x in self.tree['columns']: # 这里面没有 '#0'
            self.tree.column(x, stretch=False)

        # 清理
        for x in self.tree.get_children(""):
            self.tree.delete(x)
        
        data = read_pickle.read( data_file_name )

        for x in data:
            temp_string = []
            
            # 表格 内容
            for y in columns:
                temp_string.append( data[x].get(y,"") )
            
        
            self.tree.insert(
                             "",
                             "end",
                             iid=x,
                             tags = data[x].get('status',"others") ,
                             # "good" "imperfect" "preliminary" "others"
                             # tags  ，The value may be either a single string or a sequence of strings. 
                             values=temp_string ,
                             )
        
        del data
        
        # 用 tag 设置 图片
        self.tree.tag_configure("good",       image = self.image_green )
        self.tree.tag_configure("imperfect",  image = self.image_yellow )
        self.tree.tag_configure("preliminary",image = self.image_red )
        self.tree.tag_configure("others",     image = self.image_black )
        
        # 标记拥有列表
        self.other_functions_mark_available_games(mark_available=True,mark_un_available=False)
            
        
        
        time2 = time.time()
        print()
        print("列表初始化时间")
        print(time2 - time1)
        print()
  
    # 一些变量初始化
    def ui_initial_functions_variable_initial(self,):
        
        # 标记，是否使用 tk scaling
        self.menu_index_tk_scaling_use_flag.set( self.ini_data["tk_scaling_use_flag"] )
        
        # # 标记，是否使用 背景色
        # 取消了，自己设置背景色，细节太多了
        #self.menu_index_use_background_flag.set( self.ini_data["use_background_flag"] )
        
        self.search_mark = False # 设置 初始 状态
        self.index_set_remembered = set() # 设置 初始 状态
        
        # self.menu_mouse_index_edit_flag = tk.IntVar() # 初始化在 ui_index_pop_up_menu 函数中，
        self.ini_files_be_edited = set() # 被编辑的文件，记录
        # self.ini_files_editable # 外部列表初始化时，初始化这个变量
        
        
        # 拥有列表，自定义过滤文本
        self.available_hide_set = set()
        hide_file = self.data_from_main['available_hide_file']
        
        if os.path.isfile( hide_file ):
            try:
                text_file = open(hide_file, 'rt',encoding='utf_8_sig')
                lines = text_file.readlines()
                text_file.close()
                
                temp = []
                search_str = r'^\s*(\S.*?)\s*$'
                p=re.compile( search_str, )
                
                for line in lines:
                    m=p.search( line ) 
                    if m:
                        temp.append( m.group(1).lower() ) # 转小写
                
                self.available_hide_set = set(temp) & self.data['set_data']['all_set']
                print()
                print("hide_set")
                print( len(self.available_hide_set) )
                print()
                # 测试
                if "10yard85" in self.available_hide_set:
                    print("in")
            except:
                pass

       
        # 拥有列表，过滤项目，初始化
        #  self.filter ，，
        #       set ， 但保存到配置文件时，用的 list ，因为 set 用 print 输出来格式不一致
        #  self.filter_set
        self.filter = self.ini_data["filter"]
        # 转为 集合
        if len(self.filter) > 0:
            self.filter = set(self.filter)
        else :
            self.filter = set()
        self.filter_set = set()
        # 从配置文件内容，计算 self.filter_set
        for x in self.filter:
            if x in self.data['set_data']:
                self.filter_set =  self.filter_set | self.data['set_data'][x] 
            elif x in self.data['internal_index']:
                # 第一层
                self.filter_set = self.filter_set | set( self.data['internal_index'][x]["gamelist"] )
                # 那 第二层呢 ，暂没用到


        # 压缩包，图片，是否使用 zip
        if int(self.ini_data["extra_image_usezip"]) == 0:
            self.extra_image_usezip.set(0)  # 此变量在 ui_extra 中定义
        else:
            self.extra_image_usezip.set(1)
            
        if int(self.ini_data["extra_image_usezip_2"]) == 0:
            self.extra_image_usezip_2.set(0)  # 此变量在 ui_extra 中定义
        else:
            self.extra_image_usezip_2.set(1)            
            
        # font
        self.font_name_remember = None
        if self.ini_data["font"] in tkfont.families():
            self.font_name_remember = self.ini_data["font"]
            
        self.font_size_remember = 0
        if self.ini_data["font_size"] > 0:
            self.font_size_remember = self.ini_data["font_size"]

        self.row_height_remember = 0
        if self.ini_data["row_height"] >0:
            self.row_height_remember = self.ini_data["row_height"]        
    # 背景色，初始化，主函数 调用
    def ui_initial_functions_background(self):
    
        c1 = self.ini_data["colour_bg"]
        c2 = self.ini_data["colour_panedwindow_bg"]
                
        self.style.configure('.', background=c1) 
        self.style.configure('.', fieldbackground=c1) 

        self.style.configure('Treeview', background=c1) 
        self.style.configure('Treeview', fieldbackground =c1)   
            # 在 部分主题里有用
        self.style.configure('Treeview.Heading', background=c1,) 
            # 部分主题里 有效 

        self.style.configure('TPanedwindow', background=c2) 
        #style.configure('TPanedwindow.Sash ', background='black') 
        #style.configure('TPanedwindow.Sash ', handlesize =200) 
        #style.configure('TPanedwindow.Sash ', sashthickness =200) 

        # ??????
        #style.configure('TEntry', background='grey50') 
        self.style.configure('TEntry', fieldbackground=c1) 
        #style.configure('TEntry', lightcolor ='grey50') 
        #style.configure('TEntry', selectbackground  ='grey50') 

        self.style.configure('TCombobox', fieldbackground =c1)
        self.style.configure('TCombobox', padding=(1,1))
        self.style.map('TCombobox', fieldbackground=[('readonly','c1')])  
            ####
            # 因为设置了 readonly ???
        #self.style.configure('TCombobox', background =c1) 


        self.style.configure('TNotebook', background =c1) 
        self.style.configure('TNotebook.Tab', background =c1) 
        #self.style.configure('Tab', bordercolor  =c1) 
        
        # tk.Canvas 
        # self.extra_image  
        self.extra_image["background"]  =c1
        self.extra_image_2["background"]=c1
        
        # tk.Text
        # self.extra_text 
        self.extra_text["background"]=c1
        self.extra_command_text["background"]=c1

        # tk.Toplevle
        self.parent.option_add('*Toplevel*background', c1)
        self.parent.option_add('*Listbox*background', c1)
    # 字体，初始化，主函数调用
    def ui_initial_functions_font_init(self):
        # self.font_set( font=self.font_name_remember , 
        #                 font_size=self.font_size_remember ,
        #                 row_height=self.row_height_remember, )
        
        
        # 行高
        row_height = self.ini_data["row_height"]
        if row_height > 0:
            self.style.configure( 'Treeview', rowheight = row_height )
        
        ###
        
        def get_font(font_name,font_size):
        
            if type(font_size)!= int:
                font_size=int(font_size)
        
            if font_name not in tkfont.families() : font_name = None
            
            # if font_name == "" : font_name = None
            
            temp=None
            
            if font_name == None:# 字体没设置
                if font_size==0: # 字体大小，没设置，不管
                    temp=None
                else:# 字体大小，设置了
                    temp_font_name = None
                    temp_font_size = font_size
                    temp = (temp_font_name,temp_font_size)
            else:# 字体设置了
                if font_size==0:# 但，字体大小 没设置
                    temp_font_name = font_name
                    temp = (temp_font_name,)
                else:# 都设置了
                    temp_font_name = font_name
                    temp_font_size = font_size
                    temp = (temp_font_name,temp_font_size) 
            
            return temp

        # treeview 字体
        temp_font = None
        font_name = self.ini_data["gamelist_font"] 
        font_size = self.ini_data["gamelist_font_size"]
        
        temp_font = get_font(font_name,font_size)
        
        if temp_font != None :
            self.style.configure('Treeview', font=temp_font)
        
        # 文档字体
        temp_font = None
        font_name = self.ini_data["text_font"] 
        font_size = self.ini_data["text_font_size"]
        
        temp_font = get_font(font_name,font_size)
        
        if temp_font != None :
            self.extra_text.configure(font=temp_font)

        # 文档2 字体
        temp_font = None
        font_name = self.ini_data["text_2_font"] 
        font_size = self.ini_data["text_2_font_size"]
        
        temp_font = get_font(font_name,font_size)
        
        if temp_font != None :
            self.extra_command_text.configure(font=temp_font)
        
        # 其它 字体
        temp_font = None
        font_name = self.ini_data["others_font"] 
        font_size = self.ini_data["others_font_size"]
        
        temp_font = get_font(font_name,font_size)
        
        if temp_font != None :
            #self.style.configure('.', font=temp_font)
            self.style.configure('TLabel', font=temp_font)
            self.style.configure('TButton', font=temp_font)
            #self.style.configure('TEntry', font=temp_font)
            self.style.configure('TCheckbutton', font=temp_font)
            self.style.configure('TCombobox', font=temp_font)            
            self.style.configure('TNotebook', font=temp_font)
            self.style.configure('TNotebook.Tab', font=temp_font)
            
            self.top_entry_search.configure(font=temp_font)
                    
            self.parent.option_add("*TCombobox*Listbox.font", temp_font)
            self.parent.option_add("*font", temp_font)

            # combobox
            def ttk_combobox_font_set(a_widget,font):
                for x in a_widget.winfo_children():
                    if type(x) == type( ttk.Combobox() ):
                        x.configure(font=font)
                    
                    elif type(x) == type( ttk.Frame() ):
                        ttk_combobox_font_set(x,font)
                    
                    elif type(x) == type( ttk.PanedWindow() ):
                        ttk_combobox_font_set(x,font)
                                
            ttk_combobox_font_set( self.notebook , temp_font)
            
            # menu
            def tk_menu_font_set(a_widget,font):
                for x in a_widget.winfo_children():
                    if type(x) == type( tk.Menu() ):
                        x.configure(font=font)
                        
            tk_menu_font_set(self.menu_bar,temp_font)
            
            #self.menu_bar.configure(font=temp_font)
            self.menu_mouse_index.configure(font=temp_font)
            self.menu_mouse.configure(font=temp_font)
            self.gamelist_pop_up_menu_of_heading.configure(font=temp_font)            

    # 目录，初始化，内部 目录
    def ui_initial_functions_index_content_internal(self ):
    
        translation = self.data_from_main["index_translation"]
        index_order = self.data_from_main["index_order"]
        
        # 内部 set
        # 内部 list
        sets_data = self.data["set_data"]
        list_data = self.data["internal_index"]
        
        # sets_data
        for x in index_order:
            if x in sets_data:
                if x in translation:
                    self.tree_index.insert('','end',iid=x ,text = translation[x] ,) 
                    self.tree_index.set(x,column='type',value='internal_set')
                else:
                    self.tree_index.insert('','end',iid=x ,text = x ,)
                    self.tree_index.set(x,column='type',value='internal_set')
        
        # list_data
        # 第一层 
        for x in index_order:
            if x in list_data:
                if x in translation:
                    self.tree_index.insert('','end',iid=x ,text = translation[x] ,) 
                    self.tree_index.set(x,column='type',value='internal_list')
                else:
                    self.tree_index.insert('','end',iid=x ,text = x ,)
                    self.tree_index.set(x,column='type',value='internal_list')
        # list_data
        #第二层
        #   id 为：第一层名|第二层名
        for x in index_order:
            if x in list_data:
                for y in sorted( list_data[x]["children"]):
                    id_string = x + "|" + y
                    self.tree_index.insert(x,'end',iid=id_string ,text = y ,) 
                    self.tree_index.set(id_string,column='type',value='internal_list')

    # 目录，初始化，外部 文件
    def ui_initial_functions_index_content_external(self,):
    
        time1 = time.time()
    
        # folders_read.read_folder_ini
        # folders_read.read_folder_ini_2
        # 一开始用的 set 格式，比较浪费空间，转为 list
    
        # self.ini_data
        
        folders_path = self.ini_data["folders_path"]
        
        # 去掉 双引号，单引号
        folders_path = folders_path.replace(r"'","")
        folders_path = folders_path.replace(r'"',"")
        
        # import folders_read
        # import folders_search
        
        # 分类列表文件  
        ini_files = {} # 初始化
            # keys,为 （相对/绝对）路径 + 文件名 ，
            # values ，为 文件名，不含路径
        # 分类列表，具体信息
        ini_set_dict = {} # 初始化
            # keys,为 （相对/绝对）路径 + 文件名 ，
            # values ，为 为一个 {}
                # keys,为子分类名，
                # values,为，分类游戏，集合 ,后来 转为 list 格式了
        # 查找 文件
        for x in folders_path.split(';') :
            ini_files.update( folders_search.search_ini( x ) )
            
        # 计算分类列表 具体信息
        for x in ini_files:
            temp = folders_read.read_folder_ini_3(x) ## 
            if temp==None:
                # 格式错误，只检查了个别错误
                pass
            else: 
                ini_set_dict[x] = {} # 初始化
                ini_set_dict[x] = temp  
            
        # 添加到 目录
        # 第一层
        for x in sorted( ini_set_dict.keys()):
            # x 为 路径 + 名称
            # ini_files[x] 为 名称，无路径
            self.tree_index.insert('','end',iid=x,text=ini_files[x],values=("file",x ) )
        
        #第二层
            # iid 分隔符 原来用 分号；
            #   改掉，
            #       因为 ； 本来就可以作为 文件名、文件夹名
            #       不用 \ ，这个是分隔符 ，文件夹名\文件名
            #       不用 / ，这个是 linux 分隔符， 文件夹名/文件名
            #       不用 ： 因为盘符是冒号， d:\xxx\yyy
            #
            #  / \ : * " < > | ? 
            # 用 | 

            for y in sorted( ini_set_dict[x] ) :
                if y != "FOLDER_SETTINGS":
                    if y != "ROOT_FOLDER":
                        iid_string = x + r"|" + y
                        self.tree_index.insert(x,'end',iid = iid_string,text=y,values=("file",))

        self.ini_set_dict = ini_set_dict
        self.ini_files = ini_files
        
        self.ini_files_editable = set()
        # 找出 .ini 外部目录文件，哪些是 可写的
        for x in ini_set_dict:
            if os.access(x,os.W_OK):
                self.ini_files_editable.add(x)
                # print(x)

        time2 = time.time()
        print()
        print("外部目录，初始化时间")
        print(time2-time1)
        print()

    # 目录宽度 、周边宽度,初始化
    def ui_initial_functions_ui_width_initial(self):
    
        # Panedwindow 分隔线定位
        # 程序一开始，ui 没有显示出来，定位不准
        # 需要 ui 显示好 .wait_visibility ???  .update ????
        # .update

        self.parent.update()
        
        # 主视图，目录 分隔条 位置
        self.frame_middle.sashpos(0,self.ini_data["pos1"])
        # 主视图，周边 分隔条 位置
        self.frame_middle.sashpos(1,self.ini_data["pos2"])
        # 周边视图，图片 分隔条 位置
        self.extra_image_panedwindow.sashpos(0,self.ini_data["pos3"])
    
    # 周边，根据记录选择上次 显示的项目
    def ui_initial_functions_ui_extra_show_the_remembered_part(self):
        try:
            self.notebook.select( self.ini_data["extra_tab_index"] )
        except:
            pass


    ########

    # bindings
    
    # bindings: top ，button ，切换 1/2/3
    def top_binding_gamelist_change(self,event):
        
        # self.gamelist_change_mark
        # gamelist_pop_up_menu_of_heading_choose_columns 函数中，也用了一下
        
        def get_columns(old_columns): # 检查多余项目
            temp_list = []
            for x in old_columns:
                if x in self.tree["columns"]:
                    temp_list.append(x)
            new_columns = tuple( temp_list )
            return new_columns
        
        # 初始化
        try:
            self.gamelist_change_mark
        except:
            self.gamelist_change_mark = 1
        
        self.gamelist_change_mark += 1
        
        if self.gamelist_change_mark > 3:
            self.gamelist_change_mark %= 3 # 求余数
        
        if self.gamelist_change_mark == 1:
            self.tree.configure( displaycolumns = get_columns(self.ini_data["gamelist_columns_to_show_1"]) )
        elif self.gamelist_change_mark == 2:
            self.tree.configure( displaycolumns = get_columns(self.ini_data["gamelist_columns_to_show_2"]) )
        elif self.gamelist_change_mark == 3:
            self.tree.configure( displaycolumns = get_columns(self.ini_data["gamelist_columns"]) )

    # bindings: top ,button ，分组／不分组
    def top_binding_change_group(self,event):

        self.ini_data["gamelist_group_mark"] = not self.ini_data["gamelist_group_mark"]
            
        # 重新显示：
        self.gamelist_show( self.index_set_remembered  )

    # bindings: top ,button ，定位到
    def top_binding_see_the_game(self,event):
        temp_str = self.top_game_name.get()
        if temp_str == '':
            pass
        else:
            print(temp_str)
            try:
                self.tree.see(temp_str)
                self.tree.selection_set(temp_str)
                self.tree.focus(temp_str)               
            except:
                pass

    # bindings: top ,button ,搜索
    def top_binding_search(self,event):
        
        temp_str = self.top_search_content.get()
        
        if len( temp_str) > 0 :
        
            # 搜索范围
            # 外部目录，有可能有超出范围的内容
            if type(self.index_set_remembered) == set:
                search_set = self.index_set_remembered & self.data['set_data']['all_set']
            elif type(self.index_set_remembered)  == list:
                search_set = set( self.index_set_remembered ) & self.data['set_data']['all_set']

            temp_str = temp_str.lower() # 大小写转换
            self.search_mark = True # 标记
            temp_set = set()  # 搜索结果记录
            
            for x in search_set:
                # 图标列，内容移除了，只留下了图标
                # if temp_str in x : # 本身全是小写
                #     temp_set.add(x)
                #     continue
                for y in self.tree.item(x,"values"): 
                    if temp_str in y.lower() :# 大小写转换
                        temp_set.add(x)
                        break
            
            self.gamelist_show(temp_set)
            
        else:
            # 空字符，不用搜
            pass
        
    # bindings: top ,button ,正则搜索
    def top_binding_search_re(self,event):
        
        temp_str = self.top_search_content.get()
                
        if len( temp_str) > 0 :
            # 搜索范围
            # 外部目录，有可能有超出范围的内容
            if type(self.index_set_remembered) == set:
                search_set = self.index_set_remembered & self.data['set_data']['all_set']
            elif type(self.index_set_remembered)  == list:
                search_set = set( self.index_set_remembered ) & self.data['set_data']['all_set']
        
            p=re.compile(temp_str,re.IGNORECASE)
            
            self.search_mark = True # 标记
            temp_set = set()  # 搜索结果记录
            
            for x in search_set:
                # 图标列，内容移除了，只留下了图标
                # if p.search(x):
                #     temp_set.add(x)
                #     continue
                for y in self.tree.item(x,"values"): 
                    if p.search(y):
                        temp_set.add(x)
                        break
            
            self.gamelist_show(temp_set)
        else:
            # 空字符，不用搜
            pass    

    # bindings: top ,button ，清除 搜索栏 显示的内容
    def top_binding_search_clear(self,event):
        if self.search_mark == True:
            self.search_mark == False
            self.top_search_content.set("")
            self.gamelist_show( self.index_set_remembered ) 
        else:
            self.top_search_content.set("")


    # 目录
    
    # bindings: 目录 鼠标 滚轮 ，列表 滚动 行数
    def index_binding_mousewheel(self,event):
            if event.delta > 0:
                self.tree_index.yview(tk.SCROLL,-3,"units" )
            else:
                self.tree_index.yview(tk.SCROLL,3,"units" )
            return "break"   
    
    # bindings: 目录 ，点击 目录 ，切换列表显示内容
    def index_binding_choose_index_by_click(self,event):
        #me     = self.tree_index.focus()
            # get iid # 速度太慢 ? ，得到的是上一次的选中的行？？？
        row    = self.tree_index.identify_row(event.y)
        region = self.tree_index.identify_region(event.x,event.y)
    
        # 点击到 标题行
        if row=='':
            pass
        
        # 点击到 标题行
        elif region=="heading" :
            # 列表 下拉时
            # 标题栏挡住一行 内容
            # 此时，.identify_row(event.y) 仍能，标题栏后的一行的 iid
            # 需排除
            pass
        
        else:
            self.choose_index(row)

    # bindings: 目录 ，目录 中 按回车键，切换列表显示内容
    def index_binding_choose_index_by_press_return(self,event):
        row = self.tree_index.focus()
        if row != "":
            self.choose_index(row)
        return "break" # 默认有列表展开 功能 ，关掉

    def index_binding_key_press_right(self,event):
        tree = self.tree_index
        
        row = tree.focus()
        if row:  
            for x in tree.get_children(row):
                temp = tree.item(row,"open")
                if temp:
                    pass
                else:
                    temp = True
                    tree.item(row,open=temp )
                break
        return "break"    

    # bindings: 目录 ，鼠标 右键 菜单
    def index_binding_menu_popup(self,event):
        row    = self.tree_index.identify_row(event.y)# gei iid
        region = self.tree_index.identify_region(event.x,event.y)
            # 'nothing'、 'heading' 、'separator' 、'tree' 、'cell'
        
        if region=="heading" : # 右键，点击到 标题栏
            pass
        else:
            if row != "": # 非空
                print(row)
                
                try:
                    self.menu_mouse_index.tk_popup(event.x_root, event.y_root)
                finally:
                    self.menu_mouse_index.grab_release()          


    # 游戏列表
    
    # bindings: 游戏列表
    #   1 点击 标题 ，排序
    #   2 点击到图标列 ， 有克隆版本的，展开／关闭 子列表
    def gamelist_binding_click_heading(self, event ):
        row = self.tree.identify_row(event.y)# gei iid
        region = self.tree.identify_region(event.x,event.y)
            # 'nothing'、 'heading' 、'separator' 、'tree' 、'cell'
        #test = self.tree.identify_element(event.x,event.y) 
        column = self.tree.identify_column(event.x) # '#0' '#1' '#2' ……

        print()
        print("region")
        print(region)
        #print(test)
        print(row)
        
        if region=="heading" : # 1 点击 标题 ，排序
        
            if column == '#0': # 图标列，不用管
                return 0
            
            # 列表 下拉时
            # 标题栏挡住一行 内容
            # 此时，.identify_row(event.y) 仍能，标题栏后的一行的 iid
            # 需排除
            
            
            # 列标题 不是唯一的，而且也不能用来提取元素
            # column_heading = self.tree.heading(column,"text")
            
            # 需要用 列 id 
            column_id = self.tree.column(column,"id")
            
            if self.ini_data["gamelist_sorted_by"] == column_id:
                # 第二次 点击 同一个 标题，正序/倒序 切换
                self.ini_data["gamelist_sorted_reverse"] = not self.ini_data["gamelist_sorted_reverse"] 
            else:
                self.ini_data["gamelist_sorted_by"]  = column_id
                self.ini_data["gamelist_sorted_reverse"] = False # 第一次点击，确保是 正序
            
            print("排序标记\t"+column_id)
            print("顺序、倒序\t"+ str(self.ini_data["gamelist_sorted_reverse"]))
            
            self.gamelist_show( self.index_set_remembered  )
        else:
            if region=="tree": # 2 点击 图标列 ，展开，收起
                temp = self.tree.item(row,"open")
                
                if temp: 
                    # 如果是展开的，收起
                    temp = False
                else:  
                    # 如果是收起的，
                    # 如果 下一级 有内容，才，展开
                    for x in self.tree.get_children(row):
                        temp = True
                        break
                
                self.tree.item(row,open=temp )
                
                self.tree.selection_set(row)
                self.tree.focus(row)
                self.tree.see(row)
                
                return "break"    
    
    # bindings: 游戏列表 ，
    #   选择内容变化时，切换 状态栏、周边内容 的显示
    def gamelist_binding_selection_change(self,event ) :

        #row = tree.identify_row(event.y)
        me = self.tree.focus()
        print(me)
            
        if len(self.tree.selection()) >1 :
            return 0
       
        self.top_game_name.set(me)
        
        temp = r'|| ' 
        temp += me 
        if me in self.data['dict_data']['clone_to_parent'] :
            # 如果 me 为克版版本
            # 主版本为：self.data['dict_data']['clone_to_parent'][me]
            temp += r' .. '
            temp += '主版：' + self.data['dict_data']['clone_to_parent'][me]
        
        # romof
        try:
            status_string = self.data['dict_data']['romof'][me]
            if status_string:
                temp += r' .. '
                temp += "romof："
                temp += status_string
        except:
            pass        
        
        # 模拟状态
        try:
            status_string = self.tree.set(me, "status",)
            if status_string:
                temp += r' .. '
                temp += "模拟状态："
                temp += status_string
        except:
            pass
        
        # 存储状态
        try:
            status_string = self.tree.set(me, "savestate",)
            if status_string:
                temp += r' .. '
                temp += "存储状态："
                temp += status_string
        except:
            pass
        
        
        
        self.status_bar_text.set(temp)
        self.show_extra(me)

    # bindings: 游戏列表     鼠标 滚轮 ，列表 滚动 行数
    def gamelist_binding_mousewheel(self,event):
            # window 有效，
            # 按照，说明，linux ，方法不同
            if event.delta > 0:
                self.tree.yview(tk.SCROLL,-3,"units" )
            else:
                self.tree.yview(tk.SCROLL,3,"units" )
            return "break"

    # bindings: 游戏列表 ，  打开 MAME ,鼠标双击
    def gamelist_binding_start_game_by_double_click(self,event):
        
        # game_name
        row =    self.tree.identify_row(event.y)# gei iid
        
        region = self.tree.identify_region(event.x,event.y)
            # 'nothing'、 'heading' 、'separator' 、'tree' 、'cell'

        if row=='':
            pass
        elif region=="heading" :
            pass
        else:
            self.call_mame( row )
            
        return "break"

    # bindings: 游戏列表 ，  打开 MAME ,回车键
    def gamelist_binding_start_game_by_press_return(self,event):
                
        game_name = self.tree.focus()
        
        if game_name == "":
            pass
        else:
            self.call_mame(game_name)
            
        return "break"

    # bindings: 游戏列表 ，ctrl + A/a ,全选，
    def gamelist_binding_select_all(self,event):
        if self.menu_mouse_multi_select_mode_flag.get():
            temp = []
            for x in self.tree.get_children():
                temp.append(x)
                for y in self.tree.get_children(x):
                    temp.append(y)
            self.tree.selection_add(temp)
            del temp
    # bindings: 游戏列表 ，按“→”键。
    #   原始的 bind ，没有子项目也展开，有些主题会显示展开符号
    def gamelist_binding_key_press_right(self,event):
        tree = self.tree
        
        row = tree.focus()
        if row:  
            for x in tree.get_children(row):
                temp = tree.item(row,"open")
                if temp:
                    pass
                else:
                    temp = True
                    tree.item(row,open=temp )
                break
        return "break"
    # bindings: 游戏列表 ，按空格键
    #   原始的 bind ，展开、收起。没有子项目也展开，有些主题会显示展开符号
    def gamelist_binding_key_press_space(self,event=None,tree=None):
        # 两用
        # tree = self.tree
        # tree = self.tree_index
        
        print("space")
        
        row = tree.focus()
        
        if row:
            if tree.item(row,"open"):
                # 是展开状态
                # 需要收起
                tree.item(row,open=False)
            else:
                # 是收起状态
                # 需要展开
                for x in tree.get_children(row):
                    tree.item(row,open=True)
                    break
                    
        return "break"

    # bindings: 游戏列表 ，鼠击右键 弹出 菜单
    def gamelist_binding_menu_popup(self,event):
        row = self.tree.identify_row(event.y)# gei iid
        region = self.tree.identify_region(event.x,event.y)
            # 'nothing'、 'heading' 、'separator' 、'tree' 、'cell'
        
        if region=="heading" : # 右键，点击到 标题栏
            try:
                self.gamelist_pop_up_menu_of_heading.tk_popup(event.x_root, event.y_root)
            finally:
                self.gamelist_pop_up_menu_of_heading.grab_release()   
        else:
            if row != "": # 非空
                print(row)
                #self.tree.selection_set(row)
                #self.tree.focus(row)
                
                if self.menu_index_edit_flag.get(): # 目录，可编辑状态
                
                    # ui_gamelist_pop_up_menu 函数
                        # self.menu_mouse_index_number_1 移除
                        # self.menu_mouse_index_number_2 添加
                    self.menu_mouse.entryconfig( self.menu_mouse_index_number_2 , state="normal")
                    
                    flag = False # 标记，所在文件 是否可编辑
                    index_id = self.ini_data["index_be_chosen"]
                    
                    if self.tree_index.set( index_id ,"type") == "internal":#内部分类
                        flag = False
                    else:# 外部分类
                        ini_file_path = index_id.split(r"|",1)[0]
                        if ini_file_path in self.ini_files_editable:
                            flag = True
                            text = self.tree_index.item( index_id ,"text")
                            
                    if flag:# 目录所在条目，可编辑
                        new_label = "目录修改：从自定义目录移除："+text+r"( "+ ini_file_path +r" )"
                        self.menu_mouse.entryconfig( self.menu_mouse_index_number_1 , state="normal",label = new_label)
                    else:# 目录所在条目，不可编辑
                        self.menu_mouse.entryconfig( self.menu_mouse_index_number_1 , state="disabled",label = "目录修改：从 自定义目录 移除")
                    
                else:# 目录，不可编辑状态
                    self.menu_mouse.entryconfig( self.menu_mouse_index_number_1 , state="disabled",label = "目录修改：从 自定义目录 移除")
                    self.menu_mouse.entryconfig( self.menu_mouse_index_number_2 , state="disabled",)
                
                if row in self.tree.selection(): # row 在 已选项目 中
                    # 鼠标 右键 菜单
                    try:
                        self.menu_mouse.tk_popup(event.x_root, event.y_root)
                    finally:
                        self.menu_mouse.grab_release()
                else: # row 不在 已选项目 中
                    # 选中 鼠标 右击 项目
                    self.tree.selection_set(row)
                    self.tree.focus(row)
                    # 弹出 鼠标 右键 菜单
                    try:
                        self.menu_mouse.tk_popup(event.x_root, event.y_root)
                    finally:
                        self.menu_mouse.grab_release()                    

    # extra
    
    # bindings: extra ，# 周边 ，切换显示内容，刷新显示
    def extra_binding_notebook_tab_changed(self,event):
        game_name = self.tree.focus()
            
        if game_name != "":
            self.show_extra(game_name)
        else:
            pass
        
    # bindings: extra ，# 拉伸时，图片大小也变化
    def extra_binding_image_change_size(self,event):
    
        try:
            self.image_original
        except:
            return 0
    
        canvas_size=(event.width,event.height)
        
        # def image_get_new_size(self , image_size , canvas_size)
        new_size = self.image_get_new_size( self.size_original ,canvas_size )
        
        if self.extra_image.winfo_viewable():
        
            if new_size:
            
                self.image = ImageTk.PhotoImage(self.image_original.resize( new_size,Image.BILINEAR, ))
                
                self.extra_image.create_image(
                            int(canvas_size[0]/2),
                            int(canvas_size[1]/2), 
                            image=self.image , 
                            anchor=tk.CENTER)

    def extra_binding_image_change_size_2(self,event):

        try:
            self.image_original_2
        except:
            return 0

        canvas_size=(event.width,event.height)
        
        # def image_get_new_size(self , image_size , canvas_size)
        new_size = self.image_get_new_size( self.size_original_2 ,canvas_size )
        
        if self.extra_image_2.winfo_viewable():
        
            if new_size:
            
                self.image_2 = ImageTk.PhotoImage(self.image_original_2.resize( new_size,Image.BILINEAR, ))
                
                self.extra_image_2.create_image(
                            int(canvas_size[0]/2),
                            int(canvas_size[1]/2), 
                            image=self.image_2 , 
                            anchor=tk.CENTER)                            

    # bindings: extra ，ui 中选择，显示哪一种图片
    # 复用，文本类，也一样用
    def extra_binding_image_type_choose(self,event):

        game_name = self.tree.focus()
        
        if game_name != "":
            self.show_extra(game_name)
        else:
            pass

    # bindings: extra，    出招表 的 目录，选择
    def extra_binding_command_index_choose(self,event):
        
        # self.command_content
        # 有关的函数 show_command
    
        try:
            self.command_content
        except:
            self.extra_command_text.delete('1.0',tk.END) 
            # 清空内容
            
            return 0 
            # 如果还没有 数据 记录
            # 退出函数
        
        if self.command_content is None:
            self.extra_command_text.delete('1.0',tk.END) 
            # 清空内容
            
            return 0 
            # 退出函数
        
        
        n = self.extra_command_chooser.current()
        
        if n==0:
            self.extra_command_text.delete('1.0',tk.END)
            try:
                for x in self.command_content:
                    for y in self.command_content[x]:
                        self.extra_command_text.insert(tk.INSERT, y)
            except:
                pass
        else:
            self.extra_command_text.delete('1.0',tk.END)
            try:
                for x in self.command_content[n]:
                    self.extra_command_text.insert(tk.INSERT, x)
            except:
                pass
    

    # callback 函数
    # 菜单 callback 函数
    
    # callback 函数,菜单 ,do nothing ，
    def donothing(self,event=None):
        print("do nothing") 

    # 菜单 callback 函数：UI→切换主题
    # a topleve window 
    def menu_call_back_function_change_theme(self,):
        print("chage the theme")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("选择主题")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        window.geometry( size )
             
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        window.columnconfigure(0,weight=1)
        window.rowconfigure(0,weight=1)
        
        def for_ok_button_1():
            index = chooser_1.current()
            print(index)
            if index == -1 :
                pass
            else:
                the_theme =  theme_names_1[index]
                self.ini_data["theme"] =  the_theme
                window.destroy()
                print( the_theme )
        
        def for_ok_button_2():
            index = chooser_2.current()
            print(index)
            if index == -1 :
                pass
            else:
                the_theme =  theme_names_2[index]
                print( the_theme )
                self.ini_data["theme"] =  the_theme
                window.destroy()
        
        notebook = ttk.Notebook( window,)
        notebook.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        
        #button_ok = ttk.Button( window ,text="确认",command=for_ok_button)
        #button_ok.grid(row=0,column=0,sticky=tk.E,)
        
        # 当前使用的主题为xxxx，设置中的主题为xxxx(关闭程序，重新打开后生效)
        temp_string  = "当前使用的主题为："
        temp_string += self.style.theme_use() # 当前使用的主题
        temp_string += "\n"
        temp_string += "设置中的主题为："
        temp_string += self.ini_data["theme"]
        temp_string += "\n"
        temp_string += " (关闭程序，重新打开后生效)"
        
        # 1
            # 内置主题
        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text='使用内置主题',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        ttk.Label(frame1,text=temp_string,).grid(row=0,column=0,sticky=tk.N+tk.W,)
        ttk.Label(frame1,text="",).grid(row=1,column=0,sticky=tk.N+tk.W,)
        ttk.Label(frame1,text="选择内置主题：",).grid(row=2,column=0,sticky=tk.N+tk.W,)
        
        chooser_1 = ttk.Combobox(frame1,state="readonly" )
        chooser_1.grid(row=3,column=0,sticky=tk.N+tk.W,)
        
        button_ok_1 = ttk.Button( frame1 ,text="确认",command=for_ok_button_1)
        button_ok_1.grid(row=4,column=0,sticky=tk.E,)
        
        # self.data_from_main["internal_themes"]
        theme_names_1 = list( self.data_from_main["internal_themes"] )
        theme_names_1 = sorted( theme_names_1 )
        
        chooser_1["values"]= theme_names_1
        

        
        # 2
            # 外置主题
        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text='使用第三方主题',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        ttk.Label(frame2,text=temp_string,).grid(row=0,column=0,sticky=tk.N+tk.W,)
        ttk.Label(frame2,text="",).grid(row=1,column=0,sticky=tk.N+tk.W,)        
        ttk.Label(frame2,text="选择第三方主题（需要下载第三方主题文件）：",).grid(row=2,column=0,sticky=tk.N+tk.W,)

        chooser_2 = ttk.Combobox(frame2,state="readonly" )
        chooser_2.grid(row=3,column=0,sticky=tk.N+tk.W,)
        
        button_ok_2 = ttk.Button( frame2 ,text="确认",command=for_ok_button_2)
        button_ok_2.grid(row=4,column=0,sticky=tk.E,)
        
        # self.data_from_main["internal_themes"]
        theme_names_2 = list( self.data_from_main["other_themes"] )
        theme_names_2 = sorted( theme_names_2 )
        
        chooser_2["values"]= theme_names_2
        
        
        
        window.wait_window()
        
    # 菜单 callback 函数：UI→路径设置
    # a topleve window 
    def menu_call_back_function_set_file_path(self,):
    
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("路径设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        size = temp
        window.geometry( size )
             
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        # ttk.Notebook
        # 
        # ------------------------------------------------------------
        # |1模拟器路径 | 2 folders 路径 | 3图片 | 4 图片 zip| 5 文档 |
        # |            |                |       |           |        |
        # |-----------------------------------------------------------
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # |               ttk.Notebook                               |
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # ------------------------------------------------------------
        # |                                                          |
        # |                                                 OK Button|
        # ------------------------------------------------------------
        
        # self.ini_data
        # self.image_types
        # self.text_types
        # self.text_types_2
        
        # self.menu_call_back_function_save_ini_data()
        
        # self.data_from_main
        
        data ={}
        
        def for_ok_button():

            for x in data:
                if x in self.ini_data:
                    self.ini_data[x] = data[x].get()
                else:
                    print(x)
                    print("a wrong key")
            
            self.menu_call_back_function_save_ini_data()
            
            window.destroy()
        
        def choose_folder(v):
            # v is tk.StringVar()
            folder_path = tkinter.filedialog.askdirectory( initialdir="." )
            if folder_path=="":
                window.focus_set()
                return 0
            
            folder_path = os.path.abspath( folder_path ) # 统一格式，不然  / \ 混乱
            
            v.set( folder_path )
            window.focus_set()
        
        def add_folder(v):
            # v is tk.StringVar()
            folder_path = tkinter.filedialog.askdirectory( initialdir="." )
            if folder_path=="":
                window.focus_set()
                return 0
            
            folder_path = os.path.abspath( folder_path ) # 统一格式，不然  / \ 混乱
            
            temp=v.get()
            temp += ";" + folder_path
            v.set( temp )
            window.focus_set()
            
        def choose_zip_file(v):
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[("zip压缩包","*.zip"),],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            v.set( file_path )
            window.focus_set()
        
        def choose_dat_file(v):
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[("文档.dat","*.dat"),],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            v.set( file_path )
            window.focus_set()
        
        def choose_xml_file(v):
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[("历史文档.xml","*.xml"),],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            v.set( file_path )
            window.focus_set()
        
        def set_default_value(tk_var,temp_string):
            # self.data_from_main["ini_default"]
                # temp_string 是 key 值
                # tk_var 是前边定义 data 中的 data[temp_string]
            if temp_string in self.data_from_main["ini_default"]:
                tk_var.set( self.data_from_main["ini_default"][temp_string] )
            
        

        
        window.columnconfigure(0,weight=1)
        window.rowconfigure(0,weight=1)  
        window.rowconfigure(1,weight=0)  
        
        frame_0 = ttk.Frame(window,) # for notebook
        frame_0.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame_1 = ttk.Frame(window,) # for OK_button
        frame_1.grid(row=1,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame_0.columnconfigure(0,weight=1)
        frame_0.rowconfigure(0,weight=1)
        frame_1.columnconfigure(0,weight=1)
        frame_1.rowconfigure(0,weight=1)
        
        notebook = ttk.Notebook( frame_0,)
        notebook.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        
        button_ok = ttk.Button( frame_1 ,text="确认",command=for_ok_button)
        button_ok.grid(row=0,column=0,sticky=tk.E,)
        
        
        # 1
        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text='模拟器路径',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame1.columnconfigure(1,weight=1)
        
        def change_mame_path():
            entry_mame_path.configure( state="normal" )
            button_mame_default.configure( state="normal" )
            button_mame_chooser.configure( state="normal" )
        def change_mame_working_directory():
            entry_mame_working_directory.configure( state="normal" )
            button_mame_working_directory_default.configure( state="normal" )
            
        def choose_mame_file():
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[(".exe","*.exe"),("所有","*")],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            data["mame_path"].set( file_path )
            window.focus_set()
        
        # mame
        ttk.Label(frame1,text="mame 模拟器 路径").grid(row=0,column=0,sticky=tk.W+tk.N,)
        
        data["mame_path"]=tk.StringVar()
        entry_mame_path = ttk.Entry(frame1,textvariable=data["mame_path"],state="disabled")
        entry_mame_path.grid(row=0,column=1,sticky=tk.W+tk.N+tk.E,)
        data["mame_path"].set( self.ini_data["mame_path"] )
        
        button_mame_default = ttk.Button(frame1,text=r"默认值",width=-1,state="disabled",command=lambda a=data["mame_path"],b="mame_path" : set_default_value(a,b),)
        button_mame_default.grid(row=0,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame1,text=r"修改",width=-1,command=change_mame_path ).grid(row=0,column=3,sticky=tk.W+tk.N,)
        
        button_mame_chooser = ttk.Button(frame1,text=r"选择",width=-1,state="disabled",command=choose_mame_file)
        button_mame_chooser.grid(row=0,column=4,sticky=tk.W+tk.N,)
        # mame_working_directory
        ttk.Label(frame1,text="mame 工作目录").grid(row=1,column=0,sticky=tk.W+tk.N,)
        
        data["mame_working_directory"] = tk.StringVar()
        entry_mame_working_directory = ttk.Entry(frame1,textvariable=data["mame_working_directory"],state="disabled",)
        entry_mame_working_directory.grid(row=1,column=1,sticky=tk.W+tk.N+tk.E,)
        data["mame_working_directory"].set( self.ini_data["mame_working_directory"] )
        
        button_mame_working_directory_default=ttk.Button(frame1,text=r"默认值",width=-1,state="disabled",command=lambda a=data["mame_working_directory"],b="mame_working_directory" : set_default_value(a,b),)
        button_mame_working_directory_default.grid(row=1,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame1,text=r"修改",width=-1,command=change_mame_working_directory ).grid(row=1,column=3,sticky=tk.W+tk.N,)        
        
        n=2
        
        ttk.Label(frame1,text="").grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
        n+=1        
        
        the_dir = os.getcwd()
        the_dir = os.path.abspath( the_dir )
        
        the_temp_text  = "windows 操作系统上，MAME 都是解压就可以使用的；\n"
        the_temp_text += "因为，位置没有固定，所以默认的设置里各种路径用的是相对路径。\n"
        the_temp_text += "所以，也需要在 MAME 所在的文件夹，打开 MAME 。\n"
        the_temp_text += "第一项，填模拟器程序具体的路径，相对或者绝对路径。\n"
        the_temp_text += "（相对路径:相对于 UI 主脚本所在的文件夹）\n" 
        the_temp_text += "UI 根据你填写的值，查找并使用模拟器。\n"
        the_temp_text += "第二项，可不填：表示模拟器所在的文件夹。\n"
        the_temp_text += "前提是：第一项，填对了。程序能找到对应的模拟器文件，自然知道它所在的文件夹。"

        ttk.Label(frame1,text=the_temp_text).grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(frame1,text="").grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
        n+=1        
        
        the_temp_text_2   = "linux 操作系统：在 虚拟机 安装 Debian 11 ，测试，似乎能运行。\n"        
        the_temp_text_2  += "(我对 linux 不了解 ，但仅仅运行一下熟悉的 MAME 还可以试试。)\n"        
        the_temp_text_2  += "mame 安装在系统相关的路径里。mame 被添加到命令行指令里了。\n"
        the_temp_text_2  += "第一项，可以填指令，比如填 mame ：脚本同文件夹下不要有同名文件，免得 误以为 你填写的是 文件名。\n"
        the_temp_text_2  += "第二项，mame 的工作路径，如需要的话，自己填一下吧。\n"        
        the_temp_text_2  += "不填的话，默认应该是在 脚本 所在 文件夹。\n"        
        the_temp_text_2  += "我看到模拟器默认设置里，路径 大数多，默认设置用的是绝对路径；\n"        
        the_temp_text_2  += "所以，这一项，似乎不是很重要的样子。\n"
        the_temp_text_2  += "不像在 windows 里：模拟器默认的路径都是用相对路径。"
   
        ttk.Label(frame1,text=the_temp_text_2).grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
        n+=1
        
        # 2
        # folder 路径
        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text='folders',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame2.columnconfigure(1,weight=1)
        
        ttk.Label(frame2,text="folders 路径").grid(row=0,column=0,sticky=tk.W+tk.N,)
        
        data["folders_path"]=tk.StringVar()
        
        ttk.Entry(frame2,textvariable=data["folders_path"],width=50).grid(row=0,column=1,sticky=tk.W+tk.N+tk.E,)
        
        data["folders_path"].set( self.ini_data["folders_path"] )
        
        ttk.Button(frame2,text=r"...",width=-1,command=lambda x=None: choose_folder(data["folders_path"])).grid(row=0,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame2,text=r" + ",width=-1,command=lambda x=None: add_folder(data["folders_path"])).grid(row=0,column=3,sticky=tk.W+tk.N,)
        
        ttk.Button(frame2,text=r"默认值",width=-1,command=lambda a=data["folders_path"],b="folders_path" : set_default_value(a,b),).grid(row=0,column=4,sticky=tk.W+tk.N,)
        
        # 3
        # 图片路径
        # self.image_types
        frame3 = ttk.Frame(notebook)
        notebook.add(frame3, text='图片路径',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame3.columnconfigure(1,weight=1)
        
        # 图片名 snap
        # 路径变量名 self.ini_data["snap_path"]
        temp = {}
            # snap:snap_path ,
        for x in self.image_types:
            temp[x] = x+"_path"
        
        n=0
        for x in self.image_types :
            ttk.Label(frame3,text=x).grid(row=n,column=0,sticky=tk.W+tk.N,)
            
            temp_str = temp[x] # snap_path
            
            data[temp_str]=tk.StringVar()
            
            ttk.Entry(frame3,textvariable=data[temp_str],width=50).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
            
            data[temp_str].set( self.ini_data[temp_str] )
            
            ttk.Button(frame3,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_folder(a)).grid(row=n,column=2,sticky=tk.W+tk.N,)

            ttk.Button(frame3,text=r" + ",width=-1,command=lambda a=data[temp_str]: add_folder(a),).grid(row=n,column=3,sticky=tk.W+tk.N,)
            
            ttk.Button(frame3,text=r"默认值",width=-1,command = lambda a=data[temp_str],b=temp_str : set_default_value(a,b),).grid(row=n,column=4,sticky=tk.W+tk.N,)
            
            n += 1
        
            
        
        # 4
        # 图片压缩包路径
        frame4 = ttk.Frame(notebook)
        notebook.add(frame4, text='图片压缩包路径',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame4.columnconfigure(1,weight=1)
        
        #图片名 snap
        #路径变量名 self.ini_data["snap.zip_path"]
        temp = {}
            # snap:snap.zip_path ,
        for x in self.image_types:
            temp[x] = x+".zip_path"
        
        n=0
        for x in self.image_types :
            ttk.Label(frame4,text=x).grid(row=n,column=0,sticky=tk.W+tk.N,)
            
            temp_str = temp[x] # snap_path
            
            data[temp_str]=tk.StringVar()
            
            ttk.Entry(frame4,textvariable=data[temp_str],width=50).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
            
            data[temp_str].set( self.ini_data[temp_str] )
            
            ttk.Button(frame4,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_zip_file(a),).grid(row=n,column=2,sticky=tk.W+tk.N,)
            
            ttk.Button(frame4,text=r"默认值",width=-1,command = lambda a=data[temp_str],b=temp_str : set_default_value(a,b),).grid(row=n,column=3,sticky=tk.W+tk.N,)
            
            n += 1
        
        # 5
        frame5 = ttk.Frame(notebook)
        notebook.add(frame5, text='文档路径',sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame5.columnconfigure(1,weight=1)
        
        # self.text_types
        # self.text_types_2
        
        temp_types=set(self.text_types) | set(self.text_types_2)
        
        temp_types = sorted(temp_types)
        
        #文档名 command.dat
        #路径变量名 self.ini_data["command.dat_path"]
        temp = {}
            # command.dat : command.dat_path ,
        for x in temp_types:
            temp[x] = x+"_path"
        
        n=0
        for x in temp_types :
            ttk.Label(frame5,text=x).grid(row=n,column=0,sticky=tk.W+tk.N,)
            
            temp_str = temp[x] # snap_path
            
            data[temp_str]=tk.StringVar()
            
            ttk.Entry(frame5,textvariable=data[temp_str],width=50).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
            
            data[temp_str].set( self.ini_data[temp_str] )
            
            if x == "history.xml": 
                # xml 格式
                ttk.Button(frame5,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_xml_file(a),).grid(row=n,column=2,sticky=tk.W+tk.N,)
            else: 
                # dat 格式
                ttk.Button(frame5,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_dat_file(a),).grid(row=n,column=2,sticky=tk.W+tk.N,)
                
            ttk.Button(frame5,text=r"默认值",width=-1,command=lambda a=data[temp_str],b=temp_str : set_default_value(a,b),).grid(row=n,column=3,sticky=tk.W+tk.N,)
            
            n += 1
        
        window.wait_window()
    

    # 菜单 callback 函数：UI→启用放大倍数
    def menu_call_back_function_use_tk_scaling(self,):
        self.ini_data["tk_scaling_use_flag"] = self.menu_index_tk_scaling_use_flag.get()
        print( self.ini_data["tk_scaling_use_flag"] )
        if self.ini_data["tk_scaling_use_flag"]:
            self.parent.tk.call('tk', 'scaling', self.ini_data["tk_scaling_number"])
            self.parent.update()
        else:
            pass
    
    # 菜单 callback 函数：UI→放大倍数 设置
    # a topleve window
    def menu_call_back_function_set_tk_scaling_number(self,):
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("放大倍数")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )
        
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        window.columnconfigure(0,weight=1)
        window.columnconfigure(1,weight=0)
        #window.rowconfigure(0,weight=0)
        
        #num_0 =  self.ini_data["tk_scaling_number"]
        
        ttk.Label(window,text="已设定的值为："+ str(self.ini_data["tk_scaling_number"]) ).grid(row=0,column=0,sticky=tk.N+tk.W,)
        

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.N+tk.W,)
        
        ttk.Label(window,text="输入一个大于0的数，整数/小数").grid(row=2,column=0,sticky=tk.N+tk.W,)
        
        def get_the_number():
            try:
                the_number = input_number.get()
                the_number = eval( the_number )
                if type( the_number ) == int:
                    if the_number > 0 :
                        self.ini_data["tk_scaling_number"] = the_number
                    else:
                        self.ini_data["tk_scaling_number"] = 0
                elif type( the_number ) == float :
                    if the_number > 0.01 :
                        self.ini_data["tk_scaling_number"] = the_number
                    else:
                        self.ini_data["tk_scaling_number"] = 0
                
            except:
                pass
            window.destroy()
        
        input_number = tk.StringVar()
        entry_a = ttk.Entry(window,textvariable=input_number,)
        entry_a.grid(row=3,column=0,sticky=tk.N+tk.W,)
        
        ttk.Button(window,text="确定",command=get_the_number,).grid(row=4,column=0,sticky=tk.N+tk.W,)
        
        
        num = self.parent.tk.call('tk', 'scaling', )
        
        a_text      = tk.Text( window,undo=False )
        scrollbar_1 = ttk.Scrollbar( window, orient=tk.VERTICAL, command = a_text.yview,)
        a_text.configure(yscrollcommand=scrollbar_1.set)
        a_text.grid(row=5,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        scrollbar_1.grid(row=5,column=1,sticky=(tk.N,tk.S))
        
        #self.data_from_main["tk_scaling_number_0"]
        num = self.data_from_main["tk_scaling_number_0"]
        num = str(num)
        
        a_text.insert(tk.END, "程序启动时，读取值为：",)
        a_text.insert(tk.END, num ,)
        a_text.insert(tk.END, "\n" ,)
        
        a_text.insert(tk.END, "\n" ,)
        
        a_text.insert(tk.END, "屏幕分辨率不同，初始值应该不同\n" ,)
        a_text.insert(tk.END, "按说明的话：\n" ,)
        a_text.insert(tk.END, "　　72DPI(每英寸72个像素点)的屏幕，值设置1，达到 1:1 的效果\n" ,)
        
        a_text.insert(tk.END, "\n" ,)
        
        a_text.insert(tk.END, "如果需要放大／缩小，可以用这个功能\n" ,)
        a_text.insert(tk.END, "注意，放大以后，目录列表、游戏列表 的每一行距离并没有变化，需要手动设置 调整一下 行距\n" ,)
        
        a_text.configure(state=tk.DISABLED)
        
        window.wait_window()
        
    # 菜单 callback 函数：UI→ 行高
    #   a topleve window
    def menu_call_back_function_set_row_height(self,):
        print("行高 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("列表 行高度 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(1,weight=0)
        
        ttk.Label(window,text="").grid(row=0,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="列表 行高度 设置").grid(row=1,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=2,column=0,sticky=tk.W+tk.N)
        
        choose_value = tk.StringVar()
        chooser = ttk.Combobox( window ,
                    values=list( range(201)) ,
                    textvariable=choose_value ,
                    state="readonly" , )
        chooser.grid(row=3,column=0,sticky=tk.W+tk.N)
        if self.ini_data["row_height"] in range(201):
            chooser.set(self.ini_data["row_height"])
        else:
            chooser.set(0)
        
        ttk.Label(window,text="").grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
            temp_number = choose_value.get()
            temp_number = int( temp_number )
            print(temp_number)
            
            self.ini_data["row_height"]=temp_number
            print(self.ini_data["row_height"])
            
            if temp_number > 0:
                self.style.configure( 'Treeview', rowheight = temp_number ) 
            
            #window.destroy()
            #self.parent.lift()
        
        ttk.Label(window,text="选择 0 的话，关闭程序，下次打开，回到默认值").grid(row=5,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="因为我也不太清楚，默认值是多少").grid(row=6,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=7,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="选择其它的值，即时生效").grid(row=8,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=9,column=0,sticky=tk.W+tk.N)
        
        ttk.Button(window,text="确定",command=for_ok_button).grid( row=10,column=0,sticky=tk.N+tk.E, )
        
        
        window.wait_window()

    # 菜单 callback 函数：UI→ 列表 图标 宽度 设置
    #   a topleve window
    def menu_call_back_function_set_icon_size(self,):
        print("列表 图标 宽度 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("列表 图标 宽度 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(1,weight=0)
        
        ttk.Label(window,text="").grid(row=0,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="列表 图标 宽度 设置").grid(row=1,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=2,column=0,sticky=tk.W+tk.N)
        
        choose_value = tk.StringVar()
        chooser = ttk.Combobox( window ,
                    values=list( range(100)) ,
                    textvariable=choose_value ,
                    state="readonly" , )
        chooser.grid(row=3,column=0,sticky=tk.W+tk.N)
        
        if self.ini_data["icon_size"] in range(100):
            chooser.set(self.ini_data["icon_size"])
        else:
            chooser.set(0)
        
        ttk.Label(window,text="").grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
            temp_number = choose_value.get()
            temp_number = int( temp_number )
            print(temp_number)
            
            self.ini_data["icon_size"]=temp_number
            print(self.ini_data["icon_size"])
            
            # 图标清空
            self.tree.tag_configure("good",       image = "" )
            self.tree.tag_configure("imperfect",  image = "" )
            self.tree.tag_configure("preliminary",image = "" )
            self.tree.tag_configure("others",     image = "" )
            
            if temp_number <= 0:
            
                self.image_black  = ImageTk.PhotoImage( self.image_black_original)
                
                self.image_green  = ImageTk.PhotoImage( self.image_green_original)
                
                self.image_yellow = ImageTk.PhotoImage( self.image_yellow_original)
                
                self.image_red    = ImageTk.PhotoImage( self.image_red_original)                
            else:
                new_size = ( self.ini_data["icon_size"],self.ini_data["icon_size"] )
                
                self.image_black  = ImageTk.PhotoImage( self.image_black_original.resize( new_size,Image.BILINEAR, ))
                
                self.image_green  = ImageTk.PhotoImage( self.image_green_original.resize( new_size,Image.BILINEAR, ))
                
                self.image_yellow = ImageTk.PhotoImage( self.image_yellow_original.resize( new_size,Image.BILINEAR, ))
                
                self.image_red    = ImageTk.PhotoImage( self.image_red_original.resize( new_size,Image.BILINEAR, ))
            
            # 加截图标
            self.tree.tag_configure("good",       image = self.image_green )
            self.tree.tag_configure("imperfect",  image = self.image_yellow )
            self.tree.tag_configure("preliminary",image = self.image_red )
            self.tree.tag_configure("others",     image = self.image_black )            
            #window.destroy()
            #self.parent.lift()
            window.lift(self.parent)
        
        ttk.Label(window,text="选择 0 的话，回到图片原始大小").grid(row=5,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="我用的小图标的图片，原始大小是 16x16，你可以自己换图片").grid(row=6,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=7,column=0,sticky=tk.W+tk.N)

        
        ttk.Button(window,text="确定",command=for_ok_button).grid( row=8,column=0,sticky=tk.N+tk.E, )
        
        
        window.wait_window()        

    # 菜单 callback 函数：UI→ 列表字体
    #   a topleve window    
    def menu_call_back_function_set_gamelist_font(self,):

        print("列表 字体 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("列表 字体 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(0,weight=1)
        
        f1 = ttk.Frame(window)
        f1.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        
        self.font_chooser(master=f1 , font_var= self.ini_data["gamelist_font"] , font_size_var= self.ini_data["gamelist_font_size"] , widget_type="Treeview")

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.W+tk.N)
               
        window.wait_window()

    # 菜单 callback 函数：UI→ 文档1 字体
    #   a topleve window   
    def menu_call_back_function_set_text_font(self,):

        print("文档1 字体 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("文档1 字体 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(0,weight=1)
        
        f1 = ttk.Frame(window)
        f1.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        
        self.font_chooser(master=f1 , font_var= self.ini_data["text_font"] , font_size_var= self.ini_data["text_font_size"] , widget_type="Text")

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.W+tk.N)
               
        window.wait_window()    

    # 菜单 callback 函数：UI→ 文档2 字体
    #   a topleve window   
    def menu_call_back_function_set_text_2_font(self,):

        print("文档2 字体 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("文档2 字体 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(0,weight=1)
        
        f1 = ttk.Frame(window)
        f1.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        
        self.font_chooser(master=f1 , font_var= self.ini_data["text_2_font"] , font_size_var= self.ini_data["text_2_font_size"] , widget_type="Text_2")

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.W+tk.N)
               
        window.wait_window()    

    # 菜单 callback 函数：UI→ 其它 字体
    #   a topleve window 
    def menu_call_back_function_set_others_font(self,):
        print("其它 字体 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("其它 字体 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(0,weight=1)
        
        f1 = ttk.Frame(window)
        f1.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        
        self.font_chooser(master=f1 , font_var= self.ini_data["others_font"] , font_size_var= self.ini_data["others_font_size"] , widget_type="others")

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.W+tk.N)
               
        window.wait_window()           

    # 菜单 callback 函数：UI→ 内置主题背景色
    #   a topleve window 
    def menu_call_back_function_set_background_of_internal_themes(self,):
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("内置主题 背景色 设置")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        #size = temp
        print(size)
        window.geometry( size )

        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(0,weight=1)
        
        frame = ttk.Frame(window)
        frame.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        
        def choose_background_colour():
            label = label_bg
            new_colour = ""
            
            new_colour = tkinter.colorchooser.askcolor()
        
            #print( type(new_colour))
            #<class 'tuple'>
        
            #print(new_colour)
            # ((128, 64, 64), '#804040') 

            new_colour = new_colour[1]
            # 格式选择 
            
            if new_colour:
                try:
                    label.configure( background = new_colour )
                    nonlocal background_colour
                    background_colour = new_colour # # # 
                except:
                    pass
                    
            window.lift(self.parent)
            
        def choose_background_colour_panedwindow():
            label = label_bg_panedwindow
            new_colour = ""
            
            new_colour = tkinter.colorchooser.askcolor()
        
            #print( type(new_colour))
            #<class 'tuple'>
        
            #print(new_colour)
            # ((128, 64, 64), '#804040') 

            new_colour = new_colour[1]
            # 格式选择 
            
            if new_colour:
                try:
                    label.configure( background = new_colour )
                    nonlocal background_colour_panedwindow
                    background_colour_panedwindow = new_colour # # #
                except:
                    pass
                    
            window.lift(self.parent)            
        
        def for_ok_button():
            print( background_colour )
            print( background_colour_panedwindow )
            self.ini_data["colour_bg"] = background_colour
            self.ini_data["colour_panedwindow_bg"] = background_colour_panedwindow
            
            if self.style.theme_use() in self.data_from_main["internal_themes"]:
                self.ui_initial_functions_background()
            
            window.destroy()
        
        ttk.Label(frame,text="").grid(row=0,column=0,sticky=tk.W+tk.N,)
        ttk.Label(frame,text="仅内置主题背景色设置").grid(row=1,column=0,columnspan=2,sticky=tk.W+tk.N,)
        ttk.Label(frame,text="因为，第三方主题的话，有自己设置的颜色").grid(row=2,column=0,columnspan=2,sticky=tk.W+tk.N,)
        ttk.Label(frame,text="").grid(row=3,column=0,sticky=tk.W+tk.N,)
        
        background_colour = self.ini_data["colour_bg"]
        background_colour_panedwindow = self.ini_data["colour_panedwindow_bg"]
        
        ttk.Button(frame,text="背景色设置",command=choose_background_colour).grid(row=4,column=0,sticky=tk.W+tk.N,)
        label_bg = ttk.Label(frame,borderwidth=5,relief="raised" ,text=" "*10)
        label_bg.grid(row=4,column=1,sticky=tk.W+tk.N,)
        
        try:
            label_bg.configure( background = background_colour )
        except:
            pass

        ttk.Button(frame,text="分隔条背景色设置",command=choose_background_colour_panedwindow ).grid(row=5,column=0,sticky=tk.W+tk.N,)
        label_bg_panedwindow = ttk.Label(frame,borderwidth=5,relief="raised",text=" "*10)
        label_bg_panedwindow.grid(row=5,column=1,sticky=tk.W+tk.N,)

        try:
            label_bg_panedwindow.configure( background = background_colour_panedwindow )
        except:
            pass
        
        ttk.Label(frame,text="").grid(row=6,column=0,sticky=tk.W+tk.N,)
        
        ttk.Button(frame,text="确定",command=for_ok_button).grid(row=7,column=0,columnspan=2,sticky=tk.E+tk.N,)
        
        window.wait_window()          
    
    # 菜单 callback 函数：UI→ 保存配置文件 jjui.ini
    #       1，callback 函数,菜单 , 保存 → 保存配置文件
    #       2，被 主函数 调用，程序关闭时 调用一下
    def menu_call_back_function_save_ini_data(self,event=None):
        # from jjui import ui_configure_file
        # ui_configure_file.write_ini(ini_file_name,ini_dict)
        
        # self.filter ,为合集，但转为 list ,打印在配置文件中
        temp=[]
        for x in self.filter: 
            temp.append(x)
        self.ini_data["filter"] = temp
        del temp
        
        # 周边图片，是否使用 .zip
        self.ini_data["extra_image_usezip"] =  self.extra_image_usezip.get()
        self.ini_data["extra_image_usezip_2"] =  self.extra_image_usezip_2.get()
        
        # 周边，显示 项目，记录
        self.ini_data["extra_image_chooser_index"]  = self.extra_image_chooser.current()
        self.ini_data["extra_image_chooser_2_index"]= self.extra_image_chooser_2.current()
        self.ini_data["extra_text_chooser_index"]   = self.extra_text_chooser.current()
        self.ini_data["extra_command_type_chooser_index"]= self.extra_command_type_chooser.current()        
        
        # 周边 ,notebook ,tab ID ，记录
        self.ini_data["extra_tab_index"] = self.notebook.index( self.notebook.select() )
        
        # self.ini_data
        # self.ini_path
        #ui_configure_file.write_ini( self.ini_path , self.ini_data ,)
        # 添加 顺序 保持，用于 老版本 python 3.4.4
        ui_configure_file.write_ini( self.ini_path , self.ini_data ,self.data_from_main["ini_order"])
    # 菜单 callback 函数：UI→ 保存配置文件 jjui.ini、保存窗口大小，
    def menu_call_back_function_window_size_save(self,):
    
        # 主窗口大小
        height = self.parent.winfo_height() 
        width = self.parent.winfo_width()
        # 得到的结果不准确，因为 菜单 ？？
        # 在 设置 root.geometry 之后，马上 root.update() 一下，就准确了
        # why ?
        # # #
        # 转为字符串 如 800x600
        size = str(width) + "x" + str(height)
        self.ini_data["size"] = size
                

        temp = {}
        # 列表宽度
        # self.ini_data["gamelist_columns_width"]
        # self.data_from_main["columns"]
        for x in self.data_from_main["columns"] :
            if x in self.tree['columns']:
                try:
                    w = self.tree.column(x,option="width")
                    temp[x] = w
                except:
                    pass
        for x in temp:
            self.ini_data["gamelist_columns_width"][x] = temp[x]
        del temp        
        
        # 目录 分隔条 位置
        self.ini_data["pos1"] = self.frame_middle.sashpos(0,)
                
        # 周边 分隔条 位置
        self.ini_data["pos2"] = self.frame_middle.sashpos(1,)
        
        # 图片 分隔条 位置
        self.ini_data["pos3"] = self.extra_image_panedwindow.sashpos(0,)
        
        self.menu_call_back_function_save_ini_data()
    # 菜单 callback 函数：UI→ 保存配置文件 jjui.ini、保存窗口大小，窗口位置
    def menu_call_back_function_window_size_and_position_save(self,):
        # 用之前的函数，保存一次
        self.menu_call_back_function_window_size_save() 
        
        # 补充位置信息
        self.ini_data["size"] = self.parent.winfo_geometry() 
        
        # 再保存一次
        self.menu_call_back_function_save_ini_data() 
    
    # 菜单 callback 函数：目录→保存
    def menu_call_back_function_save_index(self,):
        for x in self.ini_files_be_edited :
            print(x)
            try:
                folders_save.save(x , self.ini_set_dict[x])
            except:
                pass
        self.ini_files_be_edited = set() # 重置
    # 菜单 callback 函数：目录→展开/收起
    def menu_call_back_function_index_show_all(self,event=None):
        try:
            self.index_show_all_mark
        except:
            self.index_show_all_mark = True
        
        if self.index_show_all_mark :
            self.tree_index['displaycolumns'] = "#all"
        else:
            self.tree_index['displaycolumns'] = ()
        
        self.index_show_all_mark = not self.index_show_all_mark    

    # 菜单 callback 函数：游戏列表→刷新列表 split 模式                   
    def menu_call_back_function_gamelist_available_refresh(self,event=None):
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        self.data['set_data']['available_set']=set() # 初始化 ,清空
        
        temp_set = self.get_files_names_in_rompath()
        
        ######
        
        self.data['set_data']['available_set'] = self.data['set_data']['all_set'] & temp_set

        self.data['set_data']['unavailable_set'] = self.data['set_data']['all_set'] - self.data['set_data']['available_set']
        
        del temp_set
        
        # 保存数据
        save_pickle.save(self.data['set_data']['available_set'],self.available_gamelist_file_path)
        self.other_functions_mark_available_games() # 列表 标记
        
        self.ini_data["index_be_chosen"] = "" # 标记重置
        
        self.tree_index.see('available_set')
        self.tree_index.selection_set('available_set')
        self.tree_index.focus('available_set')
        
        self.choose_index('available_set')

    # 菜单 callback 函数：游戏列表→刷新列表 merged 模式
    def menu_call_back_function_gamelist_available_refresh_2(self,event=None):
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        self.data['set_data']['available_set']=set() # 初始化 ,清空
        
        #####
        temp_set = self.get_files_names_in_rompath( merged = True )
        #####

        self.data['set_data']['available_set'] = self.data['set_data']['all_set'] & temp_set

        self.data['set_data']['unavailable_set'] = self.data['set_data']['all_set'] - self.data['set_data']['available_set']
        
        del temp_set
        
        # 保存数据
        save_pickle.save(self.data['set_data']['available_set'],self.available_gamelist_file_path)
        self.other_functions_mark_available_games() # 列表 标记
        
        self.ini_data["index_be_chosen"] = "" # 标记重置
        
        self.tree_index.see('available_set')
        self.tree_index.selection_set('available_set')
        self.tree_index.focus('available_set')
        
        self.choose_index('available_set')
    
    # 菜单 callback 函数：游戏列表→刷新列表 ，模拟器校验，全部
    #   Toplevel 窗口
    def menu_call_back_function_gamelist_available_refresh_audit_by_mame_all(self,event=None):
    
        # 打开小窗口 
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("-verifyroms，校验全体 roms，速度慢！！！")
        
        window.lift(self.parent)
        #window.transient(self.parent)
        #window.grab_set()        
        
        # 隐藏主窗口
        self.parent.withdraw()  
        window.lift()

        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        #size = temp
        #window.geometry( size )
        
        window.columnconfigure(0,weight=1)
        #window.rowconfigure(0,weight=1)
        
        # # #
        
        n = 0
        
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        ttk.Label(window,text="总数目(不收全集的话，一般没有这么多)：" + str( len(self.data["set_data"]["all_set"] ) ) ).grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_autid = ttk.Label(window,text=""  ) 
        label_autid.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1        
        
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_good = ttk.Label(window,text="")
        label_best_available = ttk.Label(window,text="")
        label_bad = ttk.Label(window,text="")
        label_both = ttk.Label(window,text="")
        
        label_good.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        label_best_available.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        label_bad.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1        
        
        label_both.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1        
        ###
        
        #temp_tk_var_for_waiting = tk.StringVar()
        
        after_remember = None
        
        def exit_for_window():
        
            if after_remember :
                window.after_cancel( after_remember )
                #temp_tk_var_for_waiting.set("quit")
            
            # # #
            #window.deiconify()
            #window.transient(self.parent)
            window.destroy()
            self.parent.deiconify()
            self.parent.lift()
            self.parent.update()
            
            self.tree.focus_set()            
            
            self.ini_data["index_be_chosen"] = "" # 标记重置
            
            self.tree_index.see('available_set')
            self.tree_index.selection_set('available_set')
            self.tree_index.focus('available_set')
            
            self.choose_index('available_set')            

        def start_work():
            
            # 
            the_button.configure(text="请耐心等待…………")
            the_button.configure(state="disabled")
            
            (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()

            command_list = []
            command_list.append( mame_exe )
            command_list.append( "-verifyroms" )
            
            print(  )
            print( "-verifyroms" )
            print( command_list )        
            
            number_good = 0
            number_best_available = 0
            number_bad = 0
            
            list_good  = []
            list_bad   = []
            list_best_available = []
            
            # romset mslug [neogeo] is good
            search_string_good = r"^\s*romset\s*(\S+).*\sis\s*good\s*$"
            # romset 1943 is best available
            search_string_best_available = r"^\s*romset\s*(\S+).*\sis\s*best\s*available\s*$"
            # romset kof97 [neogeo] is bad
            search_string_bad = r"^\s*romset\s*(\S+).*\sis\s*bad\s*$"
            # 39 romsets found, 39 were OK.
            search_string_result = r"^\s*(\d*)\s*romsets\s*found.*$"
            
            p_good           = re.compile( search_string_good, )
            p_bad            = re.compile( search_string_bad, )
            p_best_available = re.compile( search_string_best_available, )
            p_result         = re.compile( search_string_result, )
            
            proc = subprocess.Popen(command_list, stdout = subprocess.PIPE ,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=self.ini_data["use_shell"],cwd=mame_dir,encoding='utf_8')
            
            audit_number = 0
            line_number = 0
            flag_finsh = False
            for line in proc.stdout:
                line_number += 1
            
                the_text.insert(tk.END, line, )
                
                #the_text.see(tk.END)
                # 每一次都用 the_text.see(tk.END) ，会卡
                
                # 行数太多
                # 删减一些
                if line_number > 5000:
                    line_number = line_number - 4500
                    the_text.delete("1.0", "4501.0")
                
                audit_number = number_good + number_best_available + number_bad
                if audit_number % 100 == 0 : 
                    label_autid.configure(text=r"已检校验的数目："+str(audit_number))
                    the_progressbar.step(5.0)

                m=p_good.search( line ) 
                if m : 
                    number_good += 1
                    list_good.append( m.group(1) )
                    continue
                    
                m=p_best_available.search( line ) 
                if m : 
                    number_best_available += 1
                    list_best_available.append( m.group(1) )
                    continue
                    
                m=p_bad.search( line ) 
                if m : 
                    number_bad += 1
                    list_bad.append( m.group(1) )
                    continue
                
                m=p_result.search( line ) 
                if m : 
                    flag_finsh = True
                    
            
            the_progressbar.configure(value=100)
            # 进度条跑满
            
            the_text.see(tk.END)
            # 显示到最后一行
            
            audit_number = number_good + number_best_available + number_bad
            label_autid.configure(text=r"已检校验的数目："+str(audit_number))
            # label 记录 
            
            if flag_finsh:
                the_temp_text = r"完成，对比一下，校验结果里最后的总结，格式为："
            else:
                the_temp_text = r"结束，貌似哪里出错了，对比一下，校验结果里最后的总结，格式为："
            
            the_button.configure( text = the_temp_text )
            # label_last
            label_last.configure(text=r"(数量)???? romsets found, (数量)????? were OK")
            
            label_good.configure(text=r"good 数量 (校验通过，正确)：" + str(number_good))
            label_best_available.configure(text=r"best available 数量(校验通过，有 bad dump 或 no dump 是这种提示)："+str(number_best_available))
            label_bad.configure(text=r"bad 数量 (校验未通过，错误)："+str(number_bad))
            label_both.configure(text=r"OK 数量 (校验通过的) (good + best available)：" + str(number_good + number_best_available) )
            
            
            #######↑↑
            
            temp_set  = set(list_good) | set(list_best_available)
            
            
            self.data['set_data']['available_set'] = self.data['set_data']['all_set'] & temp_set
            self.data['set_data']['unavailable_set'] = self.data['set_data']['all_set'] - self.data['set_data']['available_set']
            
            del temp_set
            
            # 保存数据
            save_pickle.save(self.data['set_data']['available_set'],self.available_gamelist_file_path)
            self.other_functions_mark_available_games() # 列表 标记
            
            the_finish_button.grid()
            
            window.update()
            window.deiconify()
            window.lift()
            #window.withdraw()
            

        def test_threading():
            thread = threading.Thread(target=start_work)
            thread.start()


        the_progressbar=ttk.Progressbar(window,orient=tk.HORIZONTAL)
        the_progressbar.grid(row=n,column=0,sticky=tk.W+tk.N+tk.E)
        n += 1
        
        the_button = ttk.Button(window,text="开始校验，需要的时间可能有点久",command=test_threading)
        the_button.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_last = ttk.Label(window,text="")
        label_last.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1  

        the_finish_button = ttk.Button(window,text="跳转到游戏列表",command=exit_for_window)
        the_finish_button.grid(row=n,column=0,sticky=tk.W+tk.N)
        the_finish_button.grid_remove()
        n += 1      
        
        frame_for_text = ttk.Frame(window)
        frame_for_text.grid(row=n,column=0,sticky=tk.W+tk.N+tk.E+tk.S)
        
        window.rowconfigure(n,weight=1)
        frame_for_text.rowconfigure(0,weight=1)
        
        frame_for_text.columnconfigure(0,weight=1)
        frame_for_text.rowconfigure(0,weight=1)        
        
        the_text = tk.Text(frame_for_text,undo=False,wrap=tk.NONE)
        scrollbar_1 = ttk.Scrollbar( frame_for_text, orient=tk.VERTICAL, command=the_text.yview)
        scrollbar_2 = ttk.Scrollbar( frame_for_text, orient=tk.HORIZONTAL, command=the_text.xview)
        
        the_text.configure(yscrollcommand=scrollbar_1.set)
        the_text.configure(xscrollcommand=scrollbar_2.set)
        
        the_text.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        ttk.Sizegrip(frame_for_text).grid(row=1,column=1)
        
        window.protocol("WM_DELETE_WINDOW", exit_for_window)        
        window.wait_window()
    
    
    def menu_call_back_function_gamelist_available_refresh_audit_by_mame_one_by_one(self,event=None):
    
        temp_files_set = self.get_files_names_in_rompath()
        the_games = self.data['set_data']['all_set'] & temp_files_set
        
        the_number = len(the_games)
        
        
        # 打开小窗口 
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("刷新列表，用 mame 校验，逐个校验已拥有文件，split/分离模式")
        
        window.lift(self.parent)
        #window.transient(self.parent)
        #window.grab_set()        
        
        # 隐藏主窗口
        self.parent.withdraw()  
        window.lift()

        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        #size = temp
        #window.geometry( size )
        
        window.columnconfigure(0,weight=1)
        #window.rowconfigure(0,weight=1)
        
        # # # #######################################
        # 需要校验的数量   label_numbers_to_audit      
        # good             label_good   
        # best_available   label_best_available
        # bad              label_bad      
        # not found        label_not_found      
        # no roms          label_no_roms  # device 没有 roms 会有这种提示      
        #                        
        # 已检验的数量           
        # 通过校验的数量         
        # -------------------    
        #                        
        #  Text                  
        #                        
        
        n = 0
        
        label_numbers_to_audit = ttk.Label(window,text="")
        label_numbers_to_audit.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_good = ttk.Label(window,text="")
        label_good.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        label_best_available = ttk.Label(window,text="")
        label_best_available.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        label_bad = ttk.Label(window,text="")
        label_bad.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        label_not_found = ttk.Label(window,text="")
        label_not_found.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1    

        label_no_roms = ttk.Label(window,text="")
        label_no_roms.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        #
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_audited = ttk.Label(window,text="")
        label_audited.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1          
        
        label_both = ttk.Label(window,text="") # good + best_available
        label_both.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1        
        
        #
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
     
        ###
        def exit_for_window():
        
            # # #
            #window.deiconify()
            #window.transient(self.parent)
            window.destroy()
            self.parent.deiconify()
            self.parent.lift()
            self.parent.update()
            
            self.tree.focus_set()            
            
            self.ini_data["index_be_chosen"] = "" # 标记重置
            
            self.tree_index.see('available_set')
            self.tree_index.selection_set('available_set')
            self.tree_index.focus('available_set')
            
            self.choose_index('available_set')            
        
        def start_work():
            
            # 
            the_button.configure(text="请耐心等待…………")
            the_button.configure(state="disabled")
            

            label_numbers_to_audit.configure(text="需要校验的数目" + str(the_number) )
            
            (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
            
            command_list = []
            command_list.append( mame_exe )
            command_list.append( "-verifyroms" )                
        
            number_good           = 0
            number_best_available = 0
            number_bad            = 0    
            number_not_found      = 0    
            number_no_roms        = 0  # device 里面，才有这种提示
            
            list_good  = []
            list_best_available = []                
            
            # romset mslug [neogeo] is good
            search_string_good = r"^\s*romset\s*(\S+).*\sis\s*good\s*$"
            # romset 1943 is best available
            search_string_best_available = r"^\s*romset\s*(\S+).*\sis\s*best\s*available\s*$"
            # romset kof97 [neogeo] is bad
            search_string_bad = r"^\s*romset\s*(\S+).*\sis\s*bad\s*$"
            # romset "kof99" not found!
            search_string_not_found  = r'^\s*romset\s*"(\S+)"\s*not\s*found\!\s*$'
            # romset "09825_67907" has no roms!
            search_string_no_roms    = r'^\s*romset\s*"(\S+)"\s*has\s*no\s*roms\!\s*$'
            
            # 无需
            # 39 romsets found, 39 were OK.
            #search_string_result = r"^\s*(\d*)\s*romsets\s*found.*$"                
            
            p_good           = re.compile( search_string_good, )
            p_bad            = re.compile( search_string_bad, )
            p_best_available = re.compile( search_string_best_available, )
            p_not_found      = re.compile( search_string_not_found, )
            p_no_roms        = re.compile( search_string_no_roms, )
            #p_result         = re.compile( search_string_result, )                
            
            line_number = 0
            audit_number = 0
            
            for x in sorted( the_games ):

                # 行数太多
                # 删减一些
                if line_number > 5000:
                    line_number = line_number - 4500
                    the_text.delete("1.0", "4501.0")
        
                audit_number = number_good + number_best_available + number_bad + number_not_found + number_no_roms
                
                
                label_audited.configure(text=r"已检校验的数目："+str(audit_number))
                the_progressbar.step()
            
                new_command_list = command_list + [x,]
                
                lines = []
                
                proc = subprocess.Popen(new_command_list, stdout = subprocess.PIPE ,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=self.ini_data["use_shell"],cwd=mame_dir,encoding='utf_8')
        
                for line in proc.stdout:
                    lines.append(line)
                
                for line in lines:
                    line_number += 1
        
                    the_text.insert(tk.END, line, )

                    m=p_good.search( line ) 
                    if m : 
                        number_good += 1
                        list_good.append( m.group(1) )
                        continue
                
                    m=p_best_available.search( line ) 
                    if m : 
                        number_best_available += 1
                        list_best_available.append( m.group(1) )
                        continue
                
                    m=p_bad.search( line ) 
                    if m : 
                        number_bad += 1
                        #list_bad.append( m.group(1) )
                        continue
                        
                    m=p_not_found.search( line ) 
                    if m : 
                        number_not_found += 1
                        continue
                    
                    m=p_no_roms.search( line ) 
                    if m : 
                        number_no_roms += 1
                        continue
                
            the_progressbar.configure(value=100)
            # 进度条跑满
            
            the_text.see(tk.END)
            # 显示到最后一行
            
            audit_number = number_good + number_best_available + number_bad + number_not_found + number_no_roms            
            
            label_audited.configure(text=r"已检校验的数目："+str(audit_number))
            # label 记录 
            
            the_button.configure( text = "" )

            label_good.configure(text=r"good 数量 (校验通过，正确)：" + str(number_good))
            label_best_available.configure(text=r"best available 数量(校验通过，有 bad dump 或 no dump 是这种提示)："+str(number_best_available))
            label_bad.configure(text=r"bad 数量 (校验未通过，错误)："+str(number_bad))
            label_not_found.configure(text=r"not found 数量 (校验未通过，错误)："+str(number_not_found))
            label_no_roms.configure(text=r"no roms 数量 (没有 roms 的 device，好像是这种提示 )："+str(number_no_roms))
            label_both.configure(text=r"OK 数量 (校验通过的) (good + best available)：" + str(number_good + number_best_available) )
            
            
            #######↑↑
            
            temp_set  = set(list_good) | set(list_best_available)
            
            
            self.data['set_data']['available_set'] = self.data['set_data']['all_set'] & temp_set
            self.data['set_data']['unavailable_set'] = self.data['set_data']['all_set'] - self.data['set_data']['available_set']
            
            del temp_set
            
            # 保存数据
            save_pickle.save(self.data['set_data']['available_set'],self.available_gamelist_file_path)
            self.other_functions_mark_available_games() # 列表 标记
            
            the_finish_button.grid()
            
            window.update()
            window.deiconify()
            window.lift()
        
        def test_threading():
            thread = threading.Thread(target=start_work)
            thread.start()


        the_progressbar=ttk.Progressbar(window,orient=tk.HORIZONTAL)
        the_progressbar.grid(row=n,column=0,sticky=tk.W+tk.N+tk.E)
        n += 1
        
        the_button = ttk.Button(window,text="开始校验",command=test_threading)
        #the_button = ttk.Button(window,text="开始校验",command=start_work)
        the_button.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_last = ttk.Label(window,text="")
        label_last.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1  

        the_finish_button = ttk.Button(window,text="跳转到游戏列表",command=exit_for_window)
        the_finish_button.grid(row=n,column=0,sticky=tk.W+tk.N)
        the_finish_button.grid_remove()
        n += 1      
        
        frame_for_text = ttk.Frame(window)
        frame_for_text.grid(row=n,column=0,sticky=tk.W+tk.N+tk.E+tk.S)
        
        window.rowconfigure(n,weight=1)
        frame_for_text.rowconfigure(0,weight=1)
        
        frame_for_text.columnconfigure(0,weight=1)
        frame_for_text.rowconfigure(0,weight=1)        
        
        the_text = tk.Text(frame_for_text,undo=False,wrap=tk.NONE)
        scrollbar_1 = ttk.Scrollbar( frame_for_text, orient=tk.VERTICAL, command=the_text.yview)
        scrollbar_2 = ttk.Scrollbar( frame_for_text, orient=tk.HORIZONTAL, command=the_text.xview)
        
        the_text.configure(yscrollcommand=scrollbar_1.set)
        the_text.configure(xscrollcommand=scrollbar_2.set)
        
        the_text.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        ttk.Sizegrip(frame_for_text).grid(row=1,column=1)
        
        window.protocol("WM_DELETE_WINDOW", exit_for_window)        
        window.wait_window()

    
    def menu_call_back_function_gamelist_available_refresh_audit_by_mame_one_by_one_2(self,event=None):
    
        ##### 复制上一个函数，除了这行一，其它一样
        temp_files_set = self.get_files_names_in_rompath(merged = True)
        #####    
    
        the_games = self.data['set_data']['all_set'] & temp_files_set
        
        the_number = len(the_games)
        
        
        # 打开小窗口 
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("刷新列表，用 mame 校验，逐个校验已拥有文件，split/分离模式")
        
        window.lift(self.parent)
        #window.transient(self.parent)
        #window.grab_set()        
        
        # 隐藏主窗口
        self.parent.withdraw()  
        window.lift()

        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        #size = temp
        #window.geometry( size )
        
        window.columnconfigure(0,weight=1)
        #window.rowconfigure(0,weight=1)
        
        # # # #######################################
        # 需要校验的数量   label_numbers_to_audit      
        # good             label_good   
        # best_available   label_best_available
        # bad              label_bad      
        # not found        label_not_found      
        # no roms          label_no_roms  # device 没有 roms 会有这种提示      
        #                        
        # 已检验的数量           
        # 通过校验的数量         
        # -------------------    
        #                        
        #  Text                  
        #                        
        
        n = 0
        
        label_numbers_to_audit = ttk.Label(window,text="")
        label_numbers_to_audit.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_good = ttk.Label(window,text="")
        label_good.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        label_best_available = ttk.Label(window,text="")
        label_best_available.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        label_bad = ttk.Label(window,text="")
        label_bad.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        label_not_found = ttk.Label(window,text="")
        label_not_found.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1    

        label_no_roms = ttk.Label(window,text="")
        label_no_roms.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1
        
        #
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_audited = ttk.Label(window,text="")
        label_audited.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1          
        
        label_both = ttk.Label(window,text="") # good + best_available
        label_both.grid(row=n,column=0,sticky=tk.W+tk.N)
        n+=1        
        
        #
        ttk.Label(window,text="").grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
     
        ###
        def exit_for_window():
        
            # # #
            #window.deiconify()
            #window.transient(self.parent)
            window.destroy()
            self.parent.deiconify()
            self.parent.lift()
            self.parent.update()
            
            self.tree.focus_set()            
            
            self.ini_data["index_be_chosen"] = "" # 标记重置
            
            self.tree_index.see('available_set')
            self.tree_index.selection_set('available_set')
            self.tree_index.focus('available_set')
            
            self.choose_index('available_set')            
        
        def start_work():
            
            # 
            the_button.configure(text="请耐心等待…………")
            the_button.configure(state="disabled")
            

            label_numbers_to_audit.configure(text="需要校验的数目" + str(the_number) )
            
            (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
            
            command_list = []
            command_list.append( mame_exe )
            command_list.append( "-verifyroms" )                
        
            number_good           = 0
            number_best_available = 0
            number_bad            = 0    
            number_not_found      = 0    
            number_no_roms        = 0  # device 里面，才有这种提示
            
            list_good  = []
            list_best_available = []                
            
            # romset mslug [neogeo] is good
            search_string_good = r"^\s*romset\s*(\S+).*\sis\s*good\s*$"
            # romset 1943 is best available
            search_string_best_available = r"^\s*romset\s*(\S+).*\sis\s*best\s*available\s*$"
            # romset kof97 [neogeo] is bad
            search_string_bad = r"^\s*romset\s*(\S+).*\sis\s*bad\s*$"
            # romset "kof99" not found!
            search_string_not_found  = r'^\s*romset\s*"(\S+)"\s*not\s*found\!\s*$'
            # romset "09825_67907" has no roms!
            search_string_no_roms    = r'^\s*romset\s*"(\S+)"\s*has\s*no\s*roms\!\s*$'
            
            # 无需
            # 39 romsets found, 39 were OK.
            #search_string_result = r"^\s*(\d*)\s*romsets\s*found.*$"                
            
            p_good           = re.compile( search_string_good, )
            p_bad            = re.compile( search_string_bad, )
            p_best_available = re.compile( search_string_best_available, )
            p_not_found      = re.compile( search_string_not_found, )
            p_no_roms        = re.compile( search_string_no_roms, )
            #p_result         = re.compile( search_string_result, )                
            
            line_number = 0
            audit_number = 0
            
            for x in sorted( the_games ):

                # 行数太多
                # 删减一些
                if line_number > 5000:
                    line_number = line_number - 4500
                    the_text.delete("1.0", "4501.0")
        
                audit_number = number_good + number_best_available + number_bad + number_not_found + number_no_roms
                
                
                label_audited.configure(text=r"已检校验的数目："+str(audit_number))
                the_progressbar.step()
            
                new_command_list = command_list + [x,]
                
                lines = []
                
                proc = subprocess.Popen(new_command_list, stdout = subprocess.PIPE ,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=self.ini_data["use_shell"],cwd=mame_dir,encoding='utf_8')
        
                for line in proc.stdout:
                    lines.append(line)
                
                for line in lines:
                    line_number += 1
        
                    the_text.insert(tk.END, line, )

                    m=p_good.search( line ) 
                    if m : 
                        number_good += 1
                        list_good.append( m.group(1) )
                        continue
                
                    m=p_best_available.search( line ) 
                    if m : 
                        number_best_available += 1
                        list_best_available.append( m.group(1) )
                        continue
                
                    m=p_bad.search( line ) 
                    if m : 
                        number_bad += 1
                        #list_bad.append( m.group(1) )
                        continue
                        
                    m=p_not_found.search( line ) 
                    if m : 
                        number_not_found += 1
                        continue
                    
                    m=p_no_roms.search( line ) 
                    if m : 
                        number_no_roms += 1
                        continue
                
            the_progressbar.configure(value=100)
            # 进度条跑满
            
            the_text.see(tk.END)
            # 显示到最后一行
            
            audit_number = number_good + number_best_available + number_bad + number_not_found + number_no_roms            
            
            label_audited.configure(text=r"已检校验的数目："+str(audit_number))
            # label 记录 
            
            the_button.configure( text = "" )

            label_good.configure(text=r"good 数量 (校验通过，正确)：" + str(number_good))
            label_best_available.configure(text=r"best available 数量(校验通过，有 bad dump 或 no dump 是这种提示)："+str(number_best_available))
            label_bad.configure(text=r"bad 数量 (校验未通过，错误)："+str(number_bad))
            label_not_found.configure(text=r"not found 数量 (校验未通过，错误)："+str(number_not_found))
            label_no_roms.configure(text=r"no roms 数量 (没有 roms 的 device，好像是这种提示 )："+str(number_no_roms))
            label_both.configure(text=r"OK 数量 (校验通过的) (good + best available)：" + str(number_good + number_best_available) )
            
            
            #######↑↑
            
            temp_set  = set(list_good) | set(list_best_available)
            
            
            self.data['set_data']['available_set'] = self.data['set_data']['all_set'] & temp_set
            self.data['set_data']['unavailable_set'] = self.data['set_data']['all_set'] - self.data['set_data']['available_set']
            
            del temp_set
            
            # 保存数据
            save_pickle.save(self.data['set_data']['available_set'],self.available_gamelist_file_path)
            self.other_functions_mark_available_games() # 列表 标记
            
            the_finish_button.grid()
            
            window.update()
            window.deiconify()
            window.lift()
        
        def test_threading():
            thread = threading.Thread(target=start_work)
            thread.start()


        the_progressbar=ttk.Progressbar(window,orient=tk.HORIZONTAL)
        the_progressbar.grid(row=n,column=0,sticky=tk.W+tk.N+tk.E)
        n += 1
        
        the_button = ttk.Button(window,text="开始校验",command=test_threading)
        #the_button = ttk.Button(window,text="开始校验",command=start_work)
        the_button.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1
        
        label_last = ttk.Label(window,text="")
        label_last.grid(row=n,column=0,sticky=tk.W+tk.N)
        n += 1  

        the_finish_button = ttk.Button(window,text="跳转到游戏列表",command=exit_for_window)
        the_finish_button.grid(row=n,column=0,sticky=tk.W+tk.N)
        the_finish_button.grid_remove()
        n += 1      
        
        frame_for_text = ttk.Frame(window)
        frame_for_text.grid(row=n,column=0,sticky=tk.W+tk.N+tk.E+tk.S)
        
        window.rowconfigure(n,weight=1)
        frame_for_text.rowconfigure(0,weight=1)
        
        frame_for_text.columnconfigure(0,weight=1)
        frame_for_text.rowconfigure(0,weight=1)        
        
        the_text = tk.Text(frame_for_text,undo=False,wrap=tk.NONE)
        scrollbar_1 = ttk.Scrollbar( frame_for_text, orient=tk.VERTICAL, command=the_text.yview)
        scrollbar_2 = ttk.Scrollbar( frame_for_text, orient=tk.HORIZONTAL, command=the_text.xview)
        
        the_text.configure(yscrollcommand=scrollbar_1.set)
        the_text.configure(xscrollcommand=scrollbar_2.set)
        
        the_text.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        ttk.Sizegrip(frame_for_text).grid(row=1,column=1)
        
        window.protocol("WM_DELETE_WINDOW", exit_for_window)        
        window.wait_window()


    # 菜单 callback 函数：游戏列表→拥有列表，# 拥有列表标记
    def menu_call_back_function_gamelist_use_available_game_mark(self,):
        self.ini_data["use_available_game_mark"] = self.menu_gamelist_use_available_game_mark.get()

    # 菜单 callback 函数：游戏列表→拥有列表，过滤 
    #    Toplevel   过滤窗口
    def menu_call_back_function_window_available_filter(self,):
    
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        print()
        print(temp)
        print(size)        
        
        window.title("拥有列表过滤")
        window.geometry(size)
             
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.rowconfigure(0, weight=1)
        #window.columnconfigure(0, weight=1) 
        
        available_filter_bios = tk.IntVar()
        available_filter_device = tk.IntVar()
        available_filter_mechanical = tk.IntVar()
        available_filter_no_roms = tk.IntVar()        
        
        
        
        def for_ok_button():
        
            window.destroy()
            
            # self.filter
            
            if available_filter_bios.get():
                self.filter.add("bios")
            else :
                self.filter.discard("bios")

            if available_filter_device.get():
                self.filter.add("device")
            else:
                self.filter.discard("device")

            if available_filter_mechanical.get():
                self.filter.add("mechanical")
            else:
                self.filter.discard("mechanical")

            #if available_filter_no_roms.get():    
            #    self.filter.add("no_roms")
            #else:
            #    self.filter.discard("no_roms")

            self.filter_set = set() # 重置 ，重新计算
            
            for x in self.filter:
                if x in self.data['internal_index']:
                    self.filter_set = self.filter_set | set(self.data['internal_index'][x]["gamelist"])
            
            print('available_set')
            print(len(self.data['set_data']['available_set']))
            print("self.filter_set")
            print(len(self.filter_set))
            print("self.filter")
            print(len(self.filter))

            if self.ini_data["index_be_chosen"] == 'available_set':
                self.ini_data["index_be_chosen"] ="" # 重置
            
            try:
                self.tree_index.see('available_set')
                self.tree_index.selection_set(('available_set',))
                self.choose_index( 'available_set' )
            except:
                pass



        #self.filter
        

        
        if 'bios'       in self.filter :
            available_filter_bios.set(1)
        else:
            available_filter_bios.set(0)
        
        if 'device'     in self.filter : 
            available_filter_device.set(1)
        else:
            available_filter_device.set(0)
        
        if 'mechanical' in self.filter : 
            available_filter_mechanical.set(1)
        else:
            available_filter_mechanical.set(0)
        
        #if 'no_roms'        in self.filter : 
        #    available_filter_no_roms.set(1)
        #else:
        #    available_filter_no_roms.set(0)
        
        n=0
        if 'bios' in self.data['internal_index']:
            bios_set_checkbutton  = ttk.Checkbutton(window, text="bios",variable=available_filter_bios)
            bios_set_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),)
            n+=1

        if "device" in self.data['internal_index']:
            device_set_checkbutton = ttk.Checkbutton(window, text="device",variable= available_filter_device )
            device_set_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),)
            n+=1

        if "mechanical" in self.data['internal_index']:
            mechanical_set_checkbutton = ttk.Checkbutton(window, text="mechanical",variable=available_filter_mechanical)
            mechanical_set_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),)
            n+=1
        
        #if "no_roms" in self.data['internal_index']:
        #    no_roms_checkbutton = ttk.Checkbutton( window, text="no_roms",variable=available_filter_no_roms )
        #    no_roms_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),) 
        #    n+=1
            
        button=ttk.Button(window,text="确认",command=for_ok_button)
        button.grid(row=n,column=0,sticky=(tk.W,tk.N),) 
        
        window.wait_window()

    def menu_call_back_function_gamelist_load_translation(self,):
        # 翻译
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = temp
        #size = "400x300" + temp
        #print()
        #print(temp)
        #print(size)
        window.geometry(size)
        
        window.title("导入翻译文件")
        
             
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        #window.rowconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)         
        
        def load_default_translation_file():
            
            file_name = self.data_from_main["translation_file_name"]
            file_encoding = "utf_8_sig"
            
            temp_file_name_gamelist = self.data_from_main["temp_file_name_gamelist"]
                #"temp_file_name_gamelist" :temp_file_name_gamelist,
             
            if not os.path.isfile(file_name):
                text = r"翻译文件不存在：" + file_name
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            
            translation_dict={}
            
            try:
                translation_dict = jjui.initial_translation.read_translation_file( file_name,file_encoding )
            except:
                text = r"读取翻译文件，出错。注意将文件的 文本编码 保存为 uft-8-bom"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            if len( translation_dict ) == 0 :
                text = r"读取翻译文件，翻译数量为 0 ，翻译任务取消"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
                
            if len( translation_dict ) > 0 :
                # self.data['set_data']['all_set']
                
                set_1 = set( translation_dict.keys() )
                
                translationed_set = set_1 & self.data['set_data']['all_set']
                
                un_translationed_set = self.data['set_data']['all_set'] - translationed_set
            
            if len( translationed_set ) == 0 :
                text = r"有效翻译数量为 0 ，翻译任务取消"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            if len( translationed_set ) > 0 :
                
                f1 = open( temp_file_name_gamelist , 'rb')
                data = pickle.load( f1 )
                f1.close()
                
                # 添加翻译内容
                new_data = jjui.initial_translation.add_translation( translation_dict = translation_dict , gamelist_dict = data )
                
                # 保存到文件
                f2 = open( temp_file_name_gamelist , 'wb')
                pickle.dump( new_data , f2 )
                f2.close
                
                # Treeview 中修改
                
                if "translation" in self.tree['columns']:
                    for x in un_translationed_set:
                        self.tree.set(x,column="translation", value=new_data[x]["description"])
                        # 默认值 description 
                
                if "translation" in self.tree['columns']:
                    for x in translationed_set:
                        self.tree.set(x,column="translation", value=new_data[x]["translation"])
                        # 翻译值 translation
            
            window.destroy()
            
            
        def load_translation_file():

            file_name     = new_file_path.get()
            file_encoding = new_encoding.get()
            
            
            if file_name =="":
                text = r"未指翻译定文件"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            temp_file_name_gamelist = self.data_from_main["temp_file_name_gamelist"]
                #"temp_file_name_gamelist" :temp_file_name_gamelist,
             
            if not os.path.isfile(file_name):
                text = r"翻译文件不存在：" + file_name
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            
            translation_dict={}
            
            try:
                translation_dict = jjui.initial_translation.read_translation_file( file_name,file_encoding )
            except:
                text = r"读取翻译文件，出错。注意选择正确的文件、正确的文字编码"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            if len( translation_dict ) == 0 :
                text = r"读取翻译文件，翻译数量为 0 ，翻译任务取消"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
                
            if len( translation_dict ) > 0 :
                # self.data['set_data']['all_set']
                
                set_1 = set( translation_dict.keys() )
                
                translationed_set = set_1 & self.data['set_data']['all_set']
                
                un_translationed_set = self.data['set_data']['all_set'] - translationed_set
            
            if len( translationed_set ) == 0 :
                text = r"有效翻译数量为 0 ，翻译任务取消"
                tkinter.messagebox.showwarning(message=text)
                window.lift(self.parent)
                return 0
            
            if len( translationed_set ) > 0 :
                
                f1 = open( temp_file_name_gamelist , 'rb')
                data = pickle.load( f1 )
                f1.close()
                
                # 添加翻译内容
                new_data = jjui.initial_translation.add_translation( translation_dict = translation_dict , gamelist_dict = data )
                
                # 保存到文件
                f2 = open( temp_file_name_gamelist , 'wb')
                pickle.dump( new_data , f2 )
                f2.close
                
                # Treeview 中修改
                
                if "translation" in self.tree['columns']:
                    for x in un_translationed_set:
                        self.tree.set(x,column="translation", value=new_data[x]["description"])
                        # 默认值 description 
                
                if "translation" in self.tree['columns']:
                    for x in translationed_set:
                        self.tree.set(x,column="translation", value=new_data[x]["translation"])
                        # 翻译值 translation
            
            window.destroy()        

        n=0
        
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        # 默认 翻译 文件
        ttk.Label(window,text= r"默认翻译文件：" + self.data_from_main["translation_file_name"]).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text= r"默认翻译文件，文字编码为：utf_8_sig").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Button(window,text="读取默认翻译文件",width=-1,command = load_default_translation_file).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        
        #
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        
        # 其它文件
        ttk.Label(window,text="另外选择翻译文件:").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        #ttk.Label(window,text="选择文件：").grid(row=5,column=0,columnspan=2,sticky=tk.W+tk.N,)
        
        def choose_file():
            file_name = tkinter.filedialog.askopenfilename(initialdir=".")
            if file_name:
                new_file_path.set(file_name)
            window.lift(self.parent)
            
        ttk.Button(window,text="选择",width=-1,command=choose_file).grid(row=n,column=0,sticky=tk.W+tk.N,)
        
        new_file_path = tk.StringVar()
        ttk.Entry(window,textvariable=new_file_path).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
        
        n+=1
        
        
        ttk.Label(window,text="文字编码为：").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        def change_encoding():
            new_encoding_entry.configure(state="normal")
        
        ttk.Button(window,text="修改",width=-1,command=change_encoding).grid(row=n,column=0,sticky=tk.W+tk.N,)
        
        new_encoding=tk.StringVar()
        new_encoding.set("utf_8_sig")
        new_encoding_entry = ttk.Entry(window,textvariable=new_encoding)
        new_encoding_entry.grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
        new_encoding_entry.configure(state="disabled")
        
        n+=1
        
        ttk.Button(window,text="读取指定翻译文件",width=-1,command = load_translation_file).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        n+=1
        
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text="编码提示：").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text="推荐将文本保存为，utf_8_sig （utf-8 带 bom），可以包含多国文字").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1        
        
        ttk.Label(window,text="简体中文可能用到的文本编码：gb2312 、gbk 、gb18030 、……").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text="繁体中文可能用到的文本编码：big5 、……").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1        
        
        #for x in ("ascii","gb2312","gbk","gb18030","big5","utf_8","utf_8_sig"):
        #    ttk.Label(window,text=x).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        #    n+=1        
       
        window.wait_window()

    # 菜单 callback 函数： 游戏列表→游戏列表 数量，
    #   验证 对比 ，以后 可以 删掉 这个
    def menu_call_back_function_gamelist_count(self,event=None):
        
        count = 0
        
        for x in self.tree.get_children(""):
            for y in self.tree.get_children(x):
                count += 1
            count += 1
        
        messagebox.showinfo(    title   = "数量", 
                                message = "当前游戏列表数量为：" + str(count),
                                )

        print(count)

    # 菜单 callback 函数：关于→关于
    #    Toplevel   关于 窗口
    def menu_call_back_function_window_about(self,):
        about_window = tk.Toplevel()
        
        about_window.resizable(width=True, height=True)

        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "800x600" + temp
        print()
        print(temp)
        print(size)
        
        about_window.title("关于")
        about_window.geometry(size)
             
        about_window.transient(self.parent)
        about_window.lift(self.parent)
        #about_window.grab_set()
        
        about_window.rowconfigure(0, weight=1)
        about_window.columnconfigure(0, weight=1)

        
        text  = "JJui" + "\n"
        text += "街机游戏列表显示器" + "\n"
        text += "JJ 取自 “街机” 的拼音首字母" + "\n"
        text += "\n"
        
        text += "JJui 只是一个 前端／UI／GUI／front-end " + "\n"
        text += "需要配合 MAME 使用 " + "\n"
        text += "需要的游戏文件，也要靠自己找" + "\n"
        text += "\n"
        
        text += "不是程序员" + "\n"
        text += "如果有程序员看到我的代码，觉得太菜" + "\n"
        text += "不用奇怪" + "\n"
        text += "毕竟不是专业的" + "\n"
        text += "\n"
        
        text += "看了篇 Python 的 tkinter 说明" + "\n"
        text += "觉得可以动手写一下" + "\n"
        text += "很快就把列表显示出来了" + "\n"
        text += "但光一个列表不够啊" + "\n"
        text += "……" + "\n"
        text += "反正到现在" + "\n"
        text += "自己觉得" + "\n"
        text += "用是可以用了" + "\n"
        text += "简单是简单了一点" + "\n"
        text +=  "\n"
        
        text += "有 意见／建议 可以尽管说" + "\n"
        text += "但是个人 能力／时间／精力／兴趣 有限" + "\n"
        text += "大概率很难让大家满意" + "\n"
        text += "\n"
        
        text += "大家，各位街机游戏爱好者，可以免费使用" + "\n"
        text += "\n"
        
        text += "本人在琵琶行的 ID ：gdicnng" + "\n"
        text += "邮箱：gdicnng@sina.com" + "\n"
        text += "源代码：https://gitee.com/gdicnng/JJui" + "\n"
        text += "第一次上传时间： 2021年06月" + "\n"
        text +=  "\n"
        
        text += "如果觉得有必要 支持／打赏／赞助 一下" + "\n"
        text += "以下是我的 支付宝／微信 收钱码" + "\n"
        text += "\n"
        text += "\n"
        text += "\n"

        
        t = tk.Text(about_window,undo=False,padx=10,pady=10,spacing1=2,spacing2=2,spacing3=2)
        
        scrollbar_1 = ttk.Scrollbar( about_window, orient=tk.VERTICAL, command=t.yview)
        
        scrollbar_2 = ttk.Scrollbar( about_window, orient=tk.HORIZONTAL, command=t.xview)
        
        t.configure(yscrollcommand=scrollbar_1.set)
        t.configure(xscrollcommand=scrollbar_2.set)
        
        t.grid(row=0,column=0,stick=(tk.W,tk.N,tk.E,tk.S))
        scrollbar_1.grid(row=0,column=1,columnspan=2,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        t.insert("1.0", text, )
        
        try:
            image_zhifubao = Image.open( self.data_from_main['image_path_zhifubao'] )
            image_weixin = Image.open(   self.data_from_main['image_path_weixin'])
            
            size_1=image_zhifubao.size
            a=800/size_1[0]
            new_size_1 = (int(size_1[0]*a),int(size_1[1]*a))
            
            image_zhifubao = image_zhifubao.resize( new_size_1,Image.BILINEAR, )
            image_zhifubao = ImageTk.PhotoImage( image_zhifubao  )
            
            size_2=image_weixin.size
            b=800/size_2[0]
            new_size_2 = ( int(size_2[0]*b),int(size_2[1]*b))
            
            image_weixin = image_weixin.resize( new_size_2,Image.BILINEAR, )
            image_weixin = ImageTk.PhotoImage( image_weixin )
            
            t.image_create(tk.END,image=image_zhifubao)
            t.insert("1.0", "\n", )
            t.image_create(tk.END,image=image_weixin)
        except:
            pass
        
        t["state"]="disabled"
        
        about_window.wait_window()

    # 菜单 callback 函数：关于→文档
    def menu_call_back_function_open_html_file(self,):
        html_file = self.data_from_main['docs_html_index_file']
        if os.path.isfile(html_file):
            html_file = os.path.abspath(html_file)
            webbrowser.open(url=html_file,)
        

    # # # # # # 
    # index 右键 菜单 ,目录列表，全部收起
    def index_pop_up_menu_function_hide_level2(self,):
        
        # # 三层
        # flag_3_level = False
        # count = 0
        # 
        # for x in self.tree_index.get_children():
        #     for y in self.tree_index.get_children(x):
        #         for z in self.tree_index.get_children(y):
        #         
        #             flag_3_level = True
        #             
        #             self.tree_index.item(y,open=False) # 收起第二层
        #             
        #             break 
        #         
        #         self.tree_index.item(x,open=False) # 收起第一层
        #         
        #         count += 1
        #         
        #         if count > 3 :
        #             if not flag_3_level:
        #                 # 连续三次，都没有三层，不再检查第三层了
        #                 # 考虑到 万一：第一项没有第三层；但后面的项目有第三层
        #                 break
        
        # 两层
        for x in self.tree_index.get_children():
            for y in self.tree_index.get_children(x):
                self.tree_index.item(x,open=False) 
                break
        
    # index 右键 菜单 ,编辑
    def index_pop_up_menu_function_edit(self,):
        pass
    
    
    # gamelist ，标题处，右键 菜单 ，选择 显示 哪些 列
    # a topleve window 
    def gamelist_pop_up_menu_of_heading_choose_columns( self ,):
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
        
        # self.ini_data
            # self.ini_data["gamelist_columns_to_show_1"] # 第1组
            # self.ini_data["gamelist_columns_to_show_2"] # 第2组
            # self.ini_data["gamelist_columns"]           # 第3组
        # self.data_from_main
            # "columns"                                   # 第0组 ,所有项
            # "columns_translation"
        
        # self.gamelist_change_mark
            # top_binding_gamelist_change 函数中
            
        # self.tree
        
        # self.menu_call_back_function_save_ini_data()
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("选择游戏列表显示项目")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        size = temp
        window.geometry( size )
             
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        
        def add_to(add_to_a_listbox):# 第0组，选中项，添加到 另一组
            # listbox0
            a_listbox = add_to_a_listbox
            for x in listbox0.curselection():# 得到 index ，tuple 格式
                content=listbox0.get(x)
                if content in a_listbox.get(0,tk.END) :
                    print("已有")
                else:
                    a_listbox.insert(tk.END,content)  

        def delete_from_a_listbox(a_listbox):# 第1、2、3组，中，删除选中项
            x = a_listbox.curselection() # 得到 index ，tuple 格式
            if len(x) == 1 : # 如果不是 空 tuple ,且，只选中一项
                index = x[0]
                a_listbox.delete( index )
                a_listbox.selection_set( index )# 选中
        
        def move_up(a_listbox):# listbox 中的选项，选中项，向上移
            x = a_listbox.curselection() # 得到 index ，tuple 格式
            if len(x) == 1 : # 如果不是 空 tuple ,且，只选中一项
                index = x[0]
                if index>0: # 如果不是在最上边
                    content = a_listbox.get(index) 
                    a_listbox.delete(index) # 删除
                    a_listbox.insert(index-1,content) # 重新添加到上一行
                    a_listbox.selection_set(index-1)# 选中
        
        def move_down(a_listbox):# listbox 中的选项，选中项，向下移
            x = a_listbox.curselection() # 得到 index ，tuple 格式
            if len(x) == 1 : # 如果不是 空 tuple ,且，只选中一项
                index = x[0]
                if index < a_listbox.size() - 1 : # 如果不是在最下边
                    content = a_listbox.get(index) 
                    a_listbox.delete(index) # 删除
                    a_listbox.insert(index+1,content) # 重新添加到下一行
                    a_listbox.selection_set(index+1)# 选中
        
        def button_ok():
        
            print("button_ok")
            
            def get_content(a_listbox):
                
                temp_list = []
                
                for x in range(a_listbox.size()):
                
                    content = a_listbox.get(x)
                    
                    flag = False 
                    
                    # 有翻译的项目
                    for column in self.data_from_main["columns_translation"]:
                        if content == self.data_from_main["columns_translation"][column]:
                            flag = True
                            temp_list.append(column)
                            break
                    
                    # 无翻译译的项目
                    if not flag:
                        temp_list.append(content)
                
                return tuple( temp_list )
            
            
            
            print(get_content(listbox1))
            print(get_content(listbox2))
            print(get_content(listbox3))
            
            self.ini_data["gamelist_columns_to_show_1"] = get_content(listbox1)
            self.ini_data["gamelist_columns_to_show_2"] = get_content(listbox2)
            self.ini_data["gamelist_columns"]           = get_content(listbox3)
            
            try:
                del self.gamelist_change_mark # top_binding_gamelist_change 函数中
                # 删除标记，跳转到第1组
            except:
                pass
            
            def get_columns(old_columns): # 检查，有没有超出范围
                temp_list = []
                for x in old_columns:
                    if x in self.tree["columns"]:
                        temp_list.append(x)
                new_columns = tuple( temp_list )
                return new_columns            
            
            # 显示第一组
            self.tree.configure( displaycolumns = get_columns(self.ini_data["gamelist_columns_to_show_1"] ),)

            self.menu_call_back_function_save_ini_data()

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
        
        ttk.Label(window,text="第1组，默认使用中文列表，程序打开时，默认显示第1组。显示内容可以自己调整。",).grid(row=1,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位
        ttk.Label(window,text="第2组，默认使用英文列表，方便中英对照。显示内容可以自己调整。",).grid(row=2,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位
        ttk.Label(window,text="第3组，默认显示所有列。修改显示内容需要注意：",).grid(row=3,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位
        ttk.Label(window,text="第3组，添加／移除 项目之后，需要关闭本程序，重新打开后生效。",).grid(row=4,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位
        ttk.Label(window,text="第3组，未选择的项目，游戏列表从一开始，就不会读取相关数据。",).grid(row=5,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位
        ttk.Label(window,text="所以，第1组、第2组，选择的项目，应比第3组少；",).grid(row=6,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位
        ttk.Label(window,text="否则，关闭程序，重新打开后，多选的项目，也不会显示。",).grid(row=7,column=0,columnspan=4,sticky=(tk.E,tk.W),) # 占位

        button_ok = ttk.Button(window,text="确认，确认后跳转到第1组",command=button_ok)
        button_ok.grid(row=8,column=0,columnspan=4,sticky=(tk.E,tk.S),)
        
        frame0.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)
        frame1.grid(row=0,column=1,sticky=(tk.W,tk.N,tk.E,tk.S),)
        frame2.grid(row=0,column=2,sticky=(tk.W,tk.N,tk.E,tk.S),)
        frame3.grid(row=0,column=3,sticky=(tk.W,tk.N,tk.E,tk.S),)
        
        for x in (frame0,frame1,frame2,frame3,):
            #x.rowconfigure(0,weight=1)
            x.columnconfigure(0,weight=1)
        
        h = len( self.data_from_main["columns"] )
        
        # frame0
        ttk.Label(frame0,text="内容").grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        
        listbox0 = tk.Listbox(frame0,height=h, )
        listbox0.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)
        
        for x in self.data_from_main["columns"]:
            if x in self.data_from_main["columns_translation"]:
                listbox0.insert(tk.END,self.data_from_main["columns_translation"][x])
            else:
                listbox0.insert(tk.END,x)
        
        button_add_to_1=ttk.Button(frame0,text="添加到第1组",width=-1,command=lambda x=None: add_to(listbox1))
        button_add_to_2=ttk.Button(frame0,text="添加到第2组",width=-1,command=lambda x=None: add_to(listbox2))
        button_add_to_3=ttk.Button(frame0,text="添加到第3组",width=-1,command=lambda x=None: add_to(listbox3))
        
        button_add_to_1.grid()
        button_add_to_2.grid()
        button_add_to_3.grid()
        
        # frame1
        ttk.Label(frame1,text="第1组").grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        listbox1 = tk.Listbox(frame1,height=h, )
        listbox1.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)

        for x in self.ini_data["gamelist_columns_to_show_1"]:
            if x in self.data_from_main["columns_translation"]:
                listbox1.insert(tk.END,self.data_from_main["columns_translation"][x])
            else:
                listbox1.insert(tk.END,x)
        
        button_delete_from_1=ttk.Button( frame1 ,width=-1,text="从第1组移除",command=lambda x=None:delete_from_a_listbox(listbox1))
        button_delete_from_1.grid()
        
        button_move_up_1=ttk.Button( frame1 ,width=-1,text="上移",command=lambda x=None:move_up(listbox1))
        button_move_up_1.grid()
        
        button_move_down_1=ttk.Button( frame1 ,width=-1,text="下移",command=lambda x=None:move_down(listbox1))
        button_move_down_1.grid()

        # frame2
        ttk.Label(frame2,text="第2组").grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        listbox2 = tk.Listbox(frame2,height=h, )
        listbox2.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)

        for x in self.ini_data["gamelist_columns_to_show_2"]:
            if x in self.data_from_main["columns_translation"]:
                listbox2.insert(tk.END,self.data_from_main["columns_translation"][x])
            else:
                listbox2.insert(tk.END,x)

        button_delete_from_2=ttk.Button( frame2 ,text="从第2组移除",command=lambda x=None:delete_from_a_listbox(listbox2))
        button_delete_from_2.grid()
        
        button_move_up_2=ttk.Button( frame2 ,width=-1,text="上移",command=lambda x=None:move_up(listbox2))
        button_move_up_2.grid()
        
        button_move_down_2=ttk.Button( frame2 ,width=-1,text="下移",command=lambda x=None:move_down(listbox2))
        button_move_down_2.grid()

        # frame3
        ttk.Label(frame3,text="第3组").grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        listbox3 = tk.Listbox(frame3,height=h, )
        listbox3.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)

        for x in self.ini_data["gamelist_columns"]:
            if x in self.data_from_main["columns_translation"]:
                listbox3.insert(tk.END,self.data_from_main["columns_translation"][x])
            else:
                listbox3.insert(tk.END,x)
                
        button_delete_from_3=ttk.Button( frame3 ,text="从第3组移除",command=lambda x=None:delete_from_a_listbox(listbox3))
        button_delete_from_3.grid()
        
        button_move_up_3=ttk.Button( frame3 ,width=-1,text="上移",command=lambda x=None:move_up(listbox3))
        button_move_up_3.grid()
        
        button_move_down_3=ttk.Button( frame3 ,width=-1,text="下移",command=lambda x=None:move_down(listbox3))
        button_move_down_3.grid()
        
    # gamelist 右键 菜单 ，运行此游戏
    def gamelist_pop_up_menu_start_game( self,):
        game_name = self.tree.focus()
        self.call_mame( game_name )
    # gamelist 右键 菜单 ，运行此游戏，不隐藏 UI
    def gamelist_pop_up_menu_start_game_ui_not_hide( self,):
        game_name = self.tree.focus()
        self.call_mame( game_name ,hide=False) 
    # gamelist 右键 菜单 ，运行此游戏，开启多键盘功能
    def gamelist_pop_up_menu_start_game_multikeyboard( self,):
        game_name = self.tree.focus()
        other_option = ["-multikeyboard",]
        self.call_mame( game_name ,other_option)
    # gamelist 右键 菜单 ，当前列表 展开
    def gamelist_pop_up_menu_show_clone(self,):
        for x in self.tree.get_children(""):
            for y in self.tree.get_children(x):
                self.tree.item(x,open=True)
                break
    # gamelist 右键 菜单 ，当前列表 收起
    def gamelist_pop_up_menu_hide_clone(self,):
        for x in self.tree.get_children(""):
            for y in self.tree.get_children(x):
                self.tree.item(x,open=False)
                break
    # gamelist 右键 菜单 ，导出当前游戏列表
    def gamelist_pop_up_menu_export_gamelist(self,):
        file_name = self.data_from_main['export_text_file']
        
        temp_set = set()
        
        for x in self.tree.get_children(""):
            temp_set.add(x)
            for y in self.tree.get_children(x):
                temp_set.add(y)
        
        f = open( file_name , 'wt',encoding='utf_8')
        for x in sorted( temp_set ):
            print(x,file=f)
        f.close()
        
        del temp_set
    # gamelist 右键 菜单 ，导出选中游戏
    def gamelist_pop_up_menu_export_gamelist_select_items(self,):
        file_name = self.data_from_main['export_text_file']
        
        items = self.tree.selection()
        
        if len(items) > 0 :

            f = open( file_name , 'wt',encoding='utf_8')
            for x in sorted( items ):
                print(x,file=f)
            f.close()
        
        del items    
    # gamelist 右键 菜单 ，verifyroms
        #   windows 路径需要设到 mame 文件夹
    def gamelist_pop_up_menu_verify_roms(self,):
        game_name = self.tree.focus()
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()     
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_name )
        command_list.append( "-verifyroms" )
        
        content=[]
        p = subprocess.Popen( command_list, 
                            shell=self.ini_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8",
                            cwd=mame_dir,
                            )
        for line in p.stdout:
            #print(line,end='')
            content.append(line)
                
        self.show_text_winodw(content=content,title="-verifyroms",)
    # gamelist 右键 菜单 ，verifysamples
        #   windows 路径需要设到 mame 文件夹
    def gamelist_pop_up_menu_verify_samples(self,):
        game_name = self.tree.focus()

        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()     
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_name )
        command_list.append( "-verifysamples" )
        
        content=[]
        p = subprocess.Popen( command_list, 
                            shell=self.ini_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8",
                            cwd=mame_dir,
                            )
        for line in p.stdout:
            #print(line,end='')
            content.append(line)       
        
        self.show_text_winodw(content=content,title="-verifysamples",)
    # gamelist 右键 菜单 ，listroms
    def gamelist_pop_up_menu_list_roms(self,):
        game_name = self.tree.focus()
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()    
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_name )
        command_list.append( "-listroms" )
        
        content=[]
        p = subprocess.Popen( command_list, 
                            shell=self.ini_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8"
                            )
        
        for line in p.stdout:
            #print(line,end='')
            content.append(line)
        
        self.show_text_winodw(content=content,title="-listroms",)
    # gamelist 右键 菜单 ，listxml
    def gamelist_pop_up_menu_list_xml(self,):
        game_name = self.tree.focus()
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_name )
        command_list.append( "-listxml" )
        command_list.append( "-nodtd" )
        
        content=[]
        p = subprocess.Popen( command_list, 
                            shell=self.ini_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8"
                            )

        for line in p.stdout:
            #print(line,end='')
            content.append(line)
        
        self.show_text_winodw(content=content,title="-listxml",)
    # gamelist 右键 菜单 ，切换 多选模式 ／ 单选模式 
    def gamelist_pop_up_menu_select_mode(self,):
        if self.menu_mouse_multi_select_mode_flag.get() :
            self.tree.configure(selectmode = 'extended')
        else:
            self.tree.configure(selectmode = 'browse')
    # gamelist 右键 菜单 ，添加到目录
    #       Toplevel window
    def gamelist_pop_up_menu_add_to_index(self,items=set() ):
        
        # 参数
        # 得到的 items 应该是 tupple 格式的，转为 set
        items = set( items )

        # a topleve window 
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title("添加到 自定义目录")
        
        temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        size = "400x300" + temp
        window.geometry( size )
             
        window.lift(self.parent)
        window.transient(self.parent)
        #window.grab_set()
        
        window.rowconfigure(0,weight=1)
        window.rowconfigure(1,weight=0)
        window.columnconfigure(0,weight=1)

        tree = ttk.Treeview(window,columns="file",selectmode='browse',)
        tree.grid(row=0,column=0,sticky=(tk.W, tk.N, tk.E, tk.S) )
        
        scrollbar_1 = ttk.Scrollbar( window, orient=tk.VERTICAL, command = tree.yview)
        scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.E))
        
        tree.configure( yscrollcommand = scrollbar_1.set)
        
        def add_items_to_select_index():
        
            selected_id = tree.focus()
            
            if selected_id == "" : return 0 # 无选中项为 ""
            
            parent = tree.parent( selected_id )
            
            if parent == "" : # 一级列表
                # 如果 已经 全包含了，退出
                if items.issubset( self.ini_set_dict[selected_id]["ROOT_FOLDER"] ):
                    print("已包含所选项目")
                    window.destroy()
                    return 0
                
                # 如果没有全包含
                
                file_path = selected_id.split(r"|",1)[0]
                self.ini_files_be_edited.add(file_path) # 记录
                print( self.ini_files_be_edited )
                
                # 转为 set
                temp = set( self.ini_set_dict[selected_id]["ROOT_FOLDER"] )
                # 合并
                temp = items | temp
                # 转回 list
                self.ini_set_dict[selected_id]["ROOT_FOLDER"] = list( temp )
                
            else:# 二级列表
                key_parent = parent
                key_self   = selected_id.split(r"|",1)[1]
                
                if items.issubset( self.ini_set_dict[parent][key_self] ):
                    print("已包含所选项目")
                    window.destroy()                
                    return 0
                
                file_path = parent
                self.ini_files_be_edited.add(file_path) # 记录
                print( self.ini_files_be_edited )
                
                # 转为 set
                temp = set( self.ini_set_dict[key_parent][key_self] )
                # 合并
                temp = items | temp
                # 转回 list
                self.ini_set_dict[parent][key_self] = list( temp )
            
            window.destroy()
            

        button = ttk.Button(window,text = "确认" ,command=add_items_to_select_index)
        button.grid(row=1,column=0,columnspan=2,sticky=(tk.E, tk.S,))

        tree.heading("#0", text="目录" )
        tree.heading("#1", text="文件路径" )

        # 第一层
        for x in self.ini_set_dict:
            if x in self.ini_files_editable :
                # x 为 路径 + 名称
                # self.ini_files[x] 为 名称，无路径
                tree.insert('','end',iid=x,text=self.ini_files[x],values=(x, ) )
        #第二层
        for x in self.ini_files_editable:
            for y in self.ini_set_dict[x] :
                if y != "FOLDER_SETTINGS":
                    if y != "ROOT_FOLDER":
                        iid_string = x + r"|" + y
                        tree.insert(x,'end',iid = iid_string,text=y,)
    # # gamelist 右键 菜单 ，从目录移除
    def gamelist_pop_up_menu_delete_from_index(self,items=set()):
        
        # 参数
        # 得到的 items 应该是 tupple 格式的，转为 set        
        items =  set( items )
        
        index_id = self.ini_data["index_be_chosen"]
        
        parent = self.tree_index.parent( index_id )
        
        if parent == "" : # 一级列表            
            # 转为 set
            temp = set( self.ini_set_dict[index_id]["ROOT_FOLDER"] )
            # 删
            temp = temp  - items
            # 转回 list
            self.ini_set_dict[index_id]["ROOT_FOLDER"] = list( temp )
            
            # self.ini_data["index_be_chosen"]
            if self.search_mark  : self.search_mark = False # 搜索标记，重置。（万一之前是搜索状态）
            self.index_set_remembered  = self.ini_set_dict[index_id]["ROOT_FOLDER"]
            self.gamelist_show( self.ini_set_dict[index_id]["ROOT_FOLDER"] )
            
        else:# 二级列表
            key_self = index_id.split(r"|",1)[1]
            # 转为 set
            temp = set( self.ini_set_dict[parent][key_self] )
            # 删
            temp = temp - items
            # 转回 list
            self.ini_set_dict[parent][key_self] = list( temp )
            
            # self.ini_data["index_be_chosen"]
            if self.search_mark  : self.search_mark = False # 搜索标记，重置。（万一之前是搜索状态）
            self.index_set_remembered  = self.ini_set_dict[parent][key_self]
            self.gamelist_show( self.ini_set_dict[parent][key_self] )
        
        file_path = index_id.split(r"|",1)[0]
        self.ini_files_be_edited.add(file_path) # 记录
        print( self.ini_files_be_edited )        
    
     
    # 其它函数

    # 目录 ，选择
    def choose_index( self , iid ):
        
        row = iid
        
        
        # 重复行
        if row == self.ini_data["index_be_chosen"]  :
            # 搜索状态 False
            if self.search_mark  == False :
                # 忽略
                pass
            
            # 搜索状态 True
            else:
                # 取消 搜索状态 标记
                self.search_mark = False 
                # 显示 原有 内容
                self.gamelist_show ( self.index_set_remembered  )
        
        # 其它行
        else:
            #if row in self.data['set_data']:
            if self.tree_index.set(row,"type") == "internal_set": # 内部分类
                print("iid:",row)
                # 内部分类
                # 选中的 目录，集合为：
                # self.data['set_data'][row]
                
                if row == 'available_set': # 内部分类【拥有列表】，有过滤选项
                    print( )
                    print("choose_index")
                    print("available_set")
                    print("需过滤")
                    
                    #print(r"self.data['set_data']['available_set']")
                    #print(len(self.data['set_data']['available_set']))
                    #
                    #print(r"self.filter_set")
                    #print( len(self.filter_set) )
                    #
                    #print("self.available_hide_set")
                    #print(len(self.available_hide_set))
                    
                    # 过滤
                    temp = self.available_hide_set | self.filter_set
                    temp = self.data['set_data']['available_set'] - temp

                    print("过滤后")
                    print(len(temp))
                    
                    self.ini_data["index_be_chosen"] = row # 记录 ，目录点击记录
                    self.index_set_remembered = temp
                    
                    if self.search_mark  : self.search_mark = False # 搜索标记，重置。（万一之前是搜索状态）
                    
                    self.gamelist_show ( temp )
                    
                else: # 其它内部分类
                    # 记录
                    self.ini_data["index_be_chosen"] = row # 记录 ，目录点击记录
                    self.index_set_remembered  = self.data['set_data'][row] # 记录 ， 游戏列表 显示 内容记录
                    
                    if self.search_mark  : self.search_mark = False # 搜索标记，重置。（万一之前是搜索状态）
                    
                    # print( len(self.data['set_data'][row]) )
                    self.gamelist_show ( self.data['set_data'][row] )
                    
            elif self.tree_index.set(row,"type") == "internal_list":# 更多内部分类
                # 用 | 分隔第一层，第二层
                # 需要注间的是，万一第二层 的 名字里可能有 | 字符
                
                #   如果没用翻译，可以用 text 选项中的值
                #   如果以后使用了翻译，用 row.split(r"|",1)[1]
                
                # row.split(r"|",1)[0]
                # row.split(r"|",1)[1]

                print("iid:",row)
                
                #self.ini_data["index_be_chosen"] = row # 记录 ，目录点击记录
                #self.index_set_remembered  = self.data['internal_index'][row] # 记录 ，
                
                temp_list = []
                
                parent = self.tree_index.parent(row) # 上一层 的 iid
                if parent == '': # 第一层
                    
                    key_self = row
                    temp_list = self.data['internal_index'][key_self]["gamelist"]
                else: # 第二层
                    
                    # 第一层 ：id
                    key_parent = parent
                    # 第二层 ：自己的 text值 是 分类名
                    key_self = row.split(r"|",1)[1]
                    
                    temp_list = self.data['internal_index'][key_parent]["children"][key_self]["gamelist"]

                self.ini_data["index_be_chosen"]  = row # 记录
                self.index_set_remembered = temp_list
                if self.search_mark  : self.search_mark = False # 搜索标记，重置。（如果之前是搜索状态）  
                self.gamelist_show ( temp_list )
            
            
            else:# 外部分类
            
                # 用 | 分隔第一层，第二层
                # 需要注间的是，万一第二层的 名字里有 | 线
                #
                # 第一层名字，文件名，没有 | 
                # 第二层，可能会有
                # 
                # 所以 
                #   如果没用翻译，可以用 text 选项中的值
                #   如果以后使用了翻译，用 row.split(r"|",1)[1]
                #
                # row.split(r"|",1)[0]
                # row.split(r"|",1)[1]
                
                print("外部分类")
                print("iid:",row)
              
                temp_list = set()

                # self.ini_set_dict
                parent = self.tree_index.parent(row) # 上一层 的 iid
                if parent == '':
                    key_self   = row
                    temp_list  = self.ini_set_dict[key_self]["ROOT_FOLDER"]
                else:
                    key_parent = parent
                    key_self   = row.split(r"|",1)[1]
                    temp_list  = self.ini_set_dict[key_parent][key_self]
                
                self.ini_data["index_be_chosen"]  = row # 记录
                self.index_set_remembered = temp_list # 记录 。
                if self.search_mark  : self.search_mark = False # 搜索标记，重置。（如果之前是搜索状态）
                self.gamelist_show ( temp_list )
    
    # game list 显示，
    def gamelist_show(self,set_to_show):
        
        # list 比 set 节约 空间
        # 外部目录，改为 list 格式，使用时，转为 set 格式
        if type( set_to_show ) == list:
            set_to_show =  set( set_to_show ) 
        
        time_1 = time.time()
        
        # 清理
        # 不用 delete
        # 用 detach
        #      detach 之后，恢复得快
        for x in self.tree.get_children():
            for y in self.tree.get_children(x): 
                # 先清除 第二层 ，
                # 否则恢复 主版本时，连带第二层的克隆版本 一起恢复了
                self.tree.detach(y)
            self.tree.detach(x)
        
        time_2 = time.time()
        
        # 游戏列表应显示的数量
        number = len( set_to_show & self.data['set_data']['all_set'] )
        # tk.StringVar()
        # self.status_bar_number_of_index # 这变量名,之前，取得不太合适
        self.status_bar_number_of_index.set("列表数量："+ str(number) + r'. ')

        # ["all_set"]
        # ["clone_set"]
        # ["parent_set"]
        
        # 分组显示
        if self.ini_data["gamelist_group_mark"] == True : 
        
            temp_parent_set = set_to_show & self.data['set_data']["parent_set"]
            temp_clone_set  = set_to_show & self.data['set_data']["clone_set"]  

            # 主版本 真实 存在的：
            temp_clone_have_parent = []
            
            the_keys = temp_parent_set & set( self.data['dict_data']["parent_to_clone"].keys() )
            
            for parent_game in the_keys:
                temp_clone_have_parent.extend( self.data['dict_data']["parent_to_clone"][parent_game] )
            
            # 转成 set
            temp_clone_have_parent  = set( temp_clone_have_parent )
            # 与之前的，求交集
            temp_clone_have_parent  = temp_clone_have_parent & temp_clone_set
            
            # 主版本 不存在的：
            temp_clone_no_parnet    = temp_clone_set - temp_clone_have_parent
            

            
            # 分组、如果排序标记 有效
            if self.ini_data["gamelist_sorted_by"] in self.tree["columns"]:
            
                # 先加入主版本、以及 temp_clone_no_parnet
                # 排序
                temp_list = []            
            
                for x in ( temp_parent_set | temp_clone_no_parnet ):
                    # .set(iid, column=None, value=None)
                    temp_list.append( ( x , self.tree.set(x,column=self.ini_data["gamelist_sorted_by"]) ))
                        
                temp_list.sort( key=lambda x :x[1] , reverse=self.ini_data["gamelist_sorted_reverse"])
                
                for x in temp_list:# 第 0 项，是游戏名
                    self.tree.move(x[0],'','end')
                    
                del temp_list
                   
                # 再加入 ，副版本 （标准的，有主版本存在的）
                temp_list = []

                for x in temp_clone_have_parent :
                    # .set(iid, column=None, value=None)
                    temp_list.append( (x , self.tree.set(x,column=self.ini_data["gamelist_sorted_by"]) ))
                        
                temp_list.sort( key=lambda x :x[1] , reverse=self.ini_data["gamelist_sorted_reverse"])
                
                for x in temp_list:# 第 0 项，是游戏名
                    # 主版本：
                    # self.data['dict_data']['clone_to_parent'][x[0]]
                    self.tree.move(x[0],self.data['dict_data']['clone_to_parent'][x[0]],'end')

                del temp_list            
            
            # 分组、如果排序标记 无效
            else:
            
                # 先加入主版本、以及 temp_clone_no_parnet
                for x in sorted( temp_parent_set | temp_clone_no_parnet ):
                    self.tree.move(x,'','end')
                    
                # 再加入 ，副版本 （标准的，有主版本存在的）
                for x in sorted( temp_clone_have_parent ):# 第 0 项，是游戏名
                    # 主版本：
                    # self.data['dict_data']['clone_to_parent'][x]
                    self.tree.move(x,self.data['dict_data']['clone_to_parent'][x],'end')

        # 不分组显示
        else :
            # 不分组、如果排序标记 有效
            if self.ini_data["gamelist_sorted_by"] in self.tree["columns"]:
                temp_list = []

                for x in ( set_to_show & self.data['set_data']['all_set'] ) :
                    temp_list.append( (x , self.tree.set(x,column=self.ini_data["gamelist_sorted_by"]) ))
                    
                temp_list.sort( key=lambda x :x[1] , reverse=self.ini_data["gamelist_sorted_reverse"])
                for x in temp_list:# 第 0 项，是游戏名
                    self.tree.move(x[0],'','end')
                del temp_list  
                
            # 不分组、如果排序标记 无效
            else:
                for x in sorted( set_to_show & self.data['set_data']['all_set'] ):
                    self.tree.move(x,'','end')

                                

        time_3 = time.time()
        print(  )
        print("列表刷新时间统计")
        print("清理列表时间")
        print( time_2 - time_1 )
        print("重建列表时间")
        print( time_3 - time_2 )
        print("总计")
        print( time_3 - time_1 )
        print(  )    

    # 周边 显示
    def show_extra(self,game_name):
    
        # 初始化
        try :
            self.extra_remember
        except:
            self.extra_remember = None
        
        # 取消 after
        if self.extra_remember is not None:
            try:
                self.parent.after_cancel( self.extra_remember )
            except:
                pass
        
        print()
        print("show extra")
        
        # 图片
        if self.extra_image_panedwindow.winfo_viewable():
            self.extra_remember = self.parent.after(100, self.show_image,game_name)
        # 文档
        elif self.extra_text.winfo_viewable():
            n = self.extra_text_chooser.current() # 排序 0、1、2、……
            temp = self.text_types[n] # 名称 history.xml 、history.dat、……
            print(temp)
            
            if temp == "history.xml":
                self.extra_remember = self.parent.after(500, self.show_history_xml,game_name,)
            elif temp in ("history.dat","sysinfo.dat",):
                # print(temp)
                self.extra_remember = self.parent.after(100,self.show_extra_text,temp,game_name)
                #self.show_extra_text(self,temp,game_name)
            elif temp in ("gameinit.dat",):
                #show_gameinit_dat(self,type,game_name)
                self.extra_remember = self.parent.after(100 , self.show_gameinit_dat , temp, game_name)
            elif temp in ("mameinfo.dat","messinfo.dat",):
                
                # show_extra_mameinfo_dat(self,game_name)
                self.extra_remember = self.parent.after(100 , self.show_extra_mameinfo_dat,temp, game_name)
            else :
                pass
        # 文档2
        elif self.extra_command_text.winfo_viewable():
            self.extra_remember = self.parent.after(100, self.show_command,game_name,)
    # 周边 图片 显示,双图
    def show_image(self,game_name):
    
        if self.extra_image.winfo_viewable():
            if self.extra_image_usezip.get():# 使用 .zip 中的 .png
                print("try image in zip")
            
                #初始化
                try:
                    self.image_zip # 实际打开的，压缩包
                    self.image_zip_path # 实际打开的，压缩包路径，记录
                except:
                    self.image_zip = None
                    self.image_zip_path = None
                
                n = self.extra_image_chooser.current() # 序号 0，1，2，3，……
                
                #self.image_types
                #self.image_types_translation
                
                # temp 最后为 配置文件记录 的 ，压缩包的 路径
                
                temp = self.image_types[n] # 图片种类 snap,titles,flyers……
                
                temp = temp + r".zip_path" # 匹配，配置文件中的名字
             
                temp = self.ini_data[temp] # 从配置文件中，读取路径
            
                #print(temp)
                temp = temp.replace(r"'","") # 去掉单引号
                temp = temp.replace(r'"',"") # 去掉双引号
                
                if os.path.isfile(temp):
                # 配置文件中记录的文件，存在
                    pass # 下面 的一段语句，对比 self.image_zip_path 与 temp
                else:
                # 配置文件中记录的文件，不存在
                    # 找不到压缩包,也不能退出，
                    # 还得，使用 默认 图片
                    self.image_zip = None
                    self.image_zip_path = None            
                
                # 打开压缩包
                if self.image_zip_path :# 已经打开压缩包
                    if self.image_zip_path != temp : 
                    # 但
                    # 记录的 压缩包 位置 ，与 temp 不匹配
                        try:
                            self.image_zip_path = temp
                            self.image_zip = zipfile.ZipFile( self.image_zip_path , mode='r',  allowZip64=True,)
                        except:
                            self.image_zip = None 
                            self.image_zip_path = None
                else:# 还没有找开压缩包
                    try:
                        self.image_zip_path = temp
                        self.image_zip = zipfile.ZipFile( self.image_zip_path , mode='r',  allowZip64=True,)
                    except:
                        self.image_zip = None 
                        self.image_zip_path = None

                ext=r'.png'
                    
                file_name = game_name + ext # 图片名称，如 kof97.png
                
                image = None      
                
                if self.image_zip_path:

                    try:
                        image_data = self.image_zip.open(file_name, mode='r', )
                        image = Image.open(image_data, mode='r',)
                    except:
                        image = None

                    if image is None:
                        # 如果，本身没有找到，找一下主版本
                        # self.data['dict_data']['clone_to_parent'][]
                        
                        if game_name in self.data['dict_data']['clone_to_parent']:
                            print("try parent")
                        
                            parent_name = self.data['dict_data']['clone_to_parent'][game_name]
                            
                            parent_file_name = parent_name + ext
                            
                            try:
                                image_data = self.image_zip.open(parent_file_name, mode='r', )
                                image = Image.open(image_data, mode='r',)
                            except:
                                image = None                        
                        else: # 本身是主版本，pass
                            pass


                if image is None :
                    self.image_original = self.image_no 
                    self.size_original = self.size_image_no 
                else:
                    self.image_original = image
                    self.size_original = self.image_original.size
                        
                width = self.extra_image.winfo_width()
                height = self.extra_image.winfo_height()
                size =(width,height)
                
                # def image_get_new_size(self,image_size,canvas_size)
                new_size = self.image_get_new_size( self.size_original, size )
                
                if new_size:
                    if game_name == self.tree.focus():
                        
                        self.image = ImageTk.PhotoImage(self.image_original.resize( new_size,Image.BILINEAR, ))
                        
                        self.extra_image.create_image( int(width/2), int(height/2), image=self.image , anchor=tk.CENTER)
            else: # 使用 普通 .png
            
                n = self.extra_image_chooser.current() # 序号 0，1，2，3，……
                
                #self.image_types
                #self.image_types_translation
                
                # temp 最后为 配置文件记录 的 ，压缩包的 路径
                
                temp = self.image_types[n] # 图片种类 snap,titles,flyers……        

                temp = temp + "_path" # 匹配，配置文件中的名字
                
                temp = self.ini_data[temp] # 从配置文件中，读取路径
                
                #print(temp)
                temp = temp.replace(r"'","") # 去掉单引号
                temp = temp.replace(r'"',"") # 去掉双引号
                
                # 扩展名
                ext=r'.png'
                
                file_name = game_name + ext

                
                print( file_name )
                
                result =[]
                file_path = ''
                
                for x in temp.split(';') :
                    search_str = os.path.join(x, file_name)
                    #print(search_str)
                    r = glob.glob( search_str )
                    # 搜不到，结果为 []
                    #   不用通配符搜，
                    #    搜到，结果 ['f:\\snap\\snap\\2001tgm.png']
                    #    说明 search_str 路径正确
                    if r : 
                        file_path = search_str
                        break # 找到一个就行了
                
                if file_path =='':
                    # 如果，本身没有找到，找一下主版本
                    # data['set_data'][]
                    # self.data['dict_data']['clone_to_parent'][]
                    
                    parent_file_name = None 
                    
                    if game_name in self.data['dict_data']['clone_to_parent']:
                        print("try parent")
                        parent_name = self.data['dict_data']['clone_to_parent'][game_name]
                        parent_file_name = parent_name + ext
                        
                        for x in temp.split(';') :
                            search_str = os.path.join(x, parent_file_name)
                            #print(search_str)
                            r = glob.glob( search_str )
                            # 搜不到，结果为 []
                            #   不用通配符搜，
                            #    搜到，结果 ['f:\\snap\\snap\\2001tgm.png']
                            #    说明 search_str 路径正确
                            if r : 
                                file_path = search_str
                                break # 找到一个就行了                    
                    else: # 本身是主版，pass
                        pass
                

                if file_path == '' :
                    self.image_original = self.image_no 
                    self.size_original = self.size_image_no 
                else:
                    self.image_original = Image.open( file_path )
                    self.size_original = self.image_original.size
                        
                width = self.extra_image.winfo_width()
                height = self.extra_image.winfo_height()
                size =(width,height)
                
                # def image_get_new_size(self,image_size,canvas_size)
                new_size = self.image_get_new_size( self.size_original , size )
                
                if new_size :
                    if game_name == self.tree.focus():
                        
                        self.image = ImageTk.PhotoImage(self.image_original.resize( new_size,Image.BILINEAR, ))
                        
                        self.extra_image.create_image( int(width/2), int(height/2), image=self.image , anchor=tk.CENTER)
        else:
            try:
                del self.image_zip 
                del self.image_zip_path 
            except:
                pass
    
        if self.extra_image_2.winfo_viewable():
            if self.extra_image_usezip_2.get():# 使用 .zip 中的 .png
                print("try image 2 in zip")
            
                #初始化
                try:
                    self.image_zip_2 # 实际打开的，压缩包
                    self.image_zip_path_2 # 实际打开的，压缩包路径，记录
                except:
                    self.image_zip_2 = None
                    self.image_zip_path_2 = None
                
                n = self.extra_image_chooser_2.current() # 序号 0，1，2，3，……
                
                #self.image_types
                #self.image_types_translation
                
                # temp 最后为 配置文件记录 的 ，压缩包的 路径
                
                temp = self.image_types[n] # 图片种类 snap,titles,flyers……
                
                temp = temp + r".zip_path" # 匹配，配置文件中的名字
             
                temp = self.ini_data[temp] # 从配置文件中，读取路径
            
                #print(temp)
                temp = temp.replace(r"'","") # 去掉单引号
                temp = temp.replace(r'"',"") # 去掉双引号
                
                if os.path.isfile(temp):
                # 配置文件中记录的文件，存在
                    pass # 下面 的一段语句，对比 self.image_zip_path 与 temp
                else:
                # 配置文件中记录的文件，不存在
                    # 找不到压缩包,也不能退出，
                    # 还得，使用 默认 图片
                    self.image_zip_2 = None
                    self.image_zip_path_2 = None            
                
                # 打开压缩包
                if self.image_zip_path_2 :# 已经打开压缩包
                    if self.image_zip_path_2 != temp : 
                    # 但
                    # 记录的 压缩包 位置 ，与 temp 不匹配
                        try:
                            self.image_zip_path_2 = temp
                            self.image_zip_2 = zipfile.ZipFile( self.image_zip_path_2 , mode='r',  allowZip64=True,)
                        except:
                            self.image_zip_2 = None 
                            self.image_zip_path_2 = None
                else:# 还没有找开压缩包
                    try:
                        self.image_zip_path_2 = temp
                        self.image_zip_2 = zipfile.ZipFile( self.image_zip_path_2 , mode='r',  allowZip64=True,)
                    except:
                        self.image_zip_2 = None 
                        self.image_zip_path_2 = None

                ext=r'.png'
                    
                file_name = game_name + ext # 图片名称，如 kof97.png
                
                image = None      
                
                if self.image_zip_path_2:

                    try:
                        image_data = self.image_zip_2.open(file_name, mode='r', )
                        image = Image.open(image_data, mode='r',)
                    except:
                        image = None

                    if image is None:
                        # 如果，本身没有找到，找一下主版本
                        # self.data['dict_data']['clone_to_parent'][]
                        
                        if game_name in self.data['dict_data']['clone_to_parent']:
                            print("try parent")
                        
                            parent_name = self.data['dict_data']['clone_to_parent'][game_name]
                            
                            parent_file_name = parent_name + ext
                            
                            try:
                                image_data = self.image_zip_2.open(parent_file_name, mode='r', )
                                image = Image.open(image_data, mode='r',)
                            except:
                                image = None                        
                        else: # 本身是主版本，pass
                            pass


                if image is None :
                    self.image_original_2 = self.image_no 
                    self.size_original_2 = self.size_image_no 
                else:
                    self.image_original_2 = image
                    self.size_original_2 = self.image_original_2.size
                        
                width = self.extra_image_2.winfo_width()
                height = self.extra_image_2.winfo_height()
                size =(width,height)
                
                # def image_get_new_size(self,image_size,canvas_size)
                new_size = self.image_get_new_size( self.size_original_2, size )
                
                if new_size:
                    if game_name == self.tree.focus():
                        
                        self.image_2 = ImageTk.PhotoImage(self.image_original_2.resize( new_size,Image.BILINEAR, ))
                        
                        self.extra_image_2.create_image( int(width/2), int(height/2), image=self.image_2 , anchor=tk.CENTER)
            else: # 使用 普通 .png
            
                n = self.extra_image_chooser_2.current() # 序号 0，1，2，3，……
                
                #self.image_types
                #self.image_types_translation
                
                # temp 最后为 配置文件记录 的 ，压缩包的 路径
                
                temp = self.image_types[n] # 图片种类 snap,titles,flyers……        

                temp = temp + "_path" # 匹配，配置文件中的名字
                
                temp = self.ini_data[temp] # 从配置文件中，读取路径
                
                #print(temp)
                temp = temp.replace(r"'","") # 去掉单引号
                temp = temp.replace(r'"',"") # 去掉双引号
                
                # 扩展名
                ext=r'.png'
                
                file_name = game_name + ext

                
                print( file_name )
                
                result =[]
                file_path = ''
                
                for x in temp.split(';') :
                    search_str = os.path.join(x, file_name)
                    #print(search_str)
                    r = glob.glob( search_str )
                    # 搜不到，结果为 []
                    #   不用通配符搜，
                    #    搜到，结果 ['f:\\snap\\snap\\2001tgm.png']
                    #    说明 search_str 路径正确
                    if r : 
                        file_path = search_str
                        break # 找到一个就行了
                
                if file_path =='':
                    # 如果，本身没有找到，找一下主版本
                    # data['set_data'][]
                    # self.data['dict_data']['clone_to_parent'][]
                    
                    parent_file_name = None 
                    
                    if game_name in self.data['dict_data']['clone_to_parent']:
                        print("try parent")
                        parent_name = self.data['dict_data']['clone_to_parent'][game_name]
                        parent_file_name = parent_name + ext
                        
                        for x in temp.split(';') :
                            search_str = os.path.join(x, parent_file_name)
                            #print(search_str)
                            r = glob.glob( search_str )
                            # 搜不到，结果为 []
                            #   不用通配符搜，
                            #    搜到，结果 ['f:\\snap\\snap\\2001tgm.png']
                            #    说明 search_str 路径正确
                            if r : 
                                file_path = search_str
                                break # 找到一个就行了                    
                    else: # 本身是主版，pass
                        pass
                

                if file_path == '' :
                    self.image_original_2 = self.image_no 
                    self.size_original_2 = self.size_image_no 
                else:
                    self.image_original_2 = Image.open( file_path )
                    self.size_original_2 = self.image_original_2.size
                        
                width = self.extra_image_2.winfo_width()
                height = self.extra_image_2.winfo_height()
                size =(width,height)
                
                # def image_get_new_size(self,image_size,canvas_size)
                new_size = self.image_get_new_size( self.size_original_2 , size )
                
                if new_size :
                    if game_name == self.tree.focus():
                        
                        self.image_2 = ImageTk.PhotoImage(self.image_original_2.resize( new_size,Image.BILINEAR, ))
                        
                        self.extra_image_2.create_image( int(width/2), int(height/2), image=self.image_2 , anchor=tk.CENTER)                        
        else:
            try:
                del self.image_zip_2 
                del self.image_zip_path_2 
            except:
                pass            
    # 周边，文档 ,history.dat 这种格式的
    def show_extra_text(self,data_type,game_name):
        
        #print("show_extra_text")
        # print(type)
        # print(game_name)
    
        # 清除原有内容
        self.extra_text.delete('1.0',tk.END)
        
        data_type =  data_type + "_path" # "history.dat_path"
        
        path = self.ini_data[ data_type ]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        if os.path.isfile(path):
        
            new_text = []
        
            if game_name == self.tree.focus():
                text = extra_history_dat.get_content_by_file_name(path,game_name)
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

            if game_name == self.tree.focus():
                for x in new_text:
                    self.extra_text.insert(tk.END,x)
    # mameinfo.dat 、 messinfo.dat
    #   *.cpp
    def show_extra_mameinfo_dat(self,data_type,game_name):
        # mameinfo.dat
        # messinfo.dat
        
        # 清除原有内容
        self.extra_text.delete('1.0',tk.END)
        
        
        
        # 有属于 游戏 的文档
        # 还有，属于，驱动的文档
        
        # 分隔线 
        line_separator = "*"*5 +" " + "*"*5 + "\n"
       
        data_type =  data_type + "_path" # "history.dat_path"
        
        # path = self.ini_data[ "mameinfo.dat_path" ]
        # path = self.ini_data[ "messinfo.dat_path" ]
        
        path = self.ini_data[ data_type ]
        
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        print(path)
        
        if os.path.isfile(path):
        
            new_text = None # 记录该游戏的文档,读取内容后，是 []  ，
            if game_name == self.tree.focus():
                text = extra_mameinfo_dat.get_content_by_file_name(path,game_name)
                if text is not None:
                    new_text = text
                    #print(text)

            new_text_2 = None # 记录该游戏所属 驱动 的文档,[]
            
            if game_name == self.tree.focus():
            
                try:
                    sourcefile = self.tree.set( game_name, column="sourcefile",)
                except:
                    sourcefile = None
                
                if sourcefile:
                    text = extra_mameinfo_dat.get_content_by_file_name(path,sourcefile)
                    if text is not None:
                        new_text_2 = text
                    
            if game_name == self.tree.focus():
                flag1 = False
                flag2 = False

                if new_text is not None : flag1 = True
                if new_text_2 is not None : flag2 = True
                
                if flag1:
                    self.extra_text.insert(tk.END,line_separator)
                    self.extra_text.insert(tk.END,game_name)
                    self.extra_text.insert(tk.END,"\n")
                    self.extra_text.insert(tk.END,line_separator)
                    self.extra_text.insert(tk.END,"\n")
                    self.extra_text.insert(tk.END,"\n")
                    
                    
                    for x in new_text:
                        self.extra_text.insert(tk.END,x)
                        
                    self.extra_text.insert(tk.END,"\n")
                        
                if flag2:
                    self.extra_text.insert(tk.END,line_separator)
                    self.extra_text.insert(tk.END,"\n")
                    
                    self.extra_text.insert(tk.END,sourcefile)
                    self.extra_text.insert(tk.END,"\n")
                    
                    self.extra_text.insert(tk.END,"\n")
                    self.extra_text.insert(tk.END,line_separator)
                    
                    self.extra_text.insert(tk.END,"\n")
                    self.extra_text.insert(tk.END,"\n")
                    
                    for x in new_text_2:
                        self.extra_text.insert(tk.END,x)
    # gameinit.dat
    def show_gameinit_dat(self,data_type,game_name):
        print("show_gameinit_dat")
        
        # 清除原有内容
        self.extra_text.delete('1.0',tk.END)
        
        data_type =  data_type + "_path" # "gameinit.dat_path"
        
        path = self.ini_data[ data_type ]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        if os.path.isfile(path):
        
            new_text = []
        
            if game_name == self.tree.focus():
                text = extra_gameinit_dat.get_content_by_file_name(path,game_name)
                if text is not None:
                    new_text = text       
                    
            # 主版本 ？，算了，不管
            
            if game_name == self.tree.focus():
                for x in new_text:
                    self.extra_text.insert(tk.END,x)
    # 周边 history.xml 显示
    def show_history_xml(self,game_name):
        
        # 清除原有内容
        self.extra_text.delete('1.0',tk.END)
    
        path = self.ini_data["history.xml_path"]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 

        if os.path.isfile(path):
            
            new_text = ''
            
            if game_name == self.tree.focus():
                text = extra_read_history_xml.getinfo(path,game_name)
                if text is not None:
                    new_text = text
                        
            # if game_name == self.tree.focus():
            #     if new_text == '':
            #         # 再找主版本
            #         print("try parent")
            #         if game_name in self.data['dict_data']['clone_to_parent']:
            #             parent_name = self.data['dict_data']['clone_to_parent'][game_name]
            #             text = extra_read_history_xml.getinfo(path,parent_name)
            #             if text is not None:
            #                 new_text = text

            if game_name == self.tree.focus():
                self.extra_text.insert('1.0',new_text)
    # 周边 command.dat （ jjsnake 版本 ）、command_english.dat
    def show_command(self,game_name):
    
        print("show command")
        
        n = self.extra_command_type_chooser.current() # 排序 0、1、2、……
        type = self.text_types_2[n] # 名称 command.dat 、command_english.dat、……
        
        
        # 清除原有内容
        self.extra_command_text.delete('1.0',tk.END)
        
        path = type + "_path" # "command.dat_path"
        path = self.ini_data[path]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        print(path)
        
        if not os.path.isfile(path):
            self.extra_command_chooser["values"]=("",)
            self.extra_command_chooser.set("")         
            return 0 
            # 如果，文档，不存在，直接退出函数
        
        # 初始化
        try:
            self.command_content
        except:
            self.command_content =  None 

        # 读取内容
        
        # 中文版，英文版 ，格式不同
        
        try:
            if type == "command.dat":
                self.command_content = extra_command.get_content_by_file_name( path,game_name )
            elif type == "command_english.dat":
                self.command_content = extra_command_english.get_content_by_file_name( path,game_name )
        except:
            self.command_content =  None 
        
        
        if self.command_content is None:
            self.extra_command_chooser["values"]=("",)
            self.extra_command_chooser.set("") 
        elif len(self.command_content) <= 1:
            #print(r"<=1")
            self.extra_command_chooser["values"]=("全部",)
            self.extra_command_chooser.set("全部") 
            for x in self.command_content:
                for y in self.command_content[x]:
                    self.extra_command_text.insert(tk.INSERT, y)
        else:
            #print(r">1")
            index = []
            index.append("全部")
            for x in self.command_content:
                # 提取 每一段 第一行，做为小标题
                try:
                    index.append( self.command_content[x][0] )
                except:
                    index.append("")
            self.extra_command_chooser["values"]=index
            self.extra_command_chooser.set("全部") 
            
            for x in self.command_content:
                for y in self.command_content[x]:
                    self.extra_command_text.insert(tk.INSERT, y)

    # 图片，拉伸，按照图片原有比例
    def image_get_new_size(self,image_size,canvas_size):
        
        flag = False
        
        if canvas_size[0] >0:
            if canvas_size[1] >0:
                if image_size[0] >0:
                    if image_size[1] >0:
                        flag = True
                        
        if flag:
        
                a1 = canvas_size[0] / image_size[0]
                a2 = canvas_size[1] / image_size[1]
                
                # 按比例拉伸，取最小的
                if a1>a2:
                    new_width  = image_size[0] * a2
                    new_height = image_size[1] * a2
                else:
                    new_width  = image_size[0] * a1
                    new_height = image_size[1] * a1
                    
                new_image_size = ( int(new_width),int(new_height) ) 
                
                return new_image_size
        else:
            return None

    # MAME
    def call_mame(self,game_name,other_option=None,hide=True):

        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_name )
        
        if other_option:
            for x in other_option:
                command_list.append( x )

        print(  )
        print( mame_dir )
        print( command_list )
        
        if hide: # 打开游戏，影藏 UI
            #self.parent.iconify()
            self.parent.withdraw()
            
            proc = subprocess.Popen(command_list, shell=self.ini_data["use_shell"],cwd=mame_dir)
            
            proc.wait()
            self.parent.deiconify()
            self.tree.focus_set()
        else: # 打开游戏，保留 UI
            proc = subprocess.Popen(command_list, shell=self.ini_data["use_shell"],cwd=mame_dir)
    
    # top level window, 显示文本信息
    def show_text_winodw(self,content=[],title="",):
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        if title:    
            window.title(title)
            
        size  = "400x300"
        size += self.get_root_window_x_y()
        window.geometry(size)
        
        window.transient(self.parent)
        window.lift(self.parent)
        #window.grab_set()
        
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        t = tk.Text(window,undo=False,padx=10,pady=10,spacing1=2,spacing2=2,spacing3=2)
        
        scrollbar_1 = ttk.Scrollbar( window, orient=tk.VERTICAL, command=t.yview)
        
        scrollbar_2 = ttk.Scrollbar( window, orient=tk.HORIZONTAL, command=t.xview)
        
        t.configure(yscrollcommand=scrollbar_1.set)
        t.configure(xscrollcommand=scrollbar_2.set)
        
        t.grid(row=0,column=0,stick=(tk.W,tk.N,tk.E,tk.S))
        scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        ttk.Sizegrip(window).grid(row=1,column=1,sticky=(tk.N,tk.S))
        
        if content:
            for x in content:
                t.insert(tk.END, x, )
        
        t["state"]="disabled"    

    # 获得 主窗口 坐标，用于 TopLevel Window 定位
    def get_root_window_x_y(self,num=None ):
        # num 移动 值 
        if num is None: num = 20
        
        size = self.parent.winfo_geometry()
            #"400x300+x+y" ,'wxh±x±y' , + 或 - 
        
        print()
        print("获取窗口位置")
        print(size)
        
        str_to_find = r"\d+x\d+([\+-])(\d+)([\+-])(\d+)" # ±x±y 1 ,2 ,3, 4,
        
        p = re.compile( pattern= str_to_find , flags= re.ASCII )
        
        m = p.search(size)
        
        if m:
            #print(m.group(0))
            x = int(m.group(2))
            y = int(m.group(4))
            new_srt = m.group(1) + str(x+num) + m.group(3) + str(y+num)
            print(new_srt)
            #print(type(new_srt))
            return new_srt # 'wxh±x±y' ±x±y
        else:
            return ""

    # 在 空 Frame 中，建立 字体选择 界面
    #   菜单，字体选择，函数中，调用此处
    def font_chooser(self,master,font_var,font_size_var,widget_type):

        # 字体
        
        ttk.Label(master,text = "",).grid(row=0,column=0,sticky=tk.W+tk.N)
        
        font_name_tkstring = tk.StringVar()

        label_font = ttk.Label(master,text = "字体选择",)
        label_font.grid( row=1,column=0,sticky=tk.W+tk.E)
        
        font_choose_box = ttk.Combobox(master, textvariable = font_name_tkstring,state="readonly",width=30)
        font_choose_box.grid( row=1,column=1,sticky=(tk.W,tk.E) )
        
        temp = sorted( tkfont.families() )
        values = []
        values.append("")
        for x in temp:
            values.append(x)
        font_choose_box["values"]= values
        
        if font_var in values:
            font_choose_box.set(font_var)
        else:
            font_choose_box.set("")
        
        # 字体大小
        ttk.Label(master,text = "",).grid(row=2,column=0,sticky=tk.W+tk.N)
        
        font_size_tkstring = tk.StringVar()
        
        label_font_size = ttk.Label(master,text = r"字体大小",)
        label_font_size.grid( row=3,column=0,sticky=(tk.W,tk.E) )
        
        font_size_box = ttk.Combobox(master, textvariable = font_size_tkstring,state="readonly")
        font_size_box.grid(row=3,column=1,sticky=(tk.W,tk.E))
        
        font_size_box["values"]= tuple(range(101))
        
        if font_size_var in range(101):
            font_size_box.set(font_size_var)
        else:
            font_size_box.set(0)
        
        #
        ttk.Label(master,text = "",).grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
        
            font_name = font_name_tkstring.get()
            font_size = font_size_tkstring.get()
            font_size = int(font_size)
            
            if font_name == "" : font_name = None
            
            temp=None
            
            if font_name == None:# 字体没设置
                if font_size==0: # 字体大小，没设置，不管
                    temp=None
                else:# 字体大小，设置了
                    temp_font_name = None
                    temp_font_size = font_size
                    temp = (temp_font_name,temp_font_size)
            else:# 字体设置了
                if font_size==0:# 但，字体大小 没设置
                    temp_font_name = font_name
                    temp = (temp_font_name,)
                else:# 都设置了
                    temp_font_name = font_name
                    temp_font_size = font_size
                    temp = (temp_font_name,temp_font_size)
                    
            if temp != None :
                print(temp)
                #self.style.configure('.', font=temp) 
                #self.extra_text["font"]=tkfont.Font(font=temp)
                #self.extra_command_text["font"]=tkfont.Font(font=temp)
                #self.parent.option_add('*font', temp,priority=80)
                #self.parent.option_add('*Button*font', temp,priority=80)
                #self.parent.option_add(pattern, value, priority=None)
                #*font: Verdana 10              

                if widget_type == "Treeview":
                    self.style.configure('Treeview', font=temp)
                    self.ini_data["gamelist_font"] = font_name
                    self.ini_data["gamelist_font_size"] = font_size
                
                elif widget_type == "Text" :
                    print("text")
                    self.extra_text.configure(font=temp)
                    #self.extra_command_text.configure(font=temp)

                    self.ini_data["text_font"] = font_name
                    self.ini_data["text_font_size"] = font_size
                    
                elif widget_type == "Text_2" :
                    print("text")
                    #self.extra_text.configure(font=temp)
                    self.extra_command_text.configure(font=temp)

                    self.ini_data["text_2_font"] = font_name
                    self.ini_data["text_2_font_size"] = font_size
                    
                elif widget_type == "others" :
                    print("others")
                    #self.style.configure('.', font=temp)
                    self.style.configure('TLabel', font=temp)
                    self.style.configure('TButton', font=temp)
                    #self.style.configure('TEntry', font=temp)
                    self.style.configure('TCheckbutton', font=temp)
                    self.style.configure('TCombobox', font=temp)
                    self.style.configure('TNotebook', font=temp)
                    self.style.configure('TNotebook.Tab', font=temp)
                    
                    self.top_entry_search.configure(font=temp)
                    
                    self.parent.option_add("*TCombobox*Listbox.font", temp)
                    self.parent.option_add("*font", temp)

                    self.ini_data["others_font"] = font_name
                    self.ini_data["others_font_size"] = font_size                     
                    
                    # combobox
                    def ttk_combobox_font_set(a_widget,font):
                        for x in a_widget.winfo_children():
                            if type(x) == type( ttk.Combobox() ):
                                x.configure(font=font)
                            
                            elif type(x) == type( ttk.Frame() ):
                                ttk_combobox_font_set(x,font)
                            
                            elif type(x) == type( ttk.PanedWindow() ):
                                ttk_combobox_font_set(x,font)
                                
                    ttk_combobox_font_set( self.notebook , temp)
                    
                    # menu
                    def tk_menu_font_set(a_widget,font):
                        for x in a_widget.winfo_children():
                            if type(x) == type( tk.Menu() ):
                                x.configure(font=font)
                                
                    tk_menu_font_set(self.menu_bar,temp)
                    
                    self.menu_mouse_index.configure(font=temp)
                    self.menu_mouse.configure(font=temp)
                    self.gamelist_pop_up_menu_of_heading.configure(font=temp)
            
            else :
                if widget_type == "Treeview":
                    self.ini_data["gamelist_font"] = ""
                    self.ini_data["gamelist_font_size"] = 0
                elif widget_type == "Text":
                    self.ini_data["text_font"] = ""
                    self.ini_data["text_font_size"] = 0
                elif widget_type == "Text_2":
                    self.ini_data["text_2_font"] = ""
                    self.ini_data["text_2_font_size"] = 0
                elif widget_type == "others":
                    self.ini_data["others_font"] = ""
                    self.ini_data["others_font_size"] = 0                    
                    
                    
            #master.destroy()
            #self.parent.lift()
        
        ttk.Button(master,text="确定",command=for_ok_button).grid( row=5,column=0,sticky=tk.N+tk.E, )

    def show_current_working_directory(self,event=None):
        print("current working directory")
        temp = os.getcwd()
        print(os.path.abspath(temp))

    # mame_exe
    # mame_dir
    #   用于 subprocess.Popen 函数
    def get_mame_path_and_working_directory(self):
        
        # 如果存在此文件，设为绝对值
        # 如果不存在此文件，当成 ，它 在 系统 环境变量 里
        if os.path.isfile( self.ini_data["mame_path"] ):
            mame_exe = os.path.abspath( self.ini_data["mame_path"] )
        else:
            mame_exe = self.ini_data["mame_path"]
    
        mame_working_directory = None # 默认值
        
        # 默认值
        #   如果值 没有 设置 ，为空
        #   自动设置为 mame 所在文件夹
        if self.ini_data["mame_working_directory"] == "" :
            if os.path.isfile( self.ini_data["mame_path"] ):
                mame_working_directory = os.path.dirname( self.ini_data["mame_path"] )
                mame_working_directory = os.path.abspath( mame_working_directory )
                
        else:
            if os.path.isdir( self.ini_data["mame_working_directory"] ):
                mame_working_directory = os.path.abspath( self.ini_data["mame_path"] )
        
        return (mame_exe , mame_working_directory)
    
    # mame -showconfig 中
    #   rompath 这一项
    def get_rompath_from_command_line(self,event=None):
        print("get_rompath_from_command_line")
    
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( "-showconfig" )
        
        rom_path="roms" # 默认值
        
        #rompath                   "roms;"
        str_1 = r"^rompath\s+(\S.*?)\s*$"
        p=re.compile(str_1, )        
        
        sub_process = subprocess.Popen( command_list, 
                            shell=self.ini_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8",
                            cwd=mame_dir,
                            )
                            
        for line in sub_process.stdout:
            print(line)
            m = p.search(line)
            if m :
                rom_path = m.group(1)
                #print("find")
                break
        
        print(rom_path)
        return rom_path
    
    # 找到拥有的 *.zip 、*.7z 、文件夹
    def get_files_names_in_rompath(self,merged = False):
        ### ###
        # 还有一种情况 
        # 路径里有变量：$HOME/mame/roms
            ####
            # 有变量的，到底有几种格式？  


        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        # rompath 里记录的文件，相对位置是相对于模拟器的，这个还得改一下            

        rom_path = self.get_rompath_from_command_line()
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()        
        
        if rom_path:
            rom_path = rom_path.replace(r"'","") # 去掉单引号
            rom_path = rom_path.replace(r'"',"") # 去掉双引号
        
        temp_set = set()
        
        temp=[]
        
        for x in rom_path.split(r';'):
            if x:
                print(x)

                #######
                # rompath ，记录的相对路径，是相对于模拟器的
                
                
                ### ###
                # 还有一种情况
                # 路径里有变量：$HOME/mame/roms
                    ####
                    # 有变量的，到底有几种格式？
                    
                # 情况1，如果有变量，展开，
                temp_path = x
                try:
                    temp_path = os.path.expandvars( x )
                except:
                    temp_path = x

                if os.path.isabs(temp_path): # 如果是，绝对路径，不用转换
                    y = temp_path
                else: # 如果是，相对路径，转换
                    if mame_dir != None:# 已设置 mame 工作文件夹
                        # mame 所在文件夹 ,绝对路径
                        mame_folders = mame_dir
                        mame_folders = os.path.abspath( mame_folders )
                        
                        # 相对转换路径后的绝对路径
                        y = os.path.join(mame_folders,temp_path)
                        
                        y = os.path.abspath( y )
                        
                    else:# 未设置 mame 工作文件夹，且不是默认值
                        #当成与 jjui 同文件夹对待？
                        y = x

                print(y)
                
                if os.path.isdir(y):
                
                    files_zip = glob.glob( os.path.join(y,"*.zip") )
                    for a in files_zip:
                        temp.append(  os.path.basename(a).lower()[0:-4] )# zip
                    
                    files_7z  = glob.glob( os.path.join(y,"*.7z") )
                    for b in files_7z:
                        temp.append(  os.path.basename(b).lower()[0:-3] )# 7z
                    
                    files_all = glob.glob( os.path.join(y,"*") )
                    files_left = set(files_all) - set(files_zip) - set(files_7z)
                    for c in files_left:
                        if os.path.isdir(c):
                            temp.append(  os.path.basename(c).lower() )

        temp_set = set( temp )
        
        temp_set = self.data['set_data']['all_set'] & temp_set
        
        # merged
        if merged :
            # 现有的主版
            the_parent = temp_set & self.data['set_data']['parent_set']
            
            # 其中，有副版本的
            the_parent = the_parent & set( self.data['dict_data']['parent_to_clone'].keys() )
            
            # 关联的副版本
            the_colne = []
            for x in the_parent:
                the_colne.extend( self.data['dict_data']['parent_to_clone'][x] )
            the_colne = set( the_colne )
            
            # 合并
            the_result = temp_set | the_colne
            return  the_result
        
        # split
        else:
            return temp_set


    def other_functions_show_mame_help(self):
        
        mame_path = self.ini_data["mame_path"]

        command_list = []
        command_list.append( mame_path )
        command_list.append( "-help" )
        
        p = subprocess.Popen( command_list, 
                            shell=self.ini_data["use_shell"],
                            #stdout=subprocess.PIPE , 
                            #stderr=subprocess.STDOUT ,
                            #stdin=subprocess.PIPE,
                            #encoding="utf_8",
                            #cwd=mame_dir,
                            )
    
    def other_functions_mark_available_games(self,mark_available=True,mark_un_available=True):
        # 标记拥有列表
        #   刷新列表后，未拥有的列表，也需要清除原的标记，
        #       除非一开始初始化的时候
        def mark_available_games():
            if self.ini_data["use_available_game_mark"]:
                for game_name in self.data['set_data']['available_set']:
                    self.tree.item(game_name,text=self.ini_data["available_game_mark"])
        def mark_unavailable_games():
            for game_name in self.data['set_data']['all_set'] - self.data['set_data']['available_set']:
                self.tree.item(game_name,text="")
        if mark_available:
            mark_available_games()
        if mark_un_available:
            mark_unavailable_games()

    
                            
if __name__ == "__main__" :
    
    # ui 界面测试

    root=tk.Tk()
    
    root.title("ui 界面测试")

    
    ui = MyUi(root,ini_data = {} ,ini_path="fake_path",ttk_style=None)
    

    root.mainloop()



