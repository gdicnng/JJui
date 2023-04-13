# -*- coding: utf_8_sig-*-
import sys

import tkinter as tk
from tkinter import ttk

# 鼠标右击 ，mac 似乎不一样
if sys.platform.startswith('darwin'): # macos
    #event_mouse_right_click   = r'<Button-2>'
    #event_mouse_right_release = r'<ButtonRelease-2>'
    event_mouse_right_click_double = r'<Double-Button-2>'
else:
    #event_mouse_right_click   = r'<Button-3>'
    #event_mouse_right_release = r'<ButtonRelease-3>'
    event_mouse_right_click_double ='<Double-Button-3>'

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
        
        self.new_ui_tree.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        self.new_ui_scrollbar_v.grid(row=0,column=1,sticky=tk.N+tk.S,)
        self.new_ui_scrollbar_h.grid(row=1,column=0,sticky=tk.W+tk.E,)

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

# 分类目录处
# 一个 treeview 显示 分类目录
# 另一个 treeview 显示 搜索结果
class Treeview_for_index(ttk.Treeview):
    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        self.new_var_string_remember = ""
        self.new_var_after_remember = None

        self.new_func_bindings()
        
    def new_func_bindings(self,):
        # bindings 目录
        # 滚动条
        
        # 鼠标 滚轮 ，列表 滚动 行数 ，改成 3 行
        #if sys.platform.startswith('win'):
            # windows 系统，不同系统，方安不太一样
        self.bind('<MouseWheel>',self.new_func_tree_binding_mousewheel )

        # 按“→”键 ，展开
        self.bind('<Right>',  self.new_func_tree_binding_key_press_right)

        # 按 空格 键 ，展开、收起，重新 bind
        self.bind('<Key-space>',self.new_func_tree_binding_key_press_space)
        
        # Home 键，到 开头
        self.bind('<Home>',lambda event : self.yview(tk.MOVETO,0))
        # End 键，到 结尾
        self.bind('<End>', lambda event : self.yview(tk.MOVETO,1))

        # 按键，输入字符，一定时间后，自动向下搜索内容
        self.bind('<KeyPress>',self.new_func_tree_binding_key_press)

        # 复制 某行 显示的 文本内容
        # Ctrl + C
        self.bind('<Control-KeyPress-c>', self.new_func_copy_text ) 
        self.bind('<Control-KeyPress-C>', self.new_func_copy_text ) 

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

    def new_func_tree_binding_key_press(self,event):
        delay_time = 400 # 毫秒

        char = event.char
        if char:
            self.new_var_string_remember += char
            
            if self.new_var_after_remember is not None:
                self.after_cancel(self.new_var_after_remember)
            self.new_var_after_remember = self.after(delay_time,self.new_func_search_later_content)

    # 搜全部，有点乱
    # 在第一层：仅搜索 第一层 与 第二层展开的
    # 在第二层：仅搜索 同一层
    def new_func_search_later_content(self,):

        # 记录
        s = self.new_var_string_remember.strip().lower()
        
        # 重置
        self.new_var_string_remember = ""

        if s == "":
            return
        
        print()
        print(s)
        print()

        tree = self

        # 当前项目取值
        the_current_id = tree.focus()
        search_this_id = False
        if not the_current_id:
            return

        # 如果在第一层
        # 如果在第二层
        def find_from_level_1():
            id_1 =the_current_id
            
            # 如果第一项不在搜索范围
            # 先搜第一项的子元素
            if not search_this_id:
                if tree.item(id_1,"open"): # 展开状态  
                    child_list = tree.get_children(id_1)
                    for id_2 in child_list:
                        the_text = tree.item(id_2,"text")
                        if the_text.lower().startswith(s):
                            return id_2

            # 后面
            id_1 = tree.next(id_1)
            if id_1 :
                return later_search_for_level_one(id_1)

        def find_form_level_2():
            print("from level 2")
            # 在第二层
            
            # 仅搜同一层的元素

            # 已经在第二层了
            # 不用考虑没有选中的情况，直接搜下一个元素
            id_2 = tree.next(the_current_id)

            if id_2:
                keep_search = True
                while keep_search:
                    the_text = tree.item(id_2,"text")
                    if the_text.lower().startswith(s):
                        return id_2
                    id_2 = tree.next(id_2)
                    if not id_2:
                        keep_search = False
        
        def later_search_for_level_one(id_1):
            # 第一个要 搜索 的元素在 第一层
            #print("normal search")
            if not id_1:
                return
            
            keep_search = True
            while keep_search:
                the_text = tree.item(id_1,"text")
                #print(the_text)
                if the_text.lower().startswith(s):
                    return id_1
                
                if tree.item(id_1,"open"): # 展开状态
                    child_list = tree.get_children(id_1)
                    for id_2 in child_list:
                        the_text = tree.item(id_2,"text")
                        if the_text.lower().startswith(s):
                            return id_2
                
                id_1 = tree.next(id_1)
                if not id_1:
                    keep_search = False

        if tree.parent(the_current_id)=="":
            #print("level 1")
            the_id = find_from_level_1()
        else:
            #print("level 2")
            the_id = find_form_level_2()
           
        
        if the_id is None:
            print("not found")
            
        else:
            print(the_id)
            tree.see(the_id)
            tree.focus(the_id)
            tree.selection_set( (the_id,) )


    def new_func_copy_text(self,event):
        tree = self
        item_id  = tree.focus()
        if item_id:
            the_text = tree.item(item_id,"text")
            print(the_text)
        tree.clipboard_clear()
        tree.clipboard_append(the_text)

