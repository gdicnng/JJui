# -*- coding: utf_8_sig-*-
#import sys
#import os

import math
import time
import re
import locale

import tkinter as tk
import tkinter.ttk as ttk

from PIL import Image, ImageTk
# Pillow
# DeprecationWarning: 
# BILINEAR is deprecated and will be removed in Pillow 10 (2023-07-01).
# Use Resampling.BILINEAR instead.
# 老的 Image.BILINEAR 就是 int 2
# 新的 Image.Resampling.BILINEAR 是 <enum 'Resampling'>，
#   新版本还没有出来，不知道直接用 2 ，可不可以
try:
    bilinear = Image.Resampling.BILINEAR
except:
    bilinear = Image.BILINEAR

from . import global_variable

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

from . import global_static_filepath as the_files # 图标 图片 路径
from . import ui_game_list_table_2_level

Data_Holder_base = ui_game_list_table_2_level.Data_Holder
GameList_base    = ui_game_list_table_2_level.GameList

class Data_Holder_level_2_collapse(Data_Holder_base):
    """
    
    双层列表 数据
    总是收起
    
    """

    def __init__(self,*args,**kwagrs):
        super().__init__(*args,**kwagrs)
        
        self.items_opened = set()
        self.items_opened_for_search = set()
    
    def clear(self):
        
        super().clear()
        
        self.items_opened.clear()
        self.items_opened_for_search.clear()
    
    # derived
    # 点击目录 切换列表，用这个
    #def generate_new_list_by_id(self,the_id_list):
    #    super().generate_new_list_by_id(the_id_list)

    def func_for_sort_the_list(self,the_sort_key,reverse,flag_search):
        
        if flag_search:
            items_in_level_1   = self.items_in_level_1_for_search
            #items_have_child   = self.items_have_child_for_search
            #items_have_parent  = self.items_have_parent_for_search
            #items_opened       = self.items_opened_for_search
            self.gamelist_to_show_for_search.clear() # 重置 # 最后 赋值
        else:
            items_in_level_1   = self.items_in_level_1
            #items_have_child   = self.items_have_child 
            #items_have_parent  = self.items_have_parent
            #items_opened       = self.items_opened
            self.gamelist_to_show.clear() # 重置 # 最后 赋值
            
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
        
        gamelist_to_show = sorted(
                items_in_level_1,
                key     = func_for_sort,
                reverse = reverse,)
                
        if flag_search:
            self.gamelist_to_show_for_search = gamelist_to_show
            self.items_opened_for_search = set() # 重置
        else:
            self.gamelist_to_show = gamelist_to_show
            self.items_opened = set() # 重置
    
    
    # derived
    def get_current_gamelist_number(self,):
        if self.flag_search:
            return len( self.items_in_level_1_for_search ) + len( self.items_have_parent_for_search )
        else:
            return len( self.items_in_level_1 ) + len( self.items_have_parent )
    
    # insert children
    def insert_item_s_children(self,row_number,item_id):
        
        if self.flag_search:
            #items_in_level_1   = self.items_in_level_1_for_search
            items_have_child   = self.items_have_child_for_search
            items_have_parent  = self.items_have_parent_for_search
            items_opened       = self.items_opened_for_search
            gamelist_to_show   = self.gamelist_to_show_for_search
                
        else:
            #items_in_level_1   = self.items_in_level_1
            items_have_child   = self.items_have_child 
            items_have_parent  = self.items_have_parent
            items_opened       = self.items_opened
            gamelist_to_show   = self.gamelist_to_show
        
        
        if not gamelist_to_show: return
        
        # 校验 id 
        temp_item_id = gamelist_to_show[row_number]
        if item_id != temp_item_id:
            return
        
        the_index = 0 # 列表的范围从0 开始（空列表，0 都没有）
        try:
            the_index = self.internal_data["columns"].index(self.sort_key)
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

        if item_id in items_have_child:
            
            # 标记
            items_opened.add(item_id)
            #print(items_opened)
            
            child_list = list( set(self.parent_to_clone[item_id]) & items_have_parent)
            
            child_list.sort(
                    key=func_for_sort,
                    reverse=self.sort_reverse,
                    )

            #print(child_list)
            
            # 最后一行，，不用校验，补充在最后
            if row_number + 1 == len( gamelist_to_show ):
                gamelist_to_show.extend( child_list )
            
            # 不是最后一行，校验一下，插入
            else:
                if gamelist_to_show[row_number+1] in child_list:# 已经有了
                    print("already have ,quit")
                    return
                else:
                    #for child_id in child_list:
                    #    if child_id in items_have_parent:
                    #        gamelist_to_show.insert(row_number+1, child_id )
                    gamelist_to_show[row_number+1:row_number+1]=child_list

    # delete children
    def delete_item_s_children(self,row_number,item_id):
        print("")
        print("delete children")
        
        if self.flag_search:
            #items_in_level_1   = self.items_in_level_1_for_search
            items_have_child   = self.items_have_child_for_search
            items_have_parent  = self.items_have_parent_for_search
            items_opened       = self.items_opened_for_search
            gamelist_to_show   = self.gamelist_to_show_for_search
                
        else:
            #items_in_level_1   = self.items_in_level_1
            items_have_child   = self.items_have_child 
            items_have_parent  = self.items_have_parent
            items_opened       = self.items_opened
            gamelist_to_show   = self.gamelist_to_show
        
        
        if not gamelist_to_show: return        

        # 校验 id 
        temp_item_id = gamelist_to_show[row_number]
        if item_id != temp_item_id:
            return
        
        if item_id in items_have_child:
            # 标记
            if item_id in items_opened:
                items_opened.remove(item_id)
            #print(items_opened)
            
            max_number = len(gamelist_to_show)
            
            
            if row_number >= max_number :return
            
            
            child_list = set( self.parent_to_clone[item_id]) & items_have_parent
            
            # 再验证一下，挨个数一遍？
            count=0
            for row in range(row_number+1,max_number):
                next_item_id  = gamelist_to_show[row]
                if next_item_id in child_list:
                    count+=1
                else:
                    print("children number:")
                    print(count)
                    break
            if count:
                del gamelist_to_show[row_number+1:row_number+1+count]


