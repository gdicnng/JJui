# -*- coding: utf_8_sig-*-
#import sys
import os
import sys
import subprocess
import re
import glob

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font as tkfont

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation

from . import global_variable
from . import global_static_filepath as the_files
from . import global_static_key_word_translation as key_word_translation


from . import read_user_config 
from . import save_pickle 
from . import read_pickle 
from . import translation_gamelist 


user_configure = global_variable.user_configure_data
root_window    = global_variable.root_window
root           = global_variable.root_window
columns_translation = key_word_translation.columns_translation


class Misc_functions():
    
    ######################
    ######################
    # 打开游戏
    #   接收信号
    #   "<<StartGame>>"
    def start_game(self,event):
        print()
        print(r"virtual event received <<StartGame>>")
        
        widget = event.widget
        emu_number   = widget.new_var_data_for_StartGame["emu_number"]
        game_type    = widget.new_var_data_for_StartGame["type"] # "mame" ,"softwarelist"
        game_id      = widget.new_var_data_for_StartGame["id"]
        other_option = widget.new_var_data_for_StartGame["other_option"]
        hide         = widget.new_var_data_for_StartGame["hide"]
        
        
        print("game_id   :{}".format(game_id))
        print("game_type :{}".format(game_type))
        
        if game_type == "mame":
            if emu_number   == -1 : # 默认 MAME
                self.call_mame( game_id, other_option, hide)
            elif emu_number in( 1,2,3,4,5,6,7,8,9):
                self.get_other_emu_configure(game_id,emu_number)
        
        elif game_type == "softwarelist":
            if emu_number   == -1 : # 默认 值
                emu_number = 1 # 跳转到第1组设置
            
            if emu_number   == -1:
                pass
            elif emu_number in (1,2,3,4,5,6,7,8,9,):
                self.get_other_emu_configure_sl(game_id,emu_number)
    
    # MAME
    def call_mame(self,game_name,other_option=None,hide=True):
        print()
        print("call_mame")
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()

        print("mame_exe:\n\t{}".format(mame_exe))
        print("mame_working_directory:\n\t{}".format(mame_dir))

        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_name )
        
        if other_option:
            for x in other_option:
                command_list.append( x )
        
        print()
        print( command_list )
        
        if hide: # 打开游戏，影藏 UI
            #self.parent.iconify()
            root_window.withdraw()
            
            proc = subprocess.Popen(
                    command_list,
                    shell=user_configure["use_shell"],
                    cwd=mame_dir
                    )
            
            proc.wait()
            root_window.deiconify()
            
            # 列表要不要刷新一下？
            #root_window.wait_visibility()
            #root_window.update()
                # 不能刷新太早了
                # 太早，不可见时，设置的　刷新无效
                # 算了，直接把 列表刷新的条件 table.winfo_viewable() 去掉
            
            #global_variable.the_showing_table.new_func_refresh_table()
            
            ""
        else: # 打开游戏，保留 UI
            proc = subprocess.Popen(
                    command_list, 
                    shell=user_configure["use_shell"],
                    cwd=mame_dir)
    
    def get_mame_path_and_working_directory(self,):
    # mame_exe
    # mame_dir
    #   用于 subprocess.Popen 函数
    
        # 如果存在此文件，设为绝对值
        # 如果不存在此文件，当成 ，它 在 系统 环境变量 里
        if os.path.isfile( user_configure["mame_path"] ):
            mame_exe = os.path.abspath( user_configure["mame_path"] )
        else:
            mame_exe = user_configure["mame_path"]
    
        mame_working_directory = None # 默认值
        
        # 如果已设置
        #if user_configure["mame_working_directory"] :
        if os.path.isdir( user_configure["mame_working_directory"] ):
            mame_working_directory = os.path.abspath( user_configure["mame_working_directory"] )
        # 默认值
        #   如果值 没有 设置 ，为空
        #   自动设置为 mame 所在文件夹
        else:
            #user_configure["mame_working_directory"] == "" :
            if os.path.isfile( user_configure["mame_path"] ):
                temp                   = os.path.dirname( user_configure["mame_path"] )
                mame_working_directory = os.path.abspath( temp )
                

        
        return (mame_exe , mame_working_directory)
    
    def get_other_emu_configure(self,item_id,emu_number):
        
        # item_id 为 machine
        # emu_number
        machine      = item_id

        mame_exe , mame_working_directory = self.get_mame_path_and_working_directory()
        
        the_folder = the_files.emulator_configure_folder
        the_file   = os.path.join(the_folder,str(emu_number)+".txt")
        # xxxxx\1.txt
        # xxxxx\2.txt
        
        print(the_folder)
        print(the_file)
        
        ##############
        
        if not os.path.isfile(the_file):
            return
        
        
        command_list = []
        cwd = None
        flag_use_mame = False # 如果用了 mame ，cwd 需要考虑原有值
        
        
        file_content=[]
        with open(the_file,mode="rt",encoding="utf_8_sig") as f:
            for line in f :
                file_content.append(line)
        
        # 自定义部分不要包含空字符，方便后面处理
        #   用户定义部分，中间，可以含空字符，末尾空字符去掉
        #
        # %mame% ，不管内容，替换为 mame_exe
        # %machine% ，不管内容，替换为 machine
        #
        # command 普通指令
        #
        # %cwd% ，换到内容，如果有效，替换为 cwd
        
        # 正则
        
        #空行
        str_empty =r'^\s*$'
        p_empty = re.compile( str_empty , )
        
        # 以空字符分隔
        # 内容 
        #   不含 \s
        str_1 = r'^\s*([^\s]+)\s*$'
        p=re.compile(str_1,)
        
        # 内容2
        #   含 \s
        str_2 = r'^\s*([^\s]+)\s*([^\s].*?)\s*$'
        p2=re.compile(str_2,)
        
        for line in file_content:
            # 空行测试
            m=p_empty.search( line ) 
            if m : 
                continue
                
            # 内容行 1 
            m=p.search( line )
            if m:
                if m.group(1)   == r"%mame%" :
                    command_list.append(mame_exe)
                    flag_use_mame = True
                elif m.group(1) == r"%machine%" :
                    command_list.append(machine)
                continue

            # 内容行 2
            m=p2.search( line )
            if m:
                if   m.group(1) == "command" : 
                    command_list.append(m.group(2))
                elif m.group(1) == r"%cwd%" : 
                    if os.path.isdir(m.group(2)):
                        cwd = m.group(2)
                
                elif m.group(1) == r"%mame%"     : 
                    command_list.append(mame_exe)
                    flag_use_mame = True
                elif m.group(1) == r"%machine%"      : command_list.append(machine)
        
        # 如果用了 mame
        if flag_use_mame == True:
            if not cwd:
                cwd = mame_working_directory
        
        if not command_list : return
        
        print(command_list)
        print(cwd)
        
        # start game
        root_window.withdraw()
        proc = subprocess.Popen(
                command_list,
                shell=user_configure["use_shell"],
                cwd=cwd
                )
        
        proc.wait()
        root_window.deiconify()
    
    def get_other_emu_configure_sl(self,item_id,emu_number):
        
        # item_id 为 xml + name
        # emu_number
        xml      = item_id.split(" ",1)[0]
        software = item_id.split(" ",1)[1]
        print()
        
        mame_exe , mame_working_directory = self.get_mame_path_and_working_directory()
        
        the_folder = the_files.emulator_configure_folder_sl
        the_file   = os.path.join(the_folder,xml,str(emu_number)+".txt")
        # xxxxx\nes\1.txt
        # xxxxx\nes\2.txt
        
        print(the_folder)
        print(the_file)
        
        ##############
        
        if not os.path.isfile(the_file):
            return
        
        
        command_list = []
        cwd = None
        flag_use_mame = False # 如果用了 mame ，cwd 需要考虑原有值
        
        
        
        file_content=[]
        with open(the_file,mode="rt",encoding="utf_8_sig") as f:
            for line in f :
                file_content.append(line)
        
        # 自定义部分不要包含空字符，方便后面处理
        #   用户定义部分，中间，可以含空字符，末尾空字符去掉
        #
        # %mame% ，不管内容，替换为 mame_exe
        # %xml% ，不管内容，替换为 xml
        # %software% ，不管内容，替换为 software
        # %xml:software% 不管内容，替换为 xml + : + software
        #
        # command 普通指令
        #
        # %cwd% ，换到内容，如果有效，替换为 cwd
        
        # 正则
        
        #空行
        str_empty =r'^\s*$'
        p_empty = re.compile( str_empty , )
        
        # 以空字符分隔
        # 内容 
        #   不含 \s
        str_1 = r'^\s*([^\s]+)\s*$'
        p=re.compile(str_1,)
        
        # 内容2
        #   含 \s
        str_2 = r'^\s*([^\s]+)\s*([^\s].*?)\s*$'
        p2=re.compile(str_2,)
        
        for line in file_content:
            # 空行测试
            m=p_empty.search( line ) 
            if m : 
                continue
                
            # 内容行 1 
            m=p.search( line )
            if m:
                if m.group(1)   == r"%mame%"     : 
                    command_list.append(mame_exe)
                    flag_use_mame = True
                elif m.group(1) == r"%xml%"      : command_list.append(xml)
                elif m.group(1) == r"%software%" : command_list.append(software)
                elif m.group(1) == r"%xml:software%" : command_list.append(xml+r":"+software)
                continue

            # 内容行 2
            m=p2.search( line )
            if m:
                if   m.group(1) == "command" : 
                    command_list.append(m.group(2))
                elif m.group(1) == r"%cwd%" : 
                    if os.path.isdir(m.group(2)):
                        cwd = m.group(2)
                
                elif m.group(1) == r"%mame%"     : 
                    command_list.append(mame_exe)
                    flag_use_mame = True
                elif m.group(1) == r"%xml%"      : command_list.append(xml)
                elif m.group(1) == r"%software%" : command_list.append(software)
                elif m.group(1) == r"%xml:software%" : command_list.append(xml+r":"+software)
        
        # 如果用了 mame
        if flag_use_mame == True:
            if not cwd:
                cwd = mame_working_directory
        
        
        if not command_list :return
        
        print(command_list)
        print(cwd)
        
        # start game
        root_window.withdraw()
        proc = subprocess.Popen(
                command_list,
                shell=user_configure["use_shell"],
                cwd=cwd
                )
        
        proc.wait()
        root_window.deiconify()
    
    ###############
    ###############
    # 显示信息 ：校验roms、显示 roms 信息等
    #   接收信号
    #   "<<MameShowInfo>>"    
    def mame_show_info(self,event):
        print()
        print(r"virtual event received <<MameShowInfo>>")
        
        
        
        widget = event.widget
        
        #game_type    = widget.new_var_data_for_StartGame["type"]
        game_id      = widget.new_var_data_for_StartGame["id"]
        other_option = widget.new_var_data_for_StartGame["other_option"]
        #hide         = widget.new_var_data_for_StartGame["hide"]
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( game_id )
        
        if other_option:
            for x in other_option:
                command_list.append( x )
                
        
        content=[]
        p = subprocess.Popen( command_list, 
                            shell=user_configure["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8",
                            cwd=mame_dir,
                            )
        for line in p.stdout:
            #print(line,end='')
            content.append(line)
        
        temp_string = " "
        if len(other_option)>=1:
            try:
                temp_string = str(other_option[0])
            except:
                temp_string = " "
        
        
        self.show_text_winodw(content=content,title=temp_string,)
    
    # top level window, 显示文本信息
    def show_text_winodw(self,content=None,title="",):
        
        if content is None: content =[]
        
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        if title:    
            window.title(title)
            
        size  = "400x300"
        #size += self.get_root_window_x_y()
        window.geometry(size)
        
        window.transient(root)
        window.lift()
        #window.grab_set()
        
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        t = tk.Text(window,undo=False,padx=10,pady=10,spacing1=2,spacing2=2,spacing3=2)
        
        scrollbar_1 = ttk.Scrollbar( window, orient=tk.VERTICAL, command=t.yview)
        
        scrollbar_2 = ttk.Scrollbar( window, orient=tk.HORIZONTAL, command=t.xview)
        
        t.configure(yscrollcommand=scrollbar_1.set)
        t.configure(xscrollcommand=scrollbar_2.set)
        
        t.grid(row=0,column=0,stick=(tk.W,tk.N,tk.E,tk.S))
        scrollbar_1.grid(row=0,column=1,sticky=(tk.N,tk.S))
        scrollbar_2.grid(row=1,column=0,sticky=(tk.W,tk.E))
        
        ttk.Sizegrip(window).grid(row=1,column=1,sticky=(tk.N,tk.S))
        
        if content:
            for x in content:
                t.insert(tk.END, x, )
        
        t["state"]="disabled"

        window.wait_window()
    ##########
    ##########
    # gamelist ，标题处，右键 菜单 ，选择 显示 哪些 列
    # a topleve window 
    def header_pop_up_menu_callback_choose_columns( self ,):
        # a topleve window 
        # -------------------------------
        # |所有项| 第1组 | 第2组 | all |
        # |  0   |   1   |   2   |  3  |
        # |      |       |       |     |
        # |      |       |       |     |
        # |      |       |       |     |
        # |      |       |       |     |
        # |      |       |       |     |
        # |      |       |       |     |
        # -------------------------------
        #                       确定   |
        # -------------------------------
        
        # user_configure
            # user_configure["gamelist_columns_to_show_1"] # 第1组
            # user_configure["gamelist_columns_to_show_2"] # 第2组
            # user_configure["gamelist_columns_to_show_3"]           # 第3组
        # self.data_from_main
            # "columns"                                   # 第0组 ,所有项
            # "columns_translation"
        
        # self.gamelist_change_mark
            # top_binding_gamelist_change 函数中
            
        # self.tree
        
        # self.menu_call_back_function_save_ini_data()
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("选择游戏列表显示项目"))
        
        #size = "400x300"
        #window.geometry( size )
             
        window.lift(root)
        window.transient(root)
        #window.grab_set()
        
        
        def add_to(add_to_a_listbox):# 第0组，选中项，添加到 另一组
            # listbox0
            a_listbox = add_to_a_listbox
            for x in listbox0.curselection():# 得到 index ，tuple 格式
                content=listbox0.get(x)
                if content in a_listbox.get(0,tk.END) :
                    print("already have")
                else:
                    a_listbox.insert(tk.END,content)  

        def delete_from_a_listbox(a_listbox):# 第1、2、3组，中，删除选中项
            x = a_listbox.curselection() # 得到 index ，tuple 格式
            if len(x) == 1 : # 如果不是 空 tuple ,且，只选中一项
                index = x[0]
                a_listbox.delete( index )
                a_listbox.selection_set( index )# 选中
        
        def move_up(a_listbox):# listbox 中的选项，选中项，向上移
            x = a_listbox.curselection() # 得到 index ，tuple 格式
            if len(x) == 1 : # 如果不是 空 tuple ,且，只选中一项
                index = x[0]
                if index>0: # 如果不是在最上边
                    content = a_listbox.get(index) 
                    a_listbox.delete(index) # 删除
                    a_listbox.insert(index-1,content) # 重新添加到上一行
                    a_listbox.selection_set(index-1)# 选中
        
        def move_down(a_listbox):# listbox 中的选项，选中项，向下移
            x = a_listbox.curselection() # 得到 index ，tuple 格式
            if len(x) == 1 : # 如果不是 空 tuple ,且，只选中一项
                index = x[0]
                if index < a_listbox.size() - 1 : # 如果不是在最下边
                    content = a_listbox.get(index) 
                    a_listbox.delete(index) # 删除
                    a_listbox.insert(index+1,content) # 重新添加到下一行
                    a_listbox.selection_set(index+1)# 选中
        
        def button_ok():
        
            print("button_ok")
            
            def get_content(a_listbox):
                
                temp_list = []
                
                for x in range(a_listbox.size()):
                
                    content = a_listbox.get(x)
                    
                    flag = False 
                    
                    # 有翻译的项目
                    for column in columns_translation:
                        if content == columns_translation[column]:
                            flag = True
                            temp_list.append(column)
                            break
                    
                    # 无翻译译的项目
                    if not flag:
                        temp_list.append(content)
                
                return tuple( temp_list )
            
            
            
            print(get_content(listbox1))
            print(get_content(listbox2))
            print(get_content(listbox3))
            
            user_configure["gamelist_columns_to_show_1"] = get_content(listbox1)
            user_configure["gamelist_columns_to_show_2"] = get_content(listbox2)
            user_configure["gamelist_columns_to_show_3"] = get_content(listbox3)
            
            try:
                del self.gamelist_change_mark # top_binding_gamelist_change 函数中
                # 删除标记，跳转到第1组
            except:
                pass
            
            def get_columns(old_columns): # 检查，有没有超出范围
                temp_list = []
                for x in old_columns:
                    if x in self.tree["columns"]:
                        temp_list.append(x)
                new_columns = tuple( temp_list )
                return new_columns            

            # 标记为第三组，发信号后，切换到第一组
            global_variable.column_group_counter=3
            
            # 用 root 发信号
            # 用这个 toplevel ，似乎root收不到
            root.event_generate(r"<<GameListChangeColumnsToShow>>",)

            self.save_user_configure()
            
            
            window.destroy()


        #window.rowconfigure(0,weight=1)
        window.columnconfigure(0,weight=1)
        window.columnconfigure(1,weight=1)
        window.columnconfigure(2,weight=1)
        window.columnconfigure(3,weight=1)
        
        frame0 = ttk.Frame(window,)
        frame1 = ttk.Frame(window,)
        frame2 = ttk.Frame(window,)
        frame3 = ttk.Frame(window,)
        
        
        the_text  =_("第1组，程序一开始显示的内容")
        the_text +="\n"
        the_text +=_("后面的第2组、第3组，主要是为了方便切换显示不同的内容")
        the_text +="\n"
        the_text +=_("不需要的话，可以不用去管 第2组、第3组")

        ttk.Label(window,text=the_text).grid(row=2,column=0,columnspan=4,sticky=(tk.W,tk.N),)
        
        button_ok = ttk.Button(window,text=_("确认，确认后跳转到第1组"),command=button_ok)
        button_ok.grid(row=8,column=0,columnspan=4,sticky=(tk.E),)
        
        frame0.grid(row=0,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)
        frame1.grid(row=0,column=1,sticky=(tk.W,tk.N,tk.E,tk.S),)
        frame2.grid(row=0,column=2,sticky=(tk.W,tk.N,tk.E,tk.S),)
        frame3.grid(row=0,column=3,sticky=(tk.W,tk.N,tk.E,tk.S),)
        
        for x in (frame0,frame1,frame2,frame3,):
            #x.rowconfigure(0,weight=1)
            x.columnconfigure(0,weight=1)
        
        h = len( global_variable.columns )
        
        # frame0
        ttk.Label(frame0,text=_("内容")).grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        
        listbox0 = tk.Listbox(frame0,height=h, )
        listbox0.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)
        
        for x in global_variable.columns:
            if x in columns_translation:
                listbox0.insert(tk.END,columns_translation[x])
            else:
                listbox0.insert(tk.END,x)
        
        button_add_to_1=ttk.Button(frame0,text=_("添加到第1组"),width=-1,command=lambda x=None: add_to(listbox1))
        button_add_to_2=ttk.Button(frame0,text=_("添加到第2组"),width=-1,command=lambda x=None: add_to(listbox2))
        button_add_to_3=ttk.Button(frame0,text=_("添加到第3组"),width=-1,command=lambda x=None: add_to(listbox3))
        
        button_add_to_1.grid()
        button_add_to_2.grid()
        button_add_to_3.grid()
        
        # frame1
        ttk.Label(frame1,text=_("第1组")).grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        listbox1 = tk.Listbox(frame1,height=h, )
        listbox1.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)

        for x in user_configure["gamelist_columns_to_show_1"]:
            if x in columns_translation:
                listbox1.insert(tk.END,columns_translation[x])
            else:
                listbox1.insert(tk.END,x)
        
        button_delete_from_1=ttk.Button( frame1 ,width=-1,text=_("从第1组移除"),command=lambda x=None:delete_from_a_listbox(listbox1))
        button_delete_from_1.grid()
        
        button_move_up_1=ttk.Button( frame1 ,width=-1,text=_("上移"),command=lambda x=None:move_up(listbox1))
        button_move_up_1.grid()
        
        button_move_down_1=ttk.Button( frame1 ,width=-1,text=_("下移"),command=lambda x=None:move_down(listbox1))
        button_move_down_1.grid()

        # frame2
        ttk.Label(frame2,text=_("第2组")).grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        listbox2 = tk.Listbox(frame2,height=h, )
        listbox2.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)

        for x in user_configure["gamelist_columns_to_show_2"]:
            if x in columns_translation:
                listbox2.insert(tk.END,columns_translation[x])
            else:
                listbox2.insert(tk.END,x)

        button_delete_from_2=ttk.Button( frame2 ,text=_("从第2组移除"),command=lambda x=None:delete_from_a_listbox(listbox2))
        button_delete_from_2.grid()
        
        button_move_up_2=ttk.Button( frame2 ,width=-1,text=_("上移"),command=lambda x=None:move_up(listbox2))
        button_move_up_2.grid()
        
        button_move_down_2=ttk.Button( frame2 ,width=-1,text=_("下移"),command=lambda x=None:move_down(listbox2))
        button_move_down_2.grid()

        # frame3
        ttk.Label(frame3,text=_("第3组")).grid(row=0,column=0,sticky=(tk.W,tk.N,),)
        listbox3 = tk.Listbox(frame3,height=h, )
        listbox3.grid(row=1,column=0,sticky=(tk.W,tk.N,tk.E,tk.S),)

        for x in user_configure["gamelist_columns_to_show_3"]:
            if x in columns_translation:
                listbox3.insert(tk.END,columns_translation[x])
            else:
                listbox3.insert(tk.END,x)
                
        button_delete_from_3=ttk.Button( frame3 ,text=_("从第3组移除"),command=lambda x=None:delete_from_a_listbox(listbox3))
        button_delete_from_3.grid()
        
        button_move_up_3=ttk.Button( frame3 ,width=-1,text=_("上移"),command=lambda x=None:move_up(listbox3))
        button_move_up_3.grid()
        
        button_move_down_3=ttk.Button( frame3 ,width=-1,text=_("下移"),command=lambda x=None:move_down(listbox3))
        button_move_down_3.grid()
        
        
        window.wait_window()    
    ##########
    ##########
    # 
    
    # font 初始化
    def font_initial(self,):
        print("font_initial")
        print("font_initial")
        print("font_initial")
        print("font_initial")
        
        all_font = tkfont.families()
        
        # "TkDefaultFont"
        font_defualt = tkfont.nametofont("TkDefaultFont")
        default_name = font_defualt.actual("family")
        default_size = font_defualt.actual("size")
        
        # font size 正整数 
        # font size 负整数 都可以
        
        # gamelist font
        font_name = default_name
        if user_configure["gamelist_font"] in all_font:
            font_name = user_configure["gamelist_font"]
        font_size = default_size
        if user_configure["gamelist_font_size"] != 0: 
            font_size = user_configure["gamelist_font_size"]
        # 记录
        global_variable.font_gamelist=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_gamelist_font()
        
        # gamelist header font
        the_font = tkfont.nametofont("TkHeadingFont")
        the_name = font_defualt.actual("family")
        the_size = font_defualt.actual("size")
        #
        font_name = the_name
        if user_configure["gamelist_header_font"] in all_font:
            font_name = user_configure["gamelist_header_font"]
        font_size = the_size
        if user_configure["gamelist_header_font_size"] != 0:
            font_size = user_configure["gamelist_header_font_size"]
        # 记录
        global_variable.font_gamelist_header=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_gamelist_font_for_header()
        
        # text font 1
        font_name = default_name
        if user_configure["text_font"] in all_font:
            font_name = user_configure["text_font"]
        font_size = default_size
        if user_configure["text_font_size"] != 0: 
            font_size = user_configure["text_font_size"]
        # 记录
        global_variable.font_text=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_text_1_font()

        # text font 2
        font_name = default_name
        if user_configure["text_2_font"] in all_font:
            font_name = user_configure["text_2_font"]
        font_size = default_size
        if user_configure["text_2_font_size"] != 0: 
            font_size = user_configure["text_2_font_size"]
        # 记录
        global_variable.font_text_2=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_text_2_font()
    
    # font gamelist
    def set_gamelist_font(self,):
        # Treeview
        # 自制 table
        style = ttk.Style()
        # Treeview
        style.configure('Treeview', font=global_variable.font_gamelist,)
        
        # 自制 table
        for table in global_variable.all_tables:
            table.new_func_set_colour_and_font(font=global_variable.font_gamelist)
    
    # font header
    def set_gamelist_font_for_header(self,):
        # 1,Treeview 
        # 2,自制 table
        
        # Treeview 问题，字体变化大小时，标题高度不知道怎样调？
        #style = ttk.Style()
        #style.configure("Heading",font = global_variable.font_gamelist_header)
        
        # 自制 table
        for table in global_variable.all_tables:
            table.new_func_set_colour_and_font( header_font = global_variable.font_gamelist_header )
    
    # font text 1
    def set_text_1_font(self,):
        if global_variable.tk_text_1:
            global_variable.tk_text_1.configure(font=global_variable.font_text)

    # font text 2
    def set_text_2_font(self,):
        if global_variable.tk_text_2:
            global_variable.tk_text_2.configure(font=global_variable.font_text_2)

    
    # ui 字体选择器
    def window_for_choose_font(self,the_font,title_string=None):
        if title_string is None:
            title_string = " " # 空一格。全空的话，标题似乎会继承上一级的
        
        the_original_font_name = the_font.actual("family")
        the_original_font_size = the_font.actual("size")
        
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(title_string)
        
        size = "400x300"
        window.geometry( size )
        
        window.lift()
        window.transient(root_window)
        
        window.columnconfigure(1,weight=1)
        
        # 字体
        
        ttk.Label(window,text = "",).grid(row=0,column=0,sticky=tk.W+tk.N)
        
        font_name_tkstring = tk.StringVar()

        label_font = ttk.Label(window,text = _("字体选择"),)
        label_font.grid( row=1,column=0,sticky=tk.W+tk.E)
        
        font_choose_box = ttk.Combobox(window, textvariable = font_name_tkstring,state="readonly",)
        font_choose_box.grid( row=1,column=1,sticky=(tk.W,tk.E) )
        
        temp = sorted( tkfont.families() )
        values = []
        #values.append("")
        for x in temp:
            values.append(x)
        font_choose_box["values"]= values
        
        if the_original_font_name in values:
            font_choose_box.set(the_original_font_name)
        
        
        # 字体大小
        ttk.Label(window,text = "",).grid(row=2,column=0,sticky=tk.W+tk.N)
        
        font_size_tkstring = tk.StringVar()
        
        label_font_size = ttk.Label(window,text = _(r"字体大小"),)
        label_font_size.grid( row=3,column=0,sticky=(tk.W,tk.E) )
        
        font_size_box = ttk.Combobox(window, textvariable = font_size_tkstring,state="readonly")
        font_size_box.grid(row=3,column=1,sticky=(tk.W,tk.E))
        
        # 范围 
        the_values = []
        the_values_set = set()
        # 不含 0 了吧
        for x in range(-200,0):
            temp = str(x)
            the_values.append(  temp )
            the_values_set.add( temp )
        for x in range(1,201):
            temp = str(x)
            the_values.append(  temp )
            the_values_set.add( temp )
        
        font_size_box["values"]= the_values
        
        if str(the_original_font_size) in the_values_set:
            font_size_box.set(   str(the_original_font_size)   )

        
        #
        
        
        def for_ok_button():
        
            font_name = font_name_tkstring.get()
            font_size = font_size_tkstring.get()
            font_size = int(font_size)
            
            if font_name:
                the_font.config(family=font_name)
            
            if font_size!=0:
                the_font.config(size=font_size)
            
        
        ttk.Label(window,text=_("负整数，字体单位是像素；正整数，字体单位是 point"),).grid(row=4,column=0,columnspan=2,sticky=tk.W+tk.N)
        ttk.Label(window,text = "",).grid(row=5,column=0,sticky=tk.W+tk.N)
        
        ttk.Button(window,text=_("确定"),command=for_ok_button).grid( row=6,column=0,sticky=tk.N+tk.E, )
        
        
        
        
        
        ttk.Label(window,text="").grid()
        
        
        window.wait_window()
    
    def for_save_font(self,):
        # 游戏列表字体
        the_font = global_variable.font_gamelist
        user_configure["gamelist_font"]      = the_font.actual("family")
        user_configure["gamelist_font_size"] = the_font.actual("size")
        
        # 游戏列表 标题 字体
        the_font = global_variable.font_gamelist_header
        user_configure["gamelist_header_font"]      = the_font.actual("family")
        user_configure["gamelist_header_font_size"] = the_font.actual("size")
        
        # 文本字体 一
        the_font = global_variable.font_text
        user_configure["text_font"]      = the_font.actual("family")
        user_configure["text_font_size"] = the_font.actual("size")
        
        # 文本字体 二
        the_font = global_variable.font_text_2
        user_configure["text_2_font"]      = the_font.actual("family")
        user_configure["text_2_font_size"] = the_font.actual("size")
        
    # row height
    def use_user_configure_row_height(self,):
        # gamelist row height
            # ttk.Treeview 
            # 自制 table
        # text 
        
        
        style = ttk.Style()
        if user_configure["row_height"] > 0:
            # Treeview
            style.configure('Treeview', rowheight = user_configure["row_height"])
            
            # 自制 table
            print(len(global_variable.all_tables))
            for table in global_variable.all_tables:
                
                table.new_func_set_row_height( user_configure["row_height"] )
        
    # row height for header
    def use_user_configure_row_height_for_header(self,):
        # gamelist row height
            # ttk.Treeview ,header row height ，不知道怎样设置
            # 自制 table 设置
        # text row height
        
        if user_configure["row_height_for_header"] > 0:

            # 自制 table
            for table in global_variable.all_tables:
                table.new_func_set_row_height_for_header( user_configure["row_height_for_header"] )
    
    # icon width
    def use_user_configure_icon_width(self,):
        # 自制 table
        for table in global_variable.all_tables:
            table.new_func_set_icon_width( user_configure["icon_size"] )
    ################
    #############
    # colours
    def choose_colours(self,):
        window = tk.Toplevel()
        window.resizable(width=True, height=True)
        window.title(_("颜色 设置"))
        
        size = "400x300"
        window.geometry( size )
        window.lift()
        window.transient(root_window)
        window.configure(background="grey95")
        
        frame = tk.Frame(window)
        frame.grid(row=0,column=0,sticky=tk.W+tk.N+tk.E+tk.S,)
        frame.configure(background="grey95")
        

        translation_dict = {
                # key 对应于 配置文件中的选项
                "background" : _("背景色"),
                "foreground" : _("前景色"),
                "selectbackground" : _("列表选中行背景色"),
                "selectforeground" : _("列表选中行前景色"),
                "background_for_panedwindow" : _("分隔条背景色"),
            }

        def choose_colour(event):
            widget = event.widget
            new_colour = ""
            new_colour = colorchooser.askcolor()
            #print( type(new_colour))
            #<class 'tuple'>
        
            #print(new_colour)
            # ((128, 64, 64), '#804040') 

            new_colour = new_colour[1]
            # 格式选择
            
            if new_colour:
                try:
                    widget.configure( background = new_colour )
                except:
                    pass
            
            window.lift()
        
        def make_ui(row_number,key_word):
            
            if key_word in translation_dict:
                temp_string = translation_dict[key_word]
            else:
                temp_string = key_word
            
            tk.Label(frame,text=temp_string,background="grey95",foreground="black").grid(row=row_number,column=0,sticky=tk.W+tk.N,)
            
            label = tk.Label(frame,borderwidth=4,relief="raised" ,text=" "*15)
            label.grid(row=row_number,column=1,sticky=tk.W+tk.N,)
            
            if user_configure[key_word]:
                try:
                    label.configure( background = user_configure[key_word] )
                except:
                    pass
            
            return label
        
        # ui 
        colour_widgets={}
        r=0
        for key_word in (
                "background",
                "selectbackground",
                "foreground",
                "selectforeground",
                "background_for_panedwindow",
                ):
            colour_widgets[key_word] = make_ui(r,key_word)
            r+=1
        
        # bind
        for key_word in colour_widgets:
            widget=colour_widgets[key_word]
            widget.bind("<Button-1>",choose_colour)        
        
        def for_ok_button():
            for key_word in colour_widgets:
                widget=colour_widgets[key_word]
                #print(widget["background"])
                user_configure[key_word] = widget["background"]
            
            self.use_user_configure_colours()
        
        # ui
        tk.Button(frame,text=_("确定"),background="grey95",foreground="black",command=for_ok_button).grid(row=r,column=0,columnspan=2,sticky=tk.E+tk.N,)
        r+=1
        
        
        window.wait_window()
    
    
    def use_user_configure_colours(self,):
        style = ttk.Style()
        
        if user_configure["foreground"]:
            
            cf = user_configure["foreground"]
            
            style.configure('.',foreground = cf)
            
            style.configure('TCombobox', foreground  = cf)
            style.configure('TCombobox', selectforeground   = cf)
            #style.configure('TCombobox', padding=(1,1))
            style.map('TCombobox', foreground =[ ('readonly',cf) ] )
            style.map('TCombobox', selectforeground =[ ('readonly',cf) ] )
    
            style.configure('TNotebook.Tab', foreground =cf)  # 
            style.map('TNotebook.Tab', foreground =[ ('active',cf) ] ) # 选中时    
            
            style.configure('Treeview', foreground  = cf)
            #style.configure('Heading', foreground  = cf)
            
            for table in global_variable.all_tables:
                table.new_func_set_colour_and_font(foreground=cf)
            
            for text in (global_variable.tk_text_1,global_variable.tk_text_2):
                text.configure(foreground=cf)
            
            root.option_add('*Toplevel*foreground', cf)
            root.option_add('*Text*foreground', cf)
            root.option_add('*Listbox*foreground', cf)
            root.option_add("*TCombobox*Listbox.foreground ", cf)

        if user_configure["background"]:
            
            c = user_configure["background"]
            
            style.configure('.',background       = c)
            #style.configure('.', fieldbackground = c)
            
            style.configure('Treeview', background        = c)
            style.configure('Treeview', fieldbackground   = c)
                # 在 部分主题里有用
            #style.configure('Treeview.Heading', background= c)
                # 在 部分主题里有用
            
            style.configure('TEntry', fieldbackground = c)
            
            style.configure('TCombobox', fieldbackground = c)
            style.configure('TCombobox', selectbackground  = c)
            #style.configure('TCombobox', padding=(1,1))
            style.map('TCombobox', fieldbackground=[ ('readonly',c) ] )
            style.map('TCombobox', selectbackground=[ ('readonly',c) ] )
            ####
                # 因为设置了 readonly ???
            style.configure('TCombobox', background = c)
            
            style.configure('TNotebook', background =c) 
            style.configure('TNotebook.Tab', background =c)  # 背景
            style.map('TNotebook.Tab', background =[ ('active',c) ] ) # 选中时
            #style.map('TNotebook.Tab', background =[ ('disabled',"green") ] )
            #style.map('TNotebook.Tab', background =[ ('selected',"brown") ] )
            
            
            for table in global_variable.all_tables:
                table.new_func_set_colour_and_font(background=c)
            
            for text in (global_variable.tk_text_1,global_variable.tk_text_2):
                text.configure(background=c)
            
            # Canvas
            for canvas in self.find_widget('Canvas'):
                canvas.configure(background=c)
            
            # tk.Toplevle
            root.option_add('*Toplevel*background', c)
            root.option_add('*Listbox*background', c)
            root.option_add('*Text*background', c)
            root.option_add('*Canvas*background', c)
    
        if user_configure["selectforeground"]:
            c_sf = user_configure["selectforeground"]
            
            style.configure('.',selectforeground = c_sf)
            
            style.map('Treeview', foreground =[ ('selected',c_sf) ] )
            
            for table in global_variable.all_tables:
                table.new_func_set_colour_and_font(selectforeground=c_sf)
            
            for text in (global_variable.tk_text_1,global_variable.tk_text_2):
                text.configure(selectforeground=c_sf)
        
        if user_configure["selectbackground"]:
            c_sb = user_configure["selectbackground"]
            
            style.configure('.',selectbackground = c_sb)
            
            style.map('Treeview', background =[ ('selected',c_sb) ] )
            
            for table in global_variable.all_tables:
                table.new_func_set_colour_and_font(selectbackground=c_sb)
            
            for text in (global_variable.tk_text_1,global_variable.tk_text_2):
                text.configure(selectbackground=c_sb)
        
        if user_configure["background_for_panedwindow"]:
            style.configure('TPanedwindow',background =user_configure["background_for_panedwindow"])
    
    ##########
    ##########
    # save
    def user_configure_get_window_size(self,):
        # 主窗口大小
        height = root_window.winfo_height() 
        width  = root_window.winfo_width()
        # 得到的结果不准确，因为 菜单 ？？
        # 在 设置 root.geometry 之后，马上 root.update() 一下，就准确了
        # why ?
        # # #
        # 转为字符串 如 800x600
        size = str(width) + "x" + str(height)
        user_configure["size"] = size
        
        print("")
        print("window size")
        print(user_configure["size"])
    
    def user_configure_get_window_size_and_position(self,):
        print("")
        print("window size and position")
        
        #if sys.platform.startswith("win") or sys.platform.startswith("darwin"):
        #    # normal zoomed iconic, withdrawn, icon, 
        #    # (Windows and Mac OS X only) zoomed.
        #    if root_window.wm_state() == "normal" : # 最大化
        #        size  =  root_window.geometry() # 最大化时，这个值反回的位置不太对
        #        user_configure["size"] = size
        #    else:
        #        height = root_window.winfo_height() 
        #        width  = root_window.winfo_width()
        #        size = str(width) + "x" + str(height) + "+0" + "+0"
        #        user_configure["size"] = size
        #else:
        #    size  =  root_window.geometry() 
        #        # windows 最大化时，这个值反回的位置不太对
        #        # 其它没试过
        #    user_configure["size"] = size

        size  =  root_window.geometry() 
            # windows 最大化时，这个值反回的位置不太对
            # 其它没试过
        user_configure["size"] = size
        
        
        print(user_configure["size"])
    
    def user_configure_get_widget_position(self,):
        # 分隔线位置
        if global_variable.PanedWindow is not None:
            # 目录 游戏列表 ，分隔条 位置
            user_configure["pos1"] = global_variable.PanedWindow.sashpos(0,)
            # 游戏开表 周边 ，分隔条 位置
            user_configure["pos2"] = global_variable.PanedWindow.sashpos(1,)
        if global_variable.PanedWindow_2 is not None:
            # 图片处还有一条分隔线
            user_configure["pos3"] = global_variable.PanedWindow_2.sashpos(0,)
    
    def user_configure_get_widget_option(self,):
        
        # 列宽度保存
        if global_variable.the_showing_table is not None:
            top_table = global_variable.the_showing_table
            columns_width = top_table.new_func_get_column_width()
            
            # 转为整数
            for x in columns_width:
                columns_width[x] = int(columns_width[x])
            
            user_configure["gamelist_columns_width"] = columns_width
            print(user_configure["gamelist_columns_width"])
        
        # 周边，notebook tab 选择记录
        if global_variable.Notebook_for_extra is not None:
            user_configure["extra_tab_index"] = global_variable.Notebook_for_extra.index( global_variable.Notebook_for_extra.select() )
        
        # 图片区 是否使用 zip 选项记录
        if global_variable.tkint_flag_for_zip_1 is not None:
            user_configure["extra_image_usezip"] = global_variable.tkint_flag_for_zip_1.get()
        if global_variable.tkint_flag_for_zip_2 is not None:
            user_configure["extra_image_usezip_2"] = global_variable.tkint_flag_for_zip_2.get()
        # 文本区 是否使用 建立目录 记录
        if global_variable.tkint_flag_for_text_index_1 is not None:
            user_configure["extra_text_make_index_1"] = global_variable.tkint_flag_for_text_index_1.get()
        if global_variable.tkint_flag_for_text_index_2 is not None:
            user_configure["extra_text_make_index_2"] = global_variable.tkint_flag_for_text_index_2.get()
        
        # Combobox 选项记录
        #图片一
        if global_variable.Combobox_chooser_image_1 is not None:
            user_configure["extra_image_chooser_index"] = global_variable.Combobox_chooser_image_1.current()
        #图片二
        if global_variable.Combobox_chooser_image_2 is not None:
            user_configure["extra_image_chooser_2_index"] = global_variable.Combobox_chooser_image_2.current()
        #文本一
        if global_variable.Combobox_chooser_text_1 is not None:
            user_configure["extra_text_chooser_index"] = global_variable.Combobox_chooser_text_1.current()
        #文本二
        if global_variable.Combobox_chooser_text_2 is not None:
            user_configure["extra_command_type_chooser_index"] = global_variable.Combobox_chooser_text_2.current()
    
    def save_user_configure(self,):
        
        self.user_configure_get_widget_option()
        
        self.for_save_font()
        
        try:
            #read_user_config.write_ini(ini_file_name,ini_dict,order = None)
            read_user_config.write_ini(
                    the_files.file_ini_configure,
                    global_variable.user_configure_data,
                    order = global_variable.user_configure_data_order)
            print("save configure file")
        except:
            pass
    
    def save_user_configure_with_window_size(self,):
        
        self.user_configure_get_window_size()
        
        self.user_configure_get_widget_position()
        
        self.save_user_configure()
    
    def save_user_configure_with_window_size_and_position(self,):
    
        self.user_configure_get_window_size_and_position()
        
        self.user_configure_get_widget_position()
        
        self.save_user_configure()
    
    #######################
    def find_widget(self,class_name):
        # 查找
        result=[]
        
        def find_childen(window):
            for child in window.winfo_children():
                if child.winfo_class()==class_name:
                    result.append(child)

                find_childen(child)
        
        find_childen(root_window)
        
        # 结果
        #if result : 
        #    for x in result:
        #        print(x)
        return result
    
    
    #######################
    # 拥有列表
    def set_available_gamelist(self,available_items,need_save=False):
        
        # available_items 格式为  set
        if type(available_items) == set:
            pass
        else:
            available_items = set(available_items)
        
        #global_variable.internal_index
        #global_variable.set_data
        
        #global_variable.available_set
        #global_variable.available_hide_set
        
        # 记录 
        # 拥有部分
        global_variable.available_set = available_items
        
        # 保存数据
        if need_save :
            #the_files.file_pickle_gamelist_available
            save_pickle.save(available_items,the_files.file_pickle_gamelist_available)
        
        # 拥有部分添加到目录，
        # 需要，先过滤一下
            # 过滤项 1，隐藏项
            # 过滤项 2，过滤项
        global_variable.internal_index["available_set"]  = {"gamelist":[],"children":{},}
        global_variable.internal_index["available_set"]["gamelist"] = available_items - global_variable.available_hide_set - global_variable.available_filter_set
        
        # 未拥有部分，添加到目录
        global_variable.internal_index["unavailable_set"]  = {"gamelist":[],"children":{},}
        global_variable.internal_index["unavailable_set"]["gamelist"]  = global_variable.set_data["all_set"] - available_items
    
    
    
    # 刷新 拥有列表 split
    def gamelist_available_refresh(self,):
        ""
        print()
        print("gamelist available refresh")
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        temp_set = self.get_files_names_in_rompath()
        self.set_available_gamelist(temp_set,need_save=True)
        
        root_window.event_generate('<<RequestForAvailableGameList>>')
        
    # 刷新 拥有列表 merged
    def gamelist_available_refresh_2(self,):
        ""
        print()
        print("gamelist available refresh")
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        temp_set = self.get_files_names_in_rompath(merged = True)
        self.set_available_gamelist(temp_set,need_save=True)
        
        root_window.event_generate('<<RequestForAvailableGameList>>')
    
    # 拥有列表 过滤
        # 窗口
    def gamelist_available_filter(self,):
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        size = "400x300" 
        window.geometry(size)
        
        window.title(_("拥有列表过滤"))
        
             
        window.lift()
        window.transient(root_window)
        
        
        available_filter_bios = tk.IntVar()
        available_filter_device = tk.IntVar()
        available_filter_mechanical = tk.IntVar()
        available_filter_no_roms = tk.IntVar()
        
        def for_ok_button():
            global user_configure
        
            window.destroy()
            
            # 转为 set 先，之后转回来
            user_configure["filter"] = set(user_configure["filter"])
            
            if available_filter_bios.get():
                user_configure["filter"].add("bios")
            else :
                user_configure["filter"].discard("bios")

            if available_filter_device.get():
                user_configure["filter"].add("device")
            else:
                user_configure["filter"].discard("device")

            if available_filter_mechanical.get():
                user_configure["filter"].add("mechanical")
            else:
                user_configure["filter"].discard("mechanical")
            
            # 格式转回来
            user_configure["filter"] = list( user_configure["filter"] ) 
            
            global_variable.available_filter_set = set() # 重置 ，重新计算
            
            for x in user_configure["filter"]:
                if x in global_variable.internal_index:
                    global_variable.available_filter_set.update( set(global_variable.internal_index[x]["gamelist"]) )
            
            print('available_set')
            print( len(global_variable.available_set) )
            print("available_filter_set")
            print( len(global_variable.available_filter_set) )
            print("filter list")
            print( user_configure["filter"] )
            
            # 更新目录
            global_variable.internal_index["available_set"]  = {"gamelist":[],"children":{},}
            
            global_variable.internal_index["available_set"]["gamelist"] = global_variable.available_set - global_variable.available_hide_set - global_variable.available_filter_set
            
            # 显示目录
            root_window.event_generate('<<RequestForAvailableGameList>>')

        
        if 'bios'       in user_configure["filter"] :
            available_filter_bios.set(1)
        else:
            available_filter_bios.set(0)
        
        if 'device'     in user_configure["filter"]: 
            available_filter_device.set(1)
        else:
            available_filter_device.set(0)
        
        if 'mechanical' in user_configure["filter"] : 
            available_filter_mechanical.set(1)
        else:
            available_filter_mechanical.set(0)
        
        n=0
        if 'bios' in global_variable.internal_index:
            bios_set_checkbutton  = ttk.Checkbutton(window, text="bios",variable=available_filter_bios)
            bios_set_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),)
            n+=1

        if "device" in global_variable.internal_index:
            device_set_checkbutton = ttk.Checkbutton(window, text="device",variable= available_filter_device )
            device_set_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),)
            n+=1

        if "mechanical" in global_variable.internal_index:
            mechanical_set_checkbutton = ttk.Checkbutton(window, text="mechanical",variable=available_filter_mechanical)
            mechanical_set_checkbutton.grid(row=n,column=0,sticky=(tk.W,tk.N),)
            n+=1
        
        #if "no_roms" in 

            
        button=ttk.Button(window,text=_("确认"),command=for_ok_button)
        button.grid(row=n,column=0,sticky=(tk.W,tk.N),) 
        
        window.wait_window()

    # 找到拥有的 *.zip 、*.7z 、文件夹
    def get_files_names_in_rompath(self,merged = False):
        ### ###
        # 还有一种情况 
        # 路径里有变量：$HOME/mame/roms
            ####
            # 有变量的，到底有几种格式？  


        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        # rompath 里记录的文件，相对位置是相对于模拟器的，这个还得改一下            

        rom_path = self.get_rompath_from_command_line()
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        if rom_path:
            rom_path = rom_path.replace(r"'","") # 去掉单引号
            rom_path = rom_path.replace(r'"',"") # 去掉双引号
        
        temp_set = set()
        
        temp=[]
        
        for x in rom_path.split(r';'):
            if x:
                print(x)

                #######
                # rompath ，记录的相对路径，是相对于模拟器的
                
                
                ### ###
                # 还有一种情况
                # 路径里有变量：$HOME/mame/roms
                    ####
                    # 有变量的，到底有几种格式？
                    
                # 情况1，如果有变量，展开，
                temp_path = x
                try:
                    temp_path = os.path.expandvars( x )
                except:
                    temp_path = x

                if os.path.isabs(temp_path): # 如果是，绝对路径，不用转换
                    y = temp_path
                else: # 如果是，相对路径，转换
                    if mame_dir != None:# 已设置 mame 工作文件夹
                        # mame 所在文件夹 ,绝对路径
                        mame_folders = mame_dir
                        mame_folders = os.path.abspath( mame_folders )
                        
                        # 相对转换路径后的绝对路径
                        y = os.path.join(mame_folders,temp_path)
                        
                        y = os.path.abspath( y )
                        
                    else:# 未设置 mame 工作文件夹，且不是默认值
                        #当成与 jjui 同文件夹对待？
                        y = x

                print(y)
                
                if os.path.isdir(y):
                
                    files_zip = glob.glob( os.path.join(y,"*.zip") )
                    for a in files_zip:
                        temp.append(  os.path.basename(a).lower()[0:-4] )# zip
                    
                    files_7z  = glob.glob( os.path.join(y,"*.7z") )
                    for b in files_7z:
                        temp.append(  os.path.basename(b).lower()[0:-3] )# 7z
                    
                    files_all = glob.glob( os.path.join(y,"*") )
                    files_left = set(files_all) - set(files_zip) - set(files_7z)
                    for c in files_left:
                        if os.path.isdir(c):
                            temp.append(  os.path.basename(c).lower() )

        temp_set = set( temp )
        
        temp_set = global_variable.set_data['all_set'] & temp_set
        
        # merged
        if merged :
            # 现有的主版
            the_parent = temp_set & global_variable.set_data['parent_set']
            
            # 其中，有副版本的
            the_parent = the_parent & set( global_variable.dict_data['parent_to_clone'].keys() )
            
            # 关联的副版本
            the_colne = []
            for x in the_parent:
                the_colne.extend( global_variable.dict_data['parent_to_clone'][x] )
            the_colne = set( the_colne )
            
            # 合并
            the_result = temp_set | the_colne
            return  the_result
        
        # split
        else:
            return temp_set

    # mame -showconfig 中
    #   rompath 这一项
    def get_rompath_from_command_line(self,event=None):
        print("get_rompath_from_command_line")
    
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        command_list = []
        command_list.append( mame_exe )
        command_list.append( "-showconfig" )
        
        rom_path="roms" # 默认值,应该用默认值吗？还是用空的？
        rom_path=""     #  用空的吧
        
        #rompath                   "roms;"
        str_1 = r"^rompath\s+(\S.*?)\s*$"
        p=re.compile(str_1, )        
        
        sub_process = subprocess.Popen( command_list, 
                            shell=user_configure["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            encoding="utf_8",
                            cwd=mame_dir,
                            )
                            
        for line in sub_process.stdout:
            print(line)
            m = p.search(line)
            if m :
                rom_path = m.group(1)
                #print("find")
                break
        
        print(rom_path)
        return rom_path
    
    #######################
    # 更新翻译

    def gamelist_reload_translation(self,):
        # 翻译
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        size = "400x300"
        window.geometry(size)
        
        window.title(_("导入翻译文件"))
        
        window.lift()
        window.transient(root_window)
        #window.grab_set()
        
        #window.rowconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)
        
        def load_default_translation_file():
            
            file_encoding = "utf_8_sig"
            
            file_name = the_files.file_txt_translation_for_gamelist
            
            file_pickle_gamelist_data_file_name = the_files.file_pickle_gamelist_data
            
            if not os.path.isfile(file_name):
                text = _("翻译文件不存在：") + file_name
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            translation_dict={}
            
            try:
                translation_dict = translation_gamelist.read_translation_file( file_name )
            except:
                translation_dict={}
                
                text = _("读取翻译文件，出错。注意将文件的 文本编码 保存为 uft-8-bom")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            if len( translation_dict ) == 0 :
                text = _("读取翻译文件，翻译数量为 0 ，翻译任务取消")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            if len( translation_dict ) > 0 :
                set_1 = set( translation_dict.keys() )
                
                translationed_set = set_1 & global_variable.set_data['all_set']
                
                #un_translationed_set = global_variable.set_data['all_set'] - translationed_set
            
            if len( translationed_set ) == 0 :
                text = _("有效翻译数量为 0 ，翻译任务取消")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            # 列表更新
            global_variable.machine_dict = translation_gamelist.add_translation( translation_dict , global_variable.machine_dict ,global_variable.columns)
            global_variable.the_showing_table.new_func_refresh_table()
            
            # 文件更新
            data = {}
            data = read_pickle.read(file_pickle_gamelist_data_file_name)
            
            if data:
                
                data["machine_dict"] = translation_gamelist.add_translation( translation_dict , data["machine_dict"] ,data["columns"])
                
                save_pickle.save(data,file_pickle_gamelist_data_file_name)

            
            
            window.destroy()
        
        def load_translation_file():

            file_name     = new_file_path.get()

            if file_name =="":
                text = _("未指翻译定文件")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            file_pickle_gamelist_data_file_name = the_files.file_pickle_gamelist_data

             
            if not os.path.isfile(file_name):
                text = _("翻译文件不存在：") + file_name
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            
            translation_dict={}
            
            try:
                translation_dict = translation_gamelist.read_translation_file( file_name )
            except:
                translation_dict={}
                text = _("读取翻译文件，出错。注意将文件的 文本编码 保存为 uft-8-bom")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            if len( translation_dict ) == 0 :
                text = _("读取翻译文件，翻译数量为 0 ，翻译任务取消")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
                
            if len( translation_dict ) > 0 :
                set_1 = set( translation_dict.keys() )
                
                translationed_set = set_1 & global_variable.set_data['all_set']
                
                #un_translationed_set = global_variable.set_data['all_set'] - translationed_set
            
            if len( translationed_set ) == 0 :
                text = _("有效翻译数量为 0 ，翻译任务取消")
                messagebox.showwarning(message=text)
                window.lift()
                return 0
            
            # 列表更新
            global_variable.machine_dict = translation_gamelist.add_translation( translation_dict , global_variable.machine_dict ,global_variable.columns)
            global_variable.the_showing_table.new_func_refresh_table()
            
            # 文件更新
            data = {}
            data = read_pickle.read(file_pickle_gamelist_data_file_name)
            
            if data:
                
                data["machine_dict"] = translation_gamelist.add_translation( translation_dict , data["machine_dict"] ,data["columns"])
                
                save_pickle.save(data,file_pickle_gamelist_data_file_name)
            
            window.destroy()

        n=0
        
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        the_file_name = the_files.file_txt_translation_for_gamelist
        
        ttk.Label(window,text= _("默认翻译文件：") + the_file_name,).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text= _(r"默认翻译文件，文字编码为：utf_8_sig")).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Button(window,text=_("读取默认翻译文件"),width=-1,command = load_default_translation_file).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        #
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        # 其它文件
        ttk.Label(window,text=_("另外选择翻译文件:")).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        #ttk.Label(window,text="选择文件：").grid(row=5,column=0,columnspan=2,sticky=tk.W+tk.N,)
        
        def choose_file():
            file_name = filedialog.askopenfilename(initialdir=".")
            if file_name:
                new_file_path.set(file_name)
            window.lift(root_window)
        
        ttk.Button(window,text=_("选择"),width=-1,command=choose_file).grid(row=n,column=0,sticky=tk.W+tk.N,)
        
        new_file_path = tk.StringVar()
        ttk.Entry(window,textvariable=new_file_path).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
        n+=1
        
        ttk.Button(window,text="读取指定翻译文件",width=-1,command = load_translation_file).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        n+=1
        
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text="编码提示：").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text="将文本保存为，utf_8_sig （utf-8 带 bom），可以包含多国文字").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        window.wait_window()

    #     
    #######################
    # exit
    def exit_2(self,):
        print()
        print("exit")
        
        try:
            self.save_user_configure()
        except:
            pass
        
        #sys.exit()
        #print(r"root.destroy()")
        global_variable.root_window.destroy()
    #################
    #################


misc_funcs = Misc_functions()