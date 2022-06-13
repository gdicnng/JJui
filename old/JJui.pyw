# -*- coding: utf_8_sig-*-
import sys
import os
import time

import subprocess
import threading

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

import pickle

from jjui.ui import MyUi
import jjui.initial_parse_xml
import jjui.initial_translation

#from jjui import folders_read
#from jjui import folders_search
#from jjui import ui_configure_file
from jjui.save_pickle import save as save_pickle
from jjui.read_pickle import read as read_pickle

time1 = time.time()

print()
print(1)
print("查看当前目录")
print("os.getcwd()")
print(os.getcwd())

# 切换到 脚本 目录
#   如果，打包为 exe ，那么此处需要另外处理
#the_script_path = os.path.dirname(__file__)
#os.chdir( the_script_path )

# cx_Freeze 打包
# pyinstall 打包
if getattr(sys, "frozen", False):
    # The application is frozen
    executable_path = os.path.dirname(sys.executable)
    executable_path = os.path.abspath(executable_path)
    os.chdir( executable_path )
else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    the_script_path = os.path.dirname(__file__)
    the_script_path = os.path.abspath(the_script_path)
    os.chdir( the_script_path )    


print()
print(2)
print("切换目录之后，查看当前目录")
print("os.getcwd()")
print(os.getcwd())


print()
print("sys.executable")
print(sys.executable)

print()
print("sys.argv[0]") # 以脚本运行，此项为脚本路径
print(sys.argv[0])


# bug fix
# Treeview 颜色 bug ，版本 tkinter 8.6.9
def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
      elm[:2] != ('!disabled', '!selected')]


##
##
from jjui.datas import *
    # 导入 主函数中的，需要用的，乱七八糟 的 python 数据
    # 因为，全写在主函数中，看起来太累了


root=tk.Tk()

print()
print('tk', 'scaling', )
tk_scaling_number_0 = root.tk.call('tk', 'scaling', )
print( tk_scaling_number_0 )

if ini_data["tk_scaling_use_flag"]:
    if ini_data["tk_scaling_number"] > 0.01:
            try:
                root.tk.call('tk', 'scaling', ini_data["tk_scaling_number"])
            except:
                pass

print(root.tk.call('tk', 'scaling', ))

# 窗口大小
if ini_data["size"] != "" :
    try:
        root.geometry( ini_data["size"] )
    except:
        pass

root.update() 
# 设置窗口大小以后，update 一下，不然 之后，root.geometry() 得到的高度要小一点
# why ???

style = ttk.Style()

internal_themes = style.theme_names()
#print()
#print( internal_themes )

##

themes_to_delete=set()
#themes_to_delete.add("breeze")# Treeview 背景色，不全
#themes_to_delete.add("Breeze")# Treeview 背景色，不全

other_themes=set()
other_themes.add("breeze")
other_themes.add("breeze-dark")
other_themes.add("Breeze")
other_themes.add("azure")
other_themes.add("azure-dark")

ttkthemes_names = ("aquativo","black","blue","clearlooks","elegance","itft1","keramik","keramik_alt","kroc","plastik","radiance","smog","winxpblue")
other_themes.update( set(ttkthemes_names) )

awthemes_names = ("awdark","awlight",) + ("awarc","awblack","awbreeze","awbreezedark","awclearlooks","awwinxpblue",) 
other_themes.update( set(awthemes_names) )

scid_themes_names = ("scidsand","scidblue","scidmint","scidgreen","scidpink","scidgrey","scidpurple",)
other_themes.update( set(scid_themes_names) )

other_themes =  other_themes - themes_to_delete

##

use_theme_flag = True
#use_theme_flag = False

use_background=False # 内置主题时，使用一下

##

themes_dir = os.path.join(os.curdir,".jjui","themes")

