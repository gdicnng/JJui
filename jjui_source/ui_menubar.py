# -*- coding: utf-8 -*-
import sys
import os
import webbrowser
import locale
import threading
import tkinter as tk
from tkinter import ttk 
import tkinter.filedialog
import tkinter.messagebox

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
from . import global_static
from . import global_static_filepath as the_files
from . import misc

# from . import read_user_config


from . import ui_small_windows

from .ui_misc import  misc_funcs
from .ui__scrollable_frame_in_cavans import Scrollable_Frame_Container

image_types   = global_static.extra_image_types
text_types    = global_static.extra_text_types
text_types_2  = global_static.extra_text_types_2

a_long_text = """
JJui:
    在 PPXCLUB 发布的贴子：
        https://www.ppxclub.com/forum.php?mod=viewthread&tid=705838
        www.ppxclub.com/705838-1-1

    源代码
        github
        https://github.com/gdicnng/JJui
    
    第三方主题：
        https://github.com/gdicnng/JJui_themes

    在线说明：
        readthedocs 的 在线文档 功能，不知道效果怎样
        网址：
        jjui.readthedocs.io
        jjui.rtfd.io

    百度网盘：
        不知道百度网盘的链接能活多久
        链接：https://pan.baidu.com/s/1guTSDIWr66S6ewIdyMQPjA 
        提取码：r9b9 

MAME 
    官网
        https://www.mamedev.org/
    源代码 
        https://github.com/mamedev/mame
    在线文档：
        https://docs.mamedev.org/
    下载页面：
        https://www.mamedev.org/release.html
        https://www.mamedev.org/oldrel.html
        https://github.com/mamedev/mame/releases/
        https://sourceforge.net/projects/mame/files/

MESS 原来的网站：
    http://mess.redump.net/
    0.162 版本以后，MAME 合并了 MESS 。
    如果你要查看 MESS 的说明，也许 原来的网站 更有针对性一点。



PPXCLUB
    https://www.ppxclub.com
    中文论坛，街机 以及 其它机种 怀旧玩家 还是有一些人的。

简体中文游戏列表： 
    https://www.ppxclub.com/609487-1-1

M+GUI 前端，1.8.2:
    https://www.ppxclub.com/669953-1-1
    这个原来是 MamePlus 上用的，后来 MamePlus 不更新了，大家直接拿到原版 MAME 上用。
    这个老长时间没有人更新一下了

MxUI 前端:
    https://www.ppxclub.com/671046-1-1

MamePlus ：
    第三方的 MAME 。
    0.168 版本 （2015年） 之后，不再更新。
    很久以前中文就支持得好，不过后来到 0.168 版本以后，没有大神去更新了。而且后期的版本，维护的大神人少，bug 可能比较多。
    如果不介意用旧版本的话，也是不错的选择。
    如果国内网站上找到的资源，一般都应该带有完整的中文语言包，当然最好自己检查一下。
    如果国外网站上找到的资源，可能中文语言包会有缺失。
    模拟器下载：
        PPXCLUB 论坛 kof2112 编译的版本：https://www.ppxclub.com/601010-1-1
        这里有几个版本：http://sourceforge.net/projects/mameplus
        这里也有，不过语言包不一定全：http://www.progettosnaps.net/mameplus/

mame32m、mame32k：
        第三方的 MAME 。
        原始的 mame32m、mame32k，早已停更了。
        然而 Creamymami 一直有在整这个。
            https://www.ppxclub.com/1287-1-1
            C大的版本
            中文列表。
            可以联机。
            核心版本很老。
            （因为核心版本老，有兴趣的话，最好在自己电脑上试一下，兼容性怎样）
            如果电脑上使用正常的话，因为核心版本老，所以占用资源少。
            因为核心是老版本的，作弊码格式需要用老版本的。
            mame32m 中文作弊码：https://www.ppxclub.com/691039-1-1

周边图片等资源：
    jjsnake 中文出招表：
        https://www.ppxclub.com/130735-1-1
        MamePlus 在游戏中，Tab 菜单中可以显示出招表。
        JJui 可以显示出招表
        MxUI 可以显示出招表
        M+GUI 可以显示出招表，目录不分层
    
    MAME 作弊码
        Pugsy's Cheats
            http://cheat.retrogames.com/
            http://www.mamecheat.co.uk
            http://www.mamecheat.co.uk/forums
        Wayder's Cheats
            https://wayder.web.fc2.com/
            https://ss1.xrea.com/nekoziman.s601.xrea.com/cheat/
    
    progettosnaps
        http://www.progettosnaps.net/
        大量图片等资源
    
    mameUI
        http://www.mameui.info/
        一款第三方的 MAME ，英文版
        已经停止更新了
        它这上面提供的 游戏截图包 ，数量上要简洁一点。

roms 管理软件：
    ClrMamePro：
        http://mamedev.emulab.it/clrmamepro/

FB 系列的街机模拟器
    支持的街机游戏也很多。
    会用并喜欢用 MAME 的话，就不需要的这个了。
    如果不喜欢 MAME 街机模拟器 的话，可以试试这一类。
FBAS
    FBAS 发布页面（和 mame32m 、mame32k 在一起）：
    https://www.ppxclub.com/1287-1-1
        (这个可能简单点，本身带了简体中文语言包，不用到处去找语言包)
    中文作弊码：
    https://www.ppxclub.com/133649-1-1
FBA (FB Alpha)：
    http://www.fbalpha.com
    简体中文菜单：官网有，可下载
    繁体中文菜单：https://www.ppxclub.com/686323-1-1
    简体中文游戏列表：https://neo-source.com/index.php?topic=3227  第27楼
    简体中文游戏列表：https://www.ppxclub.com/685486-1-1
    作弊码：https://www.ppxclub.com/143980-1-1
FBNeo
    (FBA 团队散了，继续另外搞的大佬把名字改成了 FBNeo )
    论坛 ：https://neo-source.com
    代码 ：https://github.com/finalburnneo/FBNeo
    下载 ：https://github.com/finalburnneo/FBNeo/releases
    语言包：https://www.ppxclub.com/692732-1-1
    kof2112 编译的程序 ：https://www.ppxclub.com/688355-1-1
    作弊码 https://github.com/finalburnneo/FBNeo-cheats
    中文作弊码的话，用上边提到的以前 FBA 的资源，应该也是可以的。

retroarch
    https://www.retroarch.com/
    这一个大杂烩
    里面有收集各种模拟器
    其中也有 mame 核心、fbn 核心
    

其它：
    ......
    ......
    ......

"""


