# -*- coding: utf_8_sig-*-
"""
    Text_container ：
    
        --------------------------
        |  种类选择器  | 使用目录 |
        |-------------------------|
        |    子目分类             |
        |------------------------|
        |                        |
        |    内容                |
        |                        |
        |    ( Text_area )       |
        |                        |
        |                        |
        |                        |
        |                        |
        --------------------------
    
"""
import sys
import os
#import time

import tkinter as tk
import tkinter.ttk as ttk

#from PIL import Image, ImageTk

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation



#from . import global_static_filepath as the_files
from . import global_static
from . import global_static_key_word_translation 
from . import global_variable

from . import extra_read_history_xml
from . import extra_mameinfo_dat
from . import extra_history_dat
from . import extra_gameinit_dat
from . import extra_command
from . import extra_command_english



user_configure       = global_variable.user_configure_data
#clone_to_parent      = global_variable.dict_data['clone_to_parent']

text_types          = global_static.extra_text_types
text_types_2        = global_static.extra_text_types_2
    # ("snap","titles","flyers",......)
key_word_translation   = global_static_key_word_translation.extra_text_types_translation
key_word_translation_2 = global_static_key_word_translation.extra_text_types_2_translation


# 变量前缀
# self.new_ui_
# self.new_var_
# self.new_func_