if use_theme_flag:
    if ini_data["theme"] in internal_themes:
        style.theme_use( ini_data["theme"] )
        use_background=True
    
    elif ini_data["theme"] in other_themes :

        # 零散的
        if ini_data["theme"] in ("breeze","breeze-dark","Breeze","azure","azure-dark",):
            if ini_data["theme"]  == "breeze-dark": # 分隔条，太亮了
                #file_path=r'.\.jjui\themes\tkBreeze\breeze-dark\breeze-dark.tcl'
                file_path=os.path.join(themes_dir,"tkBreeze",'breeze-dark','breeze-dark.tcl')
            
            elif ini_data["theme"] == "azure-dark":  
                #file_path=r'.\.jjui\themes\Azure-ttk-theme\azure-dark.tcl'
                file_path=os.path.join(themes_dir,"Azure-ttk-theme",'azure-dark.tcl')
            
            elif ini_data["theme"] == "azure":
                #file_path=r'.\.jjui\themes\Azure-ttk-theme\azure.tcl'
                file_path=os.path.join(themes_dir,"Azure-ttk-theme",'azure.tcl')
            
            # 删
            elif ini_data["theme"] == "breeze":  
                #file_path=r'.\.jjui\themes\tkBreeze\breeze\breeze.tcl'
                file_path=os.path.join(themes_dir,"tkBreeze",'breeze','breeze.tcl')
                # Treeview fieldbackground 没有效果
            
            # 删
            elif ini_data["theme"] == "Breeze": 
                #file_path=r'.\.jjui\themes\ttk-Breeze\breeze.tcl'
                file_path=os.path.join(themes_dir,"ttk-Breeze",'breeze.tcl')
                # Treeview fieldbackground 没有效果
                
            else:
                pass
                
                
            if os.path.isfile( file_path ):
                root.tk.call('source',file_path)
                style.theme_use( ini_data["theme"] )
            
                # 背景色，补
                background_colour = style.lookup(".","background")
                print("background")
                print(background_colour)
                foreground_colour  = style.lookup(".","foreground")
                print("foreground")
                print(foreground_colour)

                if ini_data["theme"] in ( "breeze" ,"Breeze",):
                    style.configure('Treeview', background =background_colour)
                    style.configure('Treeview', fieldbackground=background_colour)
            
        # ttkthemes
        # 进度条，中心不管用：elegance
        # Treeview 选中颜色太浅：itft1 、smog
        elif ini_data["theme"] in ("aquativo","black","blue","clearlooks","elegance","itft1","keramik","keramik_alt","kroc","plastik","radiance","smog","winxpblue"):
            if ini_data["theme"] == "black":
                #file_path=r'.\.jjui\themes\ttkthemes\black\black.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'black','black.tcl')
            elif ini_data["theme"] == "blue":    
                #file_path=r'.\.jjui\themes\ttkthemes\blue\blue.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'blue','blue.tcl')
            elif ini_data["theme"] == "clearlooks": 
                #file_path=r'.\.jjui\themes\ttkthemes\clearlooks\clearlooks.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'clearlooks','clearlooks.tcl')
            elif ini_data["theme"] == "elegance": # scrollbar 中心不灵
                #file_path=r'.\.jjui\themes\ttkthemes\elegance\elegance.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'elegance','elegance.tcl')
            elif ini_data["theme"] == "itft1": # Treeveiew 选中颜色，实在太浅，看不清
                #file_path=r'.\.jjui\themes\ttkthemes\itft1\itft1.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'itft1','itft1.tcl')
            elif ini_data["theme"] in ( "keramik" ,"keramik_alt"):
                #file_path=r'.\.jjui\themes\ttkthemes\keramik\keramik.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'keramik','keramik.tcl')
            elif ini_data["theme"] == "kroc":
                #file_path=r'.\.jjui\themes\ttkthemes\kroc\kroc.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'kroc','kroc.tcl')
            elif ini_data["theme"] == "plastik":        
                #file_path=r'.\.jjui\themes\ttkthemes\plastik\plastik.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'plastik','plastik.tcl')
            elif ini_data["theme"] == "radiance":
                #file_path=r'.\.jjui\themes\ttkthemes\radiance\radiance.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'radiance','radiance.tcl')
            elif ini_data["theme"] == "smog":# Treeveiew 选中颜色，实在太浅，看不清
                #file_path=r'.\.jjui\themes\ttkthemes\smog\smog.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'smog','smog.tcl')
            elif ini_data["theme"] == "winxpblue":
                #file_path=r'.\.jjui\themes\ttkthemes\winxpblue\winxpblue.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'winxpblue','winxpblue.tcl')
            elif ini_data["theme"] == "aquativo":
                #file_path=r'.\.jjui\themes\ttkthemes\aquativo\aquativo.tcl'
                file_path=os.path.join(themes_dir,"ttkthemes",'aquativo','aquativo.tcl')
            else:
                pass
            
            if os.path.isfile( file_path ):
                root.tk.call('source',file_path)
                style.theme_use( ini_data["theme"] )
            
                # 背景色，补
                background_colour  = style.lookup(".","background")
                foreground_colour  = style.lookup(".","foreground")
                style.configure('Treeview', fieldbackground=background_colour)
                root.option_add('*Text*background', background_colour)
                root.option_add('*Canvas*background', background_colour)
                
                if ini_data["theme"] == "black":
                    style.configure('TEntry', fieldbackground="grey90") 
                    style.configure('TCombobox', fieldbackground ="grey90")
                    root.option_add('*Text*foreground', "#ffffff")
                elif ini_data["theme"] in ( "keramik" ,"keramik_alt","plastik"):
                    style.configure('Treeview', background =background_colour)
                    style.configure('Treeview', fieldbackground=background_colour)
                elif ini_data["theme"] == "kroc":
                    style.configure('TEntry', fieldbackground="#FFE6BA") 
                    style.configure('TCombobox', fieldbackground ="#FFE6BA")
                elif ini_data["theme"] == "itft1": # 修复 Treeview 选中颜色，颜色太浅
                    #style.configure('Treeview', background = background_colour)
                    style.map('Treeview', background = [("selected","#3c9bf7"),("focus","#ccccff"),("alternate","#FFFFFF")])
                elif ini_data["theme"] == "smog": # 修复 Treeview 选中颜色，颜色太浅
                    #style.configure('Treeview', background = background_colour)
                    style.map('Treeview', background = [("selected","#3c9bf7"),("focus","#ccccff"),("alternate","#FFFFFF")])
                    #style.map('Heading', background  = [("active","yellow"),])
        
        # scid_themes
        elif ini_data["theme"] in ("scidsand","scidblue","scidmint","scidgreen","scidpink","scidgrey","scidpurple",):
            #file_path=r'.\.jjui\themes\scidthemes\scidthemes.tcl'
            file_path=os.path.join(themes_dir,"scidthemes",'scidthemes.tcl')
            
            if os.path.isfile( file_path ):
                root.tk.call('source',file_path)
                style.theme_use( ini_data["theme"] )
                # 背景色，补
                background_colour  = style.lookup(".","background")
                foreground_colour  = style.lookup(".","foreground")
                style.configure('Treeview', background=background_colour)
                style.configure('Treeview', fieldbackground=background_colour)
                root.option_add('*Text*background', background_colour)
                root.option_add('*Canvas*background', background_colour)


        # aw
        # 总列表，数量多，进度条 不好抓取的主题：
        #   awblack awdark awlight  awwinxpblue
        elif ini_data["theme"] in ("awarc","awblack","awbreeze","awbreezedark","awclearlooks","awwinxpblue",) :# aw scalable 
            #folder_path = r'.\.jjui\themes\awthemes'
            folder_path = os.path.join(themes_dir,"awthemes")
            if os.path.isdir( folder_path ):
                root.tk.call('lappend', 'auto_path', folder_path)
                root.tk.call('package', 'require', ini_data["theme"] ,)
                style.theme_use( ini_data["theme"] )
                
                background_colour  = style.lookup(".","background")
                foreground_colour  = style.lookup(".","foreground")
                
                if background_colour != "" : 
                    root.option_add('*Text*background', background_colour)
                    root.option_add('*Canvas*background', background_colour)
                if foreground_colour  != "" : 
                    root.option_add('*Text*foreground',  foreground_colour)
            
        elif ini_data["theme"] in ("awdark","awlight",) :# aw
            #folder_path = r'.\.jjui\themes\awthemes'
            folder_path = os.path.join(themes_dir,"awthemes")
            if os.path.isdir( folder_path ):
                root.tk.call('lappend', 'auto_path', folder_path)
                root.tk.call('package', 'require', ini_data["theme"] )
                style.theme_use( ini_data["theme"] )
                
                background_colour  = style.lookup(".","background")
                foreground_colour  = style.lookup(".","foreground")
                
                if background_colour != "" : 
                    root.option_add('*Text*background', background_colour)
                    root.option_add('*Canvas*background', background_colour)
                if foreground_colour  != "" : 
                    root.option_add('*Text*foreground',  foreground_colour)

    else:
        try:
            style.theme_use( "clam" )
            use_background=True
            ini_data["theme"]=""#重置
        except:
            pass

