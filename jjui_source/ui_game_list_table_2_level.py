# -*- coding: utf_8_sig-*-
#import sys
#import os

import math
import time
import re
import locale

import tkinter as tk
import tkinter.ttk as ttk

from . import global_variable

#from PIL import Image, ImageTk
 
if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

#from . import global_static_filepath as the_files # 图标 图片 路径
from . import ui_game_list_table_1_level
Data_Holder_level_1 = ui_game_list_table_1_level.Data_Holder
GameList_level_1    = ui_game_list_table_1_level.GameList

class Data_Holder_level_2(Data_Holder_level_1):
    """
    
    双层列表 数据
    
    """

    def __init__(self,*args,**kwagrs):
        super().__init__(*args,**kwagrs)
        
        # 标记，当前列表，第一层列表范围（主版、无主版的克隆版）
        self.items_in_level_1 = set() 
        self.items_in_level_1_for_search = set()
        # 用 set() ，方便用 in 确认元素存在
        
        # 标记，当前列表，第一层中，有子元素的主版本，范围
        self.items_have_child = set()
        self.items_have_child_for_search = set()
        # 用 set() ，方便用 in 确认元素存在
        
        # 第二层 范围
        self.items_have_parent = set()
        self.items_have_parent_for_search = set()
        
        # 改一下格式，不要这个
        #self.gamelist_data_for_level_2 = {} # dict
        # parent_id : 子元素id列表
        # parent_id : 子元素id列表
        # .....
        
        # 改一下格式，不要这个
        # 提前建一个空的变量，用于上面的 gamelist_data_for_level_2
        #   要快一点
        #self.gamelist_data_for_level_2_template={}
        
        self.parent_have_more_than_1_children = set()
        
    # derived
    def feed_data(self,internal_data=None,external_index=None):
        super().feed_data(internal_data,external_index)
        
        # 改一下格式，不要这个
        #if internal_data:
        #    
        #    # 提前建一个空的变量，
        #    #   要快一点
        #    self.gamelist_data_for_level_2_template={ 
        #            parent_id : [] 
        #                    for parent_id in self.parent_to_clone
        #                    }
        if self.internal_data:
            temp = []
            for parent_id in self.parent_to_clone :
                if len( self.parent_to_clone[parent_id] ) > 1:
                    temp.append( parent_id )
            self.parent_have_more_than_1_children = set( temp )


    # derived
    # 点击目录 切换列表，用这个
    def generate_new_list_by_id(self,the_id_list,from_index=True):
        # 生成 列表
        # self.all_set    =set()
        # self.parent_set =set()
        # self.clone_set  =set()
        # self.parent_to_clone = {}
        # self.clone_to_parent = {}
        
        print("")
        print(" generate_new_list")
        time_1 = time.time()
        
        # 标记重置
        if from_index:
            self.flag_search = False
            # 正常状态，不在搜索中
        
        # 转为 set
        if type(the_id_list)==set or type(the_id_list)==frozenset :
            pass
        else:
            the_id_list = set(the_id_list)
        
        # 范围 限制
        if self.filter_set:
            if self.all_set is the_id_list: # all_set 加点速
                temp_parent_set = self.parent_set - self.filter_set
                temp_clone_set  = self.clone_set  - self.filter_set
            else:
                temp_parent_set = the_id_list & self.parent_set - self.filter_set
                temp_clone_set  = the_id_list & self.clone_set  - self.filter_set
        else:
            if self.all_set is the_id_list: # all_set 加点速
                temp_parent_set = self.parent_set
                temp_clone_set  = self.clone_set
            else:
                temp_parent_set = the_id_list & self.parent_set
                temp_clone_set  = the_id_list & self.clone_set
        
        time_2 = time.time()
        print(" generate_new_list time_A:{}".format(time_2-time_1))
        
        
        if temp_parent_set and temp_clone_set:
            print("  level_2")
            self.get_list_of_2_level(temp_parent_set,temp_clone_set)
        else:
            print("  level_1")
            self.get_list_of_1_level_only_parent_or_only_clone(temp_parent_set,temp_clone_set)
        
        #self.gamelist_to_show.clear() 
        
        time_3=time.time()
        print(" generate_new_list time_B:{}".format(time_3-time_2))
        

        
        self.sort_the_list(self.sort_key , self.sort_reverse)
        
        time_4=time.time()
        print(" generate_new_list time_C:{}".format(time_4-time_3))
        print(" generate_new_list time  :{}".format(time_4-time_1))
    
    # for self.generate_new_list_by_id()
    def get_list_of_1_level_only_parent_or_only_clone(self,temp_parent_set=None,temp_clone_set=None):
        # 仅有主版本 或者 仅有克隆版本
        
        print(1)
        
        if self.flag_search:
            # 标记 第1层 范围
            if temp_parent_set:
                self.items_in_level_1_for_search = temp_parent_set
            else:
                self.items_in_level_1_for_search = temp_clone_set
            
            print(len(self.items_in_level_1_for_search))
            
            # 标记 
            self.items_have_child_for_search  = set()
            self.items_have_parent_for_search = set()
        if not self.flag_search:
            # 标记 第1层 范围
            if temp_parent_set:
                self.items_in_level_1 = temp_parent_set
            else:
                self.items_in_level_1 = temp_clone_set
            
            print(len(self.items_in_level_1))
            
            # 标记 
            self.items_have_child  = set()
            self.items_have_parent = set()
    # for self.generate_new_list_by_id()
    def get_list_of_2_level(self,temp_parent_set=None,temp_clone_set=None):

        time_1 = time.time()
        
        # 得到分组需要的一些 set 
        def get_some_set():
            # return clone_have_parent,clone_no_parnet,parent_have_clone
            
            temp_clone_have_parent = []
            # 范围 temp_parent_set & self.parent_to_clone_keys
            for parent_game in ( temp_parent_set & self.parent_to_clone_keys ):
                temp_clone_have_parent.extend( self.parent_to_clone[parent_game] )
            
            # 克隆，主版本 存在的 ,    当前列表，交集
            clone_have_parent  = set(temp_clone_have_parent) & temp_clone_set
            
            # 克隆，主版本 不存在的：
            clone_no_parnet    = temp_clone_set - clone_have_parent
            
            temp_parent_have_clone = []
            for clone_game in clone_have_parent:
                temp_parent_have_clone.append( self.clone_to_parent[clone_game] )
            
            # 主版，克隆存在的
            parent_have_clone = set(temp_parent_have_clone) & temp_parent_set
            
            # 主版，克隆不存在的
            #panret_no_clone   = temp_parent - parent_have_clone
            
            return clone_have_parent,clone_no_parnet,parent_have_clone
        
        clone_have_parent,clone_no_parnet,parent_have_clone = get_some_set()
        
        time_2 = time.time()
        print("\tlevel_2 timeA : {}".format(time_2-time_1))
        
        
        ####
        if self.flag_search:
            # 标记 第1层 范围
            self.items_in_level_1_for_search = clone_no_parnet | temp_parent_set
            
            # 标记
            self.items_have_child_for_search  = parent_have_clone
            self.items_have_parent_for_search = clone_have_parent
        else:
            # 标记 第1层 范围
            self.items_in_level_1 = clone_no_parnet | temp_parent_set
            
            # 标记
            self.items_have_child  = parent_have_clone
            self.items_have_parent = clone_have_parent
        

        time_3 = time.time()
        print("\tlevel_2 timeB : {}".format(time_3-time_2))

        print("\tlevel_2 time  : {}".format(time_3-time_1))
    
    
    
    def func_for_sort_the_list(self,the_sort_key,reverse,flag_search):
        
        if flag_search:
            items_in_level_1   = self.items_in_level_1_for_search
            items_have_child   = self.items_have_child_for_search
            items_have_parent  = self.items_have_parent_for_search
            self.gamelist_to_show_for_search.clear() # 最后 赋值
        else:
            items_in_level_1   = self.items_in_level_1
            items_have_child   = self.items_have_child 
            items_have_parent  = self.items_have_parent
            self.gamelist_to_show.clear() # 最后 赋值
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
            def func_for_sort(item_id,machine_dict=self.machine_dict,the_index=the_index):
                return machine_dict[item_id][the_index]
            
            # 本地排序
            if the_sort_key in ("translation","alt_title"):
                if global_variable.flag_setlocale_LC_COLLATE:
                    
                    def func_for_sort(item_id,temp_dict=self.machine_dict,the_index=the_index):
                        
                        return locale.strxfrm(temp_dict[item_id][the_index])                

        
        
        gamelist_to_show = []
        

        
        # 第一层 排序
        temp_list = sorted(
                items_in_level_1,
                key     = func_for_sort,
                reverse = reverse,)
        
        # 如有 第二层
        if items_have_parent:
            # 排序
            # 范围以内的
            # 有两个以上子列表的,(子列表 可能 有多余的项目，之后还要处理)
            for parent_id in ( items_have_child & self.parent_have_more_than_1_children ):
                self.parent_to_clone[parent_id].sort(
                        key     = func_for_sort,
                        reverse = reverse,
                        )
            
            # 插入列表
            for game_id in temp_list :
                
                gamelist_to_show.append( game_id )
                
                if game_id in items_have_child:
                    for clone_id in self.parent_to_clone[game_id]:
                        if clone_id in items_have_parent:
                            gamelist_to_show.append(clone_id)
        
        # 没有 第二层
        else:
            gamelist_to_show = temp_list
            print("no level 2")
        
        if flag_search:
            self.gamelist_to_show_for_search = gamelist_to_show
        else:
            self.gamelist_to_show = gamelist_to_show


        
    def get_item_id_from_item_info(self,item_info):
        return item_info["name"]

