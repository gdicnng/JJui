# -*- coding: utf_8_sig-*-
import sys
import os
import webbrowser
import locale
import tkinter as tk
from tkinter import ttk 
import tkinter.filedialog

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation


from PIL import Image, ImageTk

from . import global_variable
from . import global_static
from . import global_static_filepath as the_files

from . import read_user_config

from .ui_misc import  misc_funcs
from .ui__scrollable_frame_in_cavans import Scrollable_Frame_Container


user_configure    = global_variable.user_configure_data
default_configure = global_variable.user_configure_data_default
root_window       = global_variable.root_window

image_types   = global_static.extra_image_types
text_types    = global_static.extra_text_types
text_types_2  = global_static.extra_text_types_2

class MenuBar(ttk.Frame):
    def __init__(self ,parent,*args,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_ui()
        self.new_func_bindings()

        
        self.new_func_ui_menu_for_ui()
        
        self.new_func_ui_menu_for_configure()
        
        self.new_func_ui_menu_for_index()
        
        self.new_func_ui_menu_for_gamelist()
        
        self.new_func_ui_menu_for_about()
        
        self.new_func_ui_menu_for_language()

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
        self.new_menu_botton_ui.grid(row=0,column=column, sticky=(tk.W,))
        column+=1
        
        
        self.new_menu_botton_configure = ttk.Menubutton(parent,direction="below",width=0,text=_("设置"),style="Toolbutton",)
        self.new_menu_botton_configure.grid(row=0,column=column, sticky=(tk.W,))
        column+=1
        
        self.new_menu_botton_gamelist=ttk.Menubutton(parent,direction="below",width=0,text=_("游戏列表"),style="Toolbutton",)
        self.new_menu_botton_gamelist.grid(row=0,column=column, sticky=(tk.W,))
        column+=1        
        
        
        self.new_menu_botton_about=ttk.Menubutton(parent,direction="below",width=0,text=_("帮助"),style="Toolbutton",)
        self.new_menu_botton_about.grid(row=0,column=column, sticky=(tk.W,))
        column+=1
        
        self.new_menu_botton_language=ttk.Menubutton(parent,direction="below",width=0,text=_(r"语言/language"),style="Toolbutton",)
        self.new_menu_botton_language.grid(row=0,column=column, sticky=(tk.W,))
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
            self.new_var_tk_high_dpi.set(user_configure["high_dpi"])
            
            
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
        if user_configure["tk_scaling_use_flag"] not in (0,1):
            user_configure["tk_scaling_use_flag"] = 0
        self.new_var_tk_scaling_use_flag.set(user_configure["tk_scaling_use_flag"])
            
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
        if user_configure["use_colour_flag"] not in (0,1):
            user_configure["use_colour_flag"] = 0
        self.new_var_tk_use_colour_flag.set( user_configure["use_colour_flag"] )
        
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
        
        m.add_command(label=_("路径设置"), 
                command=self.new_func_menu_call_back_set_file_path
                )
        

        
        m.add_separator()
        
        self.new_var_tk_extra_delay_use_flag = tk.IntVar() # default value 0
        # 初始化,需从配置文件中，读取值
        
        # 范围 
        if user_configure["extra_delay_time_use_flag"] not in (0,1):
            user_configure["extra_delay_time_use_flag"] = 1
        self.new_var_tk_extra_delay_use_flag.set(user_configure["extra_delay_time_use_flag"])
        
        m.add_checkbutton(
                label=_("周边延迟显示"), 
                variable = self.new_var_tk_extra_delay_use_flag ,
                command=self.new_func_menu_call_back_use_extra_delay_time,
                )
        
        m.add_command(label=_("周边延迟时间设置"), 
                command=self.new_func_menu_call_back_set_extra_delay_time
                )
        
        m.add_command(label=_("周边文档，建目录加速"), 
                command=misc_funcs.extra_docs_make_index
                )
    
    def new_func_ui_menu_for_index(self,):
        pass
    
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
        
        
        
        if global_variable.gamelist_type == "softwarelist":
            pass
        else:
            m.add_separator()
            m.add_command(label=_(r"拥有列表 过滤"), 
                    command=misc_funcs.gamelist_available_filter
                    )
        
        
        m.add_separator()
        m.add_command(label=_("选择列表显示项目"),
                command = misc_funcs.header_pop_up_menu_callback_choose_columns
                )
        
        m.add_separator()
        self.new_var_tk_unavailable_mark = tk.IntVar() # default value 0
            # 初始化,需从配置文件中，读取值
        
        # 全局记录 bool
        global_variable.flag_mark_unavailable_game = user_configure["unavailable_mark"]
        
        if user_configure["unavailable_mark"] :# bool
            self.new_var_tk_unavailable_mark.set(1)
            
        m.add_checkbutton(
                label=_(r"标记未拥有"),
                command=self.new_func_menu_call_back_choose_mark_unavailable,
                variable =self.new_var_tk_unavailable_mark,
                )
        
        
        m.add_separator()
        self.new_var_tk_use_local_sort = tk.IntVar() # default value 0
        # 初始化,需从配置文件中，读取值
        if user_configure["use_locale_sort"]:
            self.new_var_tk_use_local_sort.set(1)
        else:
            self.new_var_tk_use_local_sort.set(0)
        
        m.add_checkbutton(label=_("本地排序")+"(" +_("关闭程序，重新打开后生效") +")", 
                variable = self.new_var_tk_use_local_sort ,
                command=self.new_func_menu_call_back_use_local_sort
                )
        


    
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
        
    
    def new_func_ui_menu_for_about(self,):
        #self.new_menu_botton_about
        m = tk.Menu(self.new_menu_botton_about, tearoff=0)
        self.new_menu_botton_about.configure(menu=m)
        
        m.add_separator()
        
        m.add_command(label=_("关于"),
                command=self.new_func_menu_call_back_window_about
                )
        
        m.add_separator()
        
        m.add_command(
                label=_("打开帮助文档：")+the_files.file_html_index, 
                command=self.new_func_menu_call_back_open_html_file
                )
                
        m.add_command(
            label=_("如果帮助文档没有正确打开，可以找到文件，手动打开"), 
            state=tk.DISABLED)
        
        m.add_separator()
        
        m.add_command(
            label   = _("查看当前 python 版本"), 
            command = self.new_func_menu_call_back_show_python_version
            )
    
    
    
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
        window.transient(root_window)
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
                user_configure["theme"] =  the_theme
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
                user_configure["theme"] =  the_theme
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
        temp_string += user_configure["theme"]
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
        user_configure["high_dpi"] = self.new_var_tk_high_dpi.get()
        print()
        print( "high dpi : " )
        print( user_configure["high_dpi"] )

    # 菜单 callback 函数：UI→启用放大倍数
    def new_func_menu_call_back_use_tk_scaling(self,):
        user_configure["tk_scaling_use_flag"] = self.new_var_tk_scaling_use_flag.get()
        print( user_configure["tk_scaling_use_flag"] )
        #if user_configure["tk_scaling_use_flag"]:
        #    root_window.tk.call('tk', 'scaling', user_configure["tk_scaling_number"])
        #    root_window.update()
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
        window.transient(root_window)
        #window.grab_set()
        
        window.columnconfigure(0,weight=1)
        #window.columnconfigure(1,weight=0)
        #window.rowconfigure(0,weight=0)
        
        #num_0 =  self.ini_data["tk_scaling_number"]
        
        ttk.Label(window,text=_("已设定的值为：")+ str(user_configure["tk_scaling_number"]) ).grid(row=0,column=0,sticky=tk.N+tk.W,)
        

        ttk.Label(window,text="").grid(row=1,column=0,sticky=tk.N+tk.W,)
        
        ttk.Label(window,text=_("输入一个大于0的数，整数/小数")).grid(row=2,column=0,sticky=tk.N+tk.W,)

        
        def get_the_number():
            try:
                the_number = input_number.get()
                the_number = eval( the_number )
                if type( the_number ) == int:
                    if the_number > 0 :
                        user_configure["tk_scaling_number"] = the_number
                    else:
                        user_configure["tk_scaling_number"] = 0
                elif type( the_number ) == float :
                    if the_number > 0.01 :
                        user_configure["tk_scaling_number"] = the_number
                    else:
                        user_configure["tk_scaling_number"] = 0
                
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
        a_text.grid(row=5,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        scrollbar_1.grid(row=5,column=1,sticky=(tk.N,tk.S))
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
        if user_configure["row_height"] in range(201):
            chooser.set(user_configure["row_height"])
        else:
            chooser.set(0)
        
        ttk.Label(window,text="").grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
            temp_number = choose_value.get()
            temp_number = int( temp_number )
            print(temp_number)
            
            user_configure["row_height"]=temp_number
            print(user_configure["row_height"])
            
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
        if user_configure["row_height_for_header"] in range(201):
            chooser.set(user_configure["row_height_for_header"])
        else:
            chooser.set(0)
        
        ttk.Label(window,text="").grid(row=4,column=0,sticky=tk.W+tk.N)
        
        def for_ok_button():
            temp_number = choose_value.get()
            temp_number = int( temp_number )
            print(temp_number)
            
            user_configure["row_height_for_header"]=temp_number
            print(user_configure["row_height_for_header"])
            
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
        if user_configure["icon_size"] > 0:
            tkint_var.set(user_configure["icon_size"])
        elif user_configure["icon_size"] == 0:
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
            user_configure["icon_size"] = tkint_var.get()
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
        user_configure["use_colour_flag"] = self.new_var_tk_use_colour_flag.get()
        print( user_configure["use_colour_flag"] )
    
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
        window.transient(root_window)
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
        
        #user_configure
        
        data ={}
        
        def for_ok_button():

            for x in data:
                if x in user_configure:
                    user_configure[x] = data[x].get()
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
            if temp_string in default_configure:
                tk_var.set( default_configure[temp_string] )
            

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
        # mame
        ttk.Label(frame1,text=_("mame 模拟器 路径")).grid(row=0,column=0,sticky=tk.W+tk.N,)
        
        data["mame_path"]=tk.StringVar()
        entry_mame_path = ttk.Entry(frame1,textvariable=data["mame_path"],state="disabled")
        entry_mame_path.grid(row=0,column=1,sticky=tk.W+tk.N+tk.E,)
        data["mame_path"].set( user_configure["mame_path"] )
        
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
        data["mame_working_directory"].set( user_configure["mame_working_directory"] )
        
        button_mame_working_directory_default=ttk.Button(frame1,text=r"默认值",width=-1,state="disabled",command=lambda a=data["mame_working_directory"],b="mame_working_directory" : set_default_value(a,b),)
        button_mame_working_directory_default.grid(row=1,column=2,sticky=tk.W+tk.N,)
        
        ttk.Button(frame1,text=_("修改"),width=-1,command=change_mame_working_directory ).grid(row=1,column=3,sticky=tk.W+tk.N,)        
        
        n=2
        
        ttk.Label(frame1,text="").grid(row=n,column=0,columnspan=5,sticky=tk.W+tk.N,)
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
        
        data["folders_path"].set( user_configure["folders_path"] )
        
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
        # 路径变量名 user_configure["snap_path"]
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
            
            data[temp_str].set( user_configure[temp_str] )
            
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
        #路径变量名 user_configure["snap.zip_path"]
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
            
            data[temp_str].set( user_configure[temp_str] )
            
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
        
        temp_types = sorted(temp_types)
        
        #文档名 command.dat
        #路径变量名 user_configure["command.dat_path"]
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
            
            data[temp_str].set( user_configure[temp_str] )
            
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
        user_configure["extra_delay_time_use_flag"] = self.new_var_tk_extra_delay_use_flag.get()
        
        print( user_configure["extra_delay_time_use_flag"] )
    
    # 设置→周边延迟 时间设置
    def new_func_menu_call_back_set_extra_delay_time(self,):
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("周边延迟时间设置"))
        
        #size = "400x300"
        #window.geometry( size )
        
        window.lift()
        window.transient(root_window)
        window.columnconfigure(0,weight=1)
        
        delay_time = user_configure["extra_delay_time"]
        
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
            user_configure["extra_delay_time"] = tkint_var.get()
            print( user_configure["extra_delay_time"] )
        
        ok_button = ttk.Button(window,text=_("确定"),command=for_ok_button)
        ok_button.grid()
        
        
        window.wait_window()

    # 游戏列表
    def new_func_menu_call_back_choose_mark_unavailable(self,):
        if self.new_var_tk_unavailable_mark.get():
            user_configure["unavailable_mark"] = True
            global_variable.flag_mark_unavailable_game = True
        else:
            user_configure["unavailable_mark"] = False
            global_variable.flag_mark_unavailable_game = False

    #游戏列表→使用本地排序
    def new_func_menu_call_back_use_local_sort(self,):
        if self.new_var_tk_use_local_sort.get():
            user_configure["use_locale_sort"] = True
            
            if global_variable.flag_setlocale_LC_COLLATE == False :
                try:
                    locale.setlocale(locale.LC_COLLATE,locale= user_configure["locale_name"] )
                    global_variable.flag_setlocale_LC_COLLATE = True
                except:
                    global_variable.flag_setlocale_LC_COLLATE = False
            
            
        else:
            user_configure["use_locale_sort"] = False
            
            global_variable.flag_setlocale_LC_COLLATE = False
            
        print( user_configure["use_locale_sort"] )

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
             
        about_window.transient(root_window)
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
            "需要的游戏文件，也要靠自己找" + "\n"                  ,
            
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
            "简单是简单了一点，也可能还丑了点" + "\n"              ,
            
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
            
            "大家，各位街机游戏爱好者，可以免费使用" + "\n"        ,
            #"bros,it's free for use" + "\n"        ,            
            "\n"                                                  ,
            "本人在琵琶行(www.ppxclub.com)的 ID ：gdicnng" + "\n"                   ,
            #"my ID in ppxclub.com ：gdicnng" + "\n"                   ,
            r"www.ppxclub.com/forum.php?mod=viewthread&tid=705838"+"\n",
            r"www.ppxclub.com/705838-1-1"+"\n",
            "\n",
            "邮箱：gdicnng@sina.com" + "\n"                       ,
            #"email：gdicnng@sina.com" + "\n"                       ,
            "\n",
            "源代码：https://gitee.com/gdicnng/JJui" + "\n"       ,
            "源代码：https://github.com/gdicnng/JJui" + "\n"       ,
            
            "\n"       ,
            "一开始上传到 gitee ，因为国内的网络连接要好一点" + "\n"       ,
            "gitee  现在似乎 比较麻烦" + "\n"       ,
            "github 国内外网络连接一直不好太好" + "\n"       ,
            "现在可能随意上传一个，或者有时候懒得上传了" + "\n"       ,
            
            
            #"source file：https://gitee.com/gdicnng/JJui" + "\n"       ,
            #"之前是上传到 gitee 的，公开的" + "\n"       ,
            #"但是听说监管比较严了，连源代码都要管了" + "\n"       ,
            

            
            "\n",


            "第一次上传时间： 2021年06月" + "\n"                   ,
            #"the first version time is  2021 06" + "\n"                   ,
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
        scrollbar_1.grid(row=0,column=1,columnspan=2,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        t.insert("1.0", text, )
        
        try:
            print(the_files.image_path_zhifubao)
            image_zhifubao = Image.open( the_files.image_path_zhifubao )
            #image_weixin = Image.open(   self.data_from_main['image_path_weixin'])
            
            size_1=image_zhifubao.size
            a=800/size_1[0]
            new_size_1 = (int(size_1[0]*a),int(size_1[1]*a))
            
            image_zhifubao = image_zhifubao.resize( new_size_1,Image.BILINEAR, )
            image_zhifubao = ImageTk.PhotoImage( image_zhifubao  )
            
            #size_2=image_weixin.size
            #b=800/size_2[0]
            #new_size_2 = ( int(size_2[0]*b),int(size_2[1]*b))
            
            #image_weixin = image_weixin.resize( new_size_2,Image.BILINEAR, )
            #image_weixin = ImageTk.PhotoImage( image_weixin )
            
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
    
    def new_func_menu_call_back_show_python_version(self,):
        python_version  = str(sys.version)
        tkinter_version = str(tk.TkVersion)
        #pillow_version  = ""
        
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        size = "400x600" 
        window.geometry(size)
        
        window.title(_("查看 python 版本"))
        
             
        window.transient(root_window)
        window.lift()
        
        ttk.Label(window,text="").grid(sticky=tk.W)
        ttk.Label(window,text=_("python 版本：")  + python_version).grid(sticky=tk.W)
        
        ttk.Label(window,text="").grid(sticky=tk.W)
        ttk.Label(window,text=_("tkinter 版本：") + tkinter_version).grid(sticky=tk.W)
        #ttk.Label(window,text=_("Pillow 版本：") + "").grid()
        
        
        
        window.wait_window()



    # 菜单 callback 函数：保存设置
    def new_func_save_user_configure(self,):
        misc_funcs.save_user_configure()
    
    def new_func_save_user_configure_with_window_size(self,):
        misc_funcs.save_user_configure_with_window_size()
        
    def new_func_save_user_configure_with_window_size_and_position(self,):
        misc_funcs.save_user_configure_with_window_size_and_position()