change_theme_flag = True
#change_theme_flag = False

# Treeview 列表，在选中时，会有一个框框，很难看，
if change_theme_flag :
    if style.theme_use() in internal_themes + ("aquativo","black","blue","clearlooks","elegance","itft1","keramik_alt","keramik","plastik","radiance","scidsand","scidblue","scidmint","scidgreen","scidpink","scidgrey","scidpurple","smog","winxpblue",):
        style.layout("Item",[('Treeitem.padding', {'sticky': 'nswe', 'children': [('Treeitem.indicator', {'side': 'left', 'sticky': ''}), ('Treeitem.image', {'side': 'left', 'sticky': ''}), ('Treeitem.text', {'side': 'left', 'sticky': ''})]})])

# ttk.Scrollbar ，有几个主题，中心处，有图片，不灵
# 对比，两个主题发现，style.layout ，'Horizontal.Scrollbar.thumb' 元素 添加 'unit':'1' 这一项即可，虽然不懂为啥
if change_theme_flag :
    if style.theme_use() in ("elegance","awblack","awdark","awlight","awwinxpblue"):
    
        v = style.layout("Vertical.TScrollbar")
        h = style.layout("Horizontal.TScrollbar")
        
        # 数据
        # >>> s.layout("Vertical.TScrollbar")
        # [('Scrollbar.background', {'sticky': 'nswe'}), ('Vertical.Scrollbar.trough', {'sticky': 'nswe', 'children': [('Scrollbar.uparrow', {'side': 'top', 'sticky': ''}), ('Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}), ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'ns', 'children': [('Vertical.Scrollbar.grip', {'sticky': ''})]})]})]
        

        # Vertical
        temp = []
        for x in v :
            if x[0]=='Vertical.Scrollbar.trough':
                
                y=x[1] # 一个 dict 类型
                
                if 'children' in y :
                
                    # y['children'] # list 型
                    
                    # [('Scrollbar.uparrow', {'side': 'top', 'sticky': ''}), ('Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}), ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'ns', 'children': [('Vertical.Scrollbar.grip', {'sticky': ''})]})]})]
                    
                    for z in y['children']:
                        if z[0] == 'Vertical.Scrollbar.thumb':
                            if 'children' in z[1]:
                                #print(z[1])
                                z[1]['unit'] = '1'
                temp.append(x)
                
            else:
                temp.append(x)
        style.layout("Vertical.TScrollbar",temp)
        print()
        print(style.layout("Vertical.TScrollbar"))
        
        # Horizontal
        temp = []
        for x in h :
            if x[0]=='Horizontal.Scrollbar.trough':
                
                y=x[1] # 一个 dict 类型
                
                if 'children' in y :
                
                    
                    for z in y['children']:
                        if z[0] == 'Horizontal.Scrollbar.thumb':
                            if 'children' in z[1]:
                                #print(z[1])
                                z[1]['unit'] = '1'
                temp.append(x)
                
            else:
                temp.append(x)
        style.layout("Horizontal.TScrollbar",temp)
        print()
        print(style.layout("Horizontal.TScrollbar"))        
        
        del temp
        del v
        del h
    
