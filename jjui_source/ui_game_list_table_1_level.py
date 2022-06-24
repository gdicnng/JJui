# -*- coding: utf_8_sig-*-
import sys
import os
import re

# 列表 标题 id 范围 ，增加了一个变量，之后等改一下
# new_func_set_all_columns()

import math
import time

import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font

from PIL import Image, ImageTk
 
if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

from . import global_variable
from . import global_static_filepath as the_files # 图标 图片 路径

from .ui__treeview_with_scrollbar import Treeview_with_scrollbar_v as  Treeview_with_scrollbar

from .ui_misc import  misc_funcs

#from . import initial_data
#from . import data_key_word_translation

#The_Columns             = initial_data.columns
#The_Columns_Translation = data_key_word_translation.columns_translation


"""
    
    表格的特点：
        行比较多
            主列表 几万行 
            SL列表 十几万行
            其它文件列表 ……
        列比较少
        
        每一行等高就行，这样，效率就高了
        每一列宽度不同，还好 列的数量少，一一计算，速度也不会慢

    表格标题
        内容少，可以都显示完整
        而且内容固定，内容很少变动
            调节宽度时，内容变动
            根据列标题，改变表格时，需要变动
            其它时候，内容不用变
    
    表格本体
        每次只加载，需要显示的一小部分数据
        显示的内容，根据需要，随时都有可能刷新

    大致样式：
        表格标题
        表格本体
        横、竖 滚动条

    ####################################################\
    #  图标列 \ 第1列标题 \ 第2列标题 \ 第3列标题 \ …… \
    ####################################################\
    #         \           \           \          \     \
    #         \           \           \          \     \
    #         \           \           \          \     \
    #         \           \           \          \    滚
    #         \           \           \          \    动
    #         \           \           \          \    条
    #         \           \           \          \     \
    #         \           \           \          \     \
    #         \           \           \          \     \
    #----------------滚动条-----------------------------\
    
    
"""



"""
    GameList_0
        基本 ui
    
    GameList_1
        colour and font
    
    GameList_2
        添加 数据
    
    GameList_refresh_table
        补充 new_func_refresh_table() 

"""

# font ,默认的值，应该用啥子比较好呢 ？？？？

class Data_Holder_1():
    """
    
    单层列表
    
    """

    def __init__(self,internal_data=None,external_index=None):
        
        self.gamelist_to_show = []
        self.gamelist_to_show_for_search = []

        self.flag_search  = False
        
        self.sort_key     = None
        self.sort_reverse = False
        
        #self.default_sort_key     = "name"
        self.default_sort_key     = "#0"
        
        self.filter_set = set() # 过滤内容
        
            # 要不要再加速？挺麻烦
            #self.all_set_after_filter   = set()
            #self.parent_set_after_filter= set()
            #self.clone_set_after_filter = set()
        
        # 读取变量之后，更新数据
        self.machine_dict={}
        #
        self.all_set    =set()
        self.parent_set =set()
        self.clone_set  =set()
        self.parent_to_clone = {}
        self.clone_to_parent = {}
        
        #
        self.internal_data ={}
        self.external_index={}
        #
        self.feed_data(internal_data,external_index)
    
    def feed_data(self,internal_data=None,external_index=None):
        """
        
        internal_data["mame_version"]   = mame_version
        internal_data["machine_dict"]   = machine_dict
        internal_data["set_data"]       = set_data
        internal_data["dict_data"]      = dict_data
        internal_data["internal_index"] = internal_index
        
        
        external_index
        
        """
        
        
        if internal_data is None:
            self.internal_data = {}
        else:
            self.internal_data = internal_data
        
        
        if external_index is None:
            self.external_index = {}
        else:
            self.external_index=external_index
        
        if self.internal_data:
            
            self.machine_dict    = self.internal_data["machine_dict"]
            
            self.all_set         = self.internal_data['set_data']["all_set"]
            self.parent_set      = self.internal_data['set_data']["parent_set"]
            self.clone_set       = self.internal_data['set_data']["clone_set"]
            
            self.parent_to_clone = self.internal_data['dict_data']["parent_to_clone"]
            self.parent_to_clone_keys = self.parent_to_clone.keys()
            
            self.clone_to_parent = self.internal_data['dict_data']["clone_to_parent"]
            self.clone_to_parent_keys = self.clone_to_parent.keys()
            
    
    # 点击目录 切换列表，用这个
    def generate_new_list_by_id(self,the_id_list,):
        print("generate_new_list")
        t1=time.time()
        # 生成 列表
        
        # the_id_list 
            # 格式用 list ，
            # 用基它的 set 什么的，似乎也不影响，反正要用 set() 转一下
        
        # 标记重置
        self.flag_search = False
        
        
        ###
        
        # 转为 set
        if type(the_id_list)==set or type(the_id_list)==frozenset :
            # 如果本身就是 set ，省去转化的时间
            pass
        else:
            the_id_list = set(the_id_list)
        
        # 范围 限制
        if self.filter_set:
            if self.all_set is the_id_list: 
                # all_set ,如果相同
                # 这样会不会快一点？ 
                # 主要也就是 all_set 内容太多，有点慢。
                
                # python 3.6 ，还真快了一点，因为 & 交集反回 要生一个新的 set ?
                the_id_list_new = self.all_set - self.filter_set
            else:
                the_id_list_new = self.all_set & the_id_list - self.filter_set
            
        else:
            if self.all_set is the_id_list: #
                the_id_list_new = self.all_set
            else:
                the_id_list_new = self.all_set & the_id_list

        t2=time.time()
        print("generate_new_list,time A:{}".format(t2-t1))
        
        self.gamelist_to_show = list(the_id_list_new)
        # 转为 list 
        
        t3=time.time()
        print("generate_new_list,time B:{}".format(t3-t2))
        
        
        self.sort_the_list(self.sort_key , self.sort_reverse)
        
        
        t4=time.time()
        print("generate_new_list,time C:{}".format(t4-t3))
        print("generate_new_list,time  :{}".format(t4-t1))
    
    def sort_the_list(self,the_sort_key=None,reverse=False):
        
        # 测试，数字排序
        #if the_sort_key=="#0":
        #    the_sort_key="#number"
        
        if the_sort_key==None:
            if self.sort_key == None:
                the_sort_key = self.default_sort_key
            else:
                the_sort_key = self.sort_key

        # 记录
        self.sort_key     = the_sort_key
        self.sort_reverse = reverse
    
        if self.flag_search:
            self.sort_the_list_when_search(the_sort_key,reverse)
        else:
            self.sort_the_list_when_not_search(the_sort_key,reverse)
    #
    def sort_the_list_when_search(self,the_sort_key,reverse):
        print()
        print("   sort 1 level in search")
        t1 = time.time()
        
        self.func_for_sort_the_list(the_sort_key,reverse,flag_search=True)
        
        t2 = time.time()
        print("   sort 1 level in search,time:{}".format(t2-t1))
    #
    def sort_the_list_when_not_search(self,the_sort_key,reverse,):
        print()
        print("   sort 1 level")
        t1 = time.time()
        
        self.func_for_sort_the_list(the_sort_key,reverse,flag_search=False)
        
        t2 = time.time()
        print("   sort 1 level,time:{}".format(t2-t1))
    #
    # for
    # self.sort_the_list_when_not_search()
    # self.sort_the_list_when_search()
    def func_for_sort_the_list(self,the_sort_key,reverse,flag_search):
        # sort the_id_list
        if flag_search:
            the_id_list = self.gamelist_to_show_for_search
        else:
            the_id_list = self.gamelist_to_show
        
        print("   the sort key is : {}".format(the_sort_key))
        
        #
        the_index = 0 # 列表的范围从0 开始（空列表，0 都没有）
        try:
            the_index = self.internal_data["columns"].index(the_sort_key)
        except:
            the_index = -1
            print("   the sort key not found")
        print("   the sort key's index : {}".format(the_index))
        
        if the_index == -1:
            # 范围以外，主要是点击 图标列
            # 直接以 id 排序
            print("   sort by id")
            func_for_sort = None
        else:
            def func_for_sort(item_id,temp_dict=self.machine_dict,the_index=the_index):
                return temp_dict[item_id][the_index]

        
        the_id_list.sort(
                key=func_for_sort,######
                reverse=reverse,
                )

    
    def get_the_sort_key_and_reverse(self,):
        return self.sort_key , self.sort_reverse
    #
    def get_the_sort_key_index(self,):
        the_sort_key = self.sort_key
        
        the_index=None
        
        for n in range(  len( self.internal_data["columns"] ) ):
            if the_sort_key == self.internal_data["columns"][n]:
                the_index=n
                
        if the_index is None:
            the_index=0
        
        return the_index
    #
    def set_the_sort_key_and_reverse(self,the_sort_key=None,reverse=False):
        self.sort_key     = the_sort_key
        self.sort_reverse = reverse
    #
    def set_the_sort_reverse(self,reverse=False):
        self.sort_reverse = reverse
    
    def set_the_flag_search(self,bool_value = False):
        self.flag_search = bool_value
    
    def get_the_flag_search(self,):
        return self.flag_search
    
    
    ###
    
    def get_gamelist_to_show(self,):
        if self.flag_search:
            return self.gamelist_to_show_for_search
        else:
            return self.gamelist_to_show

    def get_the_original_gamelist_dict(self,):
        return self.machine_dict
    
    def get_the_original_columns(self,):
        return self.internal_data["columns"]

    def get_current_gamelist_number(self,):
        if self.flag_search:
            return len( self.gamelist_to_show_for_search )
        else:
            return len( self.gamelist_to_show )

# 添加搜索功能
class Data_Holder_2(Data_Holder_1):
    def __init__(self,internal_data=None,external_index=None):
        super().__init__(internal_data,external_index)
    
    
    def generate_new_list_by_search(self,the_search_string,the_search_range=None):
        t1=time.time()
        # 标记重置
        self.flag_search = True
        
        the_search_string = the_search_string.lower()
        
        #if the_search_range is None:
        #    the_search_range = []
        #
        
        # 全搜
        #self.gamelist_to_show
        # 搜这个
        new_list = []
        for item_id in self.gamelist_to_show:
            for x in self.machine_dict[item_id]:
                if the_search_string in x.lower() :
                    new_list.append(item_id)
                    break
        
        self.gamelist_to_show_for_search = new_list
        
        # 限制搜索项目
        
        
        self.sort_the_list(self.sort_key , self.sort_reverse)
        
        
        t2=time.time()
        print("generate_new_list_by_search,time : {}".format(t2-t1))

    def generate_new_list_by_search_regular(self,the_search_string,the_search_range=None):
        t1=time.time()
        # 标记重置
        self.flag_search = True
        
        #if the_search_range is None:
        #    the_search_range = []
        #
        
        # 全搜
        #self.gamelist_to_show
        # 搜这个
        new_list = []
        
        p=re.compile(the_search_string,re.IGNORECASE)
        
        for item_id in self.gamelist_to_show:
            for x in self.machine_dict[item_id]:
                if  p.search(x) :
                    new_list.append(item_id)
                    break
        
        self.gamelist_to_show_for_search = new_list
        
        # 限制搜索项目
        
        
        self.sort_the_list(self.sort_key , self.sort_reverse)
        
        
        t2=time.time()
        print("generate_new_list_by_search,time : {}".format(t2-t1))

    def is_current_list_empty(self,):
        if self.gamelist_to_show: return False # 不空
        else: return True #空
        

# 配合，删除当前目录选中项
class Data_Holder_3(Data_Holder_2):
    def __init__(self,internal_data=None,external_index=None):
        super().__init__(internal_data,external_index)

    def func_for_delete_items_from_current_list(self,items):
        if len(items) == 0 :return
        
        if self.flag_search:
            the_id_list = self.gamelist_to_show_for_search
        else:
            the_id_list = self.gamelist_to_show
        
        new_list = list( set(the_id_list) - items )

        if self.flag_search:
            self.gamelist_to_show_for_search = new_list
        else:
            self.gamelist_to_show            = new_list


        flag_search   = self.flag_search  
        the_sort_key  = self.sort_key  
        reverse       = self.sort_reverse

        self.func_for_sort_the_list(the_sort_key,reverse,flag_search)
        
class Data_Holder_T(Data_Holder_3):
    """
    
    单层列表
    
    
    """

    def __init__(self,internal_data=None,external_index=None):
        super().__init__(internal_data,external_index)


Data_Holder = Data_Holder_3


#########################################

