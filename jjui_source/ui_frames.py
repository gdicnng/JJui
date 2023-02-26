# -*- coding: utf_8_sig-*-
# import sys
# import os
import tkinter as tk
from tkinter import ttk 

# from . import global_variable

#user_configure = global_variable.user_configure_data

class MainFrame(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_ui()

    def new_func_ui(self,):
        
        # frames 分两行
        # menu 如果用 原始的 menu ，就不需要了
        # 内容
        
        # menu
        #   如果用 系统的 menu ，就不需要了
        #   如果用 ttk.Menubutton ，需要
        parent=self
        
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        
        self.frame_menu    =ttk.Frame( parent , )
        frame_content =ttk.Frame( parent , )
        
        self.frame_menu.grid(row=0,column=0,sticky=tk.W+tk.E,)
        frame_content.grid(row=1,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
        
        
        
        # 内容
        parent=frame_content
        
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(2, weight=0)
        parent.columnconfigure(0, weight=1)
        
        self.frame_top     = ttk.Frame( parent , ) # 上
        self.frame_middle  = ttk.PanedWindow(parent,orient=tk.HORIZONTAL)  # 中
        self.frame_bottom  = ttk.Frame( parent,   )# 下

        self.middle_1 = ttk.Frame( self.frame_middle, )
        self.middle_2 = ttk.Frame( self.frame_middle, )
        self.middle_3 = ttk.Frame( self.frame_middle, )
        
        self.frame_top.grid(row=0,column=0,sticky=tk.W+tk.E,)
        self.frame_middle.grid(row=1,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
        self.frame_bottom.grid(row=2,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
        
        #self.middle_1.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S))
        #self.middle_2.grid(row=0,column=1,sticky=(tk.W,tk.N,tk.E,tk.S))
        #self.middle_3.grid(row=0,column=2,sticky=(tk.W,tk.N,tk.E,tk.S))
        
        self.frame_middle.add(self.middle_1,weight=0)
        self.frame_middle.add(self.middle_2,weight=1)
        self.frame_middle.add(self.middle_3,weight=0)
            # weight

        ## row/column config
        self.frame_top.rowconfigure(0, weight=0)#
        self.frame_top.columnconfigure(0, weight=1)

        #
        #self.frame_bottom.rowconfigure(0, weight=0) #
        #self.frame_bottom.columnconfigure(0, weight=0)  
        #self.frame_bottom.columnconfigure(1, weight=0)  
        #self.frame_bottom.columnconfigure(2, weight=1)  
        #self.frame_bottom.columnconfigure(3, weight=0)  
        #self.frame_bottom.columnconfigure(4, weight=0)  
        #self.frame_bottom.columnconfigure(5, weight=0)  
        #self.frame_bottom.columnconfigure(6, weight=0)  

        #
        #self.frame_middle.rowconfigure(0, weight=1)
        #self.frame_middle.columnconfigure(0, weight=0)  
        #self.frame_middle.columnconfigure(1, weight=1)  
        #self.frame_middle.columnconfigure(2, weight=0)  
        
        self.middle_1.rowconfigure(0, weight=1)
        self.middle_1.columnconfigure(0, weight=1)
        self.middle_2.rowconfigure(0, weight=1)
        self.middle_2.columnconfigure(0, weight=1)
        self.middle_3.rowconfigure(0, weight=1)
        self.middle_3.columnconfigure(0, weight=1)
        
        