# aw themes 的 Treeview ，标题都没有边框，大多看不清边界
    # 但自己设置 边框的话，似乎有点难看了
# 其它主题 ， "azure" "azure-dark" "blue"
# awlight 、awclearlooks 高亮色、背景色 差距还比较大，清楚一点。
if change_theme_flag :
    if style.theme_use() in ("awarc","awblack","awbreeze",
                    "awbreezedark",
                    #"awclearlooks",
                    "awwinxpblue",
                    #"awdark",
                    #"awlight",
                    "azure",
                    "azure-dark",
                    "blue",
                    ):
        if style.theme_use() in  ("awwinxpblue","awbreeze",):
            #selectbackground = style.configure(".","selectbackground")
            selectforeground = style.configure(".","selectforeground")
            style.map("Treeview.Heading",background=[('active',selectforeground),]  )
        elif style.theme_use() in  ("awarc","awbreezedark",):
            selectbackground = style.configure(".","selectbackground")
            #selectforeground = style.configure(".","selectforeground")
            style.map("Treeview.Heading",background=[('active',selectbackground),]  )
        else:
            # "azure" "azure-dark" "blue"
            #style.configure("Heading",relief="raised",) #
            #style.configure("Heading",relief="sunken",)
            #style.configure("Heading",relief="flat",)
            style.configure("Treeview.Heading",relief="ridge",) #
            #style.configure("Heading",relief="solid",) 
            #style.configure("Heading",relief="groove",) 
            

