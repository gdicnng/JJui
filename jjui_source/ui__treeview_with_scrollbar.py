# -*- coding: utf_8_sig-*-
import sys

import tkinter as tk
from tkinter import ttk

# self.new_ui_
# self.new_var_
# self.new_func_
class Treeview_with_scrollbar(ttk.Frame):
    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        self.new_func_ui()
        self.new_func_bindings()
        
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=0)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        self.new_ui_tree = ttk.Treeview(parent,
                            padding=0,
                            selectmode='browse',)
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_tree.yview)
        self.new_ui_scrollbar_h = ttk.Scrollbar( parent, orient=tk.HORIZONTAL, command=self.new_ui_tree.xview)
        
        self.new_ui_tree.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        self.new_ui_tree.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
        
        self.new_ui_tree.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.new_ui_scrollbar_v.grid(row=0,column=1,sticky=(tk.N,tk.S))
        self.new_ui_scrollbar_h.grid(row=1,column=0,sticky=(tk.W,tk.E))

    def new_func_bindings(self,):
        # bindings 目录
        # 滚动条
        
        # 鼠标 滚轮 ，列表 滚动 行数 ，改成 3 行
        #if sys.platform.startswith('win'):
            # windows 系统，不同系统，方安不太一样
        self.new_ui_tree.bind('<MouseWheel>',self.new_func_tree_binding_mousewheel )

        # 按“→”键 ，展开
        self.new_ui_tree.bind('<Right>',  self.new_func_tree_binding_key_press_right)

        # 按 空格 键 ，展开、收起，重新 bind
        self.new_ui_tree.bind('<Key-space>',self.new_func_tree_binding_key_press_space)
        
        # Home 键，到 开头
        self.new_ui_tree.bind('<Home>',lambda event : self.new_ui_tree.yview(tk.MOVETO,0))
        # End 键，到 结尾
        self.new_ui_tree.bind('<End>', lambda event : self.new_ui_tree.yview(tk.MOVETO,1))

    # treeview bindings
    
    #   原始的 bind ，展开、收起。
    #       没有子项目也展开，有些主题会显示展开符号
    #   改成，先确认有子项目，再展子
    def new_func_tree_binding_key_press_space(self,event):
        tree = event.widget
        
        #print("space")
        
        row = tree.focus()
        
        if row:
            if tree.item(row,"open"):
                #print("open to close")
                # 是展开状态
                # 需要收起
                tree.item(row,open=False)
            else:
                # 是收起状态
                # 需要展开
                #   先检查有无子项目
                #print("close to open")
                for x in tree.get_children(row):
                    tree.item(row,open=True)
                    break
        return "break"
    
    # 鼠标 滚轮 ，列表 滚动 行数 ，改成 3 行
    def new_func_tree_binding_mousewheel(self,event):
        tree = event.widget
        if event.delta > 0:
            tree.yview(tk.SCROLL,-3,"units" )
        else:
            tree.yview(tk.SCROLL,3,"units" )
        return "break"

    def new_func_tree_binding_key_press_right(self,event):
        tree = event.widget
        
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


class Treeview_with_scrollbar_v(Treeview_with_scrollbar):
    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
    
    def new_func_ui(self,):
        super().new_func_ui()
        self.new_ui_scrollbar_h.grid_remove()
    
    
if __name__ == "__main__" :
    
    root=tk.Tk()
    root.title("test")
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    index = Treeview_with_scrollbar(root)
    index.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S))
    
    tree = index.new_ui_tree
    
    # 表格真充点内容
    header=("test 1","test 2","test 3","test 4",)
    tree['columns'] = header
    for r in range(1000):
        tree.insert("",tk.END,
            iid=str(r),
            text = str(r),
            values=["row {} ,column {} ".format(r,c) for c in range(len(header))]
            )
    for x in range(20):
        tree.insert( str(5),tk.END,
            text = "{} {}".format(5,x),
            values=["row {} ,column {} ".format(5,c) for c in range(len(header))] )
    
    root.mainloop()



