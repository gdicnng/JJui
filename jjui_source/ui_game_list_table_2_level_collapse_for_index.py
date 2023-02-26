# -*- coding: utf_8_sig-*-
#import sys
#import os

import time

import tkinter as tk
# from tkinter import ttk

# from . import global_static_key_word_translation as key_word_translation
# from . import global_static
# from . import global_variable
# from . import global_static_filepath as the_files # 图标 图片 路径



from . import ui_game_list_table_2_level_collapse
Data_Holder_base = ui_game_list_table_2_level_collapse.Data_Holder
GameList_base    = ui_game_list_table_2_level_collapse.GameList



"""
    用游戏列表的结构
    
    internal_data["mame_version"]   = mame_version
    internal_data["columns"]        = columns
    internal_data["machine_dict"]   = machine_dict
    internal_data["set_data"]       = set_data
    internal_data["dict_data"]      = dict_data
    internal_data["internal_index"] = internal_index
"""
class built_index_data():
    def __init__(self,):
        self.data={}
             
        self.data["columns"]=[_("目录"),]
        self.data["machine_dict"]={}
        self.data["set_data"]={}
        self.data["dict_data"]={}
             
        self.data["set_data"]["all_set"] = set()
        self.data["set_data"]["clone_set"] = set()
        self.data["set_data"]["parent_set"] = set()
             
        self.data["dict_data"]["clone_to_parent"] = {}
        self.data["dict_data"]["parent_to_clone"] = {}
    
    def feed_data(self,internal_index=None,external_index=None,):
        if internal_index is not None:
            self.read_internal_index(internal_index)
        
        if external_index is not None:
            self.read_external_index(external_index)
            
    
    def read_internal_index(self,internal_index):
        clone_to_parent = self.data["dict_data"]["clone_to_parent"]
        parent_to_clone = self.data["dict_data"]["parent_to_clone"]
        
        all_set    = self.data["set_data"]["all_set"]
        clone_set  = self.data["set_data"]["clone_set"]
        parent_set = self.data["set_data"]["parent_set"]
        
        machine_dict = self.data["machine_dict"]
        
        # id 为
        #   内置目录 第一层 : internal|一级目录名
        #   内置目录 第二层 : internal|一级目录名|二级分类名
        #   外置目录 第一层 : external_ini_file|文件名
        #   外置目录 第二层 : external_ini_file|文件名|分类名
        
        
        # 第一层
        for parent_string in internal_index :
            
            parent_id = "internal" + "|" + parent_string
            
            parent_set.add(parent_id)
            all_set.add(parent_id)
        
            machine_dict[parent_id]=[]
            machine_dict[parent_id].append(parent_string)
            
            print(parent_id)
            print(parent_string)
        
    
    def read_external_index(self,external_index):
        pass




class Data_Holder_for_index(Data_Holder_base):


    def __init__(self,*args,**kwagrs):
        super().__init__(*args,**kwagrs)

Data_Holder=Data_Holder_for_index

class GameList_for_index(GameList_base):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        # 发送的信号
        #原始
        #self.new_var_virtual_event_name_CurrentGame=r'<<CurrentGame>>'
        #改为：
        self.new_var_virtual_event_name_CurrentGame=r'<<IndexBeChosen>>'
        
        # 目录 保存 信号的
        self.new_var_data_for_virtual_event=None

    def new_func_bindings(self,):
        super().new_func_bindings()
        # 外形变化，刷新
        #self.bind( '<Configure>',lambda event:self.new_func_refresh_all)
        ""

    # derived
        # 之后 改
    # 图标列
    def new_func_table_draw_icon_colunm(self,row,item_id,game_info,line_position_y1,line_position_y2,foreground):
        if self.new_var_data_holder.flag_search:
            items_in_level_1   = self.new_var_data_holder.items_in_level_1_for_search
            items_have_child   = self.new_var_data_holder.items_have_child_for_search
            #items_have_parent  = self.new_var_data_holder.items_have_parent_for_search
            items_opened       = self.new_var_data_holder.items_opened_for_search
            #gamelist_to_show   = self.new_var_data_holder.gamelist_to_show_for_search
            
        else:
            items_in_level_1   = self.new_var_data_holder.items_in_level_1
            items_have_child   = self.new_var_data_holder.items_have_child 
            #items_have_parent  = self.new_var_data_holder.items_have_parent
            items_opened       = self.new_var_data_holder.items_opened
            #gamelist_to_show   = self.new_var_data_holder.gamelist_to_show        
        
        if foreground==self.new_var_foreground:
            image_plus  = self.new_image_plus
            image_minus = self.new_image_minus
        else:
            image_plus  = self.new_image_plus_select
            image_minus = self.new_image_minus_select
        
        
        if item_id in items_in_level_1:
            #第一层
            space_before_icon  = self.new_var_space_before_icon*2+self.new_var_icon_width
        else:
            #第二层
            space_before_icon  = self.new_var_space_before_icon*2+self.new_var_icon_width*2

        # + - ，展开收起图标
        if item_id in items_have_child:# 有克隆版本的
            if item_id in items_opened : 
                # 减号
                #self.new_ui_table.create_text( 
                #            0 , 
                #            int((line_position_y1+line_position_y2)/2),
                #            anchor=tk.W,
                #            text = self.new_var_text_for_minus_sign,
                #            #state='disabled',
                #            fill=foreground,
                #            tags=(
                #                "text_sign_minus",# 此标记用于 .tag_bind
                #                "item_id "+item_id, # "item_id " + item_id ,
                #                # 因为不能用纯数字，所以加个字符前缀 "item_id "
                #                "row_number " + str(row),
                #            ),
                #            )
                self.new_ui_table.create_image(
                            self.new_var_space_before_icon , 
                            int((line_position_y1+line_position_y2)/2),
                            anchor=tk.W,
                            image=image_minus,
                            tags=(
                                "image_sign_minus",# 此标记用于 .tag_bind
                                "item_id "+item_id, # "item_id " + item_id ,
                                # 因为不能用纯数字，所以加个字符前缀 "item_id "
                                "row_number " + str(row)
                            )
                            
                )
            # 加号
            else:
                #self.new_ui_table.create_text( 
                #            0 , 
                #            int((line_position_y1+line_position_y2)/2),
                #            anchor=tk.W,
                #            text = self.new_var_text_for_plus_sign,
                #            #state='disabled',
                #            fill=foreground,
                #            tags=(
                #                "text_sign_plus",# 此标记用于 .tag_bind
                #                "item_id "+item_id, # "item_id " + item_id ,
                #                # 因为不能用纯数字，所以加个字符前缀 "item_id "
                #                "row_number " + str(row), )
                #            )
                self.new_ui_table.create_image(
                            self.new_var_space_before_icon , 
                            int((line_position_y1+line_position_y2)/2),
                            anchor=tk.W,
                            image=image_plus,
                            tags=(
                                "image_sign_plus",# 此标记用于 .tag_bind
                                "item_id "+item_id, # "item_id " + item_id ,
                                # 因为不能用纯数字，所以加个字符前缀 "item_id "
                                "row_number " + str(row),
                            ),
                            )

    
    
    # derived
    def new_func_table_show_pop_up_menu(self,):
        #待补充
        pass
    
    # derived
    # 把发送的信号改一下名字
    def new_func_remember_select_row(self,item_id,row_number,):

        self.new_var_remember_select_row_id     = item_id
        self.new_var_remember_select_row_number = row_number
        
        #print()
        #print("  select row : {} ".format(row_number) )
        #print("  select id  : {} ".format(item_id)    )
        
        self.new_func_refresh_table()
        
        self.new_var_data_for_virtual_event = item_id # 目录用的

        self.event_generate( self.new_var_virtual_event_name_CurrentGame )