# Toplevel 背景色
if change_theme_flag :
    if style.theme_use() in other_themes:# 第三方主题
    
        background_colour  = style.lookup(".","background")
        #foreground_colour  = style.lookup(".","foreground")
        
        if background_colour != "" : 
            root.option_add('*Toplevel*background', background_colour)


###
###

###

#file_path=r'.\.jjui\themes\tkBreeze\breeze\breeze.tcl'
#root.tk.call('source',file_path)
#style.theme_use( "breeze" )
#
#background_colour = style.lookup(".","background")
#print("background")
#print(background_colour)
#foreground_colour  = style.lookup(".","foreground")
#print("foreground")
#print(foreground_colour)
#
#style.configure('Treeview', background =background_colour)
#style.configure('Treeview', fieldbackground=background_colour)
#style.configure('Item', fieldbackground=background_colour)


#
print()
print(style.theme_use())
print()
for x in style.theme_names():
    if x not in internal_themes:
        print(x)


# bug fix
# Treeview 颜色 bug ，版本 tkinter 8.6.9
if root.tk.call('info', 'patchlevel')=="8.6.9":
    print("8.6.9")
    style.map('Treeview', 
                foreground=fixed_map('foreground'),
                background=fixed_map('background'))  
# 放在 style.theme_use("xxxxxx") 后面 ，才有用
# ？？？？？               

# 题标
# data 在之后 读取
# 之后，再改一次名，加入版本信息
str_title = r"JJui 街机游戏列表显示器 v.1.0.test  ----  "
root.title( str_title )

# 图标
try:
    root.iconphoto(False, tk.PhotoImage(file= image_path_icon_for_jjui ) )
except:
    pass


data_pass_to_ui =   {   "columns"             : columns ,
                        "columns_translation" : columns_translation ,
                        "index_translation"   : index_translation ,
                        "index_order"         : index_order ,

                        "internal_themes"     : internal_themes ,
                        "other_themes"        : other_themes ,
                        "tk_scaling_number_0" : tk_scaling_number_0 ,
                        
                        # .jjui.ini
                        "ini_default"         : ini_default ,
                        "ini_data"            : ini_data    ,
                        "ini_path"            : ini_file    ,
                        "ini_order"           : ini_order   , # 保存顺序，旧版本需要


                        "translation_file_name"   : translation_file_name,
                        
                        # .\.jjui\cache_data_1.bin
                        "temp_file_name"               :temp_file_name,
                        
                        # .\.jjui\cache_data_2_gamelist.bin
                        "temp_file_name_gamelist" :temp_file_name_gamelist,
                        
                        # .\.jjui\cache_available.bin
                        "temp_file_name_available" :temp_file_name_available,
                        
                        'available_hide_file':available_hide_file,
                        
                        'docs_html_index_file':docs_html_index_file,
                        
                        'image_path_icon_for_jjui':image_path_icon_for_jjui ,
                        'image_path_no_image'     :image_path_no_image      ,
                        'image_path_icon_black'   :image_path_icon_black    ,
                        'image_path_icon_red'     :image_path_icon_red      ,
                        'image_path_icon_yellow'  :image_path_icon_yellow   ,
                        'image_path_icon_green'   :image_path_icon_green    ,
                        'image_path_zhifubao'     :image_path_zhifubao      ,
                        'image_path_weixin'       :image_path_weixin        ,
                        
                        'export_text_file':export_text_file,
}

# ui
ui = MyUi(  root ,
            #ini_data = ini_data ,
            #ini_path=ini_file , 
            data_from_main = data_pass_to_ui,
            ttk_style = style )#

