# -*- coding: utf-8 -*-
#import sys
# import re

import tkinter as tk
# from tkinter import ttk
from .ui__text_with_scrollbar import Text_with_scrollbar

#default_window_size = "400x300"

default_width = 500
default_height= 500

    # modal dialog
    # https://stackoverflow.com/questions/16803686/how-to-create-a-modal-dialog-in-tkinter
    # w.grab_set 函数似乎有 bug ,win + D 最小化，会卡住，出不来
    #w.wait_visibility()   
    #w.grab_set()         
    #w.transient(parent)  
    #w.wait_window()    
    
    # w.wm_attributes("-disabled", True)
    # w.wm_attributes("-disabled", False)
        #   https://wiki.tcl.tk/9457
        #   https://wiki.tcl-lang.org/page/wm+attributes
        # 这个似乎只对 windows 有用？
        # tcl8.6.10rc2-html/tcl8.6.10/html/TkCmd/wm.htm
    
    # win.protocol('WM_DELETE_WINDOW', func) 在 mac 有 bug ?
    # https://www.python.org/download/mac/tcltk/
    #If you are using macOS 12 Monterey or later, you may see problems with file open and save dialogs when using IDLE or other tkinter-based applications. The most recent versions of python.org installers (for 3.10.0 and 3.9.8) have patched versions of Tk to avoid these problems. They should be fixed in an upcoming Tk 8.6.12 release.

# self.new_ui_
# self.new_var_
# self.new_func_
class Toplevel_Window(tk.Toplevel):
    def __init__(self,root=None,center=False,*args,**kwargs):
        
        # 如果没有指定 大小，使用默认大小
        #kwagrs_2={**kwargs}
        if ("width" not in kwargs) and ("height" not in kwargs) :
            kwargs["width"]  = default_width
            kwargs["height"] = default_height
        
        super().__init__(*args,**kwargs)
        
        self.resizable(width=True, height=True)
        
        # 位置定位
        # 新窗口，打开的位置，位于母窗口的中间
            # 万一定位不准，显示超过显示器范围，就麻烦了。
            # 多个显示器，情况是不是一样
        if center:
            # 新窗口
            width  = self.winfo_reqwidth()
            height = self.winfo_reqheight()
            
            width_of_screen =  self.winfo_screenwidth()
            height_of_screen = self.winfo_screenheight()
            
            x= int( (width_of_screen-width  )/2   )
            y= int( (height_of_screen-height)/2 )
            if x <= 0 : x=1
            if y <= 0 : y=1
            
            new_srt="".join(   (
                    str(width),
                    "x",
                    str(height),
                    "+",
                    str(x),
                    "+",
                    str(y),
                        )   )
            print("new:",new_srt)
            self.geometry( new_srt )


class Dialog_holder(Toplevel_Window):

    def __init__(self,root=None,*args,**kwargs):
        
        super().__init__(root,*args,**kwargs)
        
        if root != None : self.transient(root)

# 仅 windows
# 不用吧
class Modal_Dialog_holder_on_windows(Toplevel_Window):

    def __init__(self,root=None,*args,**kwargs):
        
        super().__init__(root,*args,**kwargs)
        
        if root != None : self.transient(root)
        
        self.new_var_root=root
        
        if root != None:
        
            root.wm_attributes("-disabled", True)
            
            self.protocol("WM_DELETE_WINDOW", self.new_func_quit)
        
    def new_func_quit(self,):
        self.new_var_root.wm_attributes("-disabled", False)
        
        self.destroy()

# windows 感觉 效果没有上一个好
# 不用吧
class Modal_Dialog_holder(Toplevel_Window):
    
    def __init__(self,root=None,*args,**kwargs):
        
        super().__init__(root,*args,**kwargs)
        
        if root != None : self.transient(root)
        
        if root != None:
            
            self.bind('<Map>'  ,self.new_func_bindings_for_map)
            
            self.bind('<Unmap>',self.new_func_bindings_for_unmap)
            
            self.protocol("WM_DELETE_WINDOW", self.new_func_quit)
    
    def new_func_bindings_for_map(self,event):
        self.lift()
        self.grab_set()
    
    def new_func_bindings_for_unmap(self,event):
        self.grab_release()
    
    def new_func_quit(self,):
        self.grab_release()
        self.destroy()


class Window_with_scrollbar(Toplevel_Window):
    def __init__(self,root=None,*args,**kwargs):
        
        super().__init__(root,*args,**kwargs)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        text_with_scrollbar = Text_with_scrollbar(self,
                horizontal=True,
                sizegrip=True,
                wrap=tk.NONE,
                )
        text_with_scrollbar.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        
        self.new_ui_text = text_with_scrollbar.new_ui_text

if __name__ == "__main__" :
    
    root=tk.Tk()
    root.title("test")
    root.geometry('200x200')

    def test_Toplevel_Window():
        t=Toplevel_Window(root,center=True)
        t.wait_window()
    def test_Dialog_holder():
        t=Dialog_holder(root)
        t.wait_window()
    def test_Modal_Dialog_holder_on_windows():
        t=Modal_Dialog_holder_on_windows(root=root)
        t.wait_window()
    def test_Modal_Dialog_holder():
        t=Modal_Dialog_holder(root=root)
        t.wait_window()
    def test_Window_with_scrollbar():
        t=Window_with_scrollbar(root)
        t.wait_window()
        
    def test():
        root.update_idletasks()
        print( root.winfo_geometry() )
        print( root.geometry() )
    tk.Button(root,text="test",command=test).grid()
    tk.Button(root,text="Toplevel_Window",command=test_Toplevel_Window).grid()
    tk.Button(root,text="Dialog_holder",command=test_Dialog_holder).grid()
    tk.Button(root,text="Modal_Dialog_holder_on_windows",command=test_Modal_Dialog_holder_on_windows).grid()
    tk.Button(root,text="test_Modal_Dialog_holder",command=test_Modal_Dialog_holder_on_windows).grid()
    tk.Button(root,text="test_Window_with_scrollbar",command=test_Window_with_scrollbar).grid()
    
    root.mainloop()