class Text_area(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_func_ui()
        self.new_func_ui_popup_menu()
        self.new_func_bindings()
        
        
    def new_func_ui(self,):
        parent=self
        
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        self.new_ui_text = tk.Text(
                    parent,
                    borderwidth        = 0,
                    highlightthickness = 0,
                    takefocus = False,
                    undo      = False,
                    state     = tk.DISABLED,
                    wrap      = "char",
                    )
        self.new_ui_scrollbar_v = ttk.Scrollbar( parent, orient=tk.VERTICAL, command=self.new_ui_text.yview)
        
        self.new_ui_text.configure(yscrollcommand=self.new_ui_scrollbar_v.set)
        
        self.new_ui_text.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.new_ui_scrollbar_v.grid(row=0,column=1,sticky=(tk.N,tk.S))
        
        parent.rowconfigure(1, weight=0)
        
        #
        
        self.new_ui_scrollbar_h = ttk.Scrollbar( parent, orient=tk.HORIZONTAL , command=self.new_ui_text.xview)
            
        self.new_ui_text.configure(xscrollcommand=self.new_ui_scrollbar_h.set)
            
        #self.new_ui_scrollbar_h.grid(row=1,column=0,columnspan=2,sticky=(tk.W,tk.E))
        
        ""
    
    def new_func_ui_popup_menu(self,):
        # 右键菜单
        self.new_ui_index_popup_menu = tk.Menu(self.new_ui_text, tearoff=0)
        
        self.new_ui_index_popup_menu.add_command(label=_("不换行"),
                command = self.new_func_wrap_by_none
                )
        
        self.new_ui_index_popup_menu.add_command(label=_("以词换行"),
                command = self.new_func_wrap_by_word
                )
        
        self.new_ui_index_popup_menu.add_command(label=_("以字符换行"),
                command = self.new_func_wrap_by_char
                )
        
        #self.new_ui_index_popup_menu.add_command(label=_("显示横向进度条"),
        #        command = self.new_func_show_scrollbar_h
        #        )
        #
        #self.new_ui_index_popup_menu.add_command(label=_("关闭横向进度条"),
        #        command = self.new_func_close_scrollbar_h
        #        )
        
        ""
    
    def new_func_bindings(self,):
        ""
        # 右键菜单
        self.new_ui_text.bind('<ButtonPress-3>',self.new_func_bindings_right_click_to_show_menu)
    
    def new_func_bindings_right_click_to_show_menu(self,event):
        try:
            self.new_ui_index_popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.new_ui_index_popup_menu.grab_release()

    def new_func_insert_string(self,a_string=''):
        self.new_ui_text.configure(state="normal")
        
        self.new_ui_text.insert(tk.END,a_string)
        
        self.new_ui_text.configure(state="disabled")

    def new_func_wrap_by_none(self,):
        self.new_ui_text.configure(wrap="none")
        
        self.new_func_show_scrollbar_h()
    
    def new_func_wrap_by_char(self,):
        self.new_ui_text.configure(wrap="char")
        
        self.new_func_close_scrollbar_h()
    
    def new_func_wrap_by_word(self,):
        self.new_ui_text.configure(wrap="word")
        
        self.new_func_close_scrollbar_h()
    
    def new_func_show_scrollbar_h(self,):
        if not self.new_ui_scrollbar_h.winfo_ismapped():
            self.new_ui_scrollbar_h.grid(row=1,column=0,columnspan=2,sticky=(tk.W,tk.E))
    
    def new_func_close_scrollbar_h(self,):
        if self.new_ui_scrollbar_h.winfo_ismapped():
            self.new_ui_scrollbar_h.grid_forget()




class Text_container(ttk.Frame):
    
    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "extra_text_1"
        
        self.new_var_virtual_event_name_CurrentGame=r'<<CurrentGame>>'
            # 不在这里用这个了
        
        self.new_var_remember_text_type = None
        
        self.new_func_ui()
        self.new_func_bindings()
        self.new_func_initialize()
        
    def new_func_ui(self,):
        parent = self
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=0)
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
        # 第一行 选择栏
        self.new_var_string_for_text_chooser = tk.StringVar()
        self.new_ui_text_chooser = ttk.Combobox( parent ,takefocus=False,textvariable=self.new_var_string_for_text_chooser,state="readonly")
        self.new_ui_text_chooser.grid(row=0 , column=0 ,columnspan=2, sticky=(tk.W,tk.N,tk.E,),)
        
        # 第一行 标记 ：创建目录 
        self.new_var_index_flag = tk.IntVar()
        self.new_ui_index_checkbutton = ttk.Checkbutton( parent ,
                takefocus=False,
                text=_("建目录"),
                variable=self.new_var_index_flag,
                )
        #self.new_ui_index_checkbutton.grid(row=0 , column=1 ,columnspan=2, sticky= (tk.N,tk.E, ),)
        
        
        # 第二行 选择栏 2
        self.new_var_string_for_chooser_2 = tk.StringVar()
        self.new_ui_chooser_2 = ttk.Combobox( parent ,takefocus=False,textvariable=self.new_var_string_for_chooser_2,state="readonly")
        self.new_ui_chooser_2.grid(row=1 , column=0 , columnspan=2,sticky=(tk.W,tk.N,tk.E,),)
        
        
        # 第三行 文本显示区
        self.new_ui_text_area = Text_area(parent)
        self.new_ui_text_area.grid(row=2 , column=0 ,columnspan=2, sticky=(tk.W,tk.N,tk.E,tk.S),)
    
    #### ??
    def new_func_bindings(self,):
        #self.new_ui_image_chooser.bind(r"<<ComboboxSelected>>",self.new_func_for_virtual_event_of_combobox)
        
        #self.bind_all(self.new_var_virtual_event_name_CurrentGame,self.new_func_bindings_receive_virtual_event,"+")
            # 不在这里用这个
        ""
    
    def new_func_initialize(self,):
        
        # 记录
        global_variable.Combobox_chooser_text_1 = self.new_ui_text_chooser
        
        global_variable.tkint_flag_for_text_index_1 = self.new_var_index_flag
        self.new_var_index_flag.set( user_configure["extra_text_make_index_1"] )
        
        # 记录 
        global_variable.tk_text_1 = self.new_ui_text_area.new_ui_text
        
        
        temp=[]
        for x in text_types:
            if x in key_word_translation:
                temp.append(key_word_translation[x])
            else:
                temp.append(x)
        self.new_ui_text_chooser["values"]= temp
        
        try: # 读取配置文件中 记录的 index
            n = user_configure["extra_text_chooser_index"] 
            if n < len(text_types):
                pass
            else:
                n=0
            self.new_ui_text_chooser.set( temp[n] )
        except:
            self.new_ui_text_chooser.set( temp[0] )
        
        self.new_func_get_info_from_choice()# 初始数据读取
    
    def new_func_insert_string(self,a_string = ""):
        self.new_ui_text_area.new_ui_text.configure(state="normal")
        
        self.new_ui_text_area.new_ui_text.insert(tk.END,a_string)
        
        self.new_ui_text_area.new_ui_text.configure(state="disabled")
    
    def new_func_clear_chooer(self,):
        self.new_ui_chooser_2["values"]=("",)
        self.new_ui_chooser_2.set("") 
    
    def new_func_clear_content(self,):
        self.new_ui_text_area.new_ui_text.configure(state="normal")
        
        self.new_ui_text_area.new_ui_text.delete('1.0',tk.END)
        
        self.new_ui_text_area.new_ui_text.configure(state="disabled")

    # ??
    def new_func_get_info_from_choice(self,):

        number_index = self.new_ui_text_chooser.current()
        
        
        text_type = text_types[number_index]
        
        #
        self.new_var_remember_text_type = text_type
    

    # 用这个
    def new_func_show(self,item_id):
        
        if item_id != global_variable.current_item : return 
        
        # 清理选择框
        self.new_func_clear_chooer()
        
        # 清理文本区
        self.new_func_clear_content()
        
        if self.new_ui_text_area.winfo_viewable():
            #if self.new_var_index_flag.get():
            
            # 是否创建目录 加速
            
            n = self.new_ui_text_chooser.current()
            temp = text_types[n]
            
            if temp == "history.xml":
                self.new_func_show_history_xml(item_id)
            elif temp in ("mameinfo.dat","messinfo.dat",):
                self.new_func_show_mameinfo_dat(temp,item_id)
            elif temp in ("history.dat","sysinfo.dat",):
                self.new_func_show_history_dat(temp,item_id)
            elif temp in ("gameinit.dat",):
                #show_gameinit_dat(self,type,game_name)
                self.new_func_show_gameinit_dat(temp, item_id)
            

    def new_func_show_history_xml(self,game_name):

        path = user_configure["history.xml_path"]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号
        
        if not os.path.isfile(path) : return
        
        if game_name != global_variable.current_item : return
        
        new_text = ''
        
        def get_content(path,game_name):
            text = extra_read_history_xml.getinfo(path,game_name)
            return text
            
        new_text = get_content(path,game_name)
        
        if not new_text : return 
        
        if game_name == global_variable.current_item :
                self.new_func_insert_string(new_text)

    # ("mameinfo.dat","messinfo.dat",)
    def new_func_show_mameinfo_dat(self,data_type,game_name):
        # 有属于 游戏 的文档
        # 还有，属于，驱动的文档
        
        # 分隔线 
        line_separator = "*"*5 +" " + "*"*5 + "\n"
        
        data_type =  data_type + "_path" 
        # path = self.ini_data[ "mameinfo.dat_path" ]
        # path = self.ini_data[ "messinfo.dat_path" ]
        path = user_configure[ data_type ]
        
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        print(path)
        
        if not os.path.isfile(path): return
        
        new_text = None # 记录该游戏的文档,读取内容后，是 []  ，
        if game_name == global_variable.current_item:
            text = extra_mameinfo_dat.get_content_by_file_name(path,game_name)
            if text is not None:
                new_text = text
                
        new_text_2 = None # 记录该游戏所属 驱动 的文档,[]
        
        if game_name != global_variable.current_item: return
        
        try:
            game_info = global_variable.machine_dict[game_name]
            sourcefile = game_info[ global_variable.columns_index["sourcefile"] ]
        except:
            sourcefile = None
        
        if sourcefile:
            text = extra_mameinfo_dat.get_content_by_file_name(path,sourcefile)
            if text is not None:
                new_text_2 = text
        
        if game_name != global_variable.current_item: return

        flag1 = False
        flag2 = False
        if new_text is not None : flag1 = True
        if new_text_2 is not None : flag2 = True
        
        if flag1:
            self.new_func_insert_string(line_separator)
            self.new_func_insert_string(game_name)
            self.new_func_insert_string("\n")
            self.new_func_insert_string(line_separator)
            self.new_func_insert_string("\n")
            self.new_func_insert_string("\n")
            
            
            for x in new_text:
                self.new_func_insert_string(x)
            
            self.new_func_insert_string("\n")
                
        if flag2:
            self.new_func_insert_string(line_separator)
            self.new_func_insert_string("\n")
                 
            self.new_func_insert_string(sourcefile)
            self.new_func_insert_string("\n")
                 
            self.new_func_insert_string("\n")
            self.new_func_insert_string(line_separator)
                 
            self.new_func_insert_string("\n")
            self.new_func_insert_string("\n")
            
            for x in new_text_2:
                self.new_func_insert_string(x)

    # ("history.dat","sysinfo.dat",)
    def new_func_show_history_dat(self,data_type,game_name):

        data_type =  data_type + "_path" # "history.dat_path"
        
        path = user_configure[ data_type ]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        if os.path.isfile(path):
        
            new_text = []
        
            if game_name == global_variable.current_item:
                text = extra_history_dat.get_content_by_file_name(path,game_name)
                if text is not None:
                    new_text = text
        
            # if new_text == '':
            #     if game_name == self.tree.focus():
            #         # 再找主版本
            #         print("try parent")
            #         if game_name in self.data['dict_data']['clone_to_parent']:
            #             parent_name = self.data['dict_data']['clone_to_parent'][game_name]
            #             text = extra_history_dat.get_content_by_file_name(path,parent_name)
            #             if text is not None:
            #                 new_text = text

            if game_name == global_variable.current_item:
                for x in new_text:
                    self.new_func_insert_string(x)

    # ("gameinit.dat",)
    def new_func_show_gameinit_dat(self,data_type,game_name):
        
        data_type =  data_type + "_path" # "gameinit.dat_path"
        
        path = user_configure[ data_type ]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        if os.path.isfile(path):
        
            new_text = []
        
            if game_name == global_variable.current_item:
                text = extra_gameinit_dat.get_content_by_file_name(path,game_name)
                if text is not None:
                    new_text = text
                    
            # 主版本 ？，算了，不管
            
            if game_name == global_variable.current_item:
                for x in new_text:
                    self.new_func_insert_string(x)



