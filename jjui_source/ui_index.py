# -*- coding: utf_8_sig-*-

#import sys
import os
import time

import tkinter as tk
# import tkinter.ttk as ttk
import tkinter.messagebox

#from .ui__treeview_with_scrollbar import Treeview_with_scrollbar_v as Treeview_with_scrollbar
from .ui__treeview_with_scrollbar import Treeview_with_scrollbar_for_index as Treeview_with_scrollbar

# from . import global_static_key_word_translation as key_word_translation
# from . import global_static
# from . import global_variable

# from . import folders_search
#from . import folders_read 
#from . import folders_save 
from .ui_misc import misc_funcs



# 添加外部目录
# 外部目录 就保留 图标列，用 iid 标记类型，其它的不要了
#
# iid 为
#   添加 internal available_set 、internal unavailable_set
#   内置目录 第一层 : internal|一级目录名
#   内置目录 第二层 : internal|一级目录名|二级分类名
#   外置目录 第一层 : external_ini_file|文件名
#   外置目录 第二层 : external_ini_file|文件名|分类名
#
#
#
#   问题
#      | 字符在 windows 中，不可以用作文件名
#      | 字符在 linux 中，可以用作文件名
#
#       解决
#           self.new_func_index_generate_virtual_event()
#
#       在 Treeview 中，
#             如果是外部一层，文件名是现成的 
#                   type_name,index_name_level_1 = iid.split("|",1)
#             如果是外部二层，可以用 parent 的 iid 信息
#                   iid - parent_iid - "|"
#
# 生成 virtual event 
#   '<<IndexBeChosen>>'
# 用于记录信息的变量，self.new_var_data_for_virtual_event=None 
#         内置目录 第一层 : ("internal",一级目录名)
#         内置目录 第二层 : ("internal",一级目录名1，二级分类名)
#         外置目录 第一层 : ("external_ini_file",文件名)
#         外置目录 第二层 : ("external_ini_file",文件名,文类名)