class MenuBar(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_ui()
        self.new_func_bindings()

        self.new_func_ui_menu_for_ui()
        self.new_func_ui_menu_for_language()
        self.new_func_ui_menu_for_configure()
        
        self.new_func_ui_menu_for_index()
        
        self.new_func_ui_menu_for_gamelist()
        self.new_func_ui_menu_for_extra()
        
        
        
        self.new_func_ui_menu_for_about() # other

    def new_func_ui(self,):
        
        parent=self
        
        parent.rowconfigure(0, weight=0)
        parent.columnconfigure(0, weight=0)
        parent.columnconfigure(1, weight=0)
        
        column=0
        
        # style="TMenubutton" 
            # 默认
            # 带有箭头符号，可能还有 button 一样的背景图片        
        # style="Toolbutton"  
            #   Ttk::menubutton widgets support the Toolbutton style in all standard themes, which is useful for creating widgets for toolbars. 
        self.new_menu_botton_ui = ttk.Menubutton(parent,direction="below",width=0,text=_("UI"),style="Toolbutton")
        self.new_menu_botton_ui.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        self.new_menu_botton_language=ttk.Menubutton(parent,direction="below",width=0,text=_(r"语言/language"),style="Toolbutton",)
        self.new_menu_botton_language.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        self.new_menu_botton_configure = ttk.Menubutton(parent,direction="below",width=0,text=_("文件路径"),style="Toolbutton",)
        self.new_menu_botton_configure.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        self.new_menu_botton_index=ttk.Menubutton(parent,direction="below",width=0,text=_("分类列表"),style="Toolbutton",)
        self.new_menu_botton_index.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        self.new_menu_botton_gamelist=ttk.Menubutton(parent,direction="below",width=0,text=_("游戏列表"),style="Toolbutton",)
        self.new_menu_botton_gamelist.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        
        self.new_menu_botton_extra=ttk.Menubutton(parent,direction="below",width=0,text=_("周边"),style="Toolbutton",)
        self.new_menu_botton_extra.grid(row=0,column=column, sticky=tk.W,)
        column+=1
        
        
        self.new_menu_botton_about=ttk.Menubutton(parent,direction="below",width=0,text=_("其它"),style="Toolbutton",)
        self.new_menu_botton_about.grid(row=0,column=column, sticky=tk.W,)
        column+=1
    
    def new_func_bindings(self,):
        pass

    def new_func_ui_menu_for_ui(self,):
        m = tk.Menu(self.new_menu_botton_ui, tearoff=0)
        self.new_menu_botton_ui.configure(menu=m)
        
        m.add_command(label=_("切换主题(关闭程序，重新打开后生效)"),
                command=self.new_func_menu_call_back_change_theme
                )
        

        
        if sys.platform.startswith('win32'):
            m.add_separator()
            
            m2 = tk.Menu(m, tearoff=0)
            
            m.add_cascade(
                label=_("高分辨率屏幕"),
                menu=m2
                )
            
            
            self.new_var_tk_high_dpi = tk.IntVar() # default value 0
            self.new_var_tk_high_dpi.set(global_variable.user_configure_data["high_dpi"])
            
            
            m2.add_command(
                label=_("程序关闭，重新打开后生效。"), 
                state=tk.DISABLED)
            
            m2.add_separator()
            m2.add_radiobutton(
                label="windows high dpi "+_("不设置"), 
                value=0,
                variable=self.new_var_tk_high_dpi,
                command=self.new_func_set_high_dpi_value,
                #state=tk.DISABLED
                )
            
            m2.add_separator()
            m2.add_command(
                label=r"( Windows Vista, 7, 8 )", 
                state=tk.DISABLED)
            m2.add_radiobutton(
                label="windows high dpi "+_("方法1"), 
                value=1,
                variable=self.new_var_tk_high_dpi,
                command=self.new_func_set_high_dpi_value,
                #state=tk.DISABLED
                )
            
            m2.add_separator()
            m2.add_command(
                label=r"( >= windows 8.1 )", 
                state=tk.DISABLED)
            
            m2.add_radiobutton(
                label="windows high dpi "+_("方法2"), 
                value=2,
                variable=self.new_var_tk_high_dpi,
                command=self.new_func_set_high_dpi_value,
                #state=tk.DISABLED
                )
            m2.add_radiobutton(
                label="windows high dpi "+_("方法3"), 
                value=3,
                variable=self.new_var_tk_high_dpi,
                command=self.new_func_set_high_dpi_value,
                #state=tk.DISABLED
                )
            m2.add_radiobutton(
                label="windows high dpi "+_("方法4"), 
                value=4,
                variable=self.new_var_tk_high_dpi,
                command=self.new_func_set_high_dpi_value,
                #state=tk.DISABLED
                )
            #m2.add_radiobutton(
            #    label="windows high dpi "+_("方法5"), 
            #    value=5,
            #    variable=self.new_var_tk_high_dpi,
            #    command=self.new_func_set_high_dpi_value,
            #    #state=tk.DISABLED
            #    )

            
            m2.add_separator()
            m2.add_command(
                label=_("注"), 
                state=tk.DISABLED)            
            m2.add_command(
                label=_("当屏幕 dpi 太高，用 1:1 显示时，默认字体太小。"), 
                state=tk.DISABLED)
            m2.add_command(
                label=_("如果，在系统中，整体设置了放大，此时，有些软件处理得不好，字体又显示得模糊，"), 
                state=tk.DISABLED)
            m2.add_command(
                label=_("此时，你可以试试以上不同的选项。"), 
                state=tk.DISABLED)
            m2.add_separator()
            m2.add_command(
                label=_("网上搜到的代码，具体管不管用，不太懂"), 
                state=tk.DISABLED)
            m2.add_command(
                label=_("其中有管用的，那正好"), 
                state=tk.DISABLED)
            m2.add_command(
                label=_("都不管用的话，也就算球了"), 
                state=tk.DISABLED)
        
        m.add_separator()
        self.new_var_tk_scaling_use_flag = tk.IntVar() # default value 0
        # 初始化,从配置文件中，读取值
        if global_variable.user_configure_data["tk_scaling_use_flag"] not in (0,1):
            global_variable.user_configure_data["tk_scaling_use_flag"] = 0
        self.new_var_tk_scaling_use_flag.set(global_variable.user_configure_data["tk_scaling_use_flag"])
            
        m.add_checkbutton(
                label=_(r"启用 tk scaling 缩放（关闭程序，重新打开后生效）"), 
                variable = self.new_var_tk_scaling_use_flag ,
                command=self.new_func_menu_call_back_use_tk_scaling,
                )
        
        m.add_command(
                label=_(r"手动设置 tk scaling 缩放 值"), 
                command=self.new_func_menu_call_back_set_tk_scaling_number
                )
        
        m.add_separator()
        
        m.add_command(label=_(r"列表行高设置"), 
                command=self.new_func_menu_call_back_set_row_height
                )
        
        m.add_command(label=_(r"列表标题行高设置"), 
                command=self.new_func_menu_call_back_set_row_height_for_header
                )
        
        m.add_command(label=_(r"列表图标宽度设置"), 
                command=self.new_func_menu_call_back_set_icon_size
                )

        m.add_command(label=_(r"列表字体"), 
                command=self.new_func_menu_call_back_set_gamelist_font
                )
        
        m.add_command(label=_(r"列表标题字体"), 
                command=self.new_func_menu_call_back_set_header_font
                )
        
        m.add_command(label=_(r"文本字体1"), 
                command=self.new_func_menu_call_back_set_text_font_1
                )
        
        m.add_command(label=_(r"文本字体2"), 
                command=self.new_func_menu_call_back_set_text_font_2
                )
        
        m.add_command(label=_(r"其它字体"), 
                command=self.new_func_menu_call_back_set_others_font
                )

        m.add_separator()
        
        m.add_command(
            label=_("仅内置主题（第三方主题，可以在对应的配置文件中编辑颜色）"), 
            state=tk.DISABLED)
        
        self.new_var_tk_use_colour_flag = tk.IntVar() # default value 0
        if global_variable.user_configure_data["use_colour_flag"] not in (0,1):
            global_variable.user_configure_data["use_colour_flag"] = 0
        self.new_var_tk_use_colour_flag.set( global_variable.user_configure_data["use_colour_flag"] )
        
        m.add_checkbutton(
                label= _("内置主题") + ' ' + _(r"启用自定义颜色") + ' ' + _("需关闭、重新打开程序"), 
                variable = self.new_var_tk_use_colour_flag ,
                command=self.new_func_menu_call_back_use_colours,
                )
        
        m.add_command(label=_("内置主题")+ ' ' + _(r"自定义部分颜色"), 
                command=self.new_func_menu_call_back_set_colours
                )
        
        m.add_separator()
        
        m.add_command(label=_(r"保存配置文件"), 
                command=self.new_func_save_user_configure
                )
        m.add_command(label=_(r"保存配置文件、窗口大小"), 
                command=self.new_func_save_user_configure_with_window_size
                )
        m.add_command(label=_(r"保存配置文件、窗口大小/位置"),
                command=self.new_func_save_user_configure_with_window_size_and_position
                )
        #m.add_command(label=_("窗口最大化时，保存位置有点问题"), state=tk.DISABLED)  
        
        m.add_separator()
    
    def new_func_ui_menu_for_configure(self,):
        m = tk.Menu(self.new_menu_botton_configure, tearoff=0)
        self.new_menu_botton_configure.configure(menu=m)
        
        m.add_separator()
        
        m.add_command(label=_("文件路径设置"), 
                command=self.new_func_menu_call_back_set_file_path
                )
        
        # m.add_separator()

        # m.add_command(label=_("如果需要清空数据，可以手动删除 .jjui 文件夹下的 *.bin 文件"), 
        #         state=tk.DISABLED
        #         )
        
        
        m.add_separator()
    
    def new_func_ui_menu_for_index(self,):
        m = tk.Menu(self.new_menu_botton_index, tearoff=0)
        self.new_menu_botton_index.configure(menu=m)
        
        m.add_command(  label=_("保存"), 
                        command=misc_funcs.new_func_index_popup_menu_function_save,
                )
        m.add_command(  label=_("修改自定义目录以后，记得手动保存一下"),state="disabled")
        m.add_separator()
        
        # 导出内置分类
        m.add_command(  label=_("导出内置的分类到此文件夹：") + the_files.folder_export, 
                command=misc.export_all_internal_index,
        )
        m.add_command(  label=_("如果此文件夹已经有文件了，建议自己先手动清理一下，免得各种新旧文件混在一起"), 
                        state="disabled"
                )
        m.add_separator()
        # 导出外置分类，清理超出范围的内容
        m.add_command(  label=_("导出外置的分类到文件夹：") + the_files.folder_export + " " +_("并清理超出范围的项目") , 
                command=misc.export_all_external_index_and_clean,
        )
        m.add_command(  label=_("如果此文件夹已经有文件了，建议自己先手动清理一下，免得各种新旧文件混在一起"), 
                        state="disabled"
                )
        m.add_command(  label=_("如果有超出范围的项目，会被保存为同名的 .txt 文件"), 
                        state="disabled"
                )
        m.add_command(  label=_("超出范围是指：不在所有列表中"), 
                        state="disabled"
                )
        m.add_command(  label=_("不同版本的模拟器，会有一些文件名修改过；非官方的 MAME 可能比官方原版 收录更多的游戏；……"), 
                        state="disabled"
                )                

        m.add_separator()
        m.add_command(  label=_("谨慎操作！"), 
                        state="disabled"
                )
        m.add_command(  label=_("瘦身"), 
                        command=ui_small_windows.window_for_choose_unwanted_internal_index
                )
        m.add_separator()
    
    def new_func_ui_menu_for_gamelist(self,):
        m = tk.Menu(self.new_menu_botton_gamelist, tearoff=0)
        self.new_menu_botton_gamelist.configure(menu=m)
        
        
        #m.add_separator()
        m.add_command(label=_(r"刷新列表，split/分离模式 (不具体校验文件，只检查有没有压缩包/文件夹)"), 
                command=misc_funcs.gamelist_available_refresh
                )
                
        m.add_command(label=_(r"刷新列表，merged/合并模式 (不具体校验文件，只检查有没有压缩包/文件夹)"), 
                command=misc_funcs.gamelist_available_refresh_2
                )
                
        m.add_command(label=_(r"以上两项，只是检查文件是否存在，没有检查文件的正确性"), 
                state=tk.DISABLED,
                )
        
        m.add_separator()
        self.new_var_tk_unavailable_mark = tk.IntVar() # default value 0
            # 初始化,需从配置文件中，读取值
        
        # 全局记录 bool
        global_variable.flag_mark_unavailable_game = global_variable.user_configure_data["unavailable_mark"]
        
        if global_variable.user_configure_data["unavailable_mark"] :# bool
            self.new_var_tk_unavailable_mark.set(1)
            
        m.add_checkbutton(
                label=_(r"标记未拥有"),
                command=self.new_func_menu_call_back_choose_mark_unavailable,
                variable =self.new_var_tk_unavailable_mark,
                )
        
        if global_variable.gamelist_type == "softwarelist":
            pass
        else:
            m.add_separator()
            m.add_command(label=_(r"拥有列表 过滤"), 
                    command=ui_small_windows.window_for_gamelist_available_filter
                    )
        
        m.add_separator()
        m.add_command(label=_(r"全局 过滤"), 
                command=ui_small_windows.window_for_gamelist_filter
                )
        m.add_command(label=_(r"程序关闭后，不会保存这个值"), 
                state=tk.DISABLED,
                )
        
        m.add_separator()
        m.add_command(label=_("选择列表显示项目"),
                command = ui_small_windows.header_pop_up_menu_callback_choose_columns
                )
        
        m.add_separator()

        # 定位 
        self.new_var_tk_keep_track_of_the_select_item = tk.IntVar()
        if global_variable.user_configure_data["keep_track_of_the_select_item"]:
            self.new_var_tk_keep_track_of_the_select_item.set(1)
        else:
            self.new_var_tk_keep_track_of_the_select_item.set(0)
        m.add_checkbutton(
                label=_(r"切换列表时，尝试定位到之前的选择"),
                command=self.new_func_menu_call_back_for_keep_track_of_the_select_item,
                variable =self.new_var_tk_keep_track_of_the_select_item,
                )        
        
        m.add_separator()
        self.new_var_tk_use_local_sort = tk.IntVar() # default value 0
        # 初始化,需从配置文件中，读取值
        if global_variable.user_configure_data["use_locale_sort"]:
            self.new_var_tk_use_local_sort.set(1)
        else:
            self.new_var_tk_use_local_sort.set(0)
        
        m.add_checkbutton(label=_("本地排序")+"(" +_("关闭程序，重新打开后生效") +")", 
                variable = self.new_var_tk_use_local_sort ,
                command=self.new_func_menu_call_back_use_local_sort
                )
        
        m.add_separator()
        m.add_command(label=_("搜索 设置"),
                command = ui_small_windows.window_for_gamelist_set_search_columns
                )
        m.add_command(label=_(r"程序关闭后，不会保存这个值"), 
                state=tk.DISABLED,
                )
        
        m.add_separator()

        #子菜单
        m_sub_delete = tk.Menu(m,tearoff=0)
        m.add_cascade(label=_("瘦身"),menu=m_sub_delete)
        m_sub_delete.add_command(label=_("谨慎操作！"),
                state=tk.DISABLED,
                )
        m_sub_delete.add_command(label=_("删除内容后，程序会关闭。") + _("重新打开程序，查看效果即可。"),
                state=tk.DISABLED,
                )                
        m_sub_delete.add_command(label=_("删除不需要的列"),
                command=ui_small_windows.window_for_choose_unwanted_game_list_column,
                )        
        m_sub_delete.add_command(label=_("删除不需要的行，删除当前目录中的条目"),
                command=misc.delete_current_rows_in_game_list,
                )
        m_sub_delete.add_command(label=_("删除不需要的行，仅保留当前目录，删除其它条目"),
                command=lambda reverse=True :misc.delete_current_rows_in_game_list(reverse=reverse)
                )
    
    def new_func_ui_menu_for_extra(self,):
        m = tk.Menu(self.new_menu_botton_extra, tearoff=0)
        self.new_menu_botton_extra.configure(menu=m)
        #self.new_menu_botton_extra
        
        
        self.new_var_tk_extra_delay_use_flag = tk.IntVar() # default value 0
        # 初始化,需从配置文件中，读取值
        
        # 范围 
        if global_variable.user_configure_data["extra_delay_time_use_flag"] not in (0,1):
            global_variable.user_configure_data["extra_delay_time_use_flag"] = 1
        self.new_var_tk_extra_delay_use_flag.set(global_variable.user_configure_data["extra_delay_time_use_flag"])
        
        m.add_checkbutton(
                label=_("周边延迟显示"), 
                variable = self.new_var_tk_extra_delay_use_flag ,
                command=self.new_func_menu_call_back_use_extra_delay_time,
                )
        
        m.add_command(label=_("周边延迟时间设置"), 
                command=self.new_func_menu_call_back_set_extra_delay_time
                )
        
        m.add_separator()
        
        self.new_var_tk_extra_image_serach_file_first = tk.IntVar() # default value 0
        # 初始化,需从配置文件中，读取值
        
        # 范围 
        if global_variable.user_configure_data["extra_image_search_file_first"] not in (0,1):
            global_variable.user_configure_data["extra_image_search_file_first"] = 1
        self.new_var_tk_extra_image_serach_file_first.set(global_variable.user_configure_data["extra_image_search_file_first"])
        
        m.add_checkbutton(
                label=_("图片，使用 zip 压缩包时，仍然优先搜索普通文件"), 
                variable = self.new_var_tk_extra_image_serach_file_first ,
                command=self.new_func_menu_call_back_extra_image_search_file_first,
                )

        m.add_separator()
        
        m.add_command(label=_("周边文档，建目录加速"), 
                command=misc_funcs.extra_docs_make_index
                )
        
        m.add_separator()

        if global_variable.gamelist_type=="mame":
            m.add_command(label=_("周边文档，出招表，文字替换内容检查"), 
                    command=ui_small_windows.window_for_extra_command_character
                    )
            m.add_separator()
        
        
        # 范围 
        self.new_var_tk_extra_image_keep_aspect_ratio = tk.IntVar() # default value 0
        self.new_var_tk_extra_image_keep_aspect_ratio_2 = tk.IntVar() # default value 0
        if global_variable.user_configure_data["extra_image_keep_aspect_ratio"] not in (0,1):
            global_variable.user_configure_data["extra_image_keep_aspect_ratio"] = 0
        if global_variable.user_configure_data["extra_image_keep_aspect_ratio_2"] not in (0,1):
            global_variable.user_configure_data["extra_image_keep_aspect_ratio_2"] = 0
        self.new_var_tk_extra_image_keep_aspect_ratio.set(global_variable.user_configure_data["extra_image_keep_aspect_ratio"])
        self.new_var_tk_extra_image_keep_aspect_ratio_2.set(global_variable.user_configure_data["extra_image_keep_aspect_ratio_2"])
        m.add_checkbutton(
                    label=_("周边图片一，使用 4:3 或 3:4 的比例（仅适用于一部分游戏）"), 
                    variable = self.new_var_tk_extra_image_keep_aspect_ratio ,
                    command=self.new_func_menu_call_back_extra_image_keep_aspect_ratio,
                    )
        m.add_checkbutton(
                    label=_("周边图片二，使用 4:3 或 3:4 的比例（仅适用于一部分游戏）"), 
                    variable = self.new_var_tk_extra_image_keep_aspect_ratio_2 ,
                    command=self.new_func_menu_call_back_extra_image_keep_aspect_ratio_2,
                    )
        
        m.add_separator()
        
        m.add_command(
                    label = _("提取图片（仅当前列表）") ,
                    command = self.new_func_menu_call_back_extra_image_copy ,
                    )
        
        m.add_separator()

    def new_func_ui_menu_for_language(self,):
        m = tk.Menu(self.new_menu_botton_language, tearoff=0)
        self.new_menu_botton_language.configure(menu=m)
        
        m.add_separator()
        
        m.add_command( label=_(r"界面翻译 / UI translation") , 
                command=misc_funcs.ui_select_translation
                )
        m.add_command(label= _("关闭程序，重新打开后生效"), 
                state="disabled"
                )
        
        m.add_separator()
        
        m.add_command(label=_(r"游戏列表翻译 / gamelist translation"),
                command=misc_funcs.gamelist_reload_translation
                )
        
        m.add_separator()
        
    
    def new_func_ui_menu_for_about(self,): # other
        #self.new_menu_botton_about
        m = tk.Menu(self.new_menu_botton_about, tearoff=0)
        self.new_menu_botton_about.configure(menu=m)
        
        m.add_separator()
        
        m.add_command(label=_("关于 JJui"),
                command=self.new_func_menu_call_back_window_about
                )
        m.add_separator()
        
        m.add_command(label=_("赞助 JJui"),
                command=self.new_func_menu_call_back_window_donation
                )
        m.add_separator()
        

        
        # www.ppxclub.com/705838-1-1
        m.add_command(
            label=_("JJui 在 PPXCLUB 论坛的发布页面：www.ppxclub.com/705838-1-1"), 
            command=lambda url = "https://www.ppxclub.com/705838-1-1":self.new_func_menu_call_back_open_url(url=url)
            )
        m.add_command(
            label=_("PPXCLUB 论坛，国内的街机模拟器玩家可能多一些，但是如果不是开放注册期间，可能不方便注册"), 
            state=tk.DISABLED)
        m.add_separator()
        
        # https://github.com/gdicnng/JJui
        m.add_command(
            label=_("源代码 github：https://github.com/gdicnng/JJui"), 
            command=lambda url = "https://github.com/gdicnng/JJui":self.new_func_menu_call_back_open_url(url=url)
            )
        m.add_separator()

        m.add_command(
                label=_("打开本地 使用说明：")+the_files.file_html_index, 
                command=self.new_func_menu_call_back_open_html_file
                )
        m.add_command(
            label=_("如果使用说明，没有放在一起，另外下载后，再看"), 
            state=tk.DISABLED)
        m.add_command(
            label=_("如果使用说明没有正确打开，可以找到文件，手动打开"), 
            state=tk.DISABLED)
        
        m.add_separator()

        m.add_command(
            label=_("打开在线 使用说明：jjui.readthedocs.io"), 
            command=lambda url = "https://jjui.readthedocs.io":self.new_func_menu_call_back_open_url(url=url)
            )
        m.add_command(
            label=_("打开在线 使用说明：jjui.rtfd.io"), 
            command=lambda url = "https://jjui.rtfd.io":self.new_func_menu_call_back_open_url(url=url)
            )
        
        m.add_command(
            label=_("readthedocs 的免费在线文档功能，不知道网站连接的效果好不好"), 
            state=tk.DISABLED)
        
        # new_func_menu_call_back_open_url
        m.add_separator()
        
        m.add_command(
            label   = _("查看当前 python 版本"), 
            command = self.new_func_menu_call_back_show_python_version
            )
        m.add_separator()
        
        m.add_command(
            label   = _("一些网站链接"), 
            command = self.new_func_menu_call_back_some_website
            )
        
        m.add_separator()

    
    # 菜单 callback 函数：UI→切换主题
    # a topleve window 
    def new_func_menu_call_back_change_theme(self,):
    
        
        style=ttk.Style()
        
        print("chage the theme")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("选择主题"))
        
        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        size = "400x300" 
        #size = temp
        window.geometry( size )
             
        window.lift()
        window.transient(global_variable.root_window)
        #window.grab_set()
        
        window.columnconfigure(0,weight=1)
        window.rowconfigure(0,weight=1)
        
        def for_ok_button_1():
            index = chooser_1.current()
            print(index)
            if index == -1 :
                pass
            else:
                the_theme =  theme_names_1[index]
                global_variable.user_configure_data["theme"] =  the_theme
                window.destroy()
                print( the_theme )
        
        def for_ok_button_2():
            index = chooser_2.current()
            print(index)
            if index == -1 :
                pass
            else:
                the_theme =  theme_names_2[index]
                print( the_theme )
                global_variable.user_configure_data["theme"] =  the_theme
                window.destroy()
        
        notebook = ttk.Notebook( window,)
        notebook.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        
        #button_ok = ttk.Button( window ,text="确认",command=for_ok_button)
        #button_ok.grid(row=0,column=0,sticky=tk.E,)
        
        # 当前使用的主题为xxxx，设置中的主题为xxxx(关闭程序，重新打开后生效)
        temp_string  = _("当前使用的主题为：")
        temp_string += style.theme_use() # 当前使用的主题
        temp_string += "\n"
        temp_string += _("设置中的主题为：")
        temp_string += global_variable.user_configure_data["theme"]
        temp_string += "\n"
        temp_string += _(" (关闭程序，重新打开后生效)")
        
        # 1
            # 内置主题
        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text=_('使用内置主题'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        ttk.Label(frame1,text=temp_string,).grid(row=0,column=0,sticky=tk.N+tk.W,)
        ttk.Label(frame1,text="",).grid(row=1,column=0,sticky=tk.N+tk.W,)
        ttk.Label(frame1,text=_("选择内置主题："),).grid(row=2,column=0,sticky=tk.N+tk.W,)
        
        chooser_1 = ttk.Combobox(frame1,state="readonly" )
        chooser_1.grid(row=3,column=0,sticky=tk.N+tk.W,)
        
        button_ok_1 = ttk.Button( frame1 ,text=_("确认"),command=for_ok_button_1)
        button_ok_1.grid(row=4,column=0,sticky=tk.E,)
        
        # self.data_from_main["internal_themes"]
        theme_names_1 = list( global_variable.internal_themes )
        theme_names_1 = sorted( theme_names_1 )
        
        chooser_1["values"]= theme_names_1
        

        
        # 2
            # 外置主题
        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text=_('使用第三方主题'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        ttk.Label(frame2,text=temp_string,).grid(row=0,column=0,sticky=tk.N+tk.W,)
        ttk.Label(frame2,text="",).grid(row=1,column=0,sticky=tk.N+tk.W,)        
        ttk.Label(frame2,text=_("选择第三方主题（需要下载第三方主题文件）："),).grid(row=2,column=0,sticky=tk.N+tk.W,)

        chooser_2 = ttk.Combobox(frame2,state="readonly" )
        chooser_2.grid(row=3,column=0,sticky=tk.N+tk.W,)
        
        button_ok_2 = ttk.Button( frame2 ,text=_("确认"),command=for_ok_button_2)
        button_ok_2.grid(row=4,column=0,sticky=tk.E,)
        
        # self.data_from_main["internal_themes"]
        theme_names_2 = list( global_variable.other_themes )
        theme_names_2 = sorted( theme_names_2 )
        
        chooser_2["values"]= theme_names_2
        
        
        
        window.wait_window()

    # high dpi 值
    def new_func_set_high_dpi_value(self,):
        global_variable.user_configure_data["high_dpi"] = self.new_var_tk_high_dpi.get()
        print()
        print( "high dpi : " )
        print( global_variable.user_configure_data["high_dpi"] )

    # 菜单 callback 函数：UI→启用放大倍数
    def new_func_menu_call_back_use_tk_scaling(self,):
        global_variable.user_configure_data["tk_scaling_use_flag"] = self.new_var_tk_scaling_use_flag.get()
        print( global_variable.user_configure_data["tk_scaling_use_flag"] )
        #if global_variable.user_configure_data["tk_scaling_use_flag"]:
        #    global_variable.root_window.tk.call('tk', 'scaling', global_variable.user_configure_data["tk_scaling_number"])
        #    global_variable.root_window.update()
        #else:
        #    pass
        ""
    
    # 菜单 callback 函数：UI→放大倍数 设置
    # a topleve window
    def new_func_menu_call_back_set_tk_scaling_number(self,):
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("放大倍数"))
        
        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        #size = "400x300" 
        #size = temp
        #print(size)
        #window.geometry( size )
        
        window.lift()
        window.transient(global_variable.root_window)
        #window.grab_set()
        
        window.columnconfigure(0,weight=1)
        #window.columnconfigure(1,weight=0)
        #window.rowconfigure(0,weight=0)
        
        #num_0 =  self.ini_data["tk_scaling_number"]
        
        ttk.Label(window,text=_("已设定的值为：")+ str(global_variable.user_configure_data["tk_scaling_number"]) ).grid(row=0,column=0,sticky=tk.N+tk.W,)
        

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.N+tk.W,)
        
        ttk.Label(window,text=_("输入一个大于0的数，整数/小数")).grid(row=2,column=0,sticky=tk.N+tk.W,)

        
        def get_the_number():
            try:
                the_number = input_number.get()
                the_number = eval( the_number )
                if type( the_number ) == int:
                    if the_number > 0 :
                        global_variable.user_configure_data["tk_scaling_number"] = the_number
                    else:
                        global_variable.user_configure_data["tk_scaling_number"] = 0
                elif type( the_number ) == float :
                    if the_number > 0.01 :
                        global_variable.user_configure_data["tk_scaling_number"] = the_number
                    else:
                        global_variable.user_configure_data["tk_scaling_number"] = 0
                
            except:
                pass
            window.destroy()
        
        input_number = tk.StringVar()
        entry_a = ttk.Entry(window,textvariable=input_number,)
        entry_a.grid(row=3,column=0,sticky=tk.N+tk.W,)
        
        ttk.Button(window,text=_("确定"),command=get_the_number,).grid(row=4,column=0,sticky=tk.N+tk.W,)
        
        
        #num = self.parent.tk.call('tk', 'scaling', )
        
        a_text      = tk.Text( window,undo=False )
        scrollbar_1 = ttk.Scrollbar( window, orient=tk.VERTICAL, command = a_text.yview,)
        a_text.configure(yscrollcommand=scrollbar_1.set)
        a_text.grid(row=5,column=0,sticky=tk.N+tk.S+tk.E+tk.W,)
        scrollbar_1.grid(row=5,column=1,sticky=tk.N+tk.S,)
        window.rowconfigure(5,weight=1)
        
        
        num = global_variable.tk_scaling_number_0
        num = str(num)
        
        
        temp_string = "".join(
            [
                _("程序启动时，值为："),
                num  ,
                "\n" ,
                "\n" ,
                _("输入一个大于0的数，整数 或 小数"),"\n" ,
                _("输入0，程序关闭后，下次回到默认值"),"\n" ,
                "\n" ,
                _("万一整错了，整个界面，大小变得不太方便操作了，"),"\n" ,
                _("可以删除配置文件中对应的选项"),"\n" ,
                _("或者简单点，删除整个配置文件"),"\n" ,
                _("配置文件为  ：  "),
                the_files.file_ini_configure,
                "\n" ,
                "\n" ,
                
                _("这功能我其实并不了解"),"\n" ,
                _("也不太清楚，是不是这样子使用的"),"\n" ,
                _("当时，在搜索第三方主题时看到的"),"\n" ,
                r"https://wiki.tcl-lang.org/page/List+of+ttk+Themes","\n" ,
                _("上面提到了有些主题可以 Scalable "),"\n" ,
                "\n",
                _("如果需要的话 "),"\n" ,
                "\n",
                "\n",
                _("内置的主题可以自己试试。 "),"\n" ,
                "\n",
                "\n",
                _("第三方主题的话"),"\n" ,
                _("很多第三方的主题可能不太适用这个选项，"),"\n" ,
                _("可能有些地方放大，有些地方没有，具体可以自己试试。"),"\n" ,
                "\n",
                _("第三方主题，其中 aw 开头的，需要加载的另外的一个库文件，"),"\n" ,
                _("以使用 .svg 格式的 图片。"),"\n" ,
                _("其它主题的图片一般是 .png .gif 格式的。"),"\n" ,
                _("aw 开头的好像也有一两个不需要库文件也能使用。"),"\n" ,
                "\n" ,
                _("第三方主题"),"\n" ,
                _("使用 .svg 图片 的主题，可以先拿来试试这功能。"),"\n" ,
                _("其它的，感兴趣的，自己多试试吧"),"\n" ,

            ]
        
        )
        
        a_text.insert(tk.END,temp_string )
        
        a_text.configure(state=tk.DISABLED)
        
        window.wait_window()
    
    # UI → 行高度
    def new_func_menu_call_back_set_row_height(self,):
        print("set row height")
        
        title_string = _("列表 行高度 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title( title_string )
        
        size = "400x300" 
        window.geometry( size )

        window.lift()
        window.transient(global_variable.root_window)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(1,weight=0)
        
        ttk.Label(window,text="").grid(row=0,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text=title_string).grid(row=1,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=2,column=0,sticky=tk.W+tk.N)
        
        choose_value = tk.StringVar()
        chooser = ttk.Combobox( window ,
                    values=list( range(201)) ,
                    textvariable=choose_value ,
                    state="readonly" , )
        chooser.grid(row=3,column=0,sticky=tk.W+tk.N)
        if global_variable.user_configure_data["row_height"] in range(201):
            chooser.set(global_variable.user_configure_data["row_height"])
        else:
            chooser.set(0)
        
        ttk.Label(window,text="").grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
            temp_number = choose_value.get()
            temp_number = int( temp_number )
            print(temp_number)
            
            global_variable.user_configure_data["row_height"]=temp_number
            print(global_variable.user_configure_data["row_height"])
            
            if temp_number > 0:
                misc_funcs.use_user_configure_row_height()
            
            #window.destroy()
            #self.parent.lift()
        
        ttk.Label(window,text=_("选择 0 的话，关闭程序，下次打开，回到默认值")).grid(row=5,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=6,column=0,sticky=tk.W+tk.N)
       
        ttk.Label(window,text="").grid(row=7,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text=_("选择其它的值，即时生效")).grid(row=8,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=9,column=0,sticky=tk.W+tk.N)
        
        ttk.Button(window,text=_("确定"),command=for_ok_button).grid( row=10,column=0,sticky=tk.N+tk.E, )
        
        
        window.wait_window()
    
    # UI → 标题 行高度
    def new_func_menu_call_back_set_row_height_for_header(self,):
        print("set row height")
        
        title_string = _("列表 标题行 高度 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title( title_string )
        
        size = "400x300" 
        window.geometry( size )

        window.lift()
        window.transient(global_variable.root_window)
        #window.grab_set()
        
        #window.columnconfigure(0,weight=1)
        #window.columnconfigure(1,weight=0)
        
        ttk.Label(window,text="").grid(row=0,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text=title_string).grid(row=1,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=2,column=0,sticky=tk.W+tk.N)
        
        choose_value = tk.StringVar()
        chooser = ttk.Combobox( window ,
                    values=list( range(201)) ,
                    textvariable=choose_value ,
                    state="readonly" , )
        chooser.grid(row=3,column=0,sticky=tk.W+tk.N)
        if global_variable.user_configure_data["row_height_for_header"] in range(201):
            chooser.set(global_variable.user_configure_data["row_height_for_header"])
        else:
            chooser.set(0)
        
        ttk.Label(window,text="").grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
            temp_number = choose_value.get()
            temp_number = int( temp_number )
            print(temp_number)
            
            global_variable.user_configure_data["row_height_for_header"]=temp_number
            print(global_variable.user_configure_data["row_height_for_header"])
            
            if temp_number > 0:
                misc_funcs.use_user_configure_row_height_for_header()
            
            #window.destroy()
            #self.parent.lift()
        
        ttk.Label(window,text=_("选择 0 的话，关闭程序，下次打开，回到默认值")).grid(row=5,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=6,column=0,sticky=tk.W+tk.N)
       
        ttk.Label(window,text="").grid(row=7,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text=_("选择其它的值，即时生效")).grid(row=8,column=0,sticky=tk.W+tk.N)
        ttk.Label(window,text="").grid(row=9,column=0,sticky=tk.W+tk.N)
        
        ttk.Button(window,text=_("确定"),command=for_ok_button).grid( row=10,column=0,sticky=tk.N+tk.E, )
        
        
        window.wait_window()
    
    def new_func_menu_call_back_set_icon_size(self,):
        print("set icon size")
        
        title_string = _("列表 图标 大小 设置")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title( title_string )
        
        size = "400x300" 
        window.geometry( size )

        window.lift()
        window.transient(global_variable.root_window)
        
        
        tkint_var = tk.IntVar()
        if global_variable.user_configure_data["icon_size"] > 0:
            tkint_var.set(global_variable.user_configure_data["icon_size"])
        elif global_variable.user_configure_data["icon_size"] == 0:
            tkint_var.set( 16 )
        
        
        ttk.Label(window,text="").grid()
        
        entry = ttk.Entry(window,textvariable=tkint_var)
        entry.grid()
        
        def for_plus():
            number = tkint_var.get()
            tkint_var.set( number+1 )
        def for_minus():
            number = tkint_var.get()
            if number > 2:
                tkint_var.set( number-1 )
        def for_ok():
            global_variable.user_configure_data["icon_size"] = tkint_var.get()
            misc_funcs.use_user_configure_icon_width()
        
        button_plus = ttk.Button(window,text=" + ",command=for_plus)
        button_plus.grid()
        
        button_minus = ttk.Button(window,text=" - ",command=for_minus)
        button_minus.grid()
        
        button_minus = ttk.Button(window,text=_("确定"),command=for_ok)
        button_minus.grid()
        
        window.wait_window()
    
    # set font game list 
    def new_func_menu_call_back_set_gamelist_font(self,):
        the_font = global_variable.font_gamelist
        misc_funcs.window_for_choose_font(the_font , _("列表字体"))
    # set font header
    def new_func_menu_call_back_set_header_font(self,):
        the_font = global_variable.font_gamelist_header
        misc_funcs.window_for_choose_font(the_font , _("列表标题字体"))
    # set font text 1
    def new_func_menu_call_back_set_text_font_1(self,):
        the_font = global_variable.font_text
        misc_funcs.window_for_choose_font(the_font , _("文本字体1"))
    # set font text 2
    def new_func_menu_call_back_set_text_font_2(self,):
        the_font = global_variable.font_text_2
        misc_funcs.window_for_choose_font(the_font , _("文本字体2"))
    # set others font
    def new_func_menu_call_back_set_others_font(self,):
        the_font = global_variable.font_others
        misc_funcs.window_for_choose_font(the_font , _("其它字体"))
    
    
    
    # 是否启用颜色
    def new_func_menu_call_back_use_colours(self,):
        global_variable.user_configure_data["use_colour_flag"] = self.new_var_tk_use_colour_flag.get()
        print( global_variable.user_configure_data["use_colour_flag"] )
    
    # 颜色 选择
    def new_func_menu_call_back_set_colours(self,):
        print("")
        print("wip")
        print("new_func_menu_call_back_set_colours")
        misc_funcs.choose_colours()
    
    # 菜单 callback 函数：设置→路径设置
    # a topleve window 
    def new_func_menu_call_back_set_file_path(self,):
    
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("路径设置"))
        
        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "400x300" + temp
        #size = temp
        #window.geometry( size )
             
        window.lift()
        window.transient(global_variable.root_window)
        #window.grab_set()
        
        # ttk.Notebook
        # 
        # ------------------------------------------------------------
        # |1模拟器路径 | 2 folders 路径 | 3图片 | 4 图片 zip| 5 文档 |
        # |            |                |       |           |        |
        # |-----------------------------------------------------------
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # |               ttk.Notebook                               |
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # |                                                          |
        # ------------------------------------------------------------
        # |                                                          |
        # |                                                 OK Button|
        # ------------------------------------------------------------
        
        #global_variable.user_configure_data
        
        data ={}
        
        def for_ok_button():

            for x in data:
                if x in global_variable.user_configure_data:
                    global_variable.user_configure_data[x] = data[x].get()
                else:
                    print(x)
                    print("a wrong key")
            
            self.new_func_save_user_configure()
            
            window.destroy()
        
        def choose_folder(v):
            # v is tk.StringVar()
            folder_path = tkinter.filedialog.askdirectory( initialdir="." )
            if folder_path=="":
                window.focus_set()
                return 0
            
            folder_path = os.path.abspath( folder_path ) # 统一格式，不然  / \ 混乱
            
            v.set( folder_path )
            window.focus_set()
        
        def add_folder(v):
            # v is tk.StringVar()
            folder_path = tkinter.filedialog.askdirectory( initialdir="." )
            if folder_path=="":
                window.focus_set()
                return 0
            
            folder_path = os.path.abspath( folder_path ) # 统一格式，不然  / \ 混乱
            
            temp=v.get()
            temp += ";" + folder_path
            v.set( temp )
            window.focus_set()
            
        def choose_zip_file(v):
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[("zip压缩包","*.zip"),],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            v.set( file_path )
            window.focus_set()
        
        def choose_dat_file(v):
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[("文档.dat","*.dat"),],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            v.set( file_path )
            window.focus_set()
        
        def choose_xml_file(v):
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[("历史文档.xml","*.xml"),],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            v.set( file_path )
            window.focus_set()
        
        def set_default_value(tk_var,temp_string):
            # self.data_from_main["ini_default"]
                # temp_string 是 key 值
                # tk_var 是前边定义 data 中的 data[temp_string]
            if temp_string in global_variable.user_configure_data_default:
                tk_var.set( global_variable.user_configure_data_default[temp_string] )
            

        window.columnconfigure(0,weight=1)
        window.rowconfigure(0,weight=1)  
        window.rowconfigure(1,weight=0)  
        
        # for notebook
        # scrollable
        the_scrollable_frame_container  = Scrollable_Frame_Container(window)
        the_scrollable_frame_container.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        scrollable_frame = the_scrollable_frame_container.new_func_get_scrollable_frame()
        scrollable_frame.columnconfigure(0,weight=1)
        scrollable_frame.rowconfigure(0,weight=1)
        
        # for notebook
        #frame_0 = ttk.Frame(window,) 
        #frame_0.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        #frame_0.columnconfigure(0,weight=1)
        #frame_0.rowconfigure(0,weight=1)        
        
        # for OK_button
        frame_1 = ttk.Frame(window,) 
        frame_1.grid(row=1,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        frame_1.columnconfigure(0,weight=1)
        #frame_1.rowconfigure(0,weight=1)
        
        #notebook = ttk.Notebook( frame_0,)
        notebook = ttk.Notebook( scrollable_frame,)
        notebook.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W,)
        
        button_ok = ttk.Button( frame_1 ,text=_("确认"),command=for_ok_button)
        button_ok.grid(row=0,column=0,sticky=tk.E,)
        #
        ttk.Sizegrip(frame_1).grid(row=0,column=1,sticky=tk.E)
        
        
        # 1
        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text=_('模拟器路径'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame1.columnconfigure(1,weight=1)
        
        def change_mame_path():
            entry_mame_path.configure( state="normal" )
            button_mame_default.configure( state="normal" )
            button_mame_chooser.configure( state="normal" )
        def change_mame_working_directory():
            entry_mame_working_directory.configure( state="normal" )
            button_mame_working_directory_default.configure( state="normal" )
            
        def choose_mame_file():
            # v is tk.StringVar()
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[(".exe","*.exe"),("所有","*")],)
            if file_path=="":
                window.focus_set()
                return 0
            
            file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
            
            data["mame_path"].set( file_path )
            window.focus_set()
        
        # 1 
        # mame 路径
        # mame 工作目录
        # 清除 mame 数据
        ttk.Label(frame1,text=_("mame 模拟器 路径")).grid(row=0,column=0,sticky=tk.W+tk.N,)
        
        data["mame_path"]=tk.StringVar()
        entry_mame_path = ttk.Entry(frame1,textvariable=data["mame_path"],state="disabled")
        entry_mame_path.grid(row=0,column=1,sticky=tk.W+tk.N+tk.E,)
        data["mame_path"].set( global_variable.user_configure_data["mame_path"] )
        
        button_mame_default = ttk.Button(frame1,text=_("默认值"),width=-1,state="disabled",command=lambda a=data["mame_path"],b="mame_path" : set_default_value(a,b),)
        button_mame_default.grid(row=0,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame1,text=_("修改"),width=-1,command=change_mame_path ).grid(row=0,column=3,sticky=tk.W+tk.N,)
        
        button_mame_chooser = ttk.Button(frame1,text=_("选择"),width=-1,state="disabled",command=choose_mame_file)
        button_mame_chooser.grid(row=0,column=4,sticky=tk.W+tk.N,)
        # mame_working_directory
        ttk.Label(frame1,text=_("mame 工作目录")).grid(row=1,column=0,sticky=tk.W+tk.N,)
        
        data["mame_working_directory"] = tk.StringVar()
        entry_mame_working_directory = ttk.Entry(frame1,textvariable=data["mame_working_directory"],state="disabled",)
        entry_mame_working_directory.grid(row=1,column=1,sticky=tk.W+tk.N+tk.E,)
        data["mame_working_directory"].set( global_variable.user_configure_data["mame_working_directory"] )
        
        button_mame_working_directory_default=ttk.Button(frame1,text=r"默认值",width=-1,state="disabled",command=lambda a=data["mame_working_directory"],b="mame_working_directory" : set_default_value(a,b),)
        button_mame_working_directory_default.grid(row=1,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame1,text=_("修改"),width=-1,command=change_mame_working_directory ).grid(row=1,column=3,sticky=tk.W+tk.N,)        
        
        n=2
        
        def delete_temp_file():
            
            files_delete=[]
            files_not_delete=[]
            
            for the_file in (
                the_files.file_pickle_gamelist_data,
                the_files.file_pickle_gamelist_available,
                ):
                
                if os.path.isfile(the_file):
                    try:
                        os.remove(the_file)
                        files_delete.append(the_file)
                    except:
                        files_not_delete.append(the_file)
            
            text=""
            if files_delete:
                text+=_("已删除的文件：")
                text+="\n"
                for the_file in files_delete:
                    text+=the_file
                    text+="\n"
            if files_not_delete:
                text+="\n"
                text+=_("未能删除的文件（可以尝试手动删除）：")
                text+="\n"
                for the_file in files_not_delete:
                    text+=the_file
                    text+="\n"
                
            result = tkinter.messagebox.showinfo(message=text)
            if the_files.file_pickle_gamelist_data in files_delete:
                window.destroy()
                sys.exit()
        
        def ask_for_delete_temp_file():
            text=_("清除模拟器数据");text+="\n"
            text+=_("清除数据后，程序将关闭");text+="\n"
            text+=_("下次打开，需要重新初始化");text+="\n"
            
            result = tkinter.messagebox.askyesno(message=text,)
            if result:
                delete_temp_file()
        
        ttk.Label(frame1,text="",).grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
        n+=1
        
        button_mame_delete_temp_file = ttk.Button(
                frame1,
                text = _("清空游戏列表数据"),
                command = ask_for_delete_temp_file,
                )
        button_mame_delete_temp_file.grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
        n+=1
        
        
        
        #the_dir = os.getcwd()
        #the_dir = os.path.abspath( the_dir )
        
        
        
        # 2
        # folder 路径
        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text=_('目录路径'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame2.columnconfigure(1,weight=1)
        
        ttk.Label(frame2,text=_("目录路径")).grid(row=0,column=0,sticky=tk.W+tk.N,)
        
        data["folders_path"]=tk.StringVar()
        
        ttk.Entry(frame2,textvariable=data["folders_path"],width=50).grid(row=0,column=1,sticky=tk.W+tk.N+tk.E,)
        
        data["folders_path"].set( global_variable.user_configure_data["folders_path"] )
        
        ttk.Button(frame2,text=r"...",width=-1,command=lambda x=data["folders_path"]: choose_folder(x)).grid(row=0,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame2,text=r" + ",width=-1,command=lambda x=data["folders_path"]: add_folder(x)).grid(row=0,column=3,sticky=tk.W+tk.N,)
        
        ttk.Button(frame2,text=_("默认值"),width=-1,command=lambda a=data["folders_path"],b="folders_path" : set_default_value(a,b),).grid(row=0,column=4,sticky=tk.W+tk.N,)
        
        # 3
        # 图片路径
        # image_types
        frame3 = ttk.Frame(notebook)
        notebook.add(frame3, text=_('图片路径'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame3.columnconfigure(1,weight=1)
        
        # 图片名 snap
        # 路径变量名 global_variable.user_configure_data["snap_path"]
        temp = {}
            # snap:snap_path ,
        for x in image_types:
            temp[x] = x+"_path"
        
        n=0
        for x in image_types :
            ttk.Label(frame3,text=x).grid(row=n,column=0,sticky=tk.W+tk.N,)
            
            temp_str = temp[x] # snap_path
            
            data[temp_str]=tk.StringVar()
            
            ttk.Entry(frame3,textvariable=data[temp_str],width=50).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
            
            data[temp_str].set( global_variable.user_configure_data[temp_str] )
            
            ttk.Button(frame3,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_folder(a)).grid(row=n,column=2,sticky=tk.W+tk.N,)

            ttk.Button(frame3,text=r" + ",width=-1,command=lambda a=data[temp_str]: add_folder(a),).grid(row=n,column=3,sticky=tk.W+tk.N,)
            
            ttk.Button(frame3,text=_("默认值"),width=-1,command = lambda a=data[temp_str],b=temp_str : set_default_value(a,b),).grid(row=n,column=4,sticky=tk.W+tk.N,)
            
            n += 1
        
            
        
        # 4
        # 图片压缩包路径
        frame4 = ttk.Frame(notebook)
        notebook.add(frame4, text=_('图片压缩包路径'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame4.columnconfigure(1,weight=1)
        
        #图片名 snap
        #路径变量名 global_variable.user_configure_data["snap.zip_path"]
        temp = {}
            # snap:snap.zip_path ,
        for x in image_types:
            temp[x] = x+".zip_path"
        
        n=0
        for x in image_types :
            ttk.Label(frame4,text=x).grid(row=n,column=0,sticky=tk.W+tk.N,)
            
            temp_str = temp[x] # snap_path
            
            data[temp_str]=tk.StringVar()
            
            ttk.Entry(frame4,textvariable=data[temp_str],width=50).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
            
            data[temp_str].set( global_variable.user_configure_data[temp_str] )
            
            ttk.Button(frame4,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_zip_file(a),).grid(row=n,column=2,sticky=tk.W+tk.N,)
            
            ttk.Button(frame4,text=_("默认值"),width=-1,command = lambda a=data[temp_str],b=temp_str : set_default_value(a,b),).grid(row=n,column=3,sticky=tk.W+tk.N,)
            
            n += 1
        
        # 5
        frame5 = ttk.Frame(notebook)
        notebook.add(frame5, text=_('文档路径'),sticky=tk.N+tk.E+tk.S+tk.W,)
        
        frame5.columnconfigure(1,weight=1)
        
        # text_types
        # text_types_2
        
        temp_types=set(text_types) | set(text_types_2)
        # SL
        if global_variable.gamelist_type == "softwarelist":
            temp_types = set(text_types)
        
        temp_types = sorted(temp_types)
        
        #文档名 command.dat
        #路径变量名 global_variable.user_configure_data["command.dat_path"]
        temp = {}
            # command.dat : command.dat_path ,
        for x in temp_types:
            temp[x] = x+"_path"
        
        n=0
        for x in temp_types :
            ttk.Label(frame5,text=x).grid(row=n,column=0,sticky=tk.W+tk.N,)
            
            temp_str = temp[x] # snap_path
            
            data[temp_str]=tk.StringVar()
            
            ttk.Entry(frame5,textvariable=data[temp_str],width=50).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
            
            data[temp_str].set( global_variable.user_configure_data[temp_str] )
            
            if x == "history.xml": 
                # xml 格式
                ttk.Button(frame5,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_xml_file(a),).grid(row=n,column=2,sticky=tk.W+tk.N,)
            else: 
                # dat 格式
                ttk.Button(frame5,text=r"...",width=-1,command=lambda a=data[temp_str]: choose_dat_file(a),).grid(row=n,column=2,sticky=tk.W+tk.N,)
                
            ttk.Button(frame5,text=_("默认值"),width=-1,command=lambda a=data[temp_str],b=temp_str : set_default_value(a,b),).grid(row=n,column=3,sticky=tk.W+tk.N,)
            
            n += 1
        
        the_scrollable_frame_container.new_func_last()
        
        window.update()
        width = the_scrollable_frame_container.new_func_return_width()
        width = int(width)
        
        if width > 800: width = 800
        
        if width<400:
            size = "400"+"x"+"300"
        else:
            size = str(width)+"x"+"300"
        
        print(width)
        
        #window.update()
        window.geometry( size )
        #window.update()
        
        window.wait_window()
    
    
    # 设置→周边延迟显示
    def new_func_menu_call_back_use_extra_delay_time(self,):
        global_variable.user_configure_data["extra_delay_time_use_flag"] = self.new_var_tk_extra_delay_use_flag.get()
        
        print( global_variable.user_configure_data["extra_delay_time_use_flag"] )
    
    # 设置→周边延迟 时间设置
    def new_func_menu_call_back_set_extra_delay_time(self,):
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("周边延迟时间设置"))
        
        #size = "400x300"
        #window.geometry( size )
        
        window.lift()
        window.transient(global_variable.root_window)
        window.columnconfigure(0,weight=1)
        
        delay_time = global_variable.user_configure_data["extra_delay_time"]
        
        if type(delay_time) != int :
            delay_time = 50 # 默认值
        
        if delay_time <= 0 :
            delay_time = 50
        
        ttk.Label(window,text=_("周边延迟时间(毫秒):")).grid()
        
        tkint_var = tk.IntVar()
        tkint_var.set(delay_time)

        
        
        
        entry=ttk.Entry(window,textvariable=tkint_var,state="readonly")
        entry.grid()
        
        def func_for_change(number):
            #print(type(number)) # number 是 字符串，浮点数
            
            number = float(number) # 转为浮点数
            
            number = int(number) # 再转为整数，有小数点，不能直接转
            
            
            if number >=1:
                if number <= 1000:
                    tkint_var.set(number)
            elif number<1:
                tkint_var.set(1)
            elif number>1000:
                tkint_var.set(1000)
        
        scale = ttk.Scale(window,
            orient=tk.HORIZONTAL,
            length=300,
            from_=1,
            to=1000,
            value=delay_time,
            command=func_for_change,
            )
        scale.grid(sticky=tk.W+tk.E)
        
        
        def for_ok_button():
            global_variable.user_configure_data["extra_delay_time"] = tkint_var.get()
            print( global_variable.user_configure_data["extra_delay_time"] )
        
        ok_button = ttk.Button(window,text=_("确定"),command=for_ok_button)
        ok_button.grid()
        
        
        window.wait_window()
    
    def new_func_menu_call_back_extra_image_search_file_first(self,):
        global_variable.user_configure_data["extra_image_search_file_first"] = self.new_var_tk_extra_image_serach_file_first.get()
        
        print( global_variable.user_configure_data["extra_image_search_file_first"] )
    
    def new_func_menu_call_back_extra_image_keep_aspect_ratio(self,):
        global_variable.user_configure_data["extra_image_keep_aspect_ratio"] = self.new_var_tk_extra_image_keep_aspect_ratio.get()
    def new_func_menu_call_back_extra_image_keep_aspect_ratio_2(self,):
        global_variable.user_configure_data["extra_image_keep_aspect_ratio_2"] = self.new_var_tk_extra_image_keep_aspect_ratio_2.get()
    
    def new_func_menu_call_back_extra_image_copy(self,):
        
        the_text  = _("复制图片")
        the_text += "\n"
        
        the_text += _("范围：仅当前列表")
        the_text += "\n"
        
        the_text += _("复制到：")
        the_text += the_files.folder_export
        the_text += "\n"
        the_text += _("如果此文件夹已有其它文件，复制前最好手动清空此文件夹")
        the_text += "\n"
        
        result = tkinter.messagebox.askyesno( message=the_text )
        
        if result:
            misc_funcs.use_threading(misc.copy_extra_images)
    
    # 游戏列表
    def new_func_menu_call_back_choose_mark_unavailable(self,):
        if self.new_var_tk_unavailable_mark.get():
            global_variable.user_configure_data["unavailable_mark"] = True
            global_variable.flag_mark_unavailable_game = True
        else:
            global_variable.user_configure_data["unavailable_mark"] = False
            global_variable.flag_mark_unavailable_game = False
        
        global_variable.the_showing_table.new_func_refresh_table()
        

    def new_func_menu_call_back_for_keep_track_of_the_select_item(self,):

        number = self.new_var_tk_keep_track_of_the_select_item.get()

        if number:
            global_variable.user_configure_data["keep_track_of_the_select_item"] = True
        else:
            global_variable.user_configure_data["keep_track_of_the_select_item"] = False

    #游戏列表→使用本地排序
    def new_func_menu_call_back_use_local_sort(self,):
        if self.new_var_tk_use_local_sort.get():
            global_variable.user_configure_data["use_locale_sort"] = True
            
            if global_variable.flag_setlocale_LC_COLLATE == False :
                try:
                    locale.setlocale(locale.LC_COLLATE,locale= global_variable.user_configure_data["locale_name"] )
                    global_variable.flag_setlocale_LC_COLLATE = True
                except:
                    global_variable.flag_setlocale_LC_COLLATE = False
            
            
        else:
            global_variable.user_configure_data["use_locale_sort"] = False
            
            global_variable.flag_setlocale_LC_COLLATE = False
            
        print( global_variable.user_configure_data["use_locale_sort"] )

    ###############
    # 菜单 callback 函数：关于→关于
    #    Toplevel   关于 窗口
    def new_func_menu_call_back_window_about(self,):
        about_window = tk.Toplevel()
        
        about_window.resizable(width=True, height=True)

        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "800x600" + temp
        size = "800x600" 
        #print()
        #print(temp)
        #print(size)
        
        about_window.title(_("关于"))
        about_window.geometry(size)
             
        about_window.transient(global_variable.root_window)
        about_window.lift()
        #about_window.grab_set()
        
        about_window.rowconfigure(0, weight=1)
        about_window.columnconfigure(0, weight=1)

        
        text  = "".join(
                [
            "JJui" + "\n"                                         ,
            "街机游戏列表显示器" + "\n"                            ,
            "JJ 取自 “街机” 的拼音首字母 ｊｉē ｊī" + "\n"                 ,
            
            #"(my English is not good , but , if anyone needed :)\n"
            #"(If you do not use Chinese ,some Chinese here may not be shown correctly )\n"
            #"(cause the font people used does not include every character in the word)\n"
            #"(it doesn't matter ,right ? if you don't use Chinese)\n"
            #"(if the Chinese doesn't show correctly, )\n"
            #"(and you really want to see it the right way, )\n"
            #"(just install a proper font for Chinese,and choose the font in JJui)\n"
            #"JJui" + "\n"                                         ,
            #"a arcade game list shower" + "\n"                        ,
            #"JJ is shot for JieJi ( 街机 mean arcade machine in Chinese)" + "\n",
            "\n"
            
            #####
            
            "JJui 只是一个 前端／UI／GUI／front-end " + "\n"       ,
            "需要配合 MAME 使用 " + "\n"                          ,
            "（不提拱游戏文件，游戏文件需要自己去找）" + "\n"                  ,
            
            "JJui 用于 MAME 街机列表的显示" + "\n"                  ,
            "后来添加了 JJui_sl" + "\n"                  ,
            "JJui_sl 用于 MAME Software List 软件列表的显示（非街机类）（MAME 版本大于 0.162）" + "\n",
            #"JJui is just a UI／GUI／front-end " + "\n"       ,
            #"you need use it with MAME " + "\n"                          ,
            #"no game files offered with it ," + "\n"             ,
            #"you need to find game files yourself" + "\n"        ,
            "\n"                                                  ,
            
            #####
            
            "不是程序员" + "\n"                                   ,
            "如果有程序员看到我的代码，觉得太菜" + "\n"            ,
            "不用奇怪" + "\n"                                     ,
            "毕竟不是专业的" + "\n"                               ,
            "自己觉得" + "\n"                                     ,
            "用是可以用了" + "\n"                                 ,
            "简单是简单了一点" + "\n"              ,
            "也可能界面还丑了点" + "\n"              ,
            
            #"I'm not a professional computer programmer" + "\n"   ,
            #"if any real programmer see it,and feel it sucks" + "\n",
            #"it's ok " + "\n"                                     ,
            #"cause I'm not a professional programmer" + "\n"             ,
            #"it is simple and maybe looks ugly" + "\n"       ,
            #"but" + "\n"                                 ,
            #"it works anyway" + "\n"                              ,
            "\n"                                                 ,
            
            #################
            
            
            "有 意见／建议 可以尽管说" + "\n"                      ,
            "但是个人 能力／时间／精力／兴趣 有限" + "\n"          ,
            "大概率很难让大家满意" + "\n"                          ,
            
            #"if you got any suggestion ,you can let me know" + "\n"    ,
            #"but my time / ability is limited" + "\n"             ,
            #"I won't promise anything" + "\n"                          ,
            "\n"                                                  ,
            
            ####
            


            #"bros,it's free for use" + "\n"        ,            
            "\n"                                                  ,
            "本人在琵琶行(www.ppxclub.com)的 ID ：gdicnng" + "\n"                   ,
            "PPXCLUB 是一个论坛，有许多街机模拟器玩家。" + "\n"                   ,
            "但如果不是在开放注册期间，可能注册不太方便。" + "\n"                   ,
            #"my ID in ppxclub.com ：gdicnng" + "\n"                   ,
            r"发布在 PPXCLUB 的页面："+"\n",
            r"www.ppxclub.com/forum.php?mod=viewthread&tid=705838"+"\n",
            r"www.ppxclub.com/705838-1-1"+"\n",
            "\n",
            r"如果你没有 PPXCLUB 的帐号，以下是百度盘网的地址："+"\n",
            r"    链接：https://pan.baidu.com/s/1guTSDIWr66S6ewIdyMQPjA"+"\n",
            r"    提取码：r9b9 "+"\n",
            r"    但，百度网盘的地址，通常很容易失效。"+"\n",
            "\n",
            "邮箱：gdicnng@sina.com" + "\n"                       ,
            #"email：gdicnng@sina.com" + "\n"                       ,
            "\n",
            "源代码(这地方算球了)：https://gitee.com/gdicnng/JJui" + "\n"       ,
            "源代码：https://github.com/gdicnng/JJui" + "\n"       ,
            "一开始上传到 gitee ，因为国内的网络连接要好一点，" + "\n"       ,
            "但是，后来，gitee 似乎 比较麻烦 了。" + "\n"       ,
            "所以后来 上传 github 了" + "\n"       ,
            "然而，github 网络连接却也不太好，国内外网络连接一直不好太好" + "\n"       ,
            
            "软件的 LICENSE 我也不是很懂，大致随意选的。" + "\n",
            "更早的代码，上传 gitee 时选的 啥子 LICENSE 记不太清楚了" + "\n",
            "上传 github 时选的 GNU GENERAL PUBLIC LICENSE Version 2" + "\n",
            
            "大家，各位街机游戏爱好者，可以免费使用" + "\n"        ,
            
            #"source file：https://gitee.com/gdicnng/JJui" + "\n"       ,
            #"之前是上传到 gitee 的，公开的" + "\n"       ,
            #"但是听说监管比较严了，连源代码都要管了" + "\n"       ,
            
            
            "\n"                                                 ,
            "如果觉得有必要 支持／打赏／赞助 一下" + "\n"          ,
            
            "以下是我的 支付宝 收钱码" + "\n"                      ,
            #"donation ,see below ," + "\n"          ,
            #"if you use Alipay (a App on the mobile phone for payment, used in China ) " + "\n"                      ,
            "\n"                                                  ,
            "\n"                                                  ,
                ]
        )

        
        t = tk.Text(about_window,undo=False,padx=10,pady=10,spacing1=2,spacing2=2,spacing3=2)
        
        scrollbar_1 = ttk.Scrollbar( about_window, orient=tk.VERTICAL, command=t.yview)
        
        scrollbar_2 = ttk.Scrollbar( about_window, orient=tk.HORIZONTAL, command=t.xview)
        
        t.configure(yscrollcommand=scrollbar_1.set)
        t.configure(xscrollcommand=scrollbar_2.set)
        
        t.grid(row=0,column=0,stick=(tk.W,tk.N,tk.E,tk.S))
        scrollbar_1.grid(row=0,column=1,columnspan=2,sticky=tk.N+tk.S,)
        scrollbar_2.grid(row=1,column=0,sticky=tk.W+tk.E,)
        
        t.insert("1.0", text, )
        
        try:
            print(the_files.image_path_zhifubao)
            image_zhifubao = Image.open( the_files.image_path_zhifubao )
            #image_weixin = Image.open(   self.data_from_main['image_path_weixin'])
            
            size_1=image_zhifubao.size
            a=800/size_1[0]
            new_size_1 = (int(size_1[0]*a),int(size_1[1]*a))
            
            image_zhifubao = image_zhifubao.resize( new_size_1,bilinear, )
            image_zhifubao = ImageTk.PhotoImage( image_zhifubao  )
            
            #size_2=image_weixin.size
            #b=800/size_2[0]
            #new_size_2 = ( int(size_2[0]*b),int(size_2[1]*b))
            
            #image_weixin = image_weixin.resize( new_size_2,bilinear, )
            #image_weixin = ImageTk.PhotoImage( image_weixin )
            
            t.image_create(tk.END,image=image_zhifubao)
            t.insert("1.0", "\n", )
            #t.image_create(tk.END,image=image_weixin)
        except:
            pass
        
        t["state"]="disabled"
        
        about_window.wait_window()
    
    def new_func_menu_call_back_window_donation(self,):
        about_window = tk.Toplevel()
        
        about_window.resizable(width=True, height=True)

        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "800x600" + temp
        size = "800x600" 
        #print()
        #print(temp)
        #print(size)
        
        about_window.title(_("赞助"))
        about_window.geometry(size)
             
        about_window.transient(global_variable.root_window)
        about_window.lift()
        #about_window.grab_set()
        
        about_window.rowconfigure(0, weight=1)
        about_window.columnconfigure(0, weight=1)

        text=_("支付宝二维码：")
        text+="\n"
        text+="\n"
        
        t = tk.Text(about_window,undo=False,padx=10,pady=10,spacing1=2,spacing2=2,spacing3=2)
        
        scrollbar_1 = ttk.Scrollbar( about_window, orient=tk.VERTICAL, command=t.yview)
        
        scrollbar_2 = ttk.Scrollbar( about_window, orient=tk.HORIZONTAL, command=t.xview)
        
        t.configure(yscrollcommand=scrollbar_1.set)
        t.configure(xscrollcommand=scrollbar_2.set)
        
        t.grid(row=0,column=0,stick=(tk.W,tk.N,tk.E,tk.S))
        scrollbar_1.grid(row=0,column=1,columnspan=2,sticky=tk.N+tk.S,)
        scrollbar_2.grid(row=1,column=0,sticky=tk.W+tk.E,)
        
        
        
        try:
            print(the_files.image_path_zhifubao)
            image_zhifubao = Image.open( the_files.image_path_zhifubao )
            #image_weixin = Image.open(   self.data_from_main['image_path_weixin'])
            
            size_1=image_zhifubao.size
            a=800/size_1[0]
            new_size_1 = (int(size_1[0]*a),int(size_1[1]*a))
            
            image_zhifubao = image_zhifubao.resize( new_size_1,bilinear, )
            image_zhifubao = ImageTk.PhotoImage( image_zhifubao  )
            
            #size_2=image_weixin.size
            #b=800/size_2[0]
            #new_size_2 = ( int(size_2[0]*b),int(size_2[1]*b))
            
            #image_weixin = image_weixin.resize( new_size_2,bilinear, )
            #image_weixin = ImageTk.PhotoImage( image_weixin )
            t.insert("1.0", text, )
            
            t.image_create(tk.END,image=image_zhifubao)
            t.insert("1.0", "\n", )
            #t.image_create(tk.END,image=image_weixin)
        except:
            pass
        
        t["state"]="disabled"
        
        about_window.wait_window()
        
    
    # 菜单 callback 函数：关于→文档
    def new_func_menu_call_back_open_html_file(self,):
        html_file = the_files.file_html_index
        if os.path.isfile(html_file):
            html_file = os.path.abspath(html_file)
            webbrowser.open(url=html_file,)
    
    def new_func_menu_call_back_open_url(self,event=None,url=None):
        if url is not None:
            webbrowser.open(url=url,)
    
    def new_func_menu_call_back_show_python_version(self,):
        python_version  = str(sys.version)
        tkinter_version = str(tk.TkVersion)
        #pillow_version  = ""
        
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        size = "400x600" 
        window.geometry(size)
        
        window.title(_("查看 python 版本"))
        
             
        window.transient(global_variable.root_window)
        window.lift()
        
        ttk.Label(window,text="").grid(sticky=tk.W)
        ttk.Label(window,text=_("python 版本：")  + python_version).grid(sticky=tk.W)
        
        ttk.Label(window,text="").grid(sticky=tk.W)
        ttk.Label(window,text=_("tkinter 版本：") + tkinter_version).grid(sticky=tk.W)
        #ttk.Label(window,text=_("Pillow 版本：") + "").grid()
        
        
        
        window.wait_window()
    
    def new_func_menu_call_back_some_website(self,):

        about_window = tk.Toplevel()
        
        about_window.resizable(width=True, height=True)

        #temp = self.get_root_window_x_y() # 'wxh±x±y' ±x±y
        #size = "800x600" + temp
        size = "800x600" 
        #print()
        #print(temp)
        #print(size)
        
        about_window.title(_("关于"))
        about_window.geometry(size)
             
        about_window.transient(global_variable.root_window)
        about_window.lift()
        #about_window.grab_set()
        
        about_window.rowconfigure(0, weight=1)
        about_window.columnconfigure(0, weight=1)

        
        text = a_long_text

        
        t = tk.Text(about_window,undo=False,padx=10,pady=10,spacing1=2,spacing2=2,spacing3=2)
        
        scrollbar_1 = ttk.Scrollbar( about_window, orient=tk.VERTICAL, command=t.yview)
        
        scrollbar_2 = ttk.Scrollbar( about_window, orient=tk.HORIZONTAL, command=t.xview)
        
        t.configure(yscrollcommand=scrollbar_1.set)
        t.configure(xscrollcommand=scrollbar_2.set)
        
        t.grid(row=0,column=0,stick=(tk.W,tk.N,tk.E,tk.S))
        scrollbar_1.grid(row=0,column=1,columnspan=2,sticky=tk.N+tk.S,)
        scrollbar_2.grid(row=1,column=0,sticky=tk.W+tk.E,)
        
        t.insert("1.0", text, )
        
        
        t["state"]="disabled"
        
        about_window.wait_window()
    


    # 菜单 callback 函数：保存设置
    def new_func_save_user_configure(self,):
        misc_funcs.save_user_configure()
    
    def new_func_save_user_configure_with_window_size(self,):
        misc_funcs.save_user_configure_with_window_size()
        
    def new_func_save_user_configure_with_window_size_and_position(self,):
        misc_funcs.save_user_configure_with_window_size_and_position()