root.update() 


# 数据文件1：
#   dict_keys(['mame_version', 'set_data', 'dict_data'])
# temp_file_name = r".\.jjui\data_1.bin"
# 存在 标记
if os.path.isfile(temp_file_name):   
    temp_file_flag_1 = True
else:  
    temp_file_flag_1 = False 

# 数据文件2：
#   游戏列表
# temp_file_name_gamelist =  r".\.jjui\data_2_gamelist.bin" 
# 存在 标记 
if os.path.isfile(temp_file_name_gamelist): 
    temp_file_flag_2 = True
else: 
    temp_file_flag_2 = False 
    
temp_file_flag = temp_file_flag_1 and temp_file_flag_2


def start_ui():
   
    # ui ,
    # 数据1，读取 data 数据
    ui.ui_initial_functions_read_data()
    
    # ui ,图片 ，读取
    #   加载游戏列表时，用的 红黄绿 小图标
    ui.ui_initial_functions_read_image()     
    
    # # # # # # # # # # # #
    
    # 一些变量初始化： 
    ui.ui_initial_functions_variable_initial()

    # 字体
    ui.ui_initial_functions_font_init()

    # 背景色
    if use_background:
        ui.ui_initial_functions_background()    
    
    # ui 游戏列表，初始化
    #   需要从文件读取数据 ： temp_file_name_gamelist
    ui.ui_initial_functions_gamelist_initial()
    
    root.update() 
    
    # 目录
    # 目录，内部目录，初始化
    ui.ui_initial_functions_index_content_internal()
    #root.update() 

    # 目录，外部 目录 ，初始化
    # 读取 分类 文件
    ui.ui_initial_functions_index_content_external( )
    #root.update() 
    
    # 上次打开的目录
    temp_iid = ini_data["index_be_chosen"]
    
    flag = False # 
    # 检查，上次记录的目录，这一次，还在不在？
    for x in ui.tree_index.get_children():
        if temp_iid == x:
            flag = True
            break
        for y in ui.tree_index.get_children(x):
            if temp_iid == y:
                flag = True
                break
        if flag: 
            break
    
    if flag : # 有效 iid
        
        ui.tree_index.see( temp_iid )
        
        ui.tree_index.selection_set( (temp_iid,) )
            #ui.tree_index.selection_set( temp_iid )# 这种写法 3.4.4 bug
            #ui.tree_index.selection("set", (temp_iid,) )# 这样写 3.9 又不行了        
            # python 3.4.4 ,selection_set,这里出问题了,应该是 bug ,id 名字有空格？其它符号?
            # https://bugs.python.org/issue26386
        
        ui.tree_index.focus( temp_iid ) 
        
        ui.ini_data["index_be_chosen"]="" # 重置 ，才不影响下面的函数
        ui.choose_index( temp_iid )

    else: # 无效 iid ，数据出错
        # 默认设为 'all_set'

        ui.tree_index.see( 'all_set' )
        ui.tree_index.selection_set('all_set')
        ui.tree_index.focus('all_set')
        
        ui.choose_index( 'all_set' )
        
    del flag
    del temp_iid
    
    # 目录、周边 宽度
    
    ui.ui_initial_functions_ui_width_initial()
    ui.ui_initial_functions_ui_extra_show_the_remembered_part()
    #root.update()
    ui.other_functions_show_mame_help()
    
    time2 =time.time()
    print()
    print("时间统计")
    print(time2 -time1)
    print()
    
if temp_file_flag :
    start_ui()
 
