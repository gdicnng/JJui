# -*- coding: utf-8 -*-
"""
    Image_container ：
    
        --------------------------
        |  图片种类选择器  | zip |
        |------------------------|
        |                        |
        |                        |
        |                        |
        |    图片区              |
        |                        |
        |    ( Image_area )      |
        |                        |
        |                        |
        |                        |
        |                        |
        --------------------------
    
"""
# import sys
import os
import glob
import zipfile
#import time

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

from . import global_static_filepath as the_files
from . import global_static
from . import global_static_key_word_translation 
from . import global_variable


image_types          = global_static.extra_image_types
    # ("snap","titles","flyers",......)
key_word_translation = global_static_key_word_translation.extra_image_types_translation



"""
"""


# 变量前缀
# self.new_ui_
# self.new_var_
# self.new_func_
class Image_area(ttk.Frame):

    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        # 备用图片,Pillow 格式，使用时需转换
        self.new_var_backup_image      = Image.open( the_files.image_path_image_no )
        self.new_var_backup_image.load()
        self.new_var_backup_image_used = False
        
        # 当前图片 ,Pillow 格式，使用时需转换
        self.new_var_current_image       = self.new_var_backup_image
        
        # 当前图片 ,tk 格式
        self.new_var_tk_image = ImageTk.PhotoImage(self.new_var_current_image)
        
        self.new_var_aspect_ratio = None
        
        self.new_func_ui()
        self.new_func_bindigns()
    
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        
        self.new_ui_canvas = tk.Canvas( parent ,
                    borderwidth=0,
                    highlightthickness = 0, 
                    )
        self.new_ui_canvas.grid(row=0,column=0, sticky=tk.W+tk.N+tk.E+tk.S,)
        
        #self.new_ui_canvas.create_image(0, 0, image = self.new_var_tk_image , anchor="nw")
        ""

    def new_func_bindigns(self,):
        self.new_ui_canvas.bind('<Configure>',  self.new_func_size_changed)
        self.new_ui_canvas.bind('<Map>',        self.new_func_size_changed_map)
        
        # for test
        #self.new_ui_canvas.bind_all('<Control-KeyPress-i>',self.show_item_number_in_canvas,"+")
        ""

    # bindings
    def new_func_size_changed_map(self,event):
        
        canvas_size=(self.new_ui_canvas.winfo_width(),self.new_ui_canvas.winfo_height() )
        
        self.new_func_show_image(canvas_size , self.new_var_aspect_ratio)
    
    # bindings
    def new_func_size_changed(self,event):
        
        new_canvas_size=(event.width,event.height)
        
        self.new_func_show_image(new_canvas_size , self.new_var_aspect_ratio)
    
    def new_func_show_image(self,canvas_size,aspect_ratio=None):
        
        if not self.new_ui_canvas.winfo_viewable():
            return None
        
        def new_func_creat_new_image(canvas_size,image_current_size):
            # 画图
            
            
            # 清理 先
            self.new_ui_canvas.delete('all',)
            
            temp = self.new_var_current_image.resize( image_current_size,bilinear, )
            #size_temp = temp.size
            #print("image size \t",end='')
            #print(size_temp)
            
            self.new_var_tk_image = ImageTk.PhotoImage(temp)
            
            self.new_ui_canvas.create_image( 
                            int(canvas_size[0] / 2),
                            int(canvas_size[1] / 2), 
                            image=self.new_var_tk_image , 
                            anchor=tk.CENTER )
        
        image_original_size = self.new_var_current_image.size
        
        if aspect_ratio is not None:
            image_current_size = self.image_get_new_size_2(image_original_size,canvas_size,aspect_ratio)
        else:
            image_current_size = self.image_get_new_size(image_original_size,canvas_size)
        
        if image_current_size is None:
            return None
        
        new_func_creat_new_image(canvas_size,image_current_size)
    
    # 图片，获得图片新尺寸（按图片原有比例）
    def image_get_new_size(self,image_size,canvas_size):
        
        flag = False
        
        if canvas_size[0] > 10:# 最小 10
            if canvas_size[1] >10:# 最小 10
                flag = True

        if flag:
            
            a1 = canvas_size[0] / image_size[0]
            a2 = canvas_size[1] / image_size[1]
            
            # 按比例拉伸，取最小的
            if a1>a2:
                new_width  = image_size[0] * a2
                new_height = image_size[1] * a2
            else:
                new_width  = image_size[0] * a1
                new_height = image_size[1] * a1
                
            new_image_size = ( int(new_width),int(new_height) ) 
            
            return new_image_size
        else:
            return None
    
    # 图片，获得图片新尺寸（4:3 或 3:4）
    # mame
    def image_get_new_size_2(self,image_size,canvas_size,aspect_ratio=None):
        
        if canvas_size[0] <= 10: return None
        if canvas_size[1] <= 10: return None
        
        def get_new_size(w,h): # 比如 4:3 
            
            if canvas_size[0]/canvas_size[1] >= w/h:
                new_width  = canvas_size[1] / h * w
                new_height = canvas_size[1]
            else:
                new_width  = canvas_size[0]
                new_height = canvas_size[0] / w * h
            
            #print(new_width)
            #print(new_height)
            
            #print(r"image width height :",new_width,new_height)
            #print(r"image width/height =",new_width/new_height)
            
            return int(new_width) , int(new_height)
        
        # 其它情况
        #    目前未使用
        # aspect_ratio = 4 , 3
        # 4:3 或 3:4 自动调整
        if type(aspect_ratio) == tuple:
            # 4:3
            if image_size[0] >= image_size[1]:
                return get_new_size(aspect_ratio[0],aspect_ratio[1])
            # 3:4
            else:
                return get_new_size(aspect_ratio[1],aspect_ratio[0])
        
    
    
    # pillow 格式
    def new_func_set_new_image(self,new_image,aspect_ratio=None):
        
        self.new_var_aspect_ratio = aspect_ratio
        
        self.new_var_current_image = new_image
        
        canvas_size=(self.new_ui_canvas.winfo_width(),self.new_ui_canvas.winfo_height() )
        
        self.new_func_show_image(canvas_size,aspect_ratio)
        
        self.new_var_backup_image_used=False
    
    # 文件
    def new_func_set_new_image_from_file(self,file_name,aspect_ratio=None):
        
        try:
            self.new_var_aspect_ratio = aspect_ratio
            self.new_var_current_image = Image.open( file_name )
            self.new_var_current_image.load()
            self.new_var_backup_image_used=False
        except:
            self.new_var_current_image = self.new_var_backup_image
            self.new_var_aspect_ratio = None
            self.new_var_backup_image_used=True
        
        canvas_size=(self.new_ui_canvas.winfo_width(),self.new_ui_canvas.winfo_height() )
        self.new_func_show_image(canvas_size,aspect_ratio)

    def new_func_use_backup_image(self,):
        self.new_var_aspect_ratio = None
        
        if not self.new_var_backup_image_used:
            
            self.new_var_current_image = self.new_var_backup_image
            canvas_size=(self.new_ui_canvas.winfo_width(),self.new_ui_canvas.winfo_height() )
            self.new_func_show_image(canvas_size)
            
            self.new_var_backup_image_used=True



    def show_item_number_in_canvas(self,event):
        print()
        n=len(self.new_ui_canvas.find_all())
        print("canvas child item number is {}".format(n))