class Data_Holder_level_2_collapse_2(Data_Holder_level_2_collapse):

    def __init__(self,*args,**kwagrs):
        super().__init__(*args,**kwagrs)
    
    
    # search
    #   和前面两个列表，搜索范围不同
    #   和第一个列表，分组方式不同
    def generate_new_list_by_search(self,search_string,):
        print()
        print("generate_new_list_by_search")
        t1=time.time()
        # 标记重置
        self.flag_search = True
        
        # 范围
        # 第一层 | 第二层
        # ( self.items_in_level_1 | self.items_have_parent )
        the_id_s = self.items_in_level_1 | self.items_have_parent
        new_list = self.for_search( the_id_s ,search_string )
        
        self.generate_new_list_by_id(new_list,from_index=False)
        
        t2=time.time()
        print("generate_new_list_by_search,time : {}".format(t2-t1))
    
    # search_regular
    #   和前面两个列表，搜索范围不同
    #   和第一个列表，分组方式不同
    def generate_new_list_by_search_regular(self,search_string,the_search_range=None):
        t1=time.time()
        # 标记重置
        self.flag_search = True
        
        #################
        
        # 范围
        # 第一层 | 第二层
        # ( self.items_in_level_1 | self.items_have_parent )
        the_id_s = self.items_in_level_1 | self.items_have_parent
        new_list = self.for_search_regular( the_id_s,search_string )
        
        self.generate_new_list_by_id(new_list,from_index=False)
        
        t2=time.time()
        print("generate_new_list_by_search_regular,time : {}".format(t2-t1))
    
    
    # 多选模式，全选功能
    def get_current_list_all_id(self,):
        if self.flag_search:
            return self.items_in_level_1_for_search | self.items_have_parent_for_search
        else:
            return self.items_in_level_1 | self.items_have_parent
    
    # 多选模式 
    # ctrl + 鼠标 
    # 一个一个选
    def get_this_item_s_children(self,the_item):
        if self.flag_search:
            items_opened = self.items_opened_for_search 
            items_have_parent = self.items_have_parent_for_search 
            items_have_child = self.items_have_child_for_search
        else:
            items_opened = self.items_opened 
            items_have_parent = self.items_have_parent 
            items_have_child = self.items_have_child 
        
        if the_item not in items_have_child:
            return set()
        
        if the_item in items_opened:
            return set()
        else:
            return set(self.parent_to_clone[ the_item ]) & items_have_parent
    
    
    # 多选模式，选中第一层，如果第二层没有展开，也一起选中，
    # 根据选中的 id ，得到 其 包含 第二层的 id
    def get_hide_children(self,old_items):
        # old_items ,set 格式
        if self.flag_search:
            items_opened = self.items_opened_for_search 
            items_have_parent = self.items_in_level_1_for_search 
            items_have_child = self.items_have_child_for_search
        else:
            items_opened = self.items_opened 
            items_have_parent = self.items_have_parent 
            items_have_child = self.items_have_child 
        
        # self.parent_to_clone
        
        # 有隐藏 第二层 内容的
        parent_items_which_hide_child = (items_have_child - items_opened) & old_items
        
        if not parent_items_which_hide_child: return set()
        
        
        
        child_list = []
        for parent_id in parent_items_which_hide_child:
            child_list.extend( self.parent_to_clone[parent_id] )# 超范围
        
        return set(child_list) & items_have_parent # 范围限制