else:
    def ini_window(root,ini_data):
        # start_ui()
        
        
        root.withdraw()
        
        # 建一个 toplevel 窗口
        # 提示，从 mame 读取数据
        temp_window = tk.Toplevel()
        temp_window.title("初始化")
        
        temp_window_var = tk.StringVar()
        temp_window_var_2 = tk.StringVar()
            # w.wait_variable(v)
                # Waits until the value of variable v is set, even if the value does not change. This method enters a local wait loop, so it does not block the rest of the application.
        
        after_remember = None
        after_remember_2 = None
        
        def exit_for_temp_window():
        
            if after_remember :
                temp_window.after_cancel( after_remember )
                temp_window_var.set("quit")
            
            if after_remember_2 :
                temp_window.after_cancel( after_remember_2 )
                temp_window_var_2.set("quit") 
            
            temp_window.destroy()
            root.deiconify()
            root.destroy()
            #sys.exit()
            
        def change_mame_path():
            entry_for_mame.configure(state="normal")
            button_choose_mame.configure(state="normal")
            
        # def progressbar_start():
        #     progressbar_temp.step(2.0)
        #     temp_window.after(250,progressbar_start)        
        
        def progressbar_xml(p):
            nonlocal after_remember
            if p.poll() != None: #停止
                print("listxml finish")
                temp_window_var.set("-listxml finish")
            else: # 没停止
                progressbar_temp.step(2.0)
                after_remember = temp_window.after(500,progressbar_xml,p,)

        def progressbar_xml_parse(thread):
            nonlocal after_remember_2
            if thread.is_alive(): #运行
                progressbar_temp.step(2.0)
                after_remember_2 = temp_window.after(500,progressbar_xml_parse,thread)
            else: # 停止
                print("mame xml parse finish")
                temp_window_var_2.set("mame xml parse finish")


        def ok_button_for_temp_window():
            button_temp.configure(state="disable")
            entry_for_mame.configure(state="disable")
            button_change_temp.configure(state="disable")
            button_choose_mame.configure(state="disable")
            
            print(mame_path.get())
            #ini_data["mame_path"] = mame_path.get()
            
            # xml_file =                 r'.\.jjui\roms.xml' 
            # temp_file_name = r".\.jjui\data_1.bin"
            # temp_file_name_gamelist =  r".\.jjui\data_2_gamelist.bin" # 游戏列表 数据
            # temp_file_name_available = r".\.jjui\available.bin" # 拥有列表 数据
            # translation_file_name =    r".\.jjui\translation.txt"
            # temp_folders = r'.\.jjui'
            
            log_temp.configure(text="清理文件")
            
            if os.path.exists(xml_file):
                try:
                    os.remove(xml_file)
                except:
                    log_temp.configure(text="无法删除文件："+xml_file)
                    return 0        
            
            if os.path.exists(temp_file_name):
                try:
                    os.remove(temp_file_name)
                except:
                    log_temp.configure(text="无法删除文件："+temp_file_name)
                    return 0
                    
            if os.path.exists(temp_file_name_gamelist):
                try:
                    os.remove(temp_file_name_gamelist)
                except:
                    log_temp.configure(text="无法删除文件："+temp_file_name_gamelist)
                    return 0

            if os.path.exists(temp_file_name_available):
                try:
                    os.remove(temp_file_name_available)
                except:
                    log_temp.configure(text="无法删除文件："+temp_file_name_available)
                    return 0
            
            # 1, 导出 xml
            print("1,导出 xml")
            
            log_temp.configure(text="导出 xml 信息到文件: " + xml_file)
            
            file = open(xml_file, 'wb')
            
            # full_mame_path = os.path.abspath( mame_path.get() )
            # p=subprocess.Popen( args = [full_mame_path,"-listxml",] ,shell=True, stdout = file )
            
            p=subprocess.Popen( args = [mame_path.get(),"-listxml",] ,
                                shell=ini_data["use_shell"], 
                                stdout = file ,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,)

            progressbar_xml(p,)
            
            temp_window.wait_variable(temp_window_var)
            
            print("file close")
            file.close()
            
            # 2, 解析 xml
            print("2,解析 xml")
            
            log_temp.configure(text="解析 xml 文件、导入翻译")
            
            def mame_xml_parse():
                
                # 解析 xml
                # jjui.initial_parse_xml
                data = {}
                try:
                    data = jjui.initial_parse_xml.read_xml( xml_file )
                except:
                    pass
                
                if len( data ) == 0:
                    #log_temp.configure(text="似乎出错了")
                    return None
                
                if "machine_dict" not in data :
                    #log_temp.configure(text="似乎出错了")
                    return None
                    
                if len( data["machine_dict"] ) == 0 : 
                    #log_temp.configure(text="似乎出错了")
                    return None
                
                # 翻译
                #  jjui.initial_translation
                translation_dict={}
                if os.path.isfile(translation_file_name):
                    try:
                        translation_dict = jjui.initial_translation.read_translation_file( translation_file_name )
                    except:
                        pass
                
                if len( translation_dict ) > 0 :
                    data["machine_dict"] = jjui.initial_translation.add_translation( translation_dict = translation_dict , gamelist_dict = data["machine_dict"] )
                
                save_pickle(data["machine_dict"],temp_file_name_gamelist)
                
                del data["machine_dict"]
                
                save_pickle(data,temp_file_name)
                
                del data
                
            thread = threading.Thread(target=mame_xml_parse)
            thread.start()
            
            progressbar_xml_parse(thread,)
            
            temp_window.wait_variable(temp_window_var_2)
            
            flag_temp = False
            # 简单校验
            if os.path.exists(temp_file_name):
                if os.path.exists(temp_file_name_gamelist):
                    flag_temp = True
                    # 如果读取信息失败的话，就没有 执行 生成 这两文件了
                    ini_data["mame_path"] = mame_path.get() # 记到配置文件
                    
                    # 删除 roms.xml
                    try:
                        os.remove(xml_file)
                    except:
                        pass
                    
                    temp_window.destroy()
                    root.deiconify()
                    start_ui()
                    root.lift()
            
            if not flag_temp:
                log_temp.configure(text="似乎出错了")
                
            
        ttk.Label(temp_window,text="").grid(row=0,column=0,columnspan=3,sticky=tk.W+tk.N)
        ttk.Label(temp_window,text="模拟器路径：").grid(row=1,column=0,sticky=tk.W+tk.N)
        
        mame_path = tk.StringVar()
        mame_path.set( ini_data["mame_path"] )
        
        entry_for_mame = ttk.Entry(temp_window,width=40,textvariable=mame_path)
        entry_for_mame.grid(row=1,column=1,sticky=tk.W+tk.N)
        entry_for_mame.configure(state="disable")
        
        button_change_temp=ttk.Button(temp_window,text="修改模拟器路径",command=change_mame_path)
        button_change_temp.grid(row=1,column=2,sticky=tk.W+tk.N)
        
        def for_choose_mame():
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[(".exe","*.exe"),("所有","*")],)
            
            if file_path=="":
                temp_window.focus_set()
                return 0
                
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            mame_path.set( file_path )
            temp_window.focus_set()                
        
        button_choose_mame = ttk.Button(temp_window,text="选择 MAME",state="disable",command=for_choose_mame)
        button_choose_mame.grid(row=1,column=3,sticky=tk.W+tk.N)
        
        
        ttk.Label(temp_window,text="初始化").grid(row=2,column=0,columnspan=4,sticky=tk.W+tk.N)
        ttk.Label(temp_window,text="从此模拟器读取数据").grid(row=3,column=0,columnspan=4,sticky=tk.W+tk.N)
        
        ttk.Label(temp_window,text="读写数据的时候，最好不要关闭程序").grid(row=4,column=0,columnspan=4,sticky=tk.W+tk.N)
        ttk.Label(temp_window,text="这时候关了主窗口，读取数据的子程序还要跑一会儿").grid(row=5,column=0,columnspan=4,sticky=tk.W+tk.N)
        
        button_temp = ttk.Button(temp_window,text="确定",command=ok_button_for_temp_window)
        button_temp.grid(row=6,column=0,columnspan=4,sticky=tk.E+tk.N)
        
        
        log_temp = ttk.Label(temp_window,text="")
        log_temp.grid(row=7,column=0,columnspan=4,sticky=tk.W+tk.N)
        
        progressbar_temp=ttk.Progressbar(temp_window,orient=tk.HORIZONTAL)
        progressbar_temp.grid(row=8,column=0,columnspan=4,sticky=tk.W+tk.N+tk.E)
        
        temp_window.protocol("WM_DELETE_WINDOW", exit_for_temp_window)
        
        temp_window.wait_window()
    
    ini_window(root=root,ini_data=ini_data)
    
size = root.geometry()
print(  )
print( "窗口大小" )
print( size )
print(  )

def exit_2():
    print("exit")
    try:
        ui.menu_call_back_function_save_ini_data()
        print("ui save")
    except:
        pass
    #sys.exit()
    print(r"root.destroy()")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", exit_2)
root.mainloop()
