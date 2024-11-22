# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class Scrollable_Frame_Container(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_ui()
        self.new_func_bindings()
    
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=0)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
       
        self.new_ui_canvas = tk.Canvas(parent,
            borderwidth=0,
            highlightthickness=0,
            )
        
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_canvas.yview) 
        
        self.new_ui_scrollbar_h = ttk.Scrollbar( parent, 
                orient=tk.HORIZONTAL, 
                command=self.new_ui_canvas.xview
        )
        
        self.new_ui_canvas.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        self.new_ui_canvas.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
        
        self.new_ui_canvas.grid( row=0,column=0,sticky=tk.W+tk.N+tk.S+tk.E,)
        self.new_ui_scrollbar_v.grid(row=0,column=1,sticky=tk.N+tk.S)
        self.new_ui_scrollbar_h.grid(row=1,column=0,columnspan=2,sticky=tk.W+tk.E)
        
        # 滚动窗口
        self.new_ui_scrollable_frame =ttk.Frame(self.new_ui_canvas,)
        
        self.new_ui_canvas.create_window(
                (0, 0),
                window=self.new_ui_scrollable_frame,
                anchor=tk.NW)

    def new_func_bindings(self,):
        
        # 滚动窗口 "<Configure>" 变化时，
        #   cavans 重新设定 滚动区域
        self.new_ui_scrollable_frame.bind(
                "<Configure>",
                self.new_func_bindings_for_ui_scrollable_frame_change_size
                )

        
        self.new_ui_canvas.bind('<MouseWheel>',
                self.new_func_table_binding_mouse_wheel)
        self.new_ui_canvas.bind('<Button-4>',
                self.new_func_table_binding_mouse_wheel)
        self.new_ui_canvas.bind('<Button-5>',
                self.new_func_table_binding_mouse_wheel)
        
        # 没用
        #self.new_ui_scrollable_frame.bind('<MouseWheel>',
        #        self.new_func_table_binding_mouse_wheel)
        # 之后，
        # 找出 所有 子ui ，每一个都 bind 一下
        
    def new_func_table_binding_mouse_wheel(self,event):
        
        y1,y2 = self.new_ui_canvas.yview()
        
        if event.delta > 0 : #向上
            if y1>0:
                self.new_ui_canvas.yview(tk.SCROLL,-1,tk.UNITS)
        elif event.delta < 0:
            if y2<1:
                self.new_ui_canvas.yview(tk.SCROLL,1,tk.UNITS)
        elif event.num == 4:
            if y1>0:
                self.new_ui_canvas.yview(tk.SCROLL,-1,tk.UNITS)
        elif event.num == 5:
            if y2<1:
                self.new_ui_canvas.yview(tk.SCROLL,1,tk.UNITS)
    
    def new_func_bindings_for_ui_scrollable_frame_change_size(self,event):
        self.new_ui_canvas.configure(
                    scrollregion=self.new_ui_canvas.bbox("all"),
                )
        
    
    def new_func_get_scrollable_frame(self,):
        return self.new_ui_scrollable_frame
    
    # 插入子 ui ，然后 update() 一下，......
    def new_func_return_width(self,):
        width_scrollbar_v = self.new_ui_scrollbar_v.winfo_reqwidth()
        (x1, y1, x2, y2) =self.new_ui_canvas.bbox("all")
        return x2 + width_scrollbar_v
    
    # 当 UI 完成后，给所有 子UI ,bind 一下，
    #   让鼠标 滚动 可以 控制滚动条
    def new_func_last(self,):
        
        def new_func_find_childrens(window):
            result=[]
            
            def find_childen(window):
                for child in window.winfo_children():
                    result.append(child)
                    find_childen(child)
            
            find_childen(window)
            
            return result
        
        child_list = new_func_find_childrens( self.new_ui_scrollable_frame )
        
        for x in child_list:
            x.bind('<MouseWheel>',self.new_func_table_binding_mouse_wheel,"+")
            x.bind('<Button-4>'  ,self.new_func_table_binding_mouse_wheel,"+")
            x.bind('<Button-5>'  ,self.new_func_table_binding_mouse_wheel,"+")

        
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)    
    
    
    
    a=Scrollable_Frame_Container(root)
    a.grid(row=0,column=0,sticky=tk.W+tk.N+tk.S+tk.E,)
    b=a.new_ui_scrollable_frame
    
    number = 100
    for x in range(number):
        button=ttk.Button(b,text=str(x)+" just for test "*10)
        button.grid(row=x,column=0,sticky=tk.W)
    
    # 子ui ,bind 鼠标滚动
    a.new_func_last()
    
    root.mainloop()