# 基本 ui 
class GameList_0(ttk.Frame):
    
    
    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "mame one level"
        
        # font
        # row height
        self.new_var_font = "TkDefaultFont"
        #self.new_var_font = "宋体 30"
        #self.new_var_font = "宋体"
        the_default_font = tk_font.nametofont('TkDefaultFont',)
        linespace = the_default_font.metrics("linespace")

        self.new_var_row_height = linespace*2
        # 还需要改一下，要比 默认图标 大一点吧 16 ，20？
        if self.new_var_row_height <20 : self.new_var_row_height = 20
        
        ###################################
        # 关于 标题 行高 初始值 ************
        # header font
        # header row height
        self.new_var_font_for_header = "TkHeadingFont"
        the_heading_font = tk_font.nametofont('TkHeadingFont',)
        heading_linespace = the_default_font.metrics("linespace")
        self.new_var_row_height_for_header = heading_linespace + 6
        
        
        
        self.new_var_virtual_event_name_StartGame = r'<<StartGame>>'
        
        self.new_var_data_for_StartGame = {}
            # "id"   = None
            # "type" = "mame"
            # "other_option" = []
            # "hide" = True
        # 初始化
        self.new_var_data_for_StartGame["type"]         = "mame" # 这个一直不变
        self.new_var_data_for_StartGame["emu_number"]   = -1 # -1 ，表示默认；1-9 用于对应数字键
        self.new_var_data_for_StartGame["id"]           = None
        self.new_var_data_for_StartGame["other_option"] = []
        self.new_var_data_for_StartGame["hide"]         = True

        # 这个放最后吧
        #self.new_func_ui()
        # self.new_func_bindings()
        ""

    # ui 部分
    def new_func_ui(self,):
        
        parent=self
        
        # 标题宽度要可调的，需要用这个选项，
        #   一开始就用
        #   不然，高度调得比初始，更小时，就会有问题
        parent.rowconfigure(0,minsize=self.new_var_row_height_for_header) 
        
        
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=1)
        parent.rowconfigure(2, weight=0)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        self.new_ui_header = tk.Canvas(parent,
            #bg="grey80",
            height =self.new_var_row_height_for_header,
            #width  =self.new_var_total_width,
            borderwidth=0,
            highlightthickness=0,
            #scrollregion=(0,0,self.new_var_total_width,self.new_var_row_height), 
            )
        
        # text test
        #self.new_ui_header.create_text(0,0,anchor="nw",text="test "*2)
        
        self.new_ui_table = tk.Canvas(parent,
            #bg="grey90",
            takefocus=1,
            #height =self.new_var_total_height,
            #width  =self.new_var_total_width,
            borderwidth=0,
            highlightthickness=0,
            #scrollregion=(0,0,self.new_var_total_width,self.new_var_total_height), 
            #yscrollincrement=self.new_var_row_height,
            )
        
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_func_y_scrollbar_changed) 
        
        self.new_ui_scrollbar_h = ttk.Scrollbar( parent, 
                orient=tk.HORIZONTAL, 
                command=self.new_func_x_scrollbar_changed
        )
        
        self.new_ui_table.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        self.new_ui_table.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
        self.new_ui_header.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
        
        self.new_ui_header.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.S,tk.E,))
        self.new_ui_table.grid( row=1,column=0,sticky=(tk.W,tk.N,tk.S,tk.E,))
        self.new_ui_scrollbar_v.grid(row=0,column=1,rowspan=3,sticky=(tk.N,tk.S))
        self.new_ui_scrollbar_h.grid(row=2,column=0,sticky=(tk.W,tk.E))

    def new_func_bindings(self,):
        pass
    

    # 纵向 滚动条，控制 table 
    def new_func_y_scrollbar_changed(self,*args):
        self.new_ui_table.yview(*args)
        self.new_func_refresh_table()
    # 横向 滚动条 ，控制 header 、 table 俩
    def new_func_x_scrollbar_changed(self,*args):
        self.new_ui_table.xview(*args)
        self.new_ui_header.xview(*args)
        self.new_func_refresh_table()

    def new_func_refresh_table(self,event=None):
        # sub class
        # 后续填充内容
        pass

    def new_func_refresh_header(self,event=None):
        # sub class
        # 后续填充内容
        pass

    def new_func_refresh_all(self,):
        # sub class
        # 后续填充内容
        pass

    def new_func_do_nothing(self,):
        print()
        print("do nothing")

# colour 
# font
# icon image 
class GameList_1(GameList_0):

    
    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_icon_width = 16
        
        self.new_func_initial_colour()
        
        self.new_func_initial_image_for_icon()
        
        
    # initial olour and font
    def new_func_initial_colour(self):
        style=ttk.Style()
        
        print("")
        print("initial colours")
        
        def get_selectforeground(class_name):# treeview
            colour = None
            for x in  style.map(class_name, "foreground" ):#[('selected', '#fbfbf8')]
                if type(x)==tuple:
                    if x[0].lower() == "selected":
                        print("foreground ,find selected")
                        print(x)
                        colour = x[1]
            return colour
        
        def get_selectbackground(class_name):# treeview
            colour = None
            for x in  style.map(class_name, "background" ):#[('selected', '#fbfbf8')]
                if type(x)==tuple:
                    if x[0].lower() == "selected":
                        print("background ,find selected")
                        print(x)
                        colour = x[1]
            return colour
        
        # 使用 Treeview 的颜色
        self.new_var_foreground = style.configure('Treeview','foreground')
        self.new_var_background = style.configure('Treeview','background')
        self.new_var_selectforeground = get_selectforeground("Treeview")
        #self.new_var_selectforeground = get_selectforeground(".")
        self.new_var_selectbackground = get_selectbackground("Treeview")
        #self.new_var_selectbackground = get_selectbackground(".")
        
        
        
        #self.new_var_foreground = style.configure('.','foreground')
        #self.new_var_background = style.configure('.','background')
        #self.new_var_selectforeground = style.configure('.','selectforeground')
        #self.new_var_selectbackground = style.configure('.','selectbackground')
        
        # 如果 Treeivew 缺少 颜色设置
        # 使用全局颜色
        
        if not self.new_var_foreground :
            self.new_var_foreground = style.configure('.','foreground')
            
            if not self.new_var_foreground :
                print("not found foreground")
                self.new_var_foreground="black"
        
        if not self.new_var_background :
            self.new_var_background = style.configure('.','background')
            
            if not self.new_var_background :
                print("not found background")
                self.new_var_background="grey90"
        
        if not self.new_var_selectforeground:
            
            #self.new_var_selectforeground = get_selectforeground(".")
            
            #if not self.new_var_selectforeground:
            
            self.new_var_selectforeground = style.configure('.','selectforeground')
                # 有没有这种选项？
            
            if not self.new_var_selectforeground:
                print("not found selectforeground")
                self.new_var_selectforeground = "white"
        
        if not self.new_var_selectbackground:
            self.new_var_selectbackground = style.configure('.','selectbackground')
                #有没有这种选项？ 
            
            if not self.new_var_selectbackground:
                print("not found selectbackground")
                self.new_var_selectbackground = "LightBlue4"
        


        

    # 读取 图标 图片 ，红 黄 绿 黑
    def new_func_initial_image_for_icon(self):
        # 读取 绿、红、黄、黑，
        #self.new_image_image_none=tk.PhotoImage()
        
        # 保存原始内容
        # 方便之后调整大小
        self.new_image_black_original    = Image.open( the_files.image_path_icon_black)
        self.new_image_green_original    = Image.open( the_files.image_path_icon_green)
        self.new_image_yellow_original   = Image.open( the_files.image_path_icon_yellow)
        self.new_image_red_original      = Image.open( the_files.image_path_icon_red )
        self.new_image_not_have_original = Image.open( the_files.image_path_icon_not_have )

        self.new_func_icon_resize()
    
    def new_func_set_icon_width(self,width):
        if width<=0: 
            width = 16
        self.new_var_icon_width = width
        self.new_func_icon_resize()
        self.new_func_refresh_table()
    
    def new_func_icon_resize(self):
        new_size = ( self.new_var_icon_width,self.new_var_icon_width )
        
        self.new_image_image_black  = ImageTk.PhotoImage( 
                self.new_image_black_original.resize(  new_size,Image.BILINEAR, ) )
        
        self.new_image_image_green  = ImageTk.PhotoImage( 
                self.new_image_green_original.resize(  new_size,Image.BILINEAR, ) )
        
        self.new_image_image_yellow = ImageTk.PhotoImage( 
                self.new_image_yellow_original.resize( new_size,Image.BILINEAR, ) )
        
        self.new_image_image_red    = ImageTk.PhotoImage( 
                self.new_image_red_original.resize(    new_size,Image.BILINEAR, ) )
                
        self.new_image_image_not_have    = ImageTk.PhotoImage( 
                self.new_image_not_have_original.resize(    new_size,Image.BILINEAR, ) )
    
    def new_func_set_colour_and_font(self,
                foreground=None,
                background=None,
                selectforeground=None,
                selectbackground=None,
                font=None,
                header_font=None,
                ):
        # 在第三组列表中，此函数有变化
        
        
        if foreground is not None:
            self.new_var_foreground = foreground
        
        if background is not None:
            self.new_var_background = background
        
        if selectforeground is not None:
            self.new_var_selectforeground = selectforeground
        
        if selectbackground is not None:
            self.new_var_selectbackground = selectbackground
        
        if font is not None:
            self.new_var_font = font
            
        if header_font is not None:
            self.new_var_font_for_header = header_font
            
        self.new_func_refresh_all()
    
    def new_func_set_row_height(self,row_height):
        if row_height > 0:
            self.new_var_row_height = row_height
            
            self.new_func_refresh_all()
    
    def new_func_set_row_height_for_header(self,row_height):
        if row_height > 0:
        
            
            self.new_var_row_height_for_header = row_height
            
            self.new_ui_header.delete('all',)
            
            self.new_ui_header.configure(height=row_height)
            
            #self.new_ui_header.grid_forget()
            
            #??????????????
            # 行高度变化 ，窗口之间大小比例
            self.rowconfigure(0,minsize=row_height)

            
            #self.new_ui_header.destroy() 
            # 完全删掉
            # 重新建立
            # 好像可以
            # 那这样，它的一些 bingings ，还有效吗？
            
            #self.new_ui_header = tk.Canvas(self,
            #    #bg="grey80",
            #    height =self.new_var_row_height_for_header,
            #    #width  =self.new_var_total_width,
            #    borderwidth=0,
            #    highlightthickness=0,
            #    #scrollregion=(0,0,self.new_var_total_width,self.new_var_row_height), 
            #    )
            
            #self.new_ui_header.grid_forget()
            #self.new_ui_table.grid_forget()
            #self.new_ui_scrollbar_v.grid_forget()
            #self.new_ui_scrollbar_h.grid_forget()
            #
            #self.new_ui_header.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.S,tk.E,))
            #self.new_ui_table.grid( row=1,column=0,sticky=(tk.W,tk.N,tk.S,tk.E,))
            #self.new_ui_scrollbar_v.grid(row=0,column=1,rowspan=3,sticky=(tk.N,tk.S))
            #self.new_ui_scrollbar_h.grid(row=2,column=0,sticky=(tk.W,tk.E))
            
            
            #self.new_ui_header.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.S,tk.E,))
            
            self.new_func_refresh_all()
        

        
