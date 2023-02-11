# -*- coding: utf_8_sig-*-
import sys
import os
import tkinter as tk
from tkinter import ttk 

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

from . import global_variable
from . import ui_small_windows

class ToolBar(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_data_for_virtual_event_search = ""
        self.new_var_data_for_FindItemById         = ""
        
        self.new_func_ui()
        self.new_func_bindings()


    def new_func_ui(self,):
        
        parent=self
        
        parent.rowconfigure(0, weight=0)
        parent.columnconfigure(0, weight=0)
        parent.columnconfigure(1, weight=0)
        
        column=0
        
        button_change_columns_to_show =ttk.Button(parent,takefocus=False,text=_(r'1/2/3'),width=-1,command=self.new_func_generate_virtual_event_GameListChangeColumnsToShow,)
        button_change_columns_to_show.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        button_group =ttk.Button( parent,takefocus=False,text=_("分组/不分组"),width=-1,command=self.new_func_generate_virtual_event_GamelistChangeGroupMode)
        button_group.grid(row=0,column=column, sticky=(tk.W,))
        column+=1
        
        button_see = ttk.Button(parent,takefocus=False,text=_(r'定位到'),width=-1,command=self.new_func_generate_virtual_event_FindItemById)
        button_see.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        self.top_label_remember = ttk.Label(parent,takefocus=False,anchor=tk.W,width=10,)
        self.top_label_remember.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        label_search = ttk.Label(parent,takefocus=False,anchor=tk.W,text=_(r"搜索栏:") )
        label_search.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        ####
        self.new_var_data_for_search = tk.StringVar()
        self.new_ui_entry_search = ttk.Entry(parent,takefocus=False,justify=tk.LEFT,textvariable=self.new_var_data_for_search )
        self.new_ui_entry_search.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        top_button_search = ttk.Button(parent,takefocus=False,text=_('搜索'),width=-1,command=self.new_func_generate_virtual_event_GameListSearch)
        top_button_search.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        top_button_search_re = ttk.Button(parent,takefocus=False,text=_('正则搜索'),width=-1,command=self.new_func_generate_virtual_event_GameListSearchRegular)
        top_button_search_re.grid(row=0,column=column,sticky=(tk.W,))        
        column+=1
        
        top_button_clear = ttk.Button(parent,takefocus=False,text=_('清空'),width=-1,command=self.new_func_generate_virtual_event_GameListSearchClear)
        top_button_clear.grid(row=0,column=column,sticky=(tk.W,))
        column+=1
        
        #top_button_clear = ttk.Button(parent,takefocus=False,text=_('搜索设置'),width=-1,command=ui_small_windows.window_for_gamelist_set_search_columns)
        #top_button_clear.grid(row=0,column=column,sticky=(tk.W,))
        #column+=1
    
    def new_func_bindings(self,):
        self.bind_all('<<CurrentGame>>',self.new_func_binding_virtual_event_receive_CurrentGame,"+")
        self.new_ui_entry_search.bind('<Return>',self.new_func_generate_virtual_event_GameListSearch)
        self.new_ui_entry_search.bind('<Control-Return>',self.new_func_generate_virtual_event_GameListSearchRegular)

    # <<GameListChangeColumnsToShow>>
    # 1组，2组，3组，方便查看不同内容
    # 比如 1组看中文，2组看英文
    # global_variable.column_group_counter 计数
    def new_func_generate_virtual_event_GameListChangeColumnsToShow(self):
            self.event_generate('<<GameListChangeColumnsToShow>>')
    
    # <<GamelistChangeGroupMode>>
    # 切换游戏列表，单层列表、双层列表、双层列表（可收缩）
    def new_func_generate_virtual_event_GamelistChangeGroupMode(self):
            self.event_generate('<<GamelistChangeGroupMode>>')
    
    # <<FindItemById>>
    # self.new_var_data_for_FindItemById 
    def new_func_generate_virtual_event_FindItemById(self,):
        # 记录
        # self.new_var_data_for_FindItemById 
        # 在接收函数中记录的
        
        self.event_generate('<<FindItemById>>')
    
    # <<GameListSearch>>
    # self.new_var_data_for_virtual_event_search
    def new_func_generate_virtual_event_GameListSearch(self,event=None):
        ""
        string_for_search = self.new_var_data_for_search.get()
        
        if not string_for_search: return
        
        # 全空格字符
        flag_empty_string = True
        space = " "
        for x in string_for_search:
            if space != x:
                flag_empty_string = False
                break
        if flag_empty_string : 
            self.new_var_data_for_search.set("") # 清理
            return
        
        self.new_var_data_for_virtual_event_search = string_for_search
        
        self.event_generate('<<GameListSearch>>')
    
    #<<GameListSearchRegular>>
    # self.new_var_data_for_virtual_event_search
    def new_func_generate_virtual_event_GameListSearchRegular(self,event=None):
        ""
        string_for_search = self.new_var_data_for_search.get()
        
        if not string_for_search: return
        
        # 全空格字符
        flag_empty_string = True
        space = " "
        for x in string_for_search:
            if space != x:
                flag_empty_string = False
                break
        if flag_empty_string : 
            self.new_var_data_for_search.set("") # 清理
            return
        
        self.new_var_data_for_virtual_event_search = string_for_search
        
        self.event_generate('<<GameListSearchRegular>>')
    
    
    #<<GameListSearchClear>>
    def new_func_generate_virtual_event_GameListSearchClear(self):
        self.new_var_data_for_search.set("")# 清理
        self.event_generate('<<GameListSearchClear>>')
    
    
    def do_nothing(self,):
            print("do nothing")
    
    def new_func_binding_virtual_event_receive_CurrentGame(self,event):
        #widget  = event.widget
        #item_id = widget.new_var_data_for_CurrentGame
        item_id = global_variable.current_item

        # 记录
        self.new_var_data_for_FindItemById = item_id
        
        self.top_label_remember.configure(text= item_id)