class Image_container(ttk.Frame):

    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "extra_image_1"
        
        self.new_var_remember_image_type        = None
        #self.new_var_remember_image_folder_path = None
        self.new_var_remember_image_zip_path    = None
        self.new_var_remember_image_zip_object  = None
        
        self.new_var_virtual_event_name_CurrentGame=r'<<CurrentGame>>'
            # 不在这里用这个了
        
        self.new_func_ui()
        self.new_func_bindings()
        self.new_func_initialize()
        
    def new_func_ui(self,):
        parent = self
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        # 第一行 选择栏
        self.new_var_string_for_image_chooser = tk.StringVar()
        
        self.new_ui_image_chooser = ttk.Combobox( parent ,takefocus=False,textvariable=self.new_var_string_for_image_chooser,state="readonly")
        self.new_ui_image_chooser.grid(row=0 , column=0 , sticky=tk.W+tk.N+tk.E,)
        
        # 第一行 zip 标记
        self.new_var_zip_flag = tk.IntVar()
        
        self.new_ui_zip_checkbutton = ttk.Checkbutton( parent ,
                takefocus=False,
                text=_("zip"),
                variable=self.new_var_zip_flag,
                )
        self.new_ui_zip_checkbutton.grid(row=0 , column=1 , sticky=tk.N+tk.E,)
        
        # 第二行 图片显示区
        self.new_ui_image_area = Image_area(parent)
        self.new_ui_image_area.grid(row=1 , column=0 ,columnspan=2, sticky=tk.W+tk.N+tk.E+tk.S,)
        
    def new_func_bindings(self,):
        self.new_ui_image_chooser.bind(r"<<ComboboxSelected>>",self.new_func_for_virtual_event_of_combobox)
        
        #self.bind_all(self.new_var_virtual_event_name_CurrentGame,self.new_func_bindings_receive_virtual_event,"+")
            # 不在这里用这个
        ""
        
    def new_func_initialize(self,):
        # 1 选择栏内容
        # 2 zip 标记
        self.new_var_zip_flag.set( global_variable.user_configure_data["extra_image_usezip"] )
        global_variable.tkint_flag_for_zip_1 = self.new_var_zip_flag
        
        global_variable.Combobox_chooser_image_1 = self.new_ui_image_chooser
        
        temp=[]
        for x in image_types:
            if x in key_word_translation:
                temp.append(key_word_translation[x])
            else:
                temp.append(x)
        self.new_ui_image_chooser["values"]= temp
        
        try: # 读取配置文件中 记录的 index
            n = global_variable.user_configure_data["extra_image_chooser_index"] 
            if n < len(image_types):
                pass
            else:
                n=0
            self.new_ui_image_chooser.set( temp[n] )
        except:
            self.new_ui_image_chooser.set( temp[0] )
        
        self.new_func_get_info_from_choice()# 初始数据读取
    
    def new_func_set_new_image_from_file(self,file_name):
        self.new_ui_image_area.new_func_set_new_image_from_file(file_name)
    
    def new_func_set_new_image(self,new_image):
        self.new_ui_image_area.new_func_set_new_image(new_image)
    
    # combobox 选译时，记录
    # 算了，好像没有用到
    def new_func_for_virtual_event_of_combobox(self,event):
        print()
        print("<<ComboboxSelected>>")
        
        item_id = global_variable.current_item
        
        self.new_func_show( item_id )
        
    def new_func_get_info_from_choice(self,):
        # self.new_var_remember_image_type        = None
        ## self.new_var_remember_image_folder_path = None
        ## self.new_var_remember_image_zip_path    = None
        ## self.new_var_remember_image_zip_object  = None
        
        number_index = self.new_ui_image_chooser.current()
        
        
        image_type = image_types[number_index]
        
        #
        self.new_var_remember_image_type = image_type
    
    # 接收信号 # 不用这个了
    def new_func_bindings_receive_virtual_event(self,event):
        #print(" ")
        print("  virtual event received,")
        #print(self.new_var_ui_type)
        
        #widget  = event.widget
        #item_id = widget.new_var_data_for_CurrentGame
        item_id = global_variable.current_item
        
        if self.new_ui_image_area.winfo_viewable():
            if self.new_var_zip_flag.get():
                self.new_func_show_image_from_zip(item_id)
            else:
                self.new_func_show_image_from_folder(item_id)
    
    # 用这个
    def new_func_show(self,item_id):
        if item_id != global_variable.current_item : return 
        
        if item_id is None:
            #self.new_ui_image_area.new_func_use_backup_image()
            return
        
        if self.new_ui_image_area.winfo_viewable():
            if self.new_var_zip_flag.get():
                self.new_func_show_image_from_zip(item_id)
            else:
                self.new_func_show_image_from_folder(item_id)
    
    def new_func_get_image_folder_path(self,):
        n = self.new_ui_image_chooser.current() # 序号 0，1，2，3，……
        
        #image_types
        
        # temp 最后为 配置文件记录 的 ，压缩包的 路径
        
        temp = image_types[n] # 图片种类 snap,titles,flyers……        

        temp = temp + "_path" # 匹配，配置文件中的名字
        
        temp = global_variable.user_configure_data[temp] # 从配置文件中，读取路径
        
        #print(temp)
        return temp.replace(r'"',"") # 去掉双引号
    
    def new_func_get_image_file_path(self,game_name,folder_path):
        
        file_path = ''
        
        file_name = self.new_func_get_image_name(game_name)
        #print(file_name)
        
        for x in folder_path.split(';') :
            file_path_to_check = os.path.join(x, file_name)
            if os.path.isfile(file_path_to_check):
                file_path=file_path_to_check
                break
        
        return file_path

    def new_func_show_image_from_folder(self,game_name):
        
        folder_path = self.new_func_get_image_folder_path()
        
        file_path = self.new_func_get_image_file_path(game_name,folder_path)
        
        if not file_path:
            
            # 如果没有
            # 再，搜索一下，主版本
            if game_name in global_variable.dict_data['clone_to_parent']:
                parent_name = global_variable.dict_data['clone_to_parent'][game_name]
                file_path = self.new_func_get_image_file_path(parent_name,folder_path)
        
        if file_path:
            aspect_ratio = self.new_func_get_image_aspect_ratio()
            self.new_ui_image_area.new_func_set_new_image_from_file(file_path,aspect_ratio)
        else:
            self.new_ui_image_area.new_func_use_backup_image()

    def new_func_show_image_from_zip_but_search_file_fisrt(self,game_name,folder_path):
        
        file_path = self.new_func_get_image_file_path(game_name,folder_path)
        
        if file_path :
            #print("use file first : ",file_path)
            aspect_ratio = self.new_func_get_image_aspect_ratio()
            self.new_ui_image_area.new_func_set_new_image_from_file(file_path,aspect_ratio)
            return True
        
    def new_func_show_image_from_zip(self,game_name):
        
        search_file = global_variable.user_configure_data["extra_image_search_file_first"]
        
        # 优先搜索 普通文件
        if search_file:
            
            folder_path=self.new_func_get_image_folder_path() ##
            
            if self.new_func_show_image_from_zip_but_search_file_fisrt(game_name,folder_path):
                return
        
        # 然后搜索 .zip 中的文件
        
        #self.new_var_remember_image_zip_path    = None
            # 打开的 zip 文件路径
        #self.new_var_remember_image_zip_object  = None
            # 打开的 zip 
        
        def get_zip_file_path():
            n = self.new_ui_image_chooser.current() # 序号 0，1，2，3，……
            
            # image_types[n] ,图片种类 snap,titles,flyers……
            
            temp = image_types[n] + r".zip_path" # 匹配，配置文件中的名字
            
            temp = global_variable.user_configure_data[temp] # 从配置文件中，读取路径
            
            return temp.replace(r'"',"") # 去掉双引号
        
        def close_zip_file():
            try:
                self.new_var_remember_image_zip_object.close()
                self.new_var_remember_image_zip_object = None
                self.new_var_remember_image_zip_path = None
                print("close zip")
            except:
                self.new_var_remember_image_zip_object = None
                self.new_var_remember_image_zip_path = None
        
        def open_zip_file(zip_file_path):
            try:
                self.new_var_remember_image_zip_path = zip_file_path
                self.new_var_remember_image_zip_object = zipfile.ZipFile( self.new_var_remember_image_zip_path , mode='r',  allowZip64=True,)
                print("open zip :",zip_file_path)
            except:
                self.new_var_remember_image_zip_object = None 
                self.new_var_remember_image_zip_path = None
        
        
        # temp 最后为 配置文件记录 的 ，压缩包的 路径
        temp = get_zip_file_path()
        #print(temp)
        
        # 如果 zip 压缩包，不存在
        if not os.path.isfile(temp):
            #print("file not exist : ",temp)
            
            # 如果 zip 压缩包，不存在
            #   之前已搜过 普通文件本身
            #   再，搜索一下，普通文件 的主版本
            if search_file:
                if game_name in global_variable.dict_data['clone_to_parent']:
                    parent_name = global_variable.dict_data['clone_to_parent'][game_name]
                    if self.new_func_show_image_from_zip_but_search_file_fisrt(parent_name,folder_path):
                        return
            
            # 如果 zip 压缩包，不存在
            #   关闭已经打开的压缩包
            if self.new_var_remember_image_zip_object is not None:
                close_zip_file()
            
            # 使用 默认 图片
            self.new_ui_image_area.new_func_use_backup_image()
            
            return
        
        # zip 压缩包文件,存在，则打开压缩包
            # 还没有打开压缩包时
        if self.new_var_remember_image_zip_path is None:
            open_zip_file(temp)
        
        # zip 压缩包文件,存在，则打开压缩包
            # 已经打开压缩包
            # 但,打开的是别的文件，
            # 比如，切换不同类型图片时；比如，重新设置 zip 路径时
        elif self.new_var_remember_image_zip_path != temp :
            
            #关闭 旧 zip 文件
            close_zip_file()
            
            #打开 新 zip 文件
            open_zip_file( temp )
        
        # 图片名称，如 kof97.png
        file_name = self.new_func_get_image_name_for_zip(game_name)
        
        image = None
        
        if self.new_var_remember_image_zip_path is not None:
            
            if game_name != global_variable.current_item : return 
            
            try:
                with self.new_var_remember_image_zip_object.open(file_name, mode='r', ) as image_data:
                    image = Image.open(image_data, mode='r',)
                    image.load()
            except:
                image = None
            
            
            if game_name != global_variable.current_item : return 
            
            if image is None:
                # 如果，本身没有找到，找一下主版本
                # self.data['dict_data']['clone_to_parent'][]
                
                if game_name in global_variable.dict_data['clone_to_parent']:
                    #print("try parent")
                
                    parent_name = global_variable.dict_data['clone_to_parent'][game_name]
                    
                    # 优先搜索 普通文件
                    if search_file:
                        if self.new_func_show_image_from_zip_but_search_file_fisrt(parent_name,folder_path):
                            return
                    
                    #parent_file_name = parent_name + ext
                    parent_file_name = self.new_func_get_image_name_for_zip(parent_name)
                    
                    try:
                        with self.new_var_remember_image_zip_object.open(parent_file_name, mode='r', ) as image_data:
                            image = Image.open(image_data, mode='r',)
                            image.load()

                    except:
                        image = None
                else: # 本身是主版本，pass
                    pass

        if game_name != global_variable.current_item : return 
        
        if image is None :
            self.new_ui_image_area.new_func_use_backup_image()
        else:
            aspect_ratio = self.new_func_get_image_aspect_ratio()
            self.new_ui_image_area.new_func_set_new_image(image,aspect_ratio)

    # for files in floder
    def new_func_get_image_name(self,item_id):
        if global_variable.gamelist_type == "softwarelist":
            folder = item_id.split(" ")[0]
            name = item_id[len(folder)+1:]
            return os.path.join(folder,name+ r".png")
        else:
            return item_id + r".png"
    # for files in zip
    def new_func_get_image_name_for_zip(self,item_id):
        if global_variable.gamelist_type == "softwarelist":
            folder = item_id.split(" ")[0]
            name = item_id[len(folder)+1:]
            #print(folder + "/" + name+ r".png")
            return folder + "/" + name+ r".png"
        else:
            return item_id + r".png"
    
    def new_func_get_image_aspect_ratio(self,):
        # None ：原始比例
        # (4,3)：   4:3 或 3:4
        # 4/3 ：    4:3 ，目前未使用
        if global_variable.user_configure_data["extra_image_keep_aspect_ratio"]:
            if global_variable.current_item in global_variable.set_extra_image_keep_aspect_ratio:
                return 4,3
        return None
    