# 添加 数据
# table refresh
class GameList_2(GameList_1):
    # 内置数据
    # 外部目录 数据
    # 要显示哪些列
    
    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_list_to_show = []
            # 此列表，仅保留 id ，
        self.new_var_row_numbers  = 0
        
        self.new_var_the_original_gamelist_dict = {}
            # 只保留 id 的话，读取数据原始数据
            # 方便通过 id 得到数据
        self.new_var_the_original_columns = [] 
            # 列标题 id 
        self.new_var_the_original_columns_index={} 
            # 由 列标题 id ，得到 数字index
        
        self.new_var_all_columns     = [] # 不含 icon column
        self.new_var_columns_to_show = [] # 不含 icon column
        self.new_var_column_width    = {}
        
        self.new_var_data_holder = Data_Holder()
        
        self.new_var_icon_column_id = "#0"
        # 初始值
        self.new_var_column_width[self.new_var_icon_column_id] = 30
        
        self.new_var_space_before_cell = 5
        self.new_var_space_before_icon = 5
        
        self.new_var_remember_last_index_data   = None 
        # 目录信号，记录，
        # 重复接回到相同信号时，忽略
        
        self.new_var_remember_selected_items = set()
        # 多选模式，记录 选中项
        
        self.new_var_remember_select_row_id     = None
        self.new_var_remember_select_row_number = -1
        # 用 id 、row_number 两个记录
        #
        # row_number
        #   目录，切换时，所在行数，肯定会变化
        #   用于，
        #       1，如果值不为 -1 ，方便 知道 选中行 在当前表格中的 位置
        #       2，移动到 上一行、下一行、上一页、下一页
        #           如果 选中行（高亮行）也移动
        #           方便 记录 位置
        # id
        #   用于 标记 选中行
        #   目录，切换时，也不会变。
        #       切换列表时，如果定位 选中行 的话，浪费时间。
        #       切换列表时，如果不定位 选中行 的话，
        #           如果看到高亮行，还好
        #           如果没看到高亮行，其实没有意义
        #           就这样吧
        #           不浪费时间定位了
        #   
        #
        # 每次 目录，切换时
        # 每次 搜索 ，重载列表时
        # 每次 列表 重新排序 时
        #       row_number 应重置为 -1。此时 id 不用 重置，标记选中行（高亮行）
        # 每次选中某一行时，row_number、id 要一起设置
        
        
        
        # 接收
        self.new_var_virtual_event_name_received_from_index=r'<<IndexBeChosen>>'
        # 生成
        self.new_var_data_for_CurrentGameListNumber = 0
        self.new_var_virtual_event_name_CurrentGameListNumber=r'<<CurrentGameListNumber>>'
        
        #self.new_var_data_for_CurrentGame   = "" # id ,
            # 用 global_variable.current_item
        #self.new_var_data_for_CurrentGame_2 = "" # 状态栏显示信息 # 没用上，状态栏处自己弄
        self.new_var_virtual_event_name_CurrentGame=r'<<CurrentGame>>'
    
    #def new_func_bindings(self,):
    #    
    #    super().new_func_bindings()
    #    

    
    def new_func_bindings_for_receive_virtual_event(self,):
        self.bind_all(self.new_var_virtual_event_name_received_from_index, # virtual event name 
                self.new_func_bindings_receive_virtual_event_from_index )
    
    # 初始化，feed data
    def new_func_feed_data(self,internal_data=None,external_index=None):
        self.new_var_data_holder.feed_data(internal_data,external_index)
        
        self.new_var_the_original_gamelist_dict = self.new_var_data_holder.get_the_original_gamelist_dict() # 原始的游戏列表，
    
        self.new_var_the_original_columns = self.new_var_data_holder.get_the_original_columns()
        
        self.new_var_the_original_columns_index_dict={}
        
        for n in range( len(self.new_var_the_original_columns) ):
            column_id = self.new_var_the_original_columns[n]
            
            self.new_var_the_original_columns_index_dict[column_id]=n
    
    
    # 初始化，列项目，
    #   需要显示的列，要包含在其中
    def new_func_set_all_columns(self,columns=None):
        # # columns 格式 list []
        self.new_var_all_columns = columns # 不含 icon 列
        #设置默认宽度
        self.new_func_set_default_column_width()
    
    #   列宽度 默认
    #    for
    #    self.new_func_set_all_columns() 中调用
    def new_func_set_default_column_width(self,):
        default_width = 200
        #default_icon_column_width = 30
        
        # icon 列 已设置
        # 初始值中设置
        #column = self.new_var_icon_column_id
        #self.new_var_column_width[column] = default_icon_column_width
        
        # 其它列
        for column in self.new_var_all_columns :# 不含 icon 列
            self.new_var_column_width[column] = default_width
        
    
    # 初始化，列宽度 设置
    def new_func_set_column_width(self,**kwargs):
        
        temp_dict=kwargs
        
        
        # icon 列
        column = self.new_var_icon_column_id
        if column in temp_dict:
            self.new_var_column_width[column] = temp_dict[column]
        
        # 其它列
        for column in temp_dict:
            if column in self.new_var_all_columns:
                self.new_var_column_width[column] = temp_dict[column]
    
    def new_func_get_column_width(self,):
        return self.new_var_column_width
    
    # 设置 显示 哪些列 （不含 icon 列）
    def new_func_set_columns_to_show(self,columns=None):
        # columns 格式 list []
        if columns is None:
            self.new_var_columns_to_show = []
        else:
            temp = []
            for x in columns:
                if x in self.new_var_all_columns :
                    temp.append(x)
            self.new_var_columns_to_show = temp
        print("  table set columns")
        print("  result")
        print("  {}".format(self.new_var_columns_to_show))
            
        # self.new_var_columns_to_show
        # self.new_var_total_width
        self.new_var_total_width = self.new_func_get_all_columns_width()
    
    def new_func_get_columns_to_show(self,):
        return self.new_var_columns_to_show
    # 刷新 总
    #   1 宽度 改变时，需重置此项,head bingdings 里面
    #   2 for
    #     new_func_table_reload_the_game_list()
    def new_func_refresh_all(self,):
        # self.new_var_row_height
        self.new_var_total_width = self.new_func_get_all_columns_width()
        self.new_var_row_numbers = len( self.new_var_list_to_show )
        self.new_var_total_height=self.new_var_row_numbers * self.new_var_row_height
        
        #A tuple (w, n, e, s) that defines over how large an area the canvas can be scrolled, where w is the left side, n the top, e the right side, and s the bottom.
        # 如果 0，0，0，0， 这种空的，会有影响吗
            # 管它呢
        
        self.new_ui_header.configure(scrollregion=(
                0,
                0,
                self.new_var_total_width,
                self.new_var_row_height_for_header,
                ) )
        
        self.new_ui_table.configure(scrollregion=(
                0,
                0,
                self.new_var_total_width,
                self.new_var_total_height,
                ) )
        

        
        self.new_func_refresh_header()
        
        self.new_func_refresh_table()
    
    # 表格 内容 重新载入
    #   当列表切换时，点击目录，切换列表
    #   当列表切换时，搜索，   切换列表
    #   当列表切换时，搜索 结束， 重置列表
    #   当列表切换时，击点标题 排序 ，列表顺序改变
    def new_func_table_reload_the_game_list(self,):
        self.new_var_list_to_show = self.new_var_data_holder.get_gamelist_to_show()
        print("reload")
        print(len(self.new_var_list_to_show))
        
        
        number = self.new_var_data_holder.get_current_gamelist_number()
        
        print(number)
        
        self.new_var_data_for_CurrentGameListNumber = number
        self.event_generate( self.new_var_virtual_event_name_CurrentGameListNumber )
        
        self.new_func_refresh_all()
        
    
    # 计算总宽度
    # for
    # self.new_func_refresh_all() 
    def new_func_get_all_columns_width(self,):
        
        if not self.new_var_columns_to_show:
            return 0
        
        total_width=0
        
        # 图标列 
        total_width += self.new_var_column_width[ self.new_var_icon_column_id ]
        
        # 其它列
        for x in self.new_var_columns_to_show:
            total_width += self.new_var_column_width[x]
        
        return total_width

    # 收到 目录 变化 信号
    # 游戏列表切换
    def new_func_bindings_receive_virtual_event_from_index(self,event):
        print("")
        print("index's virtual event received")
        time_1 = time.time()
        
        gameindex_window = event.widget
        event_info = gameindex_window.new_var_data_for_virtual_event
        print(event_info)
        

        
        if event_info is None : 
            # 记录
            self.new_var_remember_last_index_data = event_info # 空的也记录，方便发信号清空
            
            # 重置 标记
            self.new_var_remember_select_row_number = -1
            #self.new_var_remember_select_row_id     = None
            self.new_var_data_holder.set_the_flag_search(False)
            
            # 载入空列表，清空
            the_id_list = [] # 空
            # 载入空列表，清空
            self.new_var_data_holder.generate_new_list_by_id(the_id_list)
            # 载入空列表，清空
            self.new_func_table_reload_the_game_list() 
            
            return
        
        ####################
        ####################
        ####################
        
        # 之前是搜索状态
        if self.new_var_data_holder.get_the_flag_search():
            self.new_var_data_holder.set_the_flag_search(False)
        # 之前是正常状态
        else:
            # 重复了
            if self.new_var_remember_last_index_data == event_info:
                print("same info from index ,quit")
                return
        
        # 对比是否重复之后，再记录
        # 记录
        self.new_var_remember_last_index_data = event_info
        
        internal_data  = self.new_var_data_holder.internal_data
        external_index = self.new_var_data_holder.external_index
        internal_index = internal_data["internal_index"]
        
        
        #all_set        = internal_data["set_data"]["all_set"]        
        
        # mame
        def get_id_list():
            
            the_id_list = [] #默认值 空
            # 类型是 list
            #  或者是 set 
            # 之后都要转为 set ，方便 检查 重复的、方便 限制 范围 
            
            # 内置目录
            if event_info[0]=="internal":
                if len(event_info)==2:# 第一层
                    the_id_list = internal_index[event_info[1]]["gamelist"]
                if len(event_info)==3:# 第二层
                    the_id_list = internal_index[event_info[1]]["children"][event_info[2]]["gamelist"]
            
            # 外置目录
            elif event_info[0]=="external_ini_file":
                if len(event_info)==2:# 第一层
                    the_id_list = external_index[event_info[1]]["ROOT_FOLDER"]
                if len(event_info)==3:# 第二层
                    the_id_list = external_index[event_info[1]][event_info[2]]
            
            # 外置目录，只读，以 source 分类
            elif event_info[0]=="external_source_ini":
                the_source_list = []
                if len(event_info)==2:# 第一层
                    the_source_list = global_variable.external_index_by_source[event_info[1]]["ROOT_FOLDER"]
                elif len(event_info)==3:# 第二层
                    the_source_list = global_variable.external_index_by_source[event_info[1]][event_info[2]]
                
                temp_list = []
                
                try:
                    for the_source in the_source_list :
                        if the_source in internal_index["sourcefile"]["children"]:
                            temp_list.extend( internal_index["sourcefile"]["children"][the_source]["gamelist"] )
                except:
                    temp_list = []
                
                the_id_list = temp_list
                

                
            
            return the_id_list
        
        # software list 略有补充
        if global_variable.gamelist_type == "softwarelist":
            #"external_xml_ini"
            
            def get_id_list():
                
                the_id_list = [] #默认值 空
                # 类型是 list
                #  或者是 set 
                # 之后都要转为 set ，方便 检查 重复的、方便 限制 范围 
                
                # 内置目录
                if event_info[0]=="internal":
                    if len(event_info)==2:# 第一层
                        the_id_list = internal_index[event_info[1]]["gamelist"]
                    if len(event_info)==3:# 第二层
                        the_id_list = internal_index[event_info[1]]["children"][event_info[2]]["gamelist"]
                
                # 外置目录
                elif event_info[0]=="external_ini_file":
                    if len(event_info)==2:# 第一层
                        the_id_list = external_index[event_info[1]]["ROOT_FOLDER"]
                    if len(event_info)==3:# 第二层
                        the_id_list = external_index[event_info[1]][event_info[2]]
                
                elif event_info[0]=="external_xml_ini":
                    if len(event_info)==2:# 第一层
                        the_xml_list = global_variable.external_index_sl_by_xml[event_info[1]]["ROOT_FOLDER"]
                    if len(event_info)==3:# 第二层
                        the_xml_list = global_variable.external_index_sl_by_xml[event_info[1]][event_info[2]]
                    
                    xml_dict = internal_data["xml"]
                    for xml_name in the_xml_list:
                        if xml_name in xml_dict:
                            the_id_list.extend(  xml_dict[xml_name]  )
                
                return the_id_list
        
        
        the_id_list = get_id_list()
        
        # 重置 标记
        self.new_var_remember_select_row_number = -1
        #self.new_var_remember_select_row_id     = None
        self.new_var_data_holder.set_the_flag_search(False)
        
        self.new_var_data_holder.generate_new_list_by_id(the_id_list)
            
        self.new_func_table_reload_the_game_list()
        
        time_2 = time.time()
        print("index's virtual event received, time : {}".format(time_2 - time_1))

    def new_func_table_clear(self,):
        self.new_ui_table.delete('all',)

    # table 显示哪些 行
    def new_func_table_get_visible_rows(self,):
        """
        行数量可能比较多
        但，行高相等
        可以根据高度计算对应的行
        
        """
        #print()
        #print("get visible rows,the last row is 1 bigger")
        #最大行数，超过行数1，因为 列表从0计数
        #table = self.new_ui_table
        #width = table.winfo_width()
        height = self.new_ui_table.winfo_height()
        #x1 , x2 = table.canvasx(0) , table.canvasx(width)
        y1 , y2 = self.new_ui_table.canvasy(0) , self.new_ui_table.canvasy(height)
        
        #the_first_row =  y1/self.new_var_row_height 
        #the_last_row  = y2/self.new_var_row_height 
        #print("{},the first row".format(the_first_row))
        #print("{},the last row".format(the_last_row))
        
        #the_first_row =   math.floor(the_first_row) # 取整，退位
        #the_last_row  =   math.ceil(the_last_row) # 取整，进位,
        
        the_first_row =   math.floor(y1/self.new_var_row_height) # 取整，退位
        the_last_row  =   math.ceil(y2/self.new_var_row_height ) # 取整，进位,
        # range(the_first_row,the_last_row) 的范围在 the_last_row 之前
        
        if the_first_row<0: # 列表从 0 计数
            the_first_row=0
        #max_line_number = len( self.new_var_list_to_show )
        #if the_last_row > max_line_number :
        if the_last_row > self.new_var_row_numbers :
            #the_last_row = max_line_number 
            the_last_row = self.new_var_row_numbers 
        #   最大行数 超过一个，因为 列表从 0 开始计数
        #   不过，后面正好，range(start_row,end_row) ，不会取到最后一个值
        
        #print()
        #print("\t {},the first row ( from 0 )".format(the_first_row))
        #print("\t {},the last row ( not included )".format(the_last_row))
        return the_first_row,the_last_row

    # table 显示哪些 列
    def new_func_table_get_visible_columns(self,):
        """
        因为列数少，逐个计算，也不会慢
        visible_column_id 不含图标列
        
        # return  flag_show_icon , visible_column_id ,table_visible_width
        
        """
        #table = self.new_ui_table
        table_visible_width = self.new_ui_table.winfo_width()
        x1 , x2 = self.new_ui_table.canvasx(0) , self.new_ui_table.canvasx(table_visible_width)
        
        # icon 列
        flag_show_icon = False
        
        icon_column_width = self.new_var_column_width[ self.new_var_icon_column_id ] 
        if x1 < icon_column_width :
            flag_show_icon = True
        
        
        # 其它列
        visible_column_id=[]
        
        width_start = icon_column_width
        for x in self.new_var_columns_to_show :
        
            width     = self.new_var_column_width[x]
            
            width_end = width_start + width
            
            if  width_end <= x1 or width_start >= x2 :
                # 如果比范围小 不显示
                # 如果比范围大 不显示
                pass
            else:
                visible_column_id.append( x )
            
            width_start += width
            
        return flag_show_icon , visible_column_id , table_visible_width

    # table 刷新
    # 元素 改为 list 格式

    def new_func_refresh_table(self,event=None):
        # 当 self.new_var_list_to_show 为 空 [] 时
        # range(0,0) 
        # 似乎也不用 另外 再补充内容
        
        # 删掉小部件
        self.new_ui_table.delete('all',)
        
        #if not self.new_ui_table.winfo_viewable() : return
            # 这里，还是不要退了，
            # 有时假，窗口隐藏，
                # 然后，再出现，
                # 刷新得太快，够不上这条件，
                # 还得 root.update() 一下
        
        if not self.new_var_list_to_show : return
        
        #
        
        #space   = self.new_var_space_before_cell # 每一格，前边的空白部分
        
        #table = self.new_ui_table
        
        the_first_row , the_last_row = self.new_func_table_get_visible_rows()
            # the_last_row 要大 1，但 range(the_first_row,the_last_row)正好取小一个
        
        # 所有标题 #不含图标列
        #headers_list = self.new_var_columns_to_show

        # 图标列标记   #可见列id   #部件宽度
            # visible_column_id 不含图标列
        flag_show_icon , visible_column_id ,table_visible_width = self.new_func_table_get_visible_columns()
        
        # line_width
        if self.new_var_total_width < table_visible_width:
            line_width = table_visible_width
        else:
            line_width = self.new_var_total_width
        
        
        # 图标列
        #columns_width     = self.new_var_column_width
        #icon_column_id    = self.new_var_icon_column_id
        icon_column_width = self.new_var_column_width[ self.new_var_icon_column_id ]
        #row_height        = self.new_var_row_height
        
        # 起点 width_start_remember
        #   如果有图标列，从0开始
        width_start_remember = 0
        #   如果没有图标列，计算一下：
        if not flag_show_icon :
            width_start_remember += icon_column_width
            for x in self.new_var_columns_to_show:
                if x in visible_column_id:
                    break
                else:
                    width_start_remember += self.new_var_column_width[ x ]
        
        ####
        ####
        ####
        #visible_column_id_and_column_index = []
        #for column_id in visible_column_id:
        #    column_index = self.new_var_the_original_columns_index_dict[column_id]
        #    visible_column_id_and_column_index.append( (column_id,column_index) )
            
            
        def draw_background(row,y1,y2,item_id,background):
            # 每一行 一个 矩形 做背景
            self.new_ui_table.create_rectangle( 
                        0, 
                        y1,
                        line_width,
                        y2,
                        fill=background,
                        width=0, 
                        tags=(
                            "background_rectangle",# 此标记用于 .tag_bind
                            "item_id "+item_id, # "item_id " + item_id ,
                            # 因为不能用纯数字，所以加个字符前缀 "item_id "
                            "row_number " + str(row),
                            ),
                       )

        def draw_content(row,width_start,game_info,y1,y2,background,foreground):
            #for column_id,column_index in visible_column_id_and_column_index:
            for column_id in visible_column_id:
                column_index = self.new_var_the_original_columns_index_dict[column_id]
            
                cell_width = self.new_var_column_width[ column_id ]
                # 每一格，画一个长方形，做背景
                self.new_ui_table.create_rectangle( 
                        width_start , 
                        y1,
                        
                        width_start + cell_width,
                        y2,
                        
                        fill=background,
                        width=0,
                        state='disabled',
                       )
                # 每一格，文字内容
                self.new_ui_table.create_text( 
                        width_start + self.new_var_space_before_cell , 
                        int((y1+y2)/2),
                        anchor=tk.W,
                        #text = str(game_info[column_index]),
                        text = game_info[column_index],
                        font=self.new_var_font,
                        state='disabled',
                        fill=foreground,
                        )
                
                width_start += cell_width
                
            # 如果行尾，长度不够，有的 text 超长了，画一个长方形，挡住
            if width_start < table_visible_width:
                
                self.new_ui_table.create_rectangle( 
                        width_start , 
                        y1,
                        
                        table_visible_width,
                        y2,
                        
                        fill=background,
                        width=0,#边宽
                        state='disabled',
                       )

        for row in range(the_first_row,the_last_row ):
            
            width_start = width_start_remember
            
            item_id ,game_info= self.new_func_table_get_id_and_gameinfo_from_row_number(row)
            
            #
            # 行高度，起点
            line_position_y1 = row*self.new_var_row_height
            # 行高度，终点
            line_position_y2 = (row+1)*self.new_var_row_height # - 1 ??
            
            # 背景 与 内容
            #   == 选中行，高亮色
            #   != 其它行，普通色
            #
            
            #**********************
            #********************** 改此处
            #********************** 
            #if item_id == self.new_var_remember_select_row_id:
            if item_id in self.new_var_remember_selected_items:
                # 背景
                draw_background(row,line_position_y1,line_position_y2,item_id,self.new_var_selectbackground)
                # icon
                if flag_show_icon :
                    self.new_func_table_draw_icon_colunm(row,item_id,game_info,line_position_y1,line_position_y2,self.new_var_selectforeground)
                    width_start+=icon_column_width
                #内容
                draw_content(row,width_start,game_info,line_position_y1,line_position_y2,
                        self.new_var_selectbackground,self.new_var_selectforeground)
            else:
                # 背景
                draw_background(row,line_position_y1,line_position_y2,item_id,self.new_var_background)
                # icon
                if flag_show_icon :
                    self.new_func_table_draw_icon_colunm(row,item_id,game_info,line_position_y1,line_position_y2,self.new_var_foreground)
                    width_start+=icon_column_width
                # 内容
                draw_content(row,width_start,game_info,line_position_y1,line_position_y2,
                        self.new_var_background,self.new_var_foreground)

    
    # for
    # self.new_func_refresh_table()
    # 单独出来，方便之后 改
    def new_func_table_draw_icon_colunm(self,row,item_id,game_info,line_position_y1,line_position_y2,foreground):
        
        # 双层列表 需要变动
        #space_before_icon  = self.new_var_space_before_icon
        #space_before_icon  = self.new_var_space_before_icon_level_2
        
        #if space_before_icon < icon_column_width:
        if self.new_var_space_before_icon < self.new_var_column_width[ self.new_var_icon_column_id ]:
            # draw_icon
            self.new_func_table_draw_icon_image(
                        # x
                        self.new_var_space_before_icon,
                        # y
                        int(  (line_position_y1+line_position_y2)/2  ),
                        # image
                        self.new_func_table_choose_icon_image(game_info),
                        
                        item_id,
                        )
    

    # for
    # self.new_func_table_draw_icon_colunm()
    def new_func_table_choose_icon_image(self,game_info):
        
        # 元素为 list 格式
        # 元素第0个为 "name"
        # 元素第1个为 "status"
        
        status = game_info[1]
        
        if status=="good":
            return self.new_image_image_green
        elif status=="imperfect":
            return self.new_image_image_yellow
        elif status=="preliminary":
            return self.new_image_image_red
        else:
            return self.new_image_image_black
    # for
    # self.new_func_table_draw_icon_colunm()
    def new_func_table_draw_icon_image(self,x,y,image,item_id,):#state='disabled'
        self.new_ui_table.create_image(
                x , 
                y ,
                image=image,
                #image=self.new_image_image_not_have,
                
                anchor=tk.W,
                state='disabled',
               )
        if global_variable.flag_mark_unavailable_game:
            if  item_id not in global_variable.available_set:
                    self.new_ui_table.create_image(
                            x , 
                            y ,
                            image=self.new_image_image_not_have,
                            
                            anchor=tk.W,
                            state='disabled',
                            )
    
    
    # 单独出来，方便之后 改
    #   原来 元素是 dict 格式，现在改成 list 格式，
    def new_func_table_get_id_and_gameinfo_from_row_number(self,row_number):
        item_id   = self.new_var_list_to_show[ row_number ]
        #game_info = self.new_var_the_original_gamelist_dict[ item_id ]
        #return item_id,game_info
        return item_id , self.new_var_the_original_gamelist_dict[ item_id ]
    
    # 单独出来，方便之后 改
    def new_func_table_get_id_from_row_number(self,row_number):
        item_id   = self.new_var_list_to_show[ row_number ]
        return item_id