# search
class Data_Holder_level_2_2(Data_Holder_level_2):

    def __init__(self,*args,**kwagrs):
        super().__init__(*args,**kwagrs)
    
    
    # for search
    #   同样是搜索第一层
    #   但是新列表，分组方式不同
    def generate_new_list_by_search(self,the_search_string,the_search_range=None):
        print()
        print("generate_new_list_by_search")
        t1=time.time()
        # 标记重置
        self.flag_search = True
        
        the_search_string = the_search_string.lower()
        
        #if the_search_range is None:
        #    the_search_range = []
        #
        
        # self.gamelist_to_show
        #   搜这个
        new_list = []
        for item_id in self.gamelist_to_show:
            for x in self.machine_dict[item_id]: # 全搜
                if the_search_string in x.lower() :
                    new_list.append(item_id)
                    break
        
        # the_id_list = set(new_list)
        # #print(len(new_list))
        # #print(len(the_id_list))
        # 
        # temp_parent_set = the_id_list & self.parent_set
        # temp_clone_set  = the_id_list & self.clone_set
        # 
        # if temp_parent_set and temp_clone_set:
        #     print("  level_2")
        #     self.get_list_of_2_level(temp_parent_set,temp_clone_set)
        # else:
        #     print("  level_1")
        #     self.get_list_of_1_level_only_parent_or_only_clone(temp_parent_set,temp_clone_set)
        # 
        # self.sort_the_list(self.sort_key , self.sort_reverse)
        
        self.generate_new_list_by_id(new_list,from_index=False)
        
        t2=time.time()
        print("generate_new_list_by_search,time : {}".format(t2-t1))

    # for search re
    def generate_new_list_by_search_regular(self,the_search_string,the_search_range=None):
        t1=time.time()
        # 标记重置
        self.flag_search = True
        
        #if the_search_range is None:
        #    the_search_range = []
        #
        
        
        #self.gamelist_to_show
        # 搜这个
        new_list = []
        
        p=re.compile(the_search_string,re.IGNORECASE)
        
        for item_id in self.gamelist_to_show:
            for x in self.machine_dict[item_id]: # 全搜 # 限制搜索项目
                if  p.search(x) :
                    new_list.append(item_id)
                    break
        
        self.generate_new_list_by_id(new_list,from_index=False)
        
        t2=time.time()
        print("generate_new_list_by_search,time : {}".format(t2-t1))