class Treeview_with_scrollbar_for_index(ttk.Frame):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        self.new_func_ui()
        self.new_func_bindings()
        
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(2, weight=0)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        self.new_var_search_string = tk.StringVar()
        self.new_ui_search_box = ttk.Entry(parent,textvariable=self.new_var_search_string)#justify=tk.CENTER,
        self.new_ui_search_box.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E,)
        
        self.new_ui_the_label = ttk.Label(parent,text=_("分类列表："),justify=tk.CENTER)#justify=tk.CENTER
        self.new_ui_the_label.grid(row=0,column=0,sticky="nesw",)
        
        self.new_ui_tree = Treeview_for_index(parent,
                            padding=0,
                            selectmode='browse',
                            show="tree",
                            )
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_tree.yview)
        #self.new_ui_scrollbar_h = ttk.Scrollbar( parent, orient=tk.HORIZONTAL, command=self.new_ui_tree.xview)
        
        self.new_ui_tree.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        #self.new_ui_tree.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
        
        self.new_ui_tree.grid(row=1,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        self.new_ui_scrollbar_v.grid(row=0,column=1,rowspan=2,sticky=tk.N+tk.S,)
        #self.new_ui_scrollbar_h.grid(row=2,column=0,sticky=(tk.W,tk.E))
        
        # 隐藏 下方 进度条
        #self.new_ui_scrollbar_h.grid_remove()

        # 搜索用的 treeview
        self.new_ui_tree_for_search = Treeview_for_index(parent,
                            padding=0,
                            selectmode='browse',
                            show="tree",
                            )
        self.new_ui_tree_for_search_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_tree_for_search.yview)
        
        self.new_ui_tree_for_search.configure(yscrollcommand=self.new_ui_tree_for_search_scrollbar_v.set)
        
        self.new_ui_tree_for_search.grid(row=1,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        self.new_ui_tree_for_search_scrollbar_v.grid(row=0,column=1,rowspan=2,sticky=tk.N+tk.S,)
        # 隐藏
        self.new_func_hide_treeview_for_search_result()

    def new_func_bindings(self,):
        
        # 点击 目录，显示 搜索 栏
        self.new_ui_the_label.bind('<Button-1>',self.new_func_label_be_clicked)
        # Esc
        self.new_ui_search_box.bind('<KeyPress-Escape>',self.new_func_search_box_esc)
        # Esc Esc
        self.new_ui_search_box.bind('<Double-KeyPress-Escape>',self.new_func_search_box_double_esc)
        self.new_ui_tree.bind('<Double-KeyPress-Escape>',self.new_func_search_box_double_esc)
        self.new_ui_tree_for_search.bind('<Double-KeyPress-Escape>',self.new_func_search_box_double_esc)
        # 鼠标右键双击，可能方便点
        self.new_ui_search_box.bind(event_mouse_right_click_double,self.new_func_search_box_double_esc)
        # Return
        self.new_ui_search_box.bind('<KeyPress-Return>',self.new_func_search_box_return)

        # 点击 目录搜索结果，切换游戏列表
        self.new_ui_tree_for_search.bind('<ButtonPress-1>', self.new_func_treeview_for_search_result_bindings_click ) 
        
        # 目录搜索结果 中，按回车键，切换游戏列表
        self.new_ui_tree_for_search.bind('<Return>', self.new_func_treeview_for_search_result_bindings_press_enter)
        


    def new_func_label_be_clicked(self,event=None):
        self.new_ui_the_label.grid_remove()
        self.new_ui_search_box.focus_set()
    
    def new_func_search_box_esc(self,event=None):
        self.new_var_search_string.set("")
        # 待补充，
        #   清空搜索内容
        #   还原 目录
        
    # Esc Esc
    def new_func_search_box_double_esc(self,event=None):
        if not self.new_ui_the_label.winfo_ismapped():
            self.new_ui_the_label.grid()
        
        the_selected = ""
        if  self.new_ui_tree_for_search.winfo_ismapped():
            the_selected = self.new_ui_tree_for_search.focus()
            print(the_selected)
        
        self.new_func_hide_treeview_for_search_result()

        if the_selected:
            self.new_ui_tree.focus(the_selected)
            self.new_ui_tree.selection_set( (the_selected,) ) ###
            self.new_ui_tree.see( the_selected )
            self.new_ui_tree.focus_set()

    #Return
    def new_func_search_box_return(self,event=None):
        s = self.new_var_search_string.get()
        # print(s)
        
        s=s.strip().lower()

        if not s :return

        #
        self.new_func_clear_treeview_for_search_result()

        tree   = self.new_ui_tree
        tree_2 = self.new_ui_tree_for_search

        all_id_1 = tree.get_children()
        for id_1 in all_id_1:
            
            # 第一层
            level_1_be_added = False

            the_text_1 = tree.item(id_1,"text")
            if s in the_text_1.lower():
                tree_2.insert("",tk.END,iid=id_1,text=the_text_1)
                level_1_be_added = True

            # 第二层
            all_id_2 = tree.get_children(id_1)

            for id_2 in all_id_2 :
                the_text = tree.item(id_2,"text")
                if s in the_text.lower():
                    if level_1_be_added:
                        tree_2.insert(id_1,tk.END,iid=id_2,text=the_text)
                    else:
                        tree_2.insert("",tk.END,iid=id_1,text=the_text_1)
                        level_1_be_added = True
                        tree_2.insert(id_1,tk.END,iid=id_2,text=the_text)
                        # 第一层 没有，但第二层有，展开第一层
                        tree_2.item(id_1,open=True)
        
        #
        self.new_func_show_treeview_for_search_result()

    #
    def new_func_index_generate_virtual_event(self,iid):
        pass # 内容之后填充


    def new_func_hide_treeview_for_search_result(self,):
        self.new_func_clear_treeview_for_search_result()
        try:
            self.new_ui_tree_for_search.grid_remove()
            self.new_ui_tree_for_search_scrollbar_v.grid_remove()
        except:
            pass

    def new_func_show_treeview_for_search_result(self,):
        try:
            self.new_ui_tree_for_search.grid()
            self.new_ui_tree_for_search_scrollbar_v.grid()
        except:
            pass
    # 清空内容
    def new_func_clear_treeview_for_search_result(self,):
        tree = self.new_ui_tree_for_search
        children = tree.get_children()
        if children:
            for child in children:
                tree.delete(child)


    # bindings 鼠标点击
    def new_func_treeview_for_search_result_bindings_click(self,event):
        tree   = event.widget
        row    = tree.identify_row(event.y)
        region = tree.identify_region(event.x,event.y)
    
        # 点击到 标题行 或 别地方
        if row=='':
            #print("iid empty")
            pass
        
        # 点击到 标题行
        elif region=="heading" :
            # 列表 下拉时
            # 标题栏挡住一行 内容
            # 此时，.identify_row(event.y) 仍能，标题栏后的一行的 iid
            # 需排除
            #print("region heading")
            pass
        
        else:
            #iid = row
            #print(row)
            #print("generate virtual event <<IndexBeChosen>>")
            self.new_func_index_generate_virtual_event(row)
    
    # bindings 回车键
    def new_func_treeview_for_search_result_bindings_press_enter(self,event):
        tree = event.widget
        row  = tree.focus()
        if row != "":
            self.new_func_index_generate_virtual_event(row)
        return "break" # 默认有列表展开 功能 ，关掉
    

if __name__ == "__main__" :
    
    root=tk.Tk()
    root.title("test")
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    index = Treeview_with_scrollbar_for_index(root)
    index.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
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