# header refresh
class GameList_3(GameList_2):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_column_translation={}
        
    # 设置，标题 翻译
    def new_func_header_set_column_translation(self,translation_dict=None):
        if not translation_dict : return
        
        if type(translation_dict)== dict:
            self.new_var_column_translation = translation_dict

    # header 刷新
    def new_func_refresh_header(self,event=None):
        """
        # 每列后面，有条分隔线
        # 线的 tags 为 字符 "header_vertical_line " + 原列 id
        #   图标列 分隔线 tags 为两组：
        #       "header_vertical_line"
        #       "id" + column_id
        #           前面加字符，避免 数字字符串 被识别为数字，而数字是 cavnas items 的 id
        #   ……
        
        ##############################
        #    |     |     |     |    |#
        ##############################
        
        """
        
        # 清空，删掉小部件
        self.new_ui_header.delete('all',)
        
        # 所有标题
        headers_list = self.new_var_columns_to_show

        sapce = self.new_var_space_before_cell
        background_colour=self.new_var_background
        foreground_colour=self.new_var_foreground

        icon_column_id = self.new_var_icon_column_id
        columns_width  = self.new_var_column_width
        icon_width     = columns_width[ icon_column_id ]
        row_height     = self.new_var_row_height_for_header

        borderwidth = 0 # 要不要 border 呢 ？
        def draw_background(width_start,cell_width,column_id=""):
            self.new_ui_header.create_rectangle( 
                        width_start, 
                        0,
                        
                        width_start + cell_width,
                        row_height,
                        
                        fill         =self.new_var_background,
                        activefill   =self.new_var_selectbackground,
                        width        =borderwidth,
                        #state=tk.DISABLED,
                        tags=(
                                "header_backgroud_rectangle" , 
                                "column_id " + column_id )
                       )

        # column_id 最后一格补长度的,没有 id，没有 tag
        def draw_background_no_id(width_start,cell_width):#column_id 最后一格补长度的没有
            self.new_ui_header.create_rectangle( 
                        width_start, 
                        0,
                        
                        width_start + cell_width,
                        row_height,
                        
                        fill         =self.new_var_background,
                        width        =borderwidth,
                       )
        def draw_content(width_start,text,column_id):
            self.new_ui_header.create_text( 
                       width_start + sapce, 
                       # 图标列 +x*self.new_var_row_height,
                       int(row_height/2),
                       anchor=tk.W,
                       text=text ,
                       fill=self.new_var_foreground,
                       font=self.new_var_font_for_header,
                       #activefill='red',
                       state='disabled',
                       tags=( 
                       #"header_text" , # 用不着
                       "header_text " + column_id,# 唯一标记，准确识别
                        )
                       )
        def draw_vertical_line(width_start,cell_width,column_id):
            self.new_ui_header.create_line(
                        width_start + cell_width , 0 ,# x0 , y0
                        width_start + cell_width , row_height , # x1 ,y1
                        fill = foreground_colour ,
                        width=1,# 宽度
                        tags=(
                                "header_vertical_line" , 
                                "column_id " + column_id ),
                                # 两组 tags
                        )
        
        
        # 图标列
        draw_background(0,icon_width,icon_column_id)
        
        # 其它列
        width_start = icon_width 
        for x in headers_list:
            cell_width = columns_width[x]
            
            # 每一格 画一个 矩形 做背景
            the_text = self.new_var_column_translation.get(x,x)
            
            draw_background(width_start,cell_width,x)
            draw_content(width_start,the_text,x)
            
            width_start = width_start + cell_width
        
        # 如果列表宽度不足显示长度
        # 画个长方形，挡住超长的文字
        total_table_width   = self.new_func_get_all_columns_width()
        total_visible_width = self.new_ui_header.winfo_width()
        if total_table_width<total_visible_width :
            temp = total_visible_width - total_table_width
            draw_background_no_id(width_start,temp)
        
        
        # 分隔线 后画，
        #       后画的，在上一层，不会被挡住
        # 图标列 
        #   就一条分隔线
        draw_vertical_line(0,icon_width,icon_column_id)
        width_start = icon_width
        for x in headers_list:
            cell_width = columns_width[x]
            draw_vertical_line(width_start,cell_width,x)
            width_start = width_start + cell_width


        # 标题 与 表格本体 之间的分隔线
        self.new_ui_header.create_line(
            0 , row_height-1,
            self.new_var_total_width , row_height-1,
            fill=foreground_colour,
            state='disabled',
            )
    