class Data_Holder_level_2_3(Data_Holder_level_2_2):

    def __init__(self,*args,**kwagrs):
        super().__init__(*args,**kwagrs)

    # derived
    # 当前列表，删除选中项
    def func_for_delete_items_from_current_list(self,items):
        if len(items) == 0 :return
        
        if self.flag_search:
            items_in_level_1   = self.items_in_level_1_for_search
            #items_have_child   = self.items_have_child_for_search
            items_have_parent  = self.items_have_parent_for_search
        else:
            items_in_level_1   = self.items_in_level_1
            #items_have_child   = self.items_have_child 
            items_have_parent  = self.items_have_parent
        
        # 当前列表的话，范围是没有问题的，不用管
        
        the_id_list = (items_in_level_1 | items_have_parent) - items
        
        self.generate_new_list_by_id(the_id_list,from_index=False)
        
        
        
        
        

Data_Holder = Data_Holder_level_2_3







class GameList_level_2(GameList_level_1):
    """
    
    双层列表
    
    """

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_table_type = "mame two level"
        
        self.new_var_data_holder = Data_Holder()
        
        #self.new_var_space_before_icon_level_2 = 10 + 16
    
    # derived
    def new_func_table_draw_icon_colunm(self,row,item_id,game_info,line_position_y1,line_position_y2,foreground):
        
        # self.new_var_icon_width = 16
        
        if self.new_var_data_holder.flag_search:
        
            if item_id in self.new_var_data_holder.items_in_level_1_for_search:
                #第一层
                space_before_icon  = self.new_var_space_before_icon 

            else:
                #第二层
                space_before_icon  = self.new_var_space_before_icon + self.new_var_icon_width
        
        else:
        
            if item_id in self.new_var_data_holder.items_in_level_1:
                #第一层
                space_before_icon  = self.new_var_space_before_icon 

            else:
                #第二层
                space_before_icon  = self.new_var_space_before_icon + self.new_var_icon_width

            
        # draw_icon
        self.new_func_table_draw_icon_image(
                    # x
                    space_before_icon,
                    # y
                    int((line_position_y1+line_position_y2)/2),
                    # image
                    self.new_func_table_choose_icon_image(game_info),
                    
                    item_id,
                    )


GameList = GameList_level_2


if __name__ == "__main__" :
    passs


