# -*- coding: utf_8_sig-*-
#import sys
import os
import sys

import tkinter as tk
from tkinter import ttk

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

from . import global_variable
from . import global_static_filepath as the_files

#from .ui_misc import  misc_funcs

themes_dir = the_files.folder_themes
ini_data       = global_variable.user_configure_data
user_configure = global_variable.user_configure_data


def main(root,style):
    print()
    print("theme in user configure file : {}".format(ini_data["theme"]))


    internal_themes = style.theme_names()
    
    # 记录
    global_variable.internal_themes = internal_themes
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


    # 记录
    global_variable.other_themes = other_themes

    #######
    use_theme_flag = True
    #use_theme_flag = False

    use_background=False # 内置主题时，使用一下

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
    print("using theme : {}".format(style.theme_use()))
    print()
    #for x in style.theme_names():
    #    if x not in internal_themes:
    #        print(x)

    

    
    