Data_Holder = Data_Holder_level_2_collapse_2

# -----------------------------------
# -----------------------------------
# -----------------------------------

class GameList_level_2_collapse(GameList_base):
    """
    
    双层列表
    总是收起
    
    """

    def __init__(self, parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        self.new_var_table_type = "mame 2 level , collapes" # 这个值别改了，在别的角本里被用了
        
        self.new_var_data_holder = Data_Holder()
        
        #self.new_var_text_for_plus_sign  = " "+_("+")#＋╬︽ ︾
        #self.new_var_text_for_minus_sign = " "+_("-")#－═︾
        
        
        
    def new_func_bindings(self,):
        super().new_func_bindings()
        #self.new_ui_table.tag_bind("text_sign_plus", '<Button-1>', self.new_func_table_binding_click_plus_sign )
        #self.new_ui_table.tag_bind("text_sign_minus",'<Button-1>', self.new_func_table_binding_click_minus_sign )
        
        #self.new_ui_table.tag_bind("text_sign_plus", '<Button-3>', self.new_func_table_binding_right_click_plus_or_miuns_sign,"+" )
        #self.new_ui_table.tag_bind("text_sign_minus",'<Button-3>', self.new_func_table_binding_right_click_plus_or_miuns_sign,"+" )

        #image
        self.new_ui_table.tag_bind("image_sign_plus", '<Button-1>', self.new_func_table_binding_click_plus_sign )
        self.new_ui_table.tag_bind("image_sign_minus",'<Button-1>', self.new_func_table_binding_click_minus_sign )
    
        self.new_ui_table.tag_bind("image_sign_plus", '<Button-3>', self.new_func_table_binding_right_click_plus_or_miuns_sign,"+" )
        self.new_ui_table.tag_bind("image_sign_minus",'<Button-3>', self.new_func_table_binding_right_click_plus_or_miuns_sign,"+" )

    # bindings
    # 点击 + 号
    def new_func_table_binding_click_plus_sign(self,event):
        print()
        print("click_plus_sign")
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        
        #   删除部件；
        #   或者，等之后，反正要刷新画面的
        
        # 选中此行
        self.new_func_remember_select_row(item_id,row_number)
        
        # 列表 插入
        self.new_var_data_holder.insert_item_s_children(row_number,item_id)
        
        # 重载列表
        self.new_func_table_reload_the_game_list()

    # bindings
    # 点击 - 号
    def new_func_table_binding_click_minus_sign(self,event):
        print()
        print("click_minus_sign")
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        
        #   删除部件；
        #   或者，等之后，反正要刷新画面的
        
        # 选中此行
        self.new_func_remember_select_row(item_id,row_number)
        
        # 列表 删除
        self.new_var_data_holder.delete_item_s_children(row_number,item_id)
        
        # 重载列表
        self.new_func_table_reload_the_game_list()
    
    
    # derived
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
            
        # 普通图标
        self.new_func_table_draw_icon_image(
                        # x
                        space_before_icon,
                        # y
                        int((line_position_y1+line_position_y2)/2),
                        # image
                        self.new_func_table_choose_icon_image(game_info),
                        
                        item_id,
                        )
    
    # bindings
    # 鼠标右击时，选中此行
    def new_func_table_binding_right_click_plus_or_miuns_sign(self,event):
        print()
        print("right click plus_sign or minus_sign")
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        self.new_func_remember_select_row(item_id,row_number)
    
    
    # derived
    # 定位 上一个选中项目
    def new_func_bindings_receive_virtual_event_for_find_item(self,event):
        print("***")
        print(r"receive_virtual_event <<FindItemById>>")
        widget  = event.widget
        item_id = widget.new_var_data_for_FindItemById
        
        if item_id : print(item_id)
        else   : return
        
        # 搜索状态、正常状态 区分
        if self.new_var_data_holder.flag_search:
            items_opened = self.new_var_data_holder.items_opened_for_search
            items_in_level_1  = self.new_var_data_holder.items_in_level_1_for_search
            items_have_parent = self.new_var_data_holder.items_have_parent_for_search
        else:
            items_opened = self.new_var_data_holder.items_opened
            items_in_level_1  = self.new_var_data_holder.items_in_level_1
            items_have_parent = self.new_var_data_holder.items_have_parent
        
        # 不在范围
        if item_id not in items_in_level_1:
            if item_id not in items_have_parent:
                print("not in here")
                return
        
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
                    # self.new_func_remember_select_row 中，有刷新
                    return
        
        # 记录无效
        
        def find_in_level_1(game_id,from_row = 0 ):
            row_remember = -1
            for row in range(from_row, len(self.new_var_list_to_show)  ):
                if game_id == self.new_func_table_get_id_from_row_number(row):
                    row_remember     = row
                    break
            return row_remember
        
        def find_in_level_2(game_id):
            # 这些，在第二层的，肯定是克隆版
            
            row_remember = -1
            
            parent_id = self.new_var_data_holder.clone_to_parent[game_id]
            
            # --------------------
            # 如果，已经是展开的状态
            if parent_id in items_opened:
                row_remember = find_in_level_1(game_id)
                return row_remember
            
            # --------------------
            # 如果，还没有展开
            row_remember = -1
            parent_row_remember = -1
            
            #找到主版本
            parent_row_remember = find_in_level_1(parent_id)
            
            # 展开主版本
            # 列表 插入
            self.new_var_data_holder.insert_item_s_children(parent_row_remember,parent_id)
            
            # 列有插入变化，需要刷新
            self.new_func_table_reload_the_game_list()
            
            row_remember = find_in_level_1(game_id,parent_row_remember)
            
            return row_remember
        
        
        if item_id in items_in_level_1:
            row = find_in_level_1(item_id)
        else:
            row = find_in_level_2(item_id)
        
        if row == -1 : 
            print("not found")
            #return
        else:
            print("found")
            print("jump to row number :")
            print(row)
            self.new_func_table_jump_to_row(row)
            self.new_func_remember_select_row(item_id,row)
            # self.new_func_remember_select_row 中，有刷新


    #####################
    #####################
    # add icons plus 
    # add icons minus
    
    
    # derived
    # 颜色变化，bitmap 颜色一起变化
    def new_func_set_colour_and_font(self,
                foreground=None,
                background=None,
                selectforeground=None,
                selectbackground=None,
                font=None,
                header_font=None,
                ):
        if foreground is not None:
            self.new_var_foreground = foreground
            # 添加
            ##############
            self.new_func_icon_bitmap_resize() # 图标颜色，随 前景色 一起变化
            #############
        
        super().new_func_set_colour_and_font(
                foreground=foreground,
                background=background,
                selectforeground=selectforeground,
                selectbackground=selectbackground,
                font=font,
                header_font=header_font,
            )


    # derived
    # 初始 ,添加
    def new_func_initial_image_for_icon(self,):
        #super().new_func_initial_image_for_icon()
            # super() 放后面
                # 因为最后边调用了 self.new_func_icon_resize()
                # 不然先 resize() 时，原图像还没有被读取好
        
        self.new_image_plus_original   = Image.open( the_files.image_path_icon_plus )
        self.new_image_minus_original  = Image.open( the_files.image_path_icon_minus )
        
        super().new_func_initial_image_for_icon()
    
    # derived
    def new_func_icon_resize(self,):
        super().new_func_icon_resize()
        
        self.new_func_icon_bitmap_resize()
    
    # new
    def new_func_icon_bitmap_resize(self,):
        new_size = (self.new_var_icon_width ,self.new_var_icon_width )
        
        plus_temp  = self.new_image_plus_original.resize( new_size,bilinear, )
        minus_temp = self.new_image_minus_original.resize(new_size,bilinear, )
        
        self.new_image_plus =ImageTk.BitmapImage(plus_temp,foreground=self.new_var_foreground)
        self.new_image_minus=ImageTk.BitmapImage(minus_temp,foreground=self.new_var_foreground)
        
        self.new_image_plus_select =ImageTk.BitmapImage(plus_temp,foreground=self.new_var_selectforeground)
        self.new_image_minus_select=ImageTk.BitmapImage(minus_temp,foreground=self.new_var_selectforeground)

# 按“→”键 ，展开
class GameList_level_2_collapse_2(GameList_level_2_collapse):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
    
    def new_func_bindings(self,):
        super().new_func_bindings()
        
        # 按“→”键 ，展开
        self.bind('<Right>',self.new_func_table_binding_press_right)
        # ←
        self.bind('<Left>' ,self.new_func_table_binding_press_left)
        # space

    def new_func_table_binding_press_right(self,event):
        if not self.new_var_list_to_show : return
        
        if self.new_var_remember_select_row_id is None : return
        
        
        if self.new_var_remember_select_row_number > -1 :
            # verify id
            try:
                item_id = self.new_var_list_to_show[ self.new_var_remember_select_row_number ]
            except:
                item_id = None
            
            
            if self.new_var_data_holder.flag_search:
                items_have_child   = self.new_var_data_holder.items_have_child_for_search
                items_opened       = self.new_var_data_holder.items_opened_for_search
            else:
                items_have_child   = self.new_var_data_holder.items_have_child 
                items_opened       = self.new_var_data_holder.items_opened
            
            
            ########
            if item_id == self.new_var_remember_select_row_id:
                if item_id in items_have_child:
                    if item_id  not in items_opened: 
                        # 选中此行
                        self.new_func_remember_select_row(item_id,self.new_var_remember_select_row_number)
                        
                        # 列表 插入
                        self.new_var_data_holder.insert_item_s_children(self.new_var_remember_select_row_number,item_id)
                        
                        # 重载列表
                        self.new_func_table_reload_the_game_list()


    def new_func_table_binding_press_left(self,event):
        
        if not self.new_var_list_to_show : return
        
        if self.new_var_remember_select_row_id is None : return
        
        
        if self.new_var_remember_select_row_number > -1 :
            # verify id
            try:
                item_id = self.new_var_list_to_show[ self.new_var_remember_select_row_number ]
            except:
                item_id = None
            
            ########
            if self.new_var_data_holder.flag_search:
                items_have_child   = self.new_var_data_holder.items_have_child_for_search
                items_opened       = self.new_var_data_holder.items_opened_for_search
            else:
                items_have_child   = self.new_var_data_holder.items_have_child 
                items_opened       = self.new_var_data_holder.items_opened            
            
            if item_id == self.new_var_remember_select_row_id:
                if item_id in items_have_child:
                    if item_id  in items_opened: 
                        # 选中此行
                        self.new_func_remember_select_row(item_id,self.new_var_remember_select_row_number)
                        
                        # 列表 删除
                        self.new_var_data_holder.delete_item_s_children(self.new_var_remember_select_row_number,item_id)

                        # 重载列表
                        self.new_func_table_reload_the_game_list()

# 多选 修改
# table 菜单，导出全部
class GameList_level_2_collapse_3(GameList_level_2_collapse_2):

    def __init__(self, parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
    
    
    # derived
    #   Control + A
    #   Control + a
    #   第 1、2 组列表，一样
    #   第3组列表，需要变动
    def new_func_table_binding_ctrl_all(self,event):
        
        print()
        print("Control + a ,select all")
        
        if not self.new_var_list_to_show : return
        
        #all_current_list = set(self.new_var_list_to_show)
        self.new_var_remember_selected_items.clear()
        
        
        self.new_var_remember_selected_items.update(  
                self.new_var_data_holder.get_current_list_all_id()  )
        
        print( len(self.new_var_remember_selected_items) )
        
        self.new_func_refresh_table()
    
    # derived
    #   Control + B1
    #   第 1、2 组列表，一样
    #   第3组列表，需要变动    ,当选中没展开第一层时，克隆版也选中
    def new_func_table_binding_ctrl_and_click(self,event):
        print()
        print("Control and mouse button 1")
        
        row_number,item_id = self.new_func_table_get_row_number_and_item_id(event)
        #print("item id : {}".format(item_id) )
        #print("row number : {}".format(row_number) )
        
        if item_id not in self.new_var_remember_selected_items:
            self.new_var_remember_selected_items.add(item_id)
            children = self.new_var_data_holder.get_this_item_s_children(item_id)
            self.new_var_remember_selected_items.update(children)
        else:
            self.new_var_remember_selected_items.remove(item_id)
            children = self.new_var_data_holder.get_this_item_s_children(item_id)
            self.new_var_remember_selected_items -= children
        
        print("select items' number : ",end="")
        print(len(self.new_var_remember_selected_items))
        #self.new_func_remember_select_row(item_id,row_number)
        self.new_func_refresh_table()
    
    # derived
    #   Shift + B1
    #   第 1、2 组列表，一样
    #   第3组列表，需要变动  ，,当选中没展开第一层时，克隆版也选中
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
        
        if row_number == self.new_var_remember_select_row_number:
            self.new_var_remember_selected_items.clear()
            self.new_var_remember_selected_items.add(item_id)
            self.new_func_refresh_table()
            return
        
        ##
        elif row_number <  self.new_var_remember_select_row_number:
            self.new_var_remember_selected_items.clear()
            
            new_id_list = self.new_var_list_to_show[ row_number : self.new_var_remember_select_row_number + 1 ]
            
            
            id_set_level_1 = set(new_id_list)
            
            id_set_level_2 = self.new_var_data_holder.get_hide_children( id_set_level_1 )
            
            if id_set_level_2:
                self.new_var_remember_selected_items.update(  id_set_level_1 | id_set_level_2 )
            else:
                self.new_var_remember_selected_items.update(  id_set_level_1 )
            
            print( len(id_set_level_1) + len(id_set_level_2) )
            
            self.new_func_refresh_table()
        
        ##
        elif row_number >  self.new_var_remember_select_row_number:
            self.new_var_remember_selected_items.clear()
            
            new_id_list = self.new_var_list_to_show[ self.new_var_remember_select_row_number  : row_number + 1 ]
            
            id_set_level_1 = set(new_id_list)
            
            id_set_level_2 = self.new_var_data_holder.get_hide_children( id_set_level_1 )
            
            if id_set_level_2:
                self.new_var_remember_selected_items.update(  id_set_level_1 | id_set_level_2)
            else:
                self.new_var_remember_selected_items.update(  id_set_level_1 )
            
            print( len(id_set_level_1) + len(id_set_level_2) )
            
            self.new_func_refresh_table()

    # derived
    #   table 右键菜单
    #   导出全部内容
    #       第1 第2 列表相同
    #       第3 列表需要修改
    def new_func_table_pop_up_menu_callback_export_gamelist(self,only_id=True):
        
        if not self.new_var_list_to_show: 
            try:
                os.remove(out_file_path)
            except:
                pass
            return
        
        out_file_path = the_files.file_txt_export
        
        
        if only_id:
            with open(out_file_path,mode="wt",encoding="utf_8") as f:
                for item_id in sorted( self.new_var_data_holder.get_current_list_all_id() ):
                    f.write(item_id)
                    f.write("\n")
        else:
            with open(out_file_path,mode="wt",encoding="utf_8") as f:
                header_list = self.new_func_get_columns_to_show()
                
                for item_id in sorted( self.new_var_data_holder.get_current_list_all_id() ):
                    game_info = self.new_var_the_original_gamelist_dict[ item_id ]
                    
                    for the_header_id in header_list:
                        if the_header_id=="#id":
                            f.write(item_id)
                            f.write("\t")
                        else:
                            if the_header_id in  global_variable.columns_index:
                                the_index = global_variable.columns_index[ the_header_id ]
                                temp = game_info[the_index]
                                f.write(temp)
                                f.write("\t")
                    
                    f.write("\n")


GameList = GameList_level_2_collapse_3


if __name__ == "__main__" :
    passs