# header bindings
class GameList_4(GameList_3):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        # 鼠标托动标题栏分隔线 标记 
        self.new_var_the_dragged_line_info=None
    
    def new_func_bindings(self,):
        super().new_func_bindings()
        
        header = self.new_ui_header
        
        # header bindings
        
        # 外形变化，刷新
        header.bind( '<Configure>',self.new_func_header_resize)
        
        #   鼠标 经过 分隔线时，变化
        header.tag_bind("header_vertical_line", '<Enter>',self.new_func_header_binding_cursor_change)
        #   鼠标 离开 分隔线时，变化 变回来
        header.tag_bind("header_vertical_line", '<Leave>',self.new_func_header_binding_cursor_change_back)
        
        #   鼠标 拖拽 ，点击，起始状态记录
        header.tag_bind("header_vertical_line", '<ButtonPress-1>',self.new_func_header_binding_drag_start)
        #   鼠标 拖拽 中 
        header.tag_bind("header_vertical_line", '<B1-Motion>',self.new_func_header_binding_dragging)
        #   鼠标 拖拽 ，放开，末尾状态处理
        header.tag_bind("header_vertical_line", '<ButtonRelease-1>',self.new_func_header_binding_drag_end)

        # 进入 标题 cell，背景色、文字色 变化
        header.tag_bind( "header_backgroud_rectangle",'<Enter>',self.new_func_header_binding_enter_a_cell)
        # 离开 标题 cell，背景色、文字色 变化
        header.tag_bind( "header_backgroud_rectangle",'<Leave>',self.new_func_header_binding_leave_a_cell)
        
        # 点击标题，排序
        header.tag_bind( "header_backgroud_rectangle",'<Button-1>',self.new_func_header_binding_click)

       
    
    
    def new_func_header_resize(self,event):
        self.new_func_refresh_header()

    # header bindings
    #   鼠标移动到 竖线 分隔线 上时，鼠标图案变化
    def new_func_header_binding_cursor_change(self,event=None):
        self.new_ui_header.configure(cursor='sb_h_double_arrow')
    # header bindings
    #   鼠标移动离开 竖线 分隔线 上时，鼠标图案，变回来
    def new_func_header_binding_cursor_change_back(self,event=None):
        self.new_ui_header.configure(cursor='')

    # header bindings
    #   鼠标 拖拽 ，点击，起始状态记录
    def new_func_header_binding_drag_start(self,event):
        # line_id ,        此分隔线 在 canvas 中 的 id
        # line_position ，此分隔线 在 canvas 中的位置
        
        # column_id ,此列 标题 id
        # left_length ,此列 标题 列宽

            # 竖线 位于 位置对应 单元格右侧，
            # 竖线与单元隔一一对应
            # 单元格 | 下一格 |
            # left_length | …… | …… |
        
        
        # line_id
        print("drag start")
        header=self.new_ui_header
        line_id = header.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        line_id = line_id[0] # canvas 内的元素，id 是一个整数
        print("line id is {} ".format(line_id))
        tags = header.gettags(line_id)
        #('header_vertical_line', 'column_id ????', 'current')
        
        # column_id
        #提取 id ，"column_id " 开头
        column_id=''
        for x in tags:
            if x.startswith("column_id " ):
                column_id=x[len("column_id "):]
                break
        print(column_id)
        

        # line_position
        line_position = 0
        line_position += self.new_var_column_width[ self.new_var_icon_column_id ]
        if column_id != self.new_var_icon_column_id :
            for x in self.new_var_columns_to_show:
                if x == column_id:
                    line_position += self.new_var_column_width[ x ]
                    break
                else:
                    line_position += self.new_var_column_width[ x ]
        
        # left_length ,就是单元格 的长度
        left_length = self.new_var_column_width[ column_id ]

        
        self.new_var_the_dragged_line_info = {}
        self.new_var_the_dragged_line_info["line_id"]       = line_id
        self.new_var_the_dragged_line_info["column_id"]     = column_id
        self.new_var_the_dragged_line_info["left_length"]   = left_length
        self.new_var_the_dragged_line_info["line_position"] = line_position
        self.new_var_the_dragged_line_info["new_position"]  = line_position
        print(self.new_var_the_dragged_line_info)

    #   鼠标 拖拽 中 
    #   标题栏，竖线 分隔线，鼠标拖动，改变列宽
    def new_func_header_binding_dragging(self,event):
        
        if not self.new_var_the_dragged_line_info :
            return
        
        header=self.new_ui_header
        line_id = header.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        line_id = line_id[0] # canvas 内的元素，id 是一个整数
        
        if line_id   != self.new_var_the_dragged_line_info["line_id"]:
            return
        
        #tags = header.gettags(line_id)
        #print(tags)
        #('header_vertical_line', 'column_id ????', 'current')
        
        left_length   = self.new_var_the_dragged_line_info["left_length"]
        line_position = self.new_var_the_dragged_line_info["line_position"]

        x0=event.x
        x=header.canvasx(x0)
        
        min_width = 10
        if x > line_position - left_length  + min_width : 
            print(x)
            move= x-self.new_var_the_dragged_line_info["new_position"]
            self.new_var_the_dragged_line_info["new_position"] = x
            header.move(line_id,move,0)

    # header bindings
    #   鼠标 拖拽 ，放开，结束状态处理    
    def new_func_header_binding_drag_end(self,event):
        #self.new_var_the_dragged_line_info["line_id"]       = line_id
        #self.new_var_the_dragged_line_info["column_id"]     = column_id
        #self.new_var_the_dragged_line_info["left_length"]   = left_length
        #self.new_var_the_dragged_line_info["line_position"] = line_position
        #self.new_var_the_dragged_line_info["new_position"] = line_position

        if not self.new_var_the_dragged_line_info :
            return
        
        header=self.new_ui_header
        line_id = header.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        line_id = line_id[0] # canvas 内的元素，id 是一个整数
        
        if line_id != self.new_var_the_dragged_line_info["line_id"]:
            return
        
        #tags = header.gettags(line_id)
        #print(tags)
        #('header_vertical_line', 'column_id ????', 'current')
            
        new_position  = self.new_var_the_dragged_line_info["new_position"]
        line_position = self.new_var_the_dragged_line_info["line_position"]
        column_id     = self.new_var_the_dragged_line_info["column_id"]

        self.new_var_the_dragged_line_info = {} # 删除,清空
        
        if new_position == line_position:
            pass
        else :
            temp=new_position-line_position
            self.new_var_column_width[column_id] +=  temp
            

            
            self.new_func_refresh_all()


    # header bindings
    # 进入 标题 cell，背景色、文字色 变化
    def new_func_header_binding_enter_a_cell(self,event):
        #rectangle_id
        #print("enter")
        header=self.new_ui_header
        id_in_cavans = header.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        id_in_cavans = id_in_cavans[0] # canvas 内的元素，id 是一个整数
        #print("id_in_cavans: {} ".format(id_in_cavans))
        tags = header.gettags(id_in_cavans)
        #('header_vertical_line', 'column_id ????', 'current')
        
        # column_id
        #提取 id ，"column_id " 开头
        column_id=''
        for x in tags:
            if x.startswith("column_id " ):
                column_id=x[len("column_id "):]
                break
        #print(column_id)
        
        #对应的文本
        #tags="header_text " + column_id
        text_item_tag="header_text "+column_id
        #print(text_item_tag)
        header.itemconfigure(text_item_tag, fill=self.new_var_selectforeground)

    # header bindings
    # 离开 标题 cell，背景色、文字色 变化
    def new_func_header_binding_leave_a_cell(self,event):
        #rectangle_id
        #print("leave")
        header=self.new_ui_header
        id_in_cavans = header.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        id_in_cavans = id_in_cavans[0] # canvas 内的元素，id 是一个整数
        #print("id_in_cavans: {} ".format(id_in_cavans))
        tags = header.gettags(id_in_cavans)
        #('header_vertical_line', 'column_id ????', 'current')
        
        # column_id
        #提取 id ，"column_id " 开头
        column_id=''
        for x in tags:
            if x.startswith("column_id " ):
                column_id=x[len("column_id "):]
                break
        #print(column_id)
        #对应的文本
        #tags="header_text " + column_id
        text_item_tag="header_text "+column_id
        #print(text_item_tag)
        header.itemconfigure(text_item_tag, fill=self.new_var_foreground)

    # 击点标题 排序
    def new_func_header_binding_click(self,event):
        time_1 =time.time()
        #rectangle_id
        print("")
        print("click on header , sort ")
        header=self.new_ui_header
        id_in_cavans = header.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        id_in_cavans = id_in_cavans[0] # canvas 内的元素，id 是一个整数
        print("id_in_cavans: {} ".format(id_in_cavans))
        tags = header.gettags(id_in_cavans)
        #('header_vertical_line', 'column_id ????', 'current')
        
        # column_id
        #提取 id ，"column_id " 开头
        column_id=''
        for x in tags:
            if x.startswith("column_id " ):
                column_id=x[len("column_id "):]
                break
        print("header id : {}".format(column_id))
        
        the_old_sort_key,old_reverse = self.new_var_data_holder.get_the_sort_key_and_reverse()
        
        if column_id == the_old_sort_key:
            reverse = not old_reverse
        else:
            reverse = False
        
        #self.new_var_data_holder.set_the_sort_reverse(reverse)
        
        self.new_var_data_holder.sort_the_list(column_id,reverse)
        
        
        # 重置 标记
        self.new_var_remember_select_row_number = -1
        #self.new_var_remember_select_row_id     = None
        
        self.new_func_table_reload_the_game_list()
        

        
        time_2=time.time()
        print("click on header , sort ,time : {}".format(time_2-time_1))


# table bindings
class GameList_5(GameList_4):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)


    def new_func_bindings(self,):
        super().new_func_bindings()
        
        table  = self.new_ui_table
        
        # table bindings
        #   table 大小变化时，刷新
        table.bind('<Configure>',  self.new_func_table_binding_resize)
        
        #   鼠标单击
        table.tag_bind("background_rectangle",'<Button-1>', self.new_func_table_binding_single_click )
        #   鼠标双击
        table.tag_bind("background_rectangle",'<Double-Button-1>', self.new_func_table_binding_double_click,)
        #   鼠标右击
        table.tag_bind("background_rectangle",'<Button-3>', self.new_func_table_binding_right_click,)

    # table bindings ，变化大小时，刷新列表
    def new_func_table_binding_resize(self,event):
        self.new_func_refresh_table()

    # for
    #   鼠标点击事件 ： 单击、右击、双击
    #   得到 row number , item id 
    def new_func_table_get_row_number_and_item_id(self,event):
        widget=self.new_ui_table
        id_in_cavans = widget.find_withtag(tk.CURRENT)# 这个反回的是一个列表
        id_in_cavans = id_in_cavans[0] # canvas 内的元素，id 是一个整数
        #print("id_in_cavans is {} ".format(id_in_cavans))
        tags = widget.gettags(id_in_cavans)
        #print(tags)
        
        #提取 id ，"item_id " 开头
        item_id    =''
        row_number =-1 # 行从0计数
        for x in tags:
            if x.startswith("item_id " ):
                item_id=x[len("item_id "):]
            elif x.startswith("row_number " ):
                row_number=int( x[len("row_number "):] )
        
        return row_number,item_id
    
    # wip
    # table binding 鼠标 单击 ( 范围 是 每行的 背景矩形)
    # 1 选择行
    # 2 发送信号，显示周边 ，待补充
    def new_func_table_binding_single_click(self,event):
        print()
        print("single click")

        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        print("item id : {}".format(item_id) )
        print("row number : {}".format(row_number) )
        
        self.new_func_remember_select_row(item_id,row_number)

    # wip
    # table binding 鼠标 双击 ( 范围 是 每行的 背景矩形)
    # 1 选择行 ，这个不用了吧，和 鼠标单击 重复了
    # 2 发送信号，打开游戏，待补充
    def new_func_table_binding_double_click(self,event):
        #print()
        #print("double click")
        #
        #row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        #print("item id : {}".format(item_id) )
        #print("row number : {}".format(row_number) )
        
        # 1 选择行 ，这个不用了吧，和 鼠标单击 重复了
        #self.new_func_remember_select_row(item_id,row_number)
        ""
    
    # wip
    #鼠标 右击
    # 1 选择行 ，这个不用了吧，和 鼠标单击 重复了
    # 2 弹出菜单，待补充
    def new_func_table_binding_right_click(self,event):
        print()
        print("right click")

        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        print("item id : {}".format(item_id) )
        print("row number : {}".format(row_number) )
        
        self.new_func_remember_select_row(item_id,row_number)
    
    # table 标记选中行
    # 鼠标点击，选中 ；鼠标右击 ？不用吧
    # 按键 上 下 选中，wip
    # 按键 pagedow pageup ? 不用吧
    # wip
    # 每次 状态栏显示信息变化
    def new_func_remember_select_row(self,item_id,row_number,):

        self.new_var_remember_select_row_id     = item_id
        self.new_var_remember_select_row_number = row_number
        
        # 多选模式 标记 清理
        ##################
        self.new_var_remember_selected_items.clear()
        self.new_var_remember_selected_items.add(item_id)
        ##################

        
        #print()
        #print("  select row : {} ".format(row_number) )
        #print("  select id  : {} ".format(item_id)    )
        
        self.new_func_refresh_table()
        
        #self.new_var_data_for_CurrentGame = item_id
        global_variable.current_item = item_id
        self.event_generate( self.new_var_virtual_event_name_CurrentGame )
        


# bindings 
#   Home、End 、上、下、PageUp、PageDown 键
#   鼠标 滚轮 # widows / linux
#   上、下 的时候，选中行要在显示范围里
class GameList_6(GameList_5):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)


    def new_func_bindings(self,):
        super().new_func_bindings()
        
        table  = self.new_ui_table
        # 鼠标滚动，似乎只有 windows 是这样
        table.bind('<MouseWheel>',self.new_func_table_binding_mouse_wheel)
        table.bind('<Button-4>',self.new_func_table_binding_mouse_wheel)
        table.bind('<Button-5>',self.new_func_table_binding_mouse_wheel)
        
        
        self.bind('<Home>'  , self.new_func_binding_key_press_home)
        self.bind('<End>'   , self.new_func_binding_key_press_end)
        self.bind('<Up>'    , self.new_func_binding_key_press_up)
        self.bind('<Down>'  , self.new_func_binding_key_press_down)
        self.bind('<Next>'  , self.new_func_binding_key_press_pagedown)
        self.bind('<Prior>'  , self.new_func_binding_key_press_pageup)
        

    # binding function  按 Home 键，到 首行 位置
    def new_func_binding_key_press_home(self,event):
        self.new_ui_table.yview(tk.MOVETO,0)
        self.new_func_refresh_table()

    # binding function  按 End 键，到 末行 位置    
    def new_func_binding_key_press_end(self,event=None):
        self.new_ui_table.yview(tk.MOVETO,1)
        self.new_func_refresh_table()

    # binding function  按键 上，上移一行 ，
    def new_func_binding_key_press_up(self,event):
        if not self.new_var_list_to_show :
            return

        if self.new_var_remember_select_row_number < 0 :
            # 之前，没有选中 行
            new_row_number = 0
        elif self.new_var_remember_select_row_number == 0:
            # 之前，选中第一行
            # 不变
            new_row_number = 0
        else:
            # 之前，选中最后其它行 
            new_row_number = self.new_var_remember_select_row_number - 1
            
            # 范围
            if new_row_number < 0 :
                new_row_number = 0
            
        item_id,game_info = self.new_func_table_get_id_and_gameinfo_from_row_number(new_row_number)
        
        
        self.new_func_table_jump_to_row( new_row_number ,need_refresh=False)
            # 这个 退出的 条件比较多，可能到不了 refresh，干脆不用 refresh
            # 放前面
        
        self.new_func_remember_select_row(item_id,new_row_number)
            # 这个必然 refresh
            # 放后面
        ""

    # binding function  按键 下，下移一行
    def new_func_binding_key_press_down(self,event):
        
        if not self.new_var_list_to_show :
            return
        
        if self.new_var_remember_select_row_number < 0 :
            # 之前，没有选中 行
            new_row_number = 0
        elif self.new_var_remember_select_row_number == self.new_var_row_numbers - 1:
            # 之前，选中最后一行 
            # 不变
            new_row_number = self.new_var_remember_select_row_number
        else:
            # 之前，选中最后其它行 
            new_row_number = self.new_var_remember_select_row_number + 1
            
            # 范围
            if new_row_number >= self.new_var_row_numbers :
                new_row_number = self.new_var_row_numbers - 1
        
        item_id,game_info =  self.new_func_table_get_id_and_gameinfo_from_row_number(new_row_number)
        
        
        self.new_func_table_jump_to_row( new_row_number ,need_refresh=False)
            # 这个 退出的 条件比较多，可能到不了 refresh，干脆不用 refresh
            # 放前面
        
        self.new_func_remember_select_row(item_id,new_row_number)
            # 这个必然 refresh
            # 放后面
        
        ""
        
        
    # binding function  按键 pageup，向上翻页 ，
    def new_func_binding_key_press_pageup(self,event):
        if not self.new_var_list_to_show :
            return
        
        a,b = self.new_ui_table.yview()
        if a<=0: return        

        height = self.new_ui_table.winfo_height()
        lines  = height/self.new_var_row_height
        
        # flag ，标记，是否要多保留一行
        # 当只有一行、两行时，不用多保留
        if lines > 2 :lines = lines -1
        else:pass
        
        change = lines/self.new_var_row_numbers
        
        a = a - change
        if a < 0:a=0
        self.new_ui_table.yview(tk.MOVETO,a)
        
        self.new_func_refresh_table()

    # binding function  按键 pagedown，向上翻页 ，
    def new_func_binding_key_press_pagedown(self,event):
        if not self.new_var_list_to_show :
            return
        
        a,b = self.new_ui_table.yview()
        if b>=1: return        

        height = self.new_ui_table.winfo_height()
        lines  = height/self.new_var_row_height
        
        # flag ，标记，是否要多保留一行
        # 当只有一行、两行时，不用多保留
        if lines > 2 :lines = lines -1
        else:pass
        
        change = lines/self.new_var_row_numbers
        
        a,b = a+change,b + change
        if b >= 1:
            self.new_ui_table.yview(tk.MOVETO,1)
        else:
            self.new_ui_table.yview(tk.MOVETO,a)
        
        self.new_func_refresh_table()

    # binding function  鼠标 滚动 上 下 滚动 三行
    def new_func_table_binding_mouse_wheel(self,event):
        if not self.new_var_list_to_show :
            return
        
        if event.delta > 0: #向上
            self.new_func_table_for_mouse_wheel_move_up()
        elif event.delta < 0: # 向下
            self.new_func_table_for_mouse_wheel_move_down()
        elif event.num == 4:
            self.new_func_table_for_mouse_wheel_move_up()
        elif event.num == 5:
            self.new_func_table_for_mouse_wheel_move_down()
        
        self.new_func_refresh_table()

    def new_func_table_for_mouse_wheel_move_up(self,):
        #print("up")
        
        a,b = self.new_ui_table.yview()
        #print(a,b)
        
        # 3 行 
        def get_changed_number():
            return   3/self.new_var_row_numbers
            
        
        if a<=0: 
            #print("no move")
            return  # 无需改变
        
        c = get_changed_number()
        
        a,b =a-c,b-c
        if a < 0: a=0
        self.new_ui_table.yview(tk.MOVETO,a)
        
    def new_func_table_for_mouse_wheel_move_down(self,):
        #print("down")
        a,b = self.new_ui_table.yview()
        #print(a,b)
        
        # 3 行 
        def get_changed_number():
            return   3/self.new_var_row_numbers
            
        
        if b >= 1: 
            #print("no move")
            return # 无需改变
        
        c = get_changed_number()
        a,b=a+c,b+c
        if b >= 1: 
            self.new_ui_table.yview(tk.MOVETO,1)
        else:
            self.new_ui_table.yview(tk.MOVETO,a)

    # 跳转到指定行
    def new_func_table_jump_to_row(self,row_number,need_refresh=True):
        if row_number < 0 : return
        #if not self.new_var_list_to_show : return # 和下一条，有点重复
        if row_number >= self.new_var_row_numbers : return # 从0开始，要小一个
        
        #table   = self.new_ui_table
        
        # 表格 显示 高度坐标 范围
        height  = self.new_ui_table.winfo_height()
        
        # 高度上，能显示全部表格内容：
        if height >= self.new_var_total_height: return
        
        #print()
        #print("jump to row:{}".format(row_number))
        
        # 指定的行 高度坐标 范围 
        h1 = row_number * self.new_var_row_height
        h2 = h1 + self.new_var_row_height
        
        
        y=(h1+h2-height)/2 # 显示在中间
            
            ####  顶点处：(h1+h1)/2  - height/2
            ####
            ####  中心处：(h1+h1)/2 
            ####
            ####  末尾处：(h1+h1)/2  + height/2
        
        
        
        # 坐标 转为 比例 0-1
        y=y/self.new_var_total_height
        
        if   y < 0 : y=0
        elif y > 1 : y=1
        
        self.new_ui_table.yview(tk.MOVETO,y)
        
        if need_refresh:
            self.new_func_refresh_table()


