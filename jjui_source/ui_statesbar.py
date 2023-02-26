# -*- coding: utf_8_sig-*-
#import sys
#import os
import tkinter as tk
from tkinter import ttk 

from . import global_variable

class StatesBar(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        parent.rowconfigure(0, weight=0)
        parent.columnconfigure(0, weight=1)
        self.new_func_ui()
        self.new_func_bindings()

    def new_func_ui(self,):
        
        parent=self
        
        parent.rowconfigure(0, weight=0)
        #parent.columnconfigure(0, weight=0)
        #parent.columnconfigure(1, weight=0)
        
        column=0
        
        self.new_ui_label_total_number = ttk.Label(parent,anchor=tk.W,text="",)
        self.new_ui_label_total_number.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        self.new_ui_label_current_list_number = ttk.Label(parent,anchor=tk.W,text="",)
        self.new_ui_label_current_list_number.grid(row=0,column=column, sticky=tk.W,)
        column+=1

        
        #
        self.new_ui_label_current_item = ttk.Label(parent,anchor=tk.W,text="")
        self.new_ui_label_current_item.grid(row=0,column=column,sticky=tk.W+tk.N+tk.E+tk.S,)
        parent.columnconfigure(column, weight=1)#### 可拉伸
        column+=1
        
        ttk.Sizegrip(parent).grid(row=0,column=column,sticky=tk.E)
        column+=1
    
    def new_func_bindings(self):
        self.bind_all('<<CurrentGameListNumber>>',self.new_func_binding_virtual_event_receive_CurrentGameListNumber,)
        self.bind_all('<<CurrentGame>>',self.new_func_binding_virtual_event_receive_CurrentGame,"+")
    
    def new_func_binding_virtual_event_receive_CurrentGameListNumber(self,event):
        widget = event.widget
        number = widget.new_var_data_for_CurrentGameListNumber
        self.new_ui_label_current_list_number.configure(text=_("列表数量：")+str(number)+" . ")
        
    def new_func_binding_virtual_event_receive_CurrentGame(self,event):
        #widget  = event.widget
        #item_id = widget.new_var_data_for_CurrentGame
        item_id = global_variable.current_item
        item_detail = global_variable.machine_dict[ item_id ]
        
        temp_string = item_id 
        
        #cloneof
        if "cloneof" in global_variable.columns_index:
            result_string = item_detail[ global_variable.columns_index["cloneof"] ]
            if result_string:
                temp_string += " | " + _("主版本：") + result_string
        #romof
        if "romof" in global_variable.columns_index:
            result_string = item_detail[ global_variable.columns_index["romof"] ]
            if result_string:
                temp_string += " | " + _("romof：") + result_string 
        #status
        if "status" in global_variable.columns_index:
            result_string = item_detail[ global_variable.columns_index["status"] ]
            if result_string:
                temp_string += " | " + _("模拟状态：") + result_string
        #savestate
        if "savestate" in global_variable.columns_index:
            result_string = item_detail[ global_variable.columns_index["savestate"] ]
            if result_string:
                temp_string += " | " + _("存盘状态：") + result_string
        self.new_ui_label_current_item.configure(text= temp_string  )#  + "·"