class Image_container_2(Image_container):
    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "extra_image_2"

    def new_func_initialize(self,):
    
        self.new_var_zip_flag.set( global_variable.user_configure_data["extra_image_usezip_2"] )
        global_variable.tkint_flag_for_zip_2 = self.new_var_zip_flag
        
        global_variable.Combobox_chooser_image_2 = self.new_ui_image_chooser
        
        temp=[]
        for x in image_types:
            if x in key_word_translation:
                temp.append(key_word_translation[x])
            else:
                temp.append(x)
        self.new_ui_image_chooser["values"]= temp
        
        try: # 读取配置文件中 记录的 index
            n = global_variable.user_configure_data["extra_image_chooser_2_index"] 
            if n < len(image_types):
                pass
            else:
                n=0
            self.new_ui_image_chooser.set( temp[n] )
        except:
            self.new_ui_image_chooser.set( temp[0] )
        
        self.new_func_get_info_from_choice()# 初始数据读取
    
    def new_func_get_image_aspect_ratio(self,):
        if global_variable.user_configure_data["extra_image_keep_aspect_ratio_2"]:
            if global_variable.current_item in global_variable.set_extra_image_keep_aspect_ratio:
                return 4,3
        return None

if __name__ == "__main__" :
    root=tk.Tk()
    root.title("test")
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.rowconfigure(1,weight=0)
    root.columnconfigure(0,weight=1)

    
    #the_files.image_path_image_no="knights.png"
    
    #c = Image_container(root)
    c = Image_container(root)
    c.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    def change():
        
        c.new_func_set_new_image_from_file("knights.png")
    
    b=tk.Button(root,text="测试，插入图片",command=change)
    b.grid(row=1,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    def show_info():
        number = len( c.new_ui_image.new_ui_canvas.find_all() )
        print("items number is  : {}  ".format(number))
    
    b2=tk.Button(root,text="测试，显示数量",command=show_info)
    b2.grid(row=2,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
    
    root.mainloop()    