class Text_container_2(Text_container):
    def __init__(self ,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.new_var_ui_type = "extra_text_2"
    
    
    def new_func_initialize(self,):
        
        
        # 记录
        global_variable.Combobox_chooser_text_2 = self.new_ui_text_chooser
        
        global_variable.tkint_flag_for_text_index_2 = self.new_var_index_flag
        self.new_var_index_flag.set( user_configure["extra_text_make_index_2"] )
        
        # 记录 
        global_variable.tk_text_2 = self.new_ui_text_area.new_ui_text
        
        #print()
        #print(text_types_2)
        #print(key_word_translation_2)
        temp=[]
        for x in text_types_2:
            if x in key_word_translation_2:
                temp.append(key_word_translation_2[x])
            else:
                temp.append(x)
        self.new_ui_text_chooser["values"]= temp
        #print(temp)
        
        try: # 读取配置文件中 记录的 index
            n = user_configure["extra_command_type_chooser_index"] 
            if n < len(text_types_2):
                pass
            else:
                n=0
            self.new_ui_text_chooser.set( temp[n] )
        except:
            self.new_ui_text_chooser.set( temp[0] )
        
        self.new_func_get_info_from_choice()# 初始数据读取
    
    def new_func_bindings(self,):
        super().new_func_bindings()
        self.new_ui_chooser_2.bind("<<ComboboxSelected>>",self.new_func_binding_command_index_choose) 
    
    
    # 用这个
    def new_func_show(self,item_id):
        
        print("text 2")
        
        if item_id != global_variable.current_item : return 
        
        # 清理选择框
        self.new_func_clear_chooer()
        
        # 清理文本区
        self.new_func_clear_content()
        
        if self.new_ui_text_area.winfo_viewable():
            #if self.new_var_index_flag.get():
            
            # 是否创建目录 加速
            
            n = self.new_ui_text_chooser.current()
            temp = text_types_2[n]
            
            self.new_func_show_command_dat(temp,item_id)
    
    def new_func_show_command_dat(self,data_type,game_name):
    
        print("show command")
        
        
        path = data_type + "_path" # "command.dat_path"
        path = user_configure[path]
        path = path.replace(r"'","") # 去掉单引号
        path = path.replace(r'"',"") # 去掉双引号 
        
        print(path)
        
        if not os.path.isfile(path):
            #self.new_ui_chooser_2["values"]=("",)
            #self.new_ui_chooser_2.set("")
            return 0 
            # 如果，文档，不存在，直接退出函数
        
        # 初始化
        try:
            self.new_var_command_content
        except:
            self.new_var_command_content =  None 

        # 读取内容
        
        # 中文版，英文版 ，格式不同
        
        try:
            if data_type == "command.dat":
                self.new_var_command_content = extra_command.get_content_by_file_name( path,game_name )
            elif data_type == "command_english.dat":
                self.new_var_command_content = extra_command_english.get_content_by_file_name( path,game_name )
        except:
            self.new_var_command_content =  None 
        
        
        if self.new_var_command_content is None:
            self.new_ui_chooser_2["values"]=("",)
            self.new_ui_chooser_2.set("") 
        elif len(self.new_var_command_content) <= 1:
            #print(r"<=1")
            self.new_ui_chooser_2["values"]=(_("全部"),)
            self.new_ui_chooser_2.set( _("全部") ) 
            for x in self.new_var_command_content:
                for y in self.new_var_command_content[x]:
                    self.new_func_insert_string( y)
        else:
            #print(r">1")
            index = []
            index.append( _("全部") )
            for x in self.new_var_command_content:
                # 提取 每一段 第一行，做为小标题
                try:
                    index.append( self.new_var_command_content[x][0] )
                except:
                    index.append("")
            self.new_ui_chooser_2["values"]=index
            self.new_ui_chooser_2.set( _("全部") ) 
            
            for x in self.new_var_command_content:
                for y in self.new_var_command_content[x]:
                    self.new_func_insert_string( y)

    def new_func_binding_command_index_choose(self,event):

        try:
            self.new_var_command_content
        except:
            self.new_func_clear_content() 
            # 清空内容
            
            return 0 
            # 如果还没有 数据 记录
            # 退出函数
        
        if self.new_var_command_content is None:
            self.new_func_clear_content() 
            # 清空内容
            
            return 0 
            # 退出函数
        
        
        n = self.new_ui_chooser_2.current()
        
        if n==0:
            self.new_func_clear_content() 
            try:
                for x in self.new_var_command_content:
                    for y in self.new_var_command_content[x]:
                        self.new_func_insert_string( y)
            except:
                pass
        else:
            self.new_func_clear_content() 
            try:
                for x in self.new_var_command_content[n]:
                    self.new_func_insert_string( x)
            except:
                pass
    


if __name__ == "__main__" :
    
    root=tk.Tk()
    root.geometry('800x600')
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    

    
    #a=Text_with_scrollbar(root)
    a=Text_container(root)
    a.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S))
    
    
    for x in range(10):
        a.new_func_insert_string("test "*30+"\n")     
    
    for x in range(1000):
        a.new_func_insert_string(str(x) + " : "+"test\n") 
    
    root.mainloop()