# 取消一些
class GameList_for_index_2(GameList_for_index):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_unbind_some_bindings()
    # derived
    #   取消
    
    # 一些接收信号的 bindings
    # 单独写在一处的，取消也方便
    def new_func_bindings_for_receive_virtual_event(self,):
        pass
    
    #def new_func_show_gamelist_again(self,):
    #    pass
    
    def new_func_unbind_some_bindings(self):
        header = self.new_ui_header
        table = self.new_ui_table
        # 点击标题，排序
        #header.tag_bind( "header_backgroud_rectangle",'<ButtonRelease-1>',self.new_func_header_binding_click)
        header.tag_unbind( "header_backgroud_rectangle",'<Button-1>',)
        
        #header.bind( '<Configure>',self.new_func_header_resize)
        #header.unbind( '<Configure>',)
        #table.bind('<Configure>',  self.new_func_table_binding_resize)
        #table.unbind('<Configure>',)


# new bindings
class GameList_for_index_3(GameList_for_index_2):

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
    
    
    def new_func_bindings(self,):
        super().new_func_bindings()
        
        #self.bind('<Configure>',self.new_func_self_resize)
    
    
    def new_func_self_resize(self,event):
        print(event.height)
        self.new_func_refresh_all()
        print("aaaa")
    def new_func_table_binding_resize(self,event):
        print("xxxxx")
        print(event.height)
        print(event.width)
        super().new_func_table_binding_resize(event)
        
        
GameList = GameList_for_index_3


if __name__ == "__main__" :
    from .read_pickle import  read as read_pickle
    from . import global_static_filepath as the_files # 图标 图片 路径
    
    root=tk.Tk()
    
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    index = GameList(root)
    index.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S)
    
    # 数据文件
    main_data_file_path = the_files.file_pickle_gamelist_data
    try:
        game_list_data = read_pickle( main_data_file_path )
        print("a")
    except:
        game_list_data = {}
        print("b")
    
    print(game_list_data.keys())

    
    temp = built_index_data()
    temp.feed_data(internal_index=game_list_data["internal_index"])
    the_data = temp.data
    
    
    
    gamelist_window=index
    
    # 添加数据
    gamelist_window.new_func_feed_data(the_data)
    # 添加数据，所有列范围
    gamelist_window.new_func_set_all_columns( columns = the_data["columns"] )
    # 添加数据，列宽度
    #gamelist_window.new_func_set_column_width( **configure_data["gamelist_columns_width"] )
    # 添加数据，要显示的 列
    gamelist_window.new_func_set_columns_to_show( columns = the_data["columns"] )
    # 添加数据，列标题 翻译
    #gamelist_window.new_func_header_set_column_translation( key_word_translation.columns_translation )
    
    
    all_content = the_data["set_data"]["all_set"]
    print(  len(all_content))
    print(  len(all_content))
    print(  len(all_content))
    gamelist_window.new_var_data_holder.generate_new_list_by_id(all_content)
    gamelist_window.new_func_table_reload_the_game_list()
    
    root.update()
    gamelist_window.new_func_refresh_all()
    # 手动添加数据
    # 而不接收信号，刷新数据
    
    
    
    def receive_virtual_event_from_index(event):
        print("")
        print("index's virtual event received")
        time_1 = time.time()
        
        gameindex_window = event.widget
        event_info = gameindex_window.new_var_data_for_virtual_event
        print(event_info)
    
    
    root.bind("<<IndexBeChosen>>",receive_virtual_event_from_index)
    
    root.mainloop()