# 右键 菜单
class GameList_7(GameList_6):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_virtual_event_name_MameShowInfo = r'<<MameShowInfo>>'
        
        
        # 编辑 外部 目录
            # 当前目录，被编辑过
            #    在搜索状态，清空搜索时，如果有这个标记，重载数据时 需要 重新计算
        self.new_var_flag_current_index_be_edited = False
            # 需要重新定义 reload 函数、接收目录信号函数
            #
            # 在 每一次 接收目录信号函数 中，重置标记为 False
            # 每一次编辑当前目录时，重置标记为 False
                # 只是 删減 当前目录 时 才有
                # 添加，不影响
                    # 因为能看到的都是当前目录，
                    # 不需要 添加到 当前 目录 这种 操作，如果添加时选中当前目录，直接 return
                    # 只能是 添加到 别的目录
            # 所以，
            # 需要在 下面 接收 <<GameListSearchClear>> 信号时，修改一下
            # 每一次编辑当前目录时，重置标记为 False
            # 每一次修改，重置目录记录为 None （self.new_var_remember_last_index_data）
        ""

    def new_func_ui(self,):
        super().new_func_ui()
        self.new_func_ui_pop_up_menu_for_table()
        self.new_func_ui_pop_up_menu_for_header()
    
    def new_func_bindings(self,):
        super().new_func_bindings()
        #header = self.new_ui_header
        #table  = self.new_ui_table
        self.new_ui_header.bind('<Button-3>', self.new_func_header_show_pop_up_menu,"+",)
        
        # 之前的：
        #table.tag_bind("background_rectangle",'<Button-3>', self.new_func_table_binding_right_click,)
        
        self.new_ui_table.tag_bind("background_rectangle",'<Button-3>',  self.new_func_table_show_pop_up_menu,"+",)
    
    def new_func_ui_pop_up_menu_for_table(self,):
        self.new_ui_pop_up_menu_for_table = tk.Menu(self , tearoff=0)
        
        self.new_ui_pop_up_menu_for_table.add_separator()
        
        self.new_ui_pop_up_menu_for_table.add_command(
                label=_("运行游戏"),
                command = self.new_func_table_pop_up_menu_callback_start_game
                )
        
        if global_variable.gamelist_type == "mame" :
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("运行游戏，不隐藏 UI"),
                    command = lambda hide_value=False: self.new_func_table_pop_up_menu_callback_start_game(hide=hide_value)
                    )
                    
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("运行游戏，开启多键盘功能"),
                    command = lambda hide_value=False: self.new_func_table_pop_up_menu_callback_start_game(other_option=["-multikeyboard", ] )
                    )#"-multikeyboard"
        
        if global_variable.gamelist_type == "mame" :
            self.new_ui_pop_up_menu_for_table.add_separator()
            
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("校验 roms，-verifyroms"),
                    command = lambda : self.new_func_table_pop_up_menu_callback_show_info(other_option=["-verifyroms", ] )
                    )
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("校验 samples，-verifysamples"),
                    command = lambda : self.new_func_table_pop_up_menu_callback_show_info(other_option=["-verifysamples", ] )
                    )
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("显示roms信息，-listroms（太简略，分不清 roms 是独立的还是共用的）"),
                    command = lambda : self.new_func_table_pop_up_menu_callback_show_info(other_option=["-listroms", ] )
                    )
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("显示roms信息，-listxml（含大量其它信息）"),
                    command = lambda : self.new_func_table_pop_up_menu_callback_show_info(other_option=["-listxml", ] )
                    )
            self.new_ui_pop_up_menu_for_table.add_command(
                    label=_("显示roms信息，-listxml -nodtd 去文件头（含大量其它信息）"),
                    command = lambda : self.new_func_table_pop_up_menu_callback_show_info(other_option=["-listxml","-nodtd" ] )
                    )
        
        self.new_ui_pop_up_menu_for_table.add_separator()
        
        
        out_file_path = the_files.file_txt_export
        
        self.new_ui_pop_up_menu_for_table.add_command(
                label=_("导出当前列表到：") + out_file_path ,
                command = self.new_func_table_pop_up_menu_callback_export_gamelist,
                    )
        self.new_ui_pop_up_menu_for_table.add_command(
                label=_("导出选中内容到：") + out_file_path,
                command = self.new_func_table_pop_up_menu_callback_export_select_items,
                    )
        self.new_ui_pop_up_menu_for_table.add_separator()
        
        self.new_ui_pop_up_menu_for_table.add_command(
                label=_("目录修改，添加到指定目录"),
                command = self.new_func_table_pop_up_menu_callback_add_items_to_a_index,
                    )
        
        
        self.new_ui_pop_up_menu_for_table.add_command(
                label=_("删减当前目录，删除选中内容。"),
                command = self.new_func_table_pop_up_menu_callback_delete_items_from_remembered_index,
                    )
        # 记录 index
        self.new_var_table_menu_index_for_delete_from_current_list = self.new_ui_pop_up_menu_for_table.index(tk.END)
        
        
        self.new_ui_pop_up_menu_for_table.add_command(
                label=_("目录修改，从指定目录删除选中内容"),
                command = self.new_func_table_pop_up_menu_callback_delete_items_from_a_index,
                    )
        ""

    def new_func_ui_pop_up_menu_for_header(self,):
        self.new_ui_pop_up_menu_for_header = tk.Menu(self , tearoff=0)
        
        self.new_ui_pop_up_menu_for_header.add_separator()
        
        self.new_ui_pop_up_menu_for_header.add_command(label=_("选择列表显示项目"),
                command = misc_funcs.header_pop_up_menu_callback_choose_columns
                )
    
    
    def new_func_header_show_pop_up_menu(self,event):
        try:
            self.new_ui_pop_up_menu_for_header.tk_popup(event.x_root, event.y_root)
        finally:
            self.new_ui_pop_up_menu_for_header.grab_release()


    def new_func_table_show_pop_up_menu(self,event=None):
        
        # 前当目录可删除标记
        flag_current_list_editable = False
        
        event_info = self.new_var_remember_last_index_data 
        
        external_index = self.new_var_data_holder.external_index
        
        # 外置目录
        the_file_name   = "" # 用于对比文件名，不能乱改
        the_last_string = "" # 显示用的，格式可以好看点
        if event_info[0]=="external_ini_file":
            the_file_name = event_info[1]
            if len(event_info)>2:
                the_last_string = the_file_name + "|" + event_info[2]
            else:
                the_last_string = the_file_name
            the_last_string = r"(" + " " + the_last_string + " " + r")"

            
            if the_file_name in global_variable.external_index_files_editable:
                flag_current_list_editable = True
        
        the_menu  = self.new_ui_pop_up_menu_for_table
        the_index = self.new_var_table_menu_index_for_delete_from_current_list
        
        the_menu.entryconfig( the_index ,label = _("删减当前目录，删除选中内容。")+the_last_string ,)
        
        if flag_current_list_editable:
            print("editable")
            the_menu.entryconfig( the_index, state="normal",)
        else:
            print("not editable")
            the_menu.entryconfig( the_index, state="disabled",)
        
        try:
            the_menu.tk_popup(event.x_root, event.y_root)
        finally:
            the_menu.grab_release()

    def new_func_table_pop_up_menu_callback_start_game(self,other_option=None,hide=True):
        if other_option is None:
            other_option=[]
        
        item_id = self.new_var_remember_select_row_id
        
        self.new_var_data_for_StartGame["emu_number"]  = -1
        self.new_var_data_for_StartGame["id"]          = item_id
        self.new_var_data_for_StartGame["other_option"]= other_option
        self.new_var_data_for_StartGame["hide"]        = hide
        # "type" = "mame"

        self.event_generate(self.new_var_virtual_event_name_StartGame)

    def new_func_table_pop_up_menu_callback_show_info(self,other_option=None,):
        if other_option==None:
            other_option = []
        
        item_id = self.new_var_remember_select_row_id
        
        self.new_var_data_for_StartGame["emu_number"]  = -1
        self.new_var_data_for_StartGame["id"]          = item_id
        self.new_var_data_for_StartGame["other_option"]= other_option
        #self.new_var_data_for_StartGame["hide"]        = True # 用不着
        # "type" = "mame"

        self.event_generate(self.new_var_virtual_event_name_MameShowInfo)
    
    # 导出列表
    # 第1 第2 列表相同
    # 第3 列表需要修改
    def new_func_table_pop_up_menu_callback_export_gamelist(self,):
        if not self.new_var_list_to_show: return
        
        out_file_path = the_files.file_txt_export
        
        with open(out_file_path,mode="wt",encoding="utf_8") as f:
            for item_id in self.new_var_list_to_show:
                print(item_id,file=f)
    
    # 导出选中项
    def new_func_table_pop_up_menu_callback_export_select_items(self,):
        if not self.new_var_list_to_show: return
        
        out_file_path = the_files.file_txt_export
        
        with open(out_file_path,mode="wt",encoding="utf_8") as f:
            for item_id in sorted(self.new_var_remember_selected_items):
                print(item_id,file=f)
    
    # 目录编辑，当前选中目录，删除
    def new_func_table_pop_up_menu_callback_delete_items_from_remembered_index(self,):
        # 后面修改
        pass

    # 目录编辑，添加选中项 到 某个 目录中
    def new_func_table_pop_up_menu_callback_add_items_to_a_index(self,):
        # 后面修改
        pass
    
    # 目录编辑，添加选中项 到 某个 目录中
    def new_func_table_pop_up_menu_callback_delete_items_from_a_index(self,):
        # 后面修改
        pass        

