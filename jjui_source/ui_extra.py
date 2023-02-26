# -*- coding: utf_8_sig-*-
# import sys
# import os
import tkinter as tk
from tkinter import ttk 

from . import global_variable
from .ui_extra_image_container import Image_container,Image_container_2
from .ui_extra_text_container import Text_container,Text_container_2


class Extra(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_virtual_event_name_CurrentGame=r'<<CurrentGame>>'
        
        self.new_var_remember_after = None
        
        
        self.new_func_ui()
        
        self.new_func_ui_for_image_area()
        self.new_func_ui_for_text_area()
        self.new_func_ui_for_text_area_2()
        
        self.new_func_bindings()

    def new_func_ui(self,):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=0)
        
        parent=self
        
        #width = self.ini_data["width_extra"]
        
        # self.new_ui_notebook
        self.new_ui_notebook = ttk.Notebook(parent , takefocus=False,)#width = width
        self.new_ui_notebook.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        #self.new_ui_notebook.state(statespec=("readonly",))
        ""
        
    def new_func_bindings(self,):
        self.bind_all(self.new_var_virtual_event_name_CurrentGame,self.new_func_bindings_receive_virtual_event,"+")
        
        self.new_ui_notebook.bind('<<NotebookTabChanged>>',self.new_func_bindings_NotebookTabChanged)
    
    # image
    def new_func_ui_for_image_area(self):

        # 图片 区域 ，放两组图
        extra_f1 = ttk.Frame(self.new_ui_notebook)  
        self.new_ui_notebook.add(extra_f1, text= _('图片'),sticky=tk.W+tk.N+tk.E+tk.S, )
        
        extra_f1.columnconfigure(0,weight=1)
        extra_f1.rowconfigure(0,weight=1)

        self.new_ui_extra_image_panedwindow = ttk.PanedWindow(extra_f1,orient=tk.VERTICAL)
        self.new_ui_extra_image_panedwindow.grid(row=0 , column=0 , sticky=tk.W+tk.N+tk.E+tk.S,)
        
        
        self.new_ui_image_container_1  = Image_container(self.new_ui_extra_image_panedwindow)
        self.new_ui_extra_image_panedwindow.add(self.new_ui_image_container_1,weight=1)
        
        self.new_ui_image_container_2  = Image_container_2(self.new_ui_extra_image_panedwindow)
        self.new_ui_extra_image_panedwindow.add(self.new_ui_image_container_2,weight=1)
    

    # text
    def new_func_ui_for_text_area(self):
        # 图片 区域 ，放两组图
        extra_t = ttk.Frame(self.new_ui_notebook)  
        self.new_ui_notebook.add(extra_t, text= _('文档'),sticky=tk.W+tk.N+tk.E+tk.S, )
        
        extra_t.columnconfigure(0,weight=1)
        extra_t.rowconfigure(0,weight=1)
        
        self.new_ui_text_container  = Text_container(extra_t)
        
        self.new_ui_text_container.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)

    # text 2
    def new_func_ui_for_text_area_2(self):
        
        
        # 图片 区域 ，放两组图
        extra_t2 = ttk.Frame(self.new_ui_notebook)  
        self.new_ui_notebook.add(extra_t2, text= _('文档2'),sticky=tk.W+tk.N+tk.E+tk.S, )
        
        extra_t2.columnconfigure(0,weight=1)
        extra_t2.rowconfigure(0,weight=1)
        
        self.new_ui_text_container_2  = Text_container_2(extra_t2)
        
        self.new_ui_text_container_2.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        

    #

    
    # 接收信号 ,
    # 显示周边
    def new_func_bindings_receive_virtual_event(self,event):
        
        #print("  event received,extra")
        
        item_id = global_variable.current_item
        
        if global_variable.user_configure_data["extra_delay_time_use_flag"]:
            
            extra_delay_time=global_variable.user_configure_data["extra_delay_time"]
            
            # 取消 after
            if self.new_var_remember_after is not None:
                try:
                    self.after_cancel( self.new_var_remember_after )
                except:
                    pass
            
            self.after(extra_delay_time, self.new_func_show_extra,item_id,)
        else:
            self.new_func_show_extra(item_id)

    def new_func_show_extra(self,game_name):
            
        # self.new_ui_notebook
        
        if self.new_ui_image_container_1.winfo_viewable():
            self.new_ui_image_container_1.new_func_show(game_name)
            
            if self.new_ui_image_container_2.winfo_viewable():
                self.new_ui_image_container_2.new_func_show(game_name)
            
        elif self.new_ui_image_container_2.winfo_viewable():
            self.new_ui_image_container_2.new_func_show(game_name)
        
        elif self.new_ui_text_container.winfo_viewable():
            self.new_ui_text_container.new_func_show(game_name)
            
        elif self.new_ui_text_container_2.winfo_viewable():
            self.new_ui_text_container_2.new_func_show(game_name)

    def new_func_bindings_NotebookTabChanged(self,evnet=None):
        print("")
        print("NotebookTabChanged")
        self.new_func_bindings_receive_virtual_event( None )
        



    

if __name__ == "__main__" :
    root=tk.Tk()
    root.title("test")
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.rowconfigure(1,weight=0)
    root.columnconfigure(0,weight=1)

    
    #the_files.image_path_image_no="knights.png"
    
    #c = Image_container(root)
    c = Extra(root)
    c.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    
    root.mainloop()    