# 变量前缀
# self.new_ui_
# self.new_var_
# self.new_func_
class GameIndex(Treeview_with_scrollbar):
    """
    ttk.Treeview
    """
    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        #width = self.ini_data["width_index"]
        self.new_var_data_for_virtual_event=None

    # 还有列宽度设置
    def new_func_ui(self,):
        super().new_func_ui()
        
        # 添加内容
        #   收起 横向 滚动条
        #   treeview 的一些设置
        #   右键菜单
        
        
        
        #   treeview 的一些设置
        
        # 初始化
        #self.new_ui_tree['columns'] = ("type","others","id")
        self.new_ui_tree['columns'] = ()

        #self.new_ui_tree.heading("#0", text=_("目录列表"))

        # 右键菜单
        self.new_ui_index_popup_menu = tk.Menu(self.new_ui_tree, tearoff=0)
        
        self.new_ui_index_popup_menu.add_command(label=_("全部收起"),
                command = self.new_func_index_popup_menu_function_hide_level2)
        self.new_ui_index_popup_menu.add_command(label=_("计数"),
                command = self.new_func_index_popup_menu_function_index_count)
        self.new_ui_index_popup_menu.add_command(label=_("保存"),
                command = misc_funcs.new_func_index_popup_menu_function_save)
        self.new_ui_index_popup_menu.add_command(label=_("搜索"),
                command = self.new_func_bindings_show_search_ui)
        #self.new_ui_index_popup_menu.add_command(label="显示横向滚动条",command = self.new_func_index_popup_menu_function_show_scrollbar_h)
        #self.new_ui_index_popup_menu.add_command(label="收起横向滚动条",command = self.new_func_index_popup_menu_function_hide_scrollbar_h)

    def new_func_bindings(self,):
        super().new_func_bindings()
        
        # 添加内容
        
        # 点击目录，切换游戏列表
        self.new_ui_tree.bind('<ButtonPress-1>', self.new_func_index_bindings_click ) 
        
        # 目录中，按回车键，切换游戏列表
        self.new_ui_tree.bind('<Return>', self.new_func_index_bindings_press_enter)
        
        # 右键菜单
        self.new_ui_tree.bind('<ButtonPress-3>',self.new_func_index_bindings_right_click)

        self.new_ui_tree.bind_all(r"<<RequestForIndexInfo>>",self.new_func_index_for_receive_virtual_event_RequestForIndexInfo)
        
        self.new_ui_tree.bind_all(r"<<RequestForAvailableGameList>>",self.new_func_index_for_receive_virtual_event_RequestForAvailableGameList)

        # 搜索 Ctrl + f ，显示搜索栏
        self.new_ui_tree.bind('<Control-KeyPress-f>', self.new_func_bindings_show_search_ui ) 
        self.new_ui_tree.bind('<Control-KeyPress-F>', self.new_func_bindings_show_search_ui ) 

    # bindings 鼠标点击
    def new_func_index_bindings_click(self,event):
        tree   = self.new_ui_tree
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
    def new_func_index_bindings_press_enter(self,event):
        tree = self.new_ui_tree
        row  = tree.focus()
        if row != "":
            self.new_func_index_generate_virtual_event(row)
        return "break" # 默认有列表展开 功能 ，关掉
    
    # bindings 鼠标 右键 ,弹出菜单
    def new_func_index_bindings_right_click(self,event):
        try:
            self.new_ui_index_popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.new_ui_index_popup_menu.grab_release()
    
    # 右键菜单 列表第二层内容 收起
    def new_func_index_popup_menu_function_hide_level2(self,event=None):
        # 两层
        tree = self.new_ui_tree
        for x in tree.get_children():
            for y in tree.get_children(x):
                tree.item(x,open=False) 
                break

    # 右键菜单 显示横向滚动条
    #def new_func_index_popup_menu_function_show_scrollbar_h(self,event=None):
    #    if not self.new_ui_scrollbar_h.winfo_ismapped():
    #        self.new_ui_scrollbar_h.grid()
    #    self.new_ui_tree['displaycolumns'] = ('#all')

    # 右键菜单 收起横向滚动条
    #def new_func_index_popup_menu_function_hide_scrollbar_h(self,event=None):
    #    if self.new_ui_scrollbar_h.winfo_ismapped():
    #        self.new_ui_scrollbar_h.grid_remove()
    #        self.new_ui_tree['displaycolumns'] = ()
    
    # 右键菜单，计数
    def new_func_index_popup_menu_function_index_count(self,event=None):
        tree = self.new_ui_tree
        
        number_level_1 = 0
        number_level_2 = 0
        
        for x in tree.get_children():
            number_level_1 += 1
            for y in tree.get_children(x):
                number_level_2 += 1
        
        the_text = "".join((
                _("第一层目录数量为：") + str(number_level_1) ,"\n",
                _("第二层目录数量为：") + str(number_level_2) ,"\n",
                _("总计：") + str(number_level_1 + number_level_2) ,"\n",
        ))
        
        #tkinter.messagebox.showinfo(title=None, message=None, **options)
        tkinter.messagebox.showinfo(title=_("目录数量"),message=the_text)
    
    # 生成 virtual event
    def new_func_index_generate_virtual_event(self,iid):
        #   添加 internal available_set、internal unavailable_set
        #   内置目录 第一层 : internal|一级目录名
        #   内置目录 第二层 : internal|一级目录名|二级分类名
        #   外置目录 第一层 : external_ini_file|文件名
        #   外置目录 第二层 : external_ini_file|文件名|分类名

        #         内置目录 第一层 : ("internal",一级目录名)
        #         内置目录 第二层 : ("internal",一级目录名1，二级分类名)
        #         外置目录 第一层 : ("external_ini_file",文件名)
        #         外置目录 第二层 : ("external_ini_file",文件名,文类名)
    

        event_info = self.new_func_get_virtual_event_info_from_iid(iid)
        self.new_var_data_for_virtual_event = event_info
        print(event_info)
        self.event_generate('<<IndexBeChosen>>')
        #print("index event generat")
        #print(event_info)

    def new_func_get_virtual_event_info_from_iid(self, iid ):
        
        # 生成 virtual event 
        #   '<<IndexBeChosen>>'
        # 用于记录信息的变量，self.new_var_data_for_virtual_event=None 
        #         添加 internal available_set、internal unavailable_set
        #         内置目录 第一层 : ("internal",一级目录名)
        #         内置目录 第二层 : ("internal",一级目录名1，二级分类名)
        #         外置目录 第一层 : ("external_ini_file",文件名)
        #         外置目录 第二层 : ("external_ini_file",文件名,文类名)
        
        result = []
        
        parent_iid = self.new_ui_tree.parent( iid )
        
        # 如果是第一层
        if parent_iid == "" :
            type_name,index_name_level_1 = iid.split("|",1)
            
            result.append(type_name)
            result.append(index_name_level_1)
        # 如果是第二层
        else:
            type_name,index_name_level_1  = parent_iid.split("|",1)
            
            # index_name_level_2 = iid.removeprefix(parent_iid)
            # 3.9 才有这 个 str.removeprefix()
            len_1 = len(parent_iid) + 1 # 还有一个 | 字符
            index_name_level_2 = iid[len_1:]
            
            result.append(type_name)
            result.append(index_name_level_1)
            result.append(index_name_level_2)
            
        return result
    
    # 接收信号
    # RequestForIndexInfo
    def new_func_index_for_receive_virtual_event_RequestForIndexInfo(self,event):
        
        # 收到此信号后，重新发送一个信号即可
        print()
        print("receive event  <<RequestForIndexInfo>>")
        print("generate event <<IndexBeChosen>>")
        self.event_generate('<<IndexBeChosen>>')
    
    # 接收信号
    # RequestForAvailableGameList
    def new_func_index_for_receive_virtual_event_RequestForAvailableGameList(self,event):
        
        # 收到此信号后，重新发送一个信号即可
        print()
        print("receive event  <<RequestForAvailableGameList>>")
        
        # 先
        # 清空一下
        self.new_var_data_for_virtual_event = None
        self.event_generate('<<IndexBeChosen>>')
        
        # 再
        # 发送 拥有列表 信号
        id_string = "internal" + "|" +"available_set"
        if id_string in self.new_ui_tree.get_children(""):
            
            self.new_ui_tree.see( id_string ) 
            
            self.new_ui_tree.selection_set( (id_string,) )
            
            self.new_ui_tree.focus( id_string ) 
            
            
            self.new_var_data_for_virtual_event = self.new_func_get_virtual_event_info_from_iid(id_string)
            self.event_generate('<<IndexBeChosen>>')
    
    
    def new_func_index_feed_data_internal(self,internal_index):
        pass
        
    # 添加内容 内置目录
    def new_func_index_set_content_internal(self,
            internal_index,
            #available_set=None,
            #unavailable_set=None,
            translation_dict=None,
            index_order=None,
            ):
        print()
        print("internal index feed data")
        t1=time.time()
        
        #if available_set is None:available_set=set()
        #if unavailable_set is None:unavailable_set=set()
        if translation_dict is None : translation_dict = {}
        if index_order is None      : index_order = []
        
        translation=translation_dict
        
        tree = self.new_ui_tree

        
        def add_available_set():
            
            id_string = "internal" + "|" + "available_set"
            
            if "available_set" in translation:
                tree.insert('','end',iid=id_string ,text = translation["available_set"] ,) 
            else:
                tree.insert('','end',iid=id_string ,text = "available_set" ,)
        def add_unavailable_set():
            id_string = "internal" + "|" + "unavailable_set"
            
            if "unavailable_set" in translation:
                tree.insert('','end',iid=id_string ,text = translation["unavailable_set"] ,) 
            else:
                tree.insert('','end',iid=id_string ,text = "unavailable_set" ,)
        
        
        if index_order:
        
        #index_order=global_static.index_order
        
            # list_data
            # 第一层 
            for x in index_order:
                
                if x in ("available_set","unavailable_set"): 
                # 之前 这两在 internal_index 中，现在 单独拿出来
                    if x == "available_set":
                        add_available_set()
                    if x == "unavailable_set":
                        add_unavailable_set()
                
                elif x in internal_index:
                    id_string = "internal" + "|" + x
                    
                    if x in translation:
                        tree.insert('','end',iid=id_string ,text = translation[x] ,) 
                    else:
                        tree.insert('','end',iid=id_string ,text = x ,)

            # list_data
            #第二层
            #   id 为：第一层名|第二层名
            for x in index_order:
                if x in internal_index:
                    parent_id_string = "internal" + "|" + x
                    if "children" in internal_index[x]:
                        for y in sorted( internal_index[x]["children"]):
                            id_string = parent_id_string + "|" + y
                            tree.insert(parent_id_string,'end',iid=id_string ,text = y ,) 

        else:
            # list_data
            # 第一层 
            temp_list = internal_index.keys() + ["available_set","unavailable_set"] 
            for x in sorted(internal_index.keys()):
                id_string = "internal" + "|" + x
                
                if x in translation:
                    tree.insert('','end',iid=id_string ,text = translation[x] ,) 
                else:
                    tree.insert('','end',iid=id_string ,text = x ,)
                        
            # list_data
            #第二层
            #   id 为：第一层名|第二层名

            for x in internal_index:
                parent_id_string = "internal" + "|" + x
                if "children" in internal_index[x]:
                    for y in sorted( internal_index[x]["children"]):
                        id_string = parent_id_string + "|" + y
                        tree.insert(parent_id_string,'end',iid=id_string ,text = y ,)
        t2=time.time()
        print(t2-t1)

    # 添加内容 外置目录
    def new_func_index_set_content_external_ini(self,external_index_data):
        
        print()
        print("external index feed data")
        t1=time.time()
        
        tree = self.new_ui_tree
        
        # 添加到 目录
        # 第一层
        for x in sorted( external_index_data.keys()):
            # x 为 路径 + 名称
            # ini_files[x] 为 名称，无路径
            basename = os.path.basename( x )
            iid_string_1 = "external_ini_file" + "|" + x
            tree.insert('','end',iid=iid_string_1,text=basename,)
        
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

            for y in sorted( external_index_data[x] ) :
                if y != "FOLDER_SETTINGS":
                    if y != "ROOT_FOLDER":
                        iid_string = iid_string_1 + r"|" + y
                        tree.insert(iid_string_1,'end',iid = iid_string,text=y,)
                        
        t2=time.time()
        print(t2-t1)

    # 添加内容 外置目录 ，只读目录，仅 sl 列表的功能
    # 以 xml 分类
    def new_func_index_set_content_external_xml_ini(self,external_index_data):

        
        print()
        print("external index feed data (SL by xml)")
        t1=time.time()
        
        tree = self.new_ui_tree
        
        # 添加到 目录
        # 第一层
        for x in sorted( external_index_data.keys()):
            # x 为 路径 + 名称
            # ini_files[x] 为 名称，无路径
            basename = os.path.basename( x )
            iid_string_1 = "external_xml_ini" + "|" + x
            tree.insert('','end',iid=iid_string_1,text=basename,)
        
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

            for y in sorted( external_index_data[x] ) :
                if y != "FOLDER_SETTINGS":
                    if y != "ROOT_FOLDER":
                        iid_string = iid_string_1 + r"|" + y
                        tree.insert(iid_string_1,'end',iid = iid_string,text=y,)
                        
        t2=time.time()
        print(t2-t1)
    
    # 添加内容 外置目录 ，只读目录，仅 mame 列表的功能
    # 以 source 分类
    def new_func_index_set_content_external_source_ini(self,external_index_data):
        
        print()
        print("external index feed data (mame by source)")
        t1=time.time()
        
        tree = self.new_ui_tree

        # 添加到 目录
        # 第一层
        for x in sorted( external_index_data.keys()):
            # x 为 路径 + 名称
            # ini_files[x] 为 名称，无路径
            basename = os.path.basename( x )
            iid_string_1 = "external_source_ini" + "|" + x
            tree.insert('','end',iid=iid_string_1,text=basename,)
            
            # 第二层
            for y in sorted( external_index_data[x] ) :
                if y != "FOLDER_SETTINGS":
                    if y != "ROOT_FOLDER":
                        iid_string = iid_string_1 + r"|" + y
                        tree.insert(iid_string_1,'end',iid = iid_string,text=y,)
                        
        t2=time.time()
        print(t2-t1)

        


    # 初始时，选中记录中的行
    def new_func_index_initial_select(self,iid_string):
        print()
        print("new_func_index_initial_select")
        
        flag_exist = False
        
        if iid_string:
            tree=self.new_ui_tree
            # 确认还存在
            flag_exist = False
            for x in tree.get_children():
                if iid_string == x :
                    flag_exist = True
                    break
                for y in tree.get_children(x):
                    if iid_string == y :
                        flag_exist = True
                        break
                if flag_exist:
                    break
        
        if flag_exist:
            # 存在
            
            # iid_string # 不变
            pass
        else:
            # 不存在
            
            # 默认 all_set
            iid_string = r"internal|all_set"
            
        try:
            self.new_ui_tree.selection_set( (iid_string,) )
            self.new_ui_tree.focus( iid_string )
            self.new_ui_tree.see( iid_string )
            
            #event_data = self..new_func_get_virtual_event_info_from_iid(iid_string)
            self.new_func_index_generate_virtual_event(iid_string)
        except:
            pass
    


    def new_func_bindings_show_search_ui(self,event=None):
        if self.new_ui_the_label.winfo_ismapped():
            self.new_ui_the_label.grid_remove()
        self.new_ui_search_box.focus_set()

if __name__ == "__main__" :
    from .read_pickle import read as read_pickle

    root=tk.Tk()
    root.title("index test")
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    index = GameIndex(root)
    index.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    data=read_pickle("cache_data_1.bin")
    index.new_func_index_set_content_internal(data)
    
    
    def catch_virtual_event(event):
        print()
        print("catch_virtual_event")
        
        widget = event.widget
        
        print(widget)
        
        data = widget.new_var_data_for_virtual_event
        
        if data is not None:
            if data:
                print("virtual event data")
                print(data)
        print()

    
    
    root.bind('<<IndexBeChosen>>',catch_virtual_event)
    root.mainloop()