# 接收信号 ，来自 top 菜单，搜索信号，接收
# 接收信号 ，来自 top 菜单，定位信号，接收
class GameList_8(GameList_7):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_virtual_event_name_FindItemById  =r'<<FindItemById>>'
        self.new_var_virtual_event_name_GameListSearch=r'<<GameListSearch>>'
        self.new_var_virtual_event_name_GameListSearchRegular=r'<<GameListSearchRegular>>'
        self.new_var_virtual_event_name_GameListSearchClear=r'<<GameListSearchClear>>'

    #def new_func_bindings(self,):
    #    super().new_func_bindings()
        
    def new_func_bindings_for_receive_virtual_event(self,):
        super().new_func_bindings_for_receive_virtual_event()
        
        # 接收 toolbar 发送的 定位信号
        self.bind_all(self.new_var_virtual_event_name_FindItemById,
            self.new_func_bindings_receive_virtual_event_for_find_item)
        # 接收 toolbar 发送的 搜索信号
        self.bind_all(self.new_var_virtual_event_name_GameListSearch,
            self.new_func_bindings_receive_virtual_event_for_search)
        # 接收 toolbar 发送的 正则搜索信号
        self.bind_all(self.new_var_virtual_event_name_GameListSearchRegular,
            self.new_func_bindings_receive_virtual_event_for_search_regular)
        # 接收 toolbar 发送的 搜索结束信号
        self.bind_all(self.new_var_virtual_event_name_GameListSearchClear,
            self.new_func_bindings_receive_virtual_event_for_search_clear)
    
    def new_func_bindings_receive_virtual_event_for_search(self,event):
        print("***")
        print(r"receive_virtual_event <<GameListSearch>>")
        widget  = event.widget
        string_for_search = widget.new_var_data_for_virtual_event_search
        print(string_for_search)
        
        if self.new_var_data_holder.is_current_list_empty():
            print("empty list ,no need to search")
            return # 空，不用搜
        
        # 搜索标记
        self.new_var_data_holder.set_the_flag_search(True)
        # 重置 标记
        self.new_var_remember_select_row_number = -1
        #self.new_var_remember_select_row_id     = None
        
        
        self.new_var_data_holder.generate_new_list_by_search(string_for_search)
        
        self.new_func_table_reload_the_game_list()
    
    def new_func_bindings_receive_virtual_event_for_search_regular(self,event):
        print("***")
        print(r"receive_virtual_event <<GameListSearchRegular>>")
        widget  = event.widget
        string_for_search = widget.new_var_data_for_virtual_event_search
        print(string_for_search)
        
        
        if self.new_var_data_holder.is_current_list_empty():
            print("empty list ,no need to search")
            return # 空，不用搜
        
        # 搜索标记
        self.new_var_data_holder.set_the_flag_search(True)
        # 重置 标记
        self.new_var_remember_select_row_number = -1
        #self.new_var_remember_select_row_id     = None
        
        
        self.new_var_data_holder.generate_new_list_by_search_regular(string_for_search)
        
        self.new_func_table_reload_the_game_list()

    def new_func_bindings_receive_virtual_event_for_search_clear(self,event):
        print("***")
        print(r"receive_virtual_event <<GameListSearchClear>>")
        
        # 搜索标记
        self.new_var_data_holder.set_the_flag_search(False)
        # 重置 标记
        self.new_var_remember_select_row_number = -1
        #self.new_var_remember_select_row_id     = None
        
        if self.new_var_flag_current_index_be_edited:
            # 重置 记录
            self.new_var_remember_last_index_data = None 
            # 重新请求目录信号
            self.event_generate('<<RequestForIndexInfo>>')

        else:
            self.new_func_table_reload_the_game_list()
        
    def new_func_bindings_receive_virtual_event_for_find_item(self,event):
        print("***")
        print(r"receive_virtual_event <<FindItemById>>")
        widget  = event.widget
        item_id = widget.new_var_data_for_FindItemById
        
        if item_id : print(item_id)
        else   : return
        
        # 使用记录数据
        if self.new_var_remember_select_row_number > -1:
            if self.new_var_remember_select_row_number < len(self.new_var_list_to_show):
                verify_id = self.new_func_table_get_id_from_row_number(
                                self.new_var_remember_select_row_number )
                if item_id==verify_id:
                    print("row number is remembered")
                    print("jump to row number :")
                    print(self.new_var_remember_select_row_number)
                    self.new_func_table_jump_to_row(
                            self.new_var_remember_select_row_number)
                    self.new_func_remember_select_row(item_id,self.new_var_remember_select_row_number)
                    return
        
        # 记录无效
        
        row_remember = -1
        print("row number is not remembered")
        
        for row in range(  len(self.new_var_list_to_show)  ):
            if item_id == self.new_func_table_get_id_from_row_number(row):
                row_remember     = row
                break
        
        if row_remember == -1:
            print("not found")
        else:
            print("found")
            print("jump to row number :")
            print(row_remember)
            self.new_func_table_jump_to_row(row_remember)
            self.new_func_remember_select_row(item_id,row_remember)

# 开始游戏，发送信号
class GameList_9(GameList_8):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        



    def new_func_bindings(self,):
        super().new_func_bindings()
        
        self.bind('<Return>', self.new_func_table_binding_press_enter,)
    
    
    # derived
    # wip
    # table binding 鼠标 双击 ( 范围 是 每行的 背景矩形)
    # 1 选择行 ，这个不用了吧，和 鼠标单击 重复了
    # 2 发送信号，打开游戏，待补充
    def new_func_table_binding_double_click(self,event):
        #   table.tag_bind("background_rectangle",'<Double-Button-1>', self.new_func_table_binding_double_click,)
        print()
        print("double click")
        
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        print("item id : {}".format(item_id) )
        print("row number : {}".format(row_number) )
        
        # 1 选择行 ，这个不用了吧，和 鼠标单击 重复了
        #self.new_func_remember_select_row(item_id,row_number)
        
        self.new_var_data_for_StartGame["emu_number"]   = -1
        self.new_var_data_for_StartGame["id"]           = item_id
        self.new_var_data_for_StartGame["other_option"].clear()
        self.new_var_data_for_StartGame["hide"]         = True
            # "id"   = None
            # "type" = "mame"
            # "other_option" = []
            # "hide" = True
        
        self.event_generate(self.new_var_virtual_event_name_StartGame)

    def new_func_table_binding_press_enter(self,event):
        print()
        print("press enter")
        #self.new_var_remember_select_row_id
        #self.new_var_remember_select_row_number
        
        if not self.new_var_list_to_show : return
        
        if self.new_var_remember_select_row_id is None : return
        
        if self.new_var_remember_select_row_number > -1 :
            # verify id
            try:
                item_id = self.new_var_list_to_show[ self.new_var_remember_select_row_number ]
            except:
                item_id = None
            
            if item_id == self.new_var_remember_select_row_id:
                self.new_var_data_for_StartGame["emu_number"]   = -1
                self.new_var_data_for_StartGame["id"]           = item_id
                self.new_var_data_for_StartGame["other_option"].clear()
                self.new_var_data_for_StartGame["hide"]         = True
                
                self.event_generate(self.new_var_virtual_event_name_StartGame)
        else: #    = -1
            pass


# 多选模式
class GameList_10(GameList_9):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_tk_gamelist_multi_select_mode = tk.IntVar() # default value 0

        
        
        #self.new_var_remember_selected_items = set() 
            #添加到前边吧
            
        
    
    # 添加 多选模式 到 鼠标右键菜单
    def new_func_ui_pop_up_menu_for_table(self,):
        
        super().new_func_ui_pop_up_menu_for_table()
        
        self.new_ui_pop_up_menu_for_table.add_separator()
        
        self.new_ui_pop_up_menu_for_table.add_checkbutton(
                label=_("多选模式"),
                variable = self.new_var_tk_gamelist_multi_select_mode,
                command = self.new_func_table_pop_up_menu_callback_multi_select_mode,
                )
        
    def new_func_table_pop_up_menu_callback_multi_select_mode(self,):
        if self.new_var_tk_gamelist_multi_select_mode.get():
            self.new_func_multi_select_mode_bind()
        else:
            self.new_func_multi_select_mode_unbind()
    
    # for 
    # self.new_func_table_pop_up_menu_callback_multi_select_mode()
    def new_func_multi_select_mode_bind(self,):
        self.new_ui_table.tag_bind("background_rectangle",'<Control-1>', self.new_func_table_binding_ctrl_and_click )
        
        self.new_ui_table.tag_bind("background_rectangle",'<Shift-1>', self.new_func_table_binding_shift_and_click )
        
        self.bind('<Control-a>', self.new_func_table_binding_ctrl_all )
        self.bind('<Control-A>', self.new_func_table_binding_ctrl_all )
    
    # for 
    # self.new_func_table_pop_up_menu_callback_multi_select_mode()
    def new_func_multi_select_mode_unbind(self,):
        self.new_ui_table.tag_unbind("background_rectangle",'<Control-1>', )
        
        self.new_ui_table.tag_unbind("background_rectangle",'<Shift-1>', )
        
        self.unbind('<Control-a>',  )
        
        self.unbind('<Control-A>',  )
    
    # Control + B1
    # 第 1、2 组列表，一样
    # 第3组列表，需要变动    
    def new_func_table_binding_ctrl_and_click(self,event):
        print()
        print("Control and mouse button 1")
        
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        #print("item id : {}".format(item_id) )
        #print("row number : {}".format(row_number) )
        
        if item_id not in self.new_var_remember_selected_items:
            self.new_var_remember_selected_items.add(item_id)
        else:
            self.new_var_remember_selected_items.remove(item_id)
        
        #self.new_func_remember_select_row(item_id,row_number)
        self.new_func_refresh_table()
    
    # Shift + B1
    # 第 1、2 组列表，一样
    # 第3组列表，需要变动
    def new_func_table_binding_shift_and_click(self,event):
        print()
        print("shift button 1")
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        #print("item id : {}".format(item_id) )
        #print("row number : {}".format(row_number) )
        
        # 之前，没有选中 行
        if self.new_var_remember_select_row_number < 0 :
            self.new_func_remember_select_row(item_id,row_number,)# 仅选择此行
            return
        
        # 记录出错，超出范围 
        if self.new_var_remember_select_row_number >= len(self.new_var_list_to_show):
            self.new_func_remember_select_row(item_id,row_number,)# 仅选择此行
                # 已有 refresh
            return
        
        if   row_number == self.new_var_remember_select_row_number:
            self.new_var_remember_selected_items.clear()
            self.new_var_remember_selected_items.add(item_id)
            self.new_func_refresh_table()
            return
        elif row_number <  self.new_var_remember_select_row_number:
            self.new_var_remember_selected_items.clear()
            
            new_id_list = self.new_var_list_to_show[ row_number : self.new_var_remember_select_row_number + 1 ]
            
            self.new_var_remember_selected_items.update(  set(new_id_list)  )
            
            self.new_func_refresh_table()
        elif row_number >  self.new_var_remember_select_row_number:
            self.new_var_remember_selected_items.clear()
            
            new_id_list = self.new_var_list_to_show[ self.new_var_remember_select_row_number  : row_number + 1 ]
            
            self.new_var_remember_selected_items.update(  set(new_id_list)  )
            
            self.new_func_refresh_table()
    
    # Control + A
    # Control + a
    # 第 1、2 组列表，一样
    # 第3组列表，需要变动
    def new_func_table_binding_ctrl_all(self,event):
        
        print()
        print("Control + a ,select all")
        
        if not self.new_var_list_to_show : return
        
        #all_current_list = set(self.new_var_list_to_show)
        self.new_var_remember_selected_items.clear()
        self.new_var_remember_selected_items.update(  set(self.new_var_list_to_show)  )
        self.new_func_refresh_table()
        
    # derived
    def new_func_table_binding_right_click(self,event):
        # 右键功能 1
        # 右键功能 2：菜单，另一个函数 ,tag_bind"+"
        
        print()
        print("right click")
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        #print("item id : {}".format(item_id) )
        #print("row number : {}".format(row_number) )
        
        
        # 多选模式：
        if self.new_var_tk_gamelist_multi_select_mode.get():
            
            # 在多选 范围 中
            if item_id in self.new_var_remember_selected_items :
                return
            # 不在多选范围 中
            else:
                self.new_func_remember_select_row(item_id,row_number)# 选中此行
                return
        
        # 单选模式
        else:
            self.new_func_remember_select_row(item_id,row_number)# 选中此行
            return

# table 右键菜单 补充
#   目录编辑，
#   有关多选模式
#   在多选模式后边
class GameList_11(GameList_10):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
    

    # derived
    #   收到 目录 变化 信号 ，游戏列表切换
    #   添加一个标记
    def new_func_bindings_receive_virtual_event_from_index(self,event):
        super().new_func_bindings_receive_virtual_event_from_index(event)
        
        ####################
        # 重置 标记
        self.new_var_flag_current_index_be_edited = False


    # derived
    #   目录编辑，当前选中目录，删除
    def new_func_table_pop_up_menu_callback_delete_items_from_remembered_index(self,):
        
        # 1
            # 当前列表中，删除 选中内容
        # 2
            # 具体数据中，external_index ，删除 选中内容
        # 3
            # 重载列表
        external_index = self.new_var_data_holder.external_index
        
        if self.new_var_remember_last_index_data is None :
            return
        
        if not self.new_var_remember_selected_items:
            return
        
        event_info = self.new_var_remember_last_index_data 

        if event_info[0]=="external_ini_file":# 外置目录
            if event_info[1] in global_variable.external_index_files_editable:
                
                self.new_var_flag_current_index_be_edited = True
                
                
                # 记录，修改过的文件
                global_variable.external_index_files_be_edited.add( event_info[1]  )
                
                print()
                for x in global_variable.external_index_files_be_edited:
                    print(x)
            
                ###################
                # 当前列表中，删除 选中内容
                # self.new_var_remember_selected_items
                self.new_var_data_holder.func_for_delete_items_from_current_list( self.new_var_remember_selected_items )
        
        
                ##############
                # 具体数据中，external_index ，删除 选中内容        
                if len(event_info)==2:# 第一层
                    temp = external_index[event_info[1]]["ROOT_FOLDER"]
                    new_list = sorted( set(temp)  -  self.new_var_remember_selected_items  )
                    external_index[event_info[1]]["ROOT_FOLDER"] = new_list
                if len(event_info)==3:# 第二层
                    temp = external_index[event_info[1]][event_info[2]]
                    new_list = sorted( set(temp)  -  self.new_var_remember_selected_items  )
                    external_index[event_info[1]][event_info[2]] = new_list
        
                ################
                ## 重载列表
                self.new_func_table_reload_the_game_list()
    
    # derived
    #   目录编辑，添加选中项 到 某个 目录中
    def new_func_table_pop_up_menu_callback_add_items_to_a_index(self,):
        # 1
            # 建一个 Treeview ，方便 选择 添加到 哪一个 项目
                # 第一层 id 为: 文件名路径
                # 第二层 id 为: 文件名路径|分类名
        # 2
            # 具体数据中，external_index ，添加 选中内容
        external_index = self.new_var_data_holder.external_index
        
        if not self.new_var_remember_selected_items:
            return
        
        items = self.new_var_remember_selected_items
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("添加到 自定义目录"))
        
        size = "400x300" 
        window.geometry( size )
        
        window.transient( global_variable.root_window )
        window.lift()
        
        window.rowconfigure(0,weight=1)
        window.rowconfigure(1,weight=0)
        window.columnconfigure(0,weight=1)
        
        tree_container = Treeview_with_scrollbar(window)
        tree_container.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S)
        tree = tree_container.new_ui_tree
        
        def add_items_to_select_index():
            selected_id = tree.focus()
            
            if selected_id == "" : return 0 # 无选中项为 ""
            
            parent = tree.parent( selected_id )
            
            if parent == "" : # 一级列表
                # 如果 已经 全包含了，退出
                original_data = set( external_index[selected_id]["ROOT_FOLDER"] )
                
                if items.issubset( original_data ): # issubset 后面，不一定要用 set 格式
                    print("items already in there ,quit")
                    window.destroy()
                    return 0
                
                # 如果没有全包含
                
                file_path = selected_id
                global_variable.external_index_files_be_edited.add(file_path) # 记录
                
                print(  )
                for x in global_variable.external_index_files_be_edited:
                    print( x )
                
                # 合并
                temp = items | original_data
                # 转回 list
                external_index[selected_id]["ROOT_FOLDER"] = list( temp )
            else:# 二级列表
                key_parent = parent
                    # key_parent|key_self 加一个竖线
                    # key_parent 为文件名
                    # key_self 为分类名
                key_self   = selected_id[ len(key_parent)+1 : ]
                
                original_data = set( external_index[key_parent][key_self] )
                
                if items.issubset( original_data ):
                    print("items already in there ,quit")
                    window.destroy()
                    return
                
                file_path = parent
                global_variable.external_index_files_be_edited.add(file_path) # 记录
                
                print(  )
                for x in global_variable.external_index_files_be_edited:
                    print( x )
                
                # 合并
                temp = items | original_data
                # 转回 list
                external_index[key_parent][key_self] = list( temp )
            
            window.destroy()
            
        
        button = ttk.Button(window,text = _("确认") ,command=add_items_to_select_index)
        button.grid(row=1,column=0,sticky=(tk.E,))
        
        tree.configure(columns=["file",])
        tree.heading("#0", text=_("目录" )     )
        tree.heading("#1", text=_("文件路径" ) )
        
        
        # external_index
        # global_variable.external_index_files_editable
        
        for x in sorted( external_index.keys()):
            # 第一层范围 
            if x in global_variable.external_index_files_editable:
                # x 为 路径 + 名称
                # ini_files[x] 为 名称，无路径
                basename = os.path.basename( x )
                tree.insert('','end',iid=x,text= basename,values=(x, )  )

        
                #第二层
                for y in sorted( external_index[x] ) :
                    if y != "FOLDER_SETTINGS":
                        if y != "ROOT_FOLDER":
                            iid_string = x + r"|" + y
                            tree.insert(x,'end',iid = iid_string,text=y,values=(y, ) )                            

        window.wait_window()

    
    # derived
    # 目录编辑，添加选中项 到 某个 目录中
    def new_func_table_pop_up_menu_callback_delete_items_from_a_index(self,):
        # 1
            # 建一个 Treeview ，方便 选择 添加到 哪一个 项目
                # 第一层 id 为: 文件名路径
                # 第二层 id 为: 文件名路径|分类名
        # 2
            # 具体数据中，external_index ，删除 选中内容
        external_index = self.new_var_data_holder.external_index
        
        if not self.new_var_remember_selected_items:
            return
        
        items = self.new_var_remember_selected_items
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("添加到 自定义目录"))
        
        size = "400x300" 
        window.geometry( size )
        
        window.transient( global_variable.root_window )
        window.lift()
        
        window.rowconfigure(0,weight=1)
        window.rowconfigure(1,weight=0)
        window.columnconfigure(0,weight=1)
        
        tree_container = Treeview_with_scrollbar(window)
        tree_container.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S)
        tree = tree_container.new_ui_tree
        
        def delete_items_to_select_index():
            selected_id = tree.focus()
            
            if selected_id == "" : return 0 # 无选中项为 ""
            
            parent = tree.parent( selected_id )
            
            if parent == "" : # 一级列表
                # 如果 已经 全包含了，退出
                original_data = set( external_index[selected_id]["ROOT_FOLDER"] )
                
                items_will_be_deleted = original_data & items
                
                if not items_will_be_deleted : #没有要删除的
                    print("items not in there ,quit")
                    window.destroy()
                    return
                
                # 删除
                
                file_path = selected_id
                global_variable.external_index_files_be_edited.add(file_path) # 记录
                
                print(  )
                for x in global_variable.external_index_files_be_edited:
                    print( x )
                
                # 合并
                temp = original_data - items_will_be_deleted
                # 转回 list
                external_index[selected_id]["ROOT_FOLDER"] = list( temp )
            else:# 二级列表
                key_parent = parent
                    # key_parent|key_self 加一个竖线 ，len(key_parent)+1
                    # key_parent 为文件名
                    # key_self 为分类名
                key_self   = selected_id[ len(key_parent)+1 : ]
                
                original_data = set( external_index[key_parent][key_self] )
                
                items_will_be_deleted = original_data & items
                
                if not items_will_be_deleted:
                    print("items not in there ,quit")
                    window.destroy()
                    return
                
                file_path = parent
                global_variable.external_index_files_be_edited.add(file_path) # 记录
                
                print(  )
                for x in global_variable.external_index_files_be_edited:
                    print( x )
                
                # 合并
                temp = original_data - items_will_be_deleted
                # 转回 list
                external_index[key_parent][key_self] = list( temp )
            
            window.destroy()
            
        
        button = ttk.Button(window,text = _("确认") ,command=delete_items_to_select_index)
        button.grid(row=1,column=0,sticky=(tk.E,))
        
        tree.configure(columns=["file",])
        tree.heading("#0", text=_("目录" )     )
        tree.heading("#1", text=_("文件路径" ) )
        
        
        # external_index
        # global_variable.external_index_files_editable
        
        for x in sorted( external_index.keys()):
            # 第一层范围 
            if x in global_variable.external_index_files_editable:
                # x 为 路径 + 名称
                # ini_files[x] 为 名称，无路径
                basename = os.path.basename( x )
                tree.insert('','end',iid=x,text= basename,values=(x, )  )

        
                #第二层
                for y in sorted( external_index[x] ) :
                    if y != "FOLDER_SETTINGS":
                        if y != "ROOT_FOLDER":
                            iid_string = x + r"|" + y
                            tree.insert(x,'end',iid = iid_string,text=y,values=(y, ) )                            


        
        
        window.wait_window()


# 按键 1 2 3 4 5 6 7 8 9
class GameList_12(GameList_11):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

    def new_func_bindings(self,):
        super().new_func_bindings()
        
        
        self.bind("<KeyPress-1>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-2>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-3>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-4>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-5>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-6>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-7>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-8>",self.new_func_table_binding_key_1_to_9)
        self.bind("<KeyPress-9>",self.new_func_table_binding_key_1_to_9)
        


    def new_func_table_binding_key_1_to_9(self,event):
        #print()
        #print("1 - 9")
        #print(event.keysym)
        
        if not self.new_var_list_to_show :
            return
        
        row_number = self.new_var_remember_select_row_number
        
        if row_number < 0 :
            return
        
        item_id    = self.new_var_remember_select_row_id
        
        if item_id != self.new_var_list_to_show [ row_number ] :
            return
        
        self.new_var_data_for_StartGame["emu_number"]   = int(event.keysym)
        self.new_var_data_for_StartGame["id"]           = item_id
        self.new_var_data_for_StartGame["other_option"].clear()
        self.new_var_data_for_StartGame["hide"]         = True
        
        self.event_generate(self.new_var_virtual_event_name_StartGame)


# 99
# 将 focus 留在 列表 里
# 显示 ctrl + i 
class GameList_99(GameList_12):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        
        
        self.new_func_ui()
        self.new_func_bindings()
        
        self.new_func_bindings_for_receive_virtual_event()
        
        self.new_func_refresh_all()
    

    def new_func_bindings(self,):
        super().new_func_bindings()
        
        # 测试用
        # 查看一些信息
        self.bind_all('<Alt-KeyPress-i>',self.new_func_binding_show_info,"+")
        
        self.bind('<Control-KeyPress-i>',self.new_func_binding_show_info,)
        self.bind('<Control-KeyPress-i>',self.new_func_show_search_flag,"+")

        self.bind('<Control-KeyPress-p>',self.new_func_find_root_window)
        
        #
        self.new_ui_table.bind("<Enter>",
                lambda event : self.new_ui_table.configure(cursor='') )
        
        # 将 focus 留在 列表 里 ，原始的 Canvas 不留 focus 的
        # focus_set()
        #    不然，Canvas 、 Frame 等，不 响应 按键 类 event
        for child_widget in self.winfo_children():
            child_widget.bind( "<Button-1>", lambda event: self.focus_set(),"+")
            child_widget.bind( "<Button-2>", lambda event: self.focus_set(),"+")
            child_widget.bind( "<Button-3>", lambda event: self.focus_set(),"+")
        #    child_widget.bind( "<Button>", lambda event: self.new_ui_table.focus_set(),"+")
        
        #
        # 这个效果太强了，影响搜索区
        #self.bind("<Enter>",lambda event : self.focus_set(),"+") 
        
        #self.new_ui_table.bind( "<Button>", lambda event: self.new_ui_table.focus_set(),"+")
        #self.new_ui_table.bind("<Enter>",lambda event : self.new_ui_table.focus_set(),"+")
        
        
        #def test(event):
        #    print(event.char)
        
        #self.new_ui_table.bind("<Any-KeyPress>",test,"+")
        ""
    # 多列表切换时，
    #   当列表，重新显示时，需要重新做的一些
    def new_func_show_gamelist_again(self,):
        
        # 提升到前面
        self.lift()
        
        # 全局记录
        global_variable.the_showing_table = self
        
        # 一些 bindging 需要重新 绑定一下
        
        # 接收目录信号
        self.bind_all(self.new_var_virtual_event_name_received_from_index, # virtual event name
            self.new_func_bindings_receive_virtual_event_from_index )
        
        # 接收 toolbar 发送的 定位信号
        self.bind_all(self.new_var_virtual_event_name_FindItemById,
            self.new_func_bindings_receive_virtual_event_for_find_item)
        # 接收 toolbar 发送的 搜索信号
        self.bind_all(self.new_var_virtual_event_name_GameListSearch,
            self.new_func_bindings_receive_virtual_event_for_search)
        # 接收 toolbar 发送的 正则搜索信号
        self.bind_all(self.new_var_virtual_event_name_GameListSearchRegular,
            self.new_func_bindings_receive_virtual_event_for_search_regular)
        # 接收 toolbar 发送的 搜索结束信号
        self.bind_all(self.new_var_virtual_event_name_GameListSearchClear,
            self.new_func_bindings_receive_virtual_event_for_search_clear)
        
        
        
        
        
        
        # 刷新
        #   不需要了。目录再发一个信号，自动刷新了。
        
        
        
        " "
    
    # 隐藏列表时，应当做的事
    def new_func_hide_gamelist(self,):
        
        self.new_var_remember_last_index_data = None
        self.new_var_remember_select_row_number = -1
        
        self.new_func_table_clear() # 清理显示内容

    # table 测试用
    def new_func_binding_show_info(self,event=None):
        print("")
        print(" show info : {}".format(self.new_var_ui_type) )
        
        number_row = len(self.new_var_list_to_show)
        print(" show info : {} table row numbers".format( number_row )  )
        
        number_1 = len( self.new_ui_table.find_all() )
        print(" show info : {} items in table".format(number_1))
        
        number_2 = len( self.new_ui_header.find_all() )
        print(" show info : {} items in table header".format(number_2))
        
        if not self.winfo_viewable():return
        
        start_row,end_row=self.new_func_table_get_visible_rows()
        
        

        if self.new_var_list_to_show:
            # 免得超出范围了
            # 空列表时，第0个，超出范围
            
            fisrt_game_id,fisrt_game_info = self.new_func_table_get_id_and_gameinfo_from_row_number(start_row)
            
            last_game_id,last_game_info   = self.new_func_table_get_id_and_gameinfo_from_row_number(end_row - 1)
            
            
            #print(fisrt_game_id)
            #print(last_game_id)
            print(" show info :start row : {} , {}".format(start_row,fisrt_game_id) )
            print(" show info :end row   : {} , {}".format(end_row,last_game_id)   )
            
        
        flag_show_icon , visible_column_id ,table_visible_width =self.new_func_table_get_visible_columns()
        
        print(" show info : visible columns : {} ".format(visible_column_id))
        

        print(" show info : select row number :",end="")
        print(self.new_var_remember_select_row_number)
        print(" show info : select row id :",end="")
        print(self.new_var_remember_select_row_id)
    
    # test 
    def new_func_show_search_flag(self,event):
        flag_search = self.new_var_data_holder.flag_search
        print("")
        print("flag_search")
        print(flag_search)
    
    # test
    def new_func_find_root_window(self,event):
        root_window=None
        
        def get_root(window):
            print(window)
            parent_string = window.winfo_parent()
            
            
            if parent_string == "" :
                return window # window is root_window
            
            print(parent_string)
            parent = window._nametowidget(parent_string)
            get_root(parent)
            
        
        get_root(self.new_ui_table)

class GameList_T(GameList_99):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)

# for softwarelist
class GameList_100(GameList_99):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        # self.new_var_data_for_StartGame["type"]         = "mame" # 这个一直不变
        self.new_var_data_for_StartGame["type"]         = "softwarelist" # 这个一直不变

    # for
    # self.new_func_table_draw_icon_colunm()
    def new_func_table_choose_icon_image(self,game_info):
        
        # 元素为 list 格式
        # 元素第0个为 "name"
        # 元素第1个为 "status"
        
        # for sl
        # 0 xml
        # 1 name
        # 2 "supported"
        status = game_info[2]
        
        if status=="yes":
            return self.new_image_image_green
        elif status=="partial":
            return self.new_image_image_yellow
        elif status=="no":
            return self.new_image_image_red
        else:
            return self.new_image_image_black






GameList     = GameList_99

if global_variable.gamelist_type == "softwarelist":
    GameList = GameList_100



if __name__ == "__main__" :
    import time
    from .read_pickle import read as read_pickle
    from .initial_data_filepath import file_pickle_gamelist_data as the_data_file
    
    time1=time.time()
    #temp_data=read_pickle("cache_data_2_gamelist.bin")
    data=read_pickle(the_data_file)
    temp_data=data["machine_dict"]
        # dict 方便检索每一个游戏
        #  子元素，也用 dict
    time2=time.time()
    print("{},time for read pickle".format(time2-time1))
    
    the_games_to_show=sorted(temp_data.keys())
    
    all_keys=['name', 'translation', 'year', 'sourcefile', 'manufacturer', 'cloneof', 'description', 'savestate', 'status']
    
    #data_to_show=[ temp_data[x] for x in the_games_to_show ]
        # list 有顺序记录的
        #  子元素 暂时用的 dict
    time3=time.time()
    print("{},time for make id list".format(time3-time2))
    print("{},number of games".format(len(the_games_to_show)))
    

    root=tk.Tk()
    root.title("table test")
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    style=ttk.Style()
    
    ###
    #the_games_to_show = ['kof97','kof98','kof97k','kof99']
    t=GameList(root,)
    t.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S))
    #a.button=ttk.Button(root,text="show_info",command=a.new_func_show_info)
    #a.button.grid(row=3,column=0,sticky=(tk.N,tk.S))
    
    time4=time.time()
    print("{},time for ui to show up".format(time4-time3))
    



    root.mainloop()



