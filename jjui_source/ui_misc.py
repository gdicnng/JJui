# -*- coding: utf_8_sig-*-
#import sys
import os
import sys
import subprocess
import threading
import re
import io
import xml.etree.ElementTree # uni-bios parse
#import glob

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font as tkfont

from . import global_variable
from . import global_static_filepath as the_files
#from . import global_static_key_word_translation as key_word_translation

#from . import ui__text_with_scrollbar 

from . import read_user_config 
from . import save_pickle 
#from . import read_pickle 
from . import translation_gamelist 
from . import folders_save

from . import misc 

# 周边建目录用
from . import extra_read_history_xml 
from . import extra_history_dat 
from . import extra_mameinfo_dat 
from . import extra_command 
#from . import extra_command_english 
#from . import extra_gameinit_dat


class Misc_functions():
    
    ######################
    ######################
    # 打开游戏
    #   接收信号
    #   "<<StartGame>>"
    # start_game
    def start_game(self,event):
        print()
        print(r"virtual event received <<StartGame>>")
        
        widget = event.widget
        emu_number   = widget.new_var_data_for_StartGame["emu_number"]
        game_type    = widget.new_var_data_for_StartGame["type"] # "mame" ,"softwarelist"
        game_id      = widget.new_var_data_for_StartGame["id"]
        other_option = widget.new_var_data_for_StartGame["other_option"]
        hide         = widget.new_var_data_for_StartGame["hide"]
        alt          = widget.new_var_data_for_StartGame["alt"] # 仅 mame
        
        
        print("game_id   :{}".format(game_id))
        print("game_type :{}".format(game_type))
        
        if game_type == "mame":
            if emu_number   == -1 : # 默认 MAME
                self.call_mame( game_id, other_option, hide)
            elif emu_number in( 0,1,2,3,4,5,6,7,8,9,):
                self.get_other_emu_configure(game_id,emu_number,hide,alt)
        
        elif game_type == "softwarelist":
            if emu_number   == -1 : # 默认 值
                emu_number = 1 # 跳转到第1组设置
            
            if emu_number   == -1:
                pass
            elif emu_number in ( 0,1,2,3,4,5,6,7,8,9,):
                self.get_other_emu_configure_sl(game_id,emu_number,hide)
    
    # start_game mame
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
        
        #print()
        #print( command_list )
        
        if hide: # 打开游戏，隐藏 UI
            self.start_emu_by_subprocess(
                    command_list,
                    shell=global_variable.user_configure_data["use_shell"],
                    cwd=mame_dir,
                    hide=True
                    )
        else: # 打开游戏，保留 UI
            self.start_emu_by_subprocess(
                    command_list,
                    shell=global_variable.user_configure_data["use_shell"],
                    cwd=mame_dir,
                    hide=False
                    )
    
    
    def start_emu_by_subprocess(self,command_list,shell=True,cwd=None,hide=True):
        print("")
        print("start_emu_by_subprocess")
        
        print("cwd \n\t",cwd)
        
        print("command_list")
        for x in command_list:
            print("\t",x)
        
        print("shell \n\t",shell)
        
        if hide: # 打开游戏，隐藏 UI
            
            # 猛虎 反应 withdraw 他的输入法会卡
            # .iconify() 可以
            
            # 问题的根源，估计应该是
            #   .focus_set() 怎样取消？
            
            # 鼠标双击时，还有在设置 focus_set()
            #   可能有影响
            #   目前已取消 鼠标双击时 的 focus_set() ，反正单击时已有了
            # 但根据 猛虎 的反应，按数字键，也会卡，那可能就不是这一处的影响
            
            # https://stackoverflow.com/questions/4299432
                # global_variable.root_window.focus_set()
                # 这能管用吗 算球了，反正 iconify() 暂时有效
            
            def window_withdraw():
                global_variable.root_window.iconify() #
                global_variable.root_window.withdraw()
                #global_variable.root_window.wm_state("withdrawn")
            def window_show_again():
                root = global_variable.root_window
                
                root.iconify()
                
                root.deiconify()
                
                # 列表要不要刷新一下？
                    # 应该不用了
                #global_variable.root_window.update()
                    # 不能刷新太早了
                    # 太早，不可见时，设置的　刷新无效
                    # 算了，直接把 列表刷新的条件 table.winfo_viewable() 去掉
                
                
                root.update()
                
                children = root.winfo_children()
                #print(children)
                if len(children)==1: # 如果没有其它 子窗口 时
                    
                    root.lift()
                    
                    #print("just 1")
                    root.call('wm', 'attributes', '.', '-topmost', True)
                    # root.attributes("-topmost", True)
                    #root.update()
                    #root.call('wm', 'attributes', '.', '-topmost', False)
                    root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
                    
                    # focus_set
                    try:
                        global_variable.the_showing_table.focus_set()
                    except:
                        pass
            
            
            window_withdraw()
            
            # returncode 不为 0 时，显示报错信息
            if global_variable.user_configure_data["show_error_info"]:
                proc = subprocess.Popen(
                        command_list,
                        shell=shell,
                        cwd=cwd,
                        # stdout=subprocess.PIPE, # 不记录这个
                        stderr=subprocess.PIPE, 
                        )
                
                outs, errs = proc.communicate()
                
                window_show_again()
                
                # returncode 不为 0 时
                # 显示 报错信息
                if (proc.returncode!=0) and errs:
                    # errs 编码 
                    # mame 运行时，应该是程序输出的编码
                    # ？？ shell=True 时 参数设置错误，程序未运行成功，命令行报错时，应该是命令行使用的编码
                    # 编码还不一样
                    
                    def bytes_to_string(errs):
                        encoding_list=[]
                        
                        if global_variable.user_configure_data["encoding"]:
                            encoding_list.append( global_variable.user_configure_data["encoding"] )
                        
                        if not encoding_list:
                            encoding_list.append('utf_8_sig') # mame 应该是这个
                        
                        if sys.platform.startswith('win32'):
                            if 'mbcs' not in encoding_list: # ansi
                                # mameplus 可能是这个
                                # 另外
                                # 如果程序没有设置正确，命令行报错，估计是这个
                                encoding_list.append('mbcs')
                        
                        text=None
                        for encoding in encoding_list:
                            try:
                                text=errs.decode(encoding=encoding)
                                print(encoding)
                                break
                            except:
                                text=None
                        
                        # 默认 
                        # 已经设置的值 或者 utf_8_sig
                        if text is None:
                            
                            if global_variable.user_configure_data["encoding"]:
                                encoding = global_variable.user_configure_data["encoding"]
                            else:
                                encoding = 'utf_8_sig'
                            
                            text = errs.decode(encoding=encoding, errors='replace')
                        
                        return text
                        
                    text = bytes_to_string(errs)
                    messagebox.showerror(title="stderr",message=text)
                elif errs:
                    print()
                    print("stderr:")
                    try:
                        sys.stdout.buffer.write(errs)
                    except:
                        pass
                    print()
                
                
            # 不显示报错信息
            else:
                proc = subprocess.Popen(
                        command_list,
                        shell=shell,
                        cwd=cwd
                        )
                
                proc.wait()
                
                window_show_again()
        
        else: # 打开游戏，不隐藏 UI
            subprocess.Popen(
                    command_list,
                    shell=shell,
                    cwd=cwd
                    )
    

    
    
    def get_mame_path_and_working_directory(self,):
        # mame_exe
        # mame_dir
        #   用于 subprocess.Popen 函数
    
        # 如果存在此文件，设为绝对值
        # 如果不存在此文件，当成 ，它 在 系统 环境变量 里
        if os.path.isfile( global_variable.user_configure_data["mame_path"] ):
            mame_exe = os.path.abspath( global_variable.user_configure_data["mame_path"] )
        else:
            mame_exe = global_variable.user_configure_data["mame_path"]
    
        mame_working_directory = None # 默认值
        
        # 如果已设置
        #if global_variable.user_configure_data["mame_working_directory"] :
        if os.path.isdir( global_variable.user_configure_data["mame_working_directory"] ):
            mame_working_directory = os.path.abspath( global_variable.user_configure_data["mame_working_directory"] )
        # 默认值
        #   如果值 没有 设置 ，为空
        #   自动设置为 mame 所在文件夹
        else:
            #global_variable.user_configure_data["mame_working_directory"] == "" :
            if os.path.isfile( global_variable.user_configure_data["mame_path"] ):
                temp                   = os.path.dirname( global_variable.user_configure_data["mame_path"] )
                mame_working_directory = os.path.abspath( temp )
                

        
        return (mame_exe , mame_working_directory)
    
    def get_bios_list(self,machine,cwd=None,mame_path=None):
        
        if mame_path is None:
            mame_path , cwd = self.get_mame_path_and_working_directory()
        
        command_list=[]
        command_list.append(mame_path)
        command_list.append(machine)
        command_list.append("-listxml")
        
        temp_io = io.BytesIO()
        temp_string=[]
        p = subprocess.Popen( command_list, 
                            shell=global_variable.user_configure_data["use_shell"],
                            stdout=subprocess.PIPE  , 
                            stderr=subprocess.PIPE ,
                            stdin=subprocess.PIPE,
                            #encoding="utf_8",# python 3.4 不兼容这选项 。同时也不方便检查 gbk
                            cwd=cwd,
                            )
        for line in p.stdout:
            temp_io.write(line)
        temp_io.seek(0)
        #for line in p.stdout:
        #    temp_string.append( line.decode() )
        
        bios_list = []
        tree = xml.etree.ElementTree.parse(temp_io)
        root = tree.getroot()
        #print(root)
        for child in root:
            if child.tag in ("machine" ,"game"):

                if( "name" in child.attrib ):
                    
                    game_name = child.attrib["name"].strip().lower()
                    
                    if game_name==machine:
                        for grandchild in child:
                            if grandchild.tag=="biosset" :
                                if "name" in grandchild.attrib:
                                    bios_name = grandchild.attrib["name"]
                                    bios_list.append(bios_name)
                        break
        
        #print(bios_list)
        return bios_list

    
    def get_uni_bios_list(self,machine,cwd=None,mame_path=None):
        
        bios_list = self.get_bios_list(machine,cwd=cwd,mame_path=mame_path)
        
        uni_bios_list =[]
        
        if not bios_list:
            return uni_bios_list
        
        for bios_name in bios_list:
            if "uni" in bios_name.lower():
                uni_bios_list.append(bios_name)
        
        #print(uni_bios_list)
        return uni_bios_list

    
    def get_uni_bios_last(self,machine,cwd=None,mame_path=None):
        uni_bios_list = self.get_uni_bios_list(machine,cwd=cwd,mame_path=mame_path)
        
        if not uni_bios_list:
            return ""
        
        uni_bios_list.sort()
        
        print("Universe Bios")
        for x in uni_bios_list:
            print("\t",x)
        
        uni_bios_choosen=""
        for x in reversed(uni_bios_list):
            if x.lower().endswith("o"): # 老版本标记
                pass
            else:
                uni_bios_choosen=x
                break
        # 默认值
        if not uni_bios_choosen:
            uni_bios_choosen=uni_bios_list[-1]
        
        if uni_bios_choosen != uni_bios_list[-1]:
            print("last",uni_bios_list[-1])
            print("choosen",uni_bios_choosen)
        else:
            print(uni_bios_list[-1])
        
        return uni_bios_choosen
    
    # 参数运行
    def run_by_file(self,file_path,item_id,hide=True):
        
        # item_id 为 machine
        # emu_number
        machine      = item_id

        mame_exe , mame_working_directory = self.get_mame_path_and_working_directory()
        
        the_folder = the_files.emulator_configure_folder
        the_file   = file_path
        
        ##############
        
        if not os.path.isfile(the_file):
            print("file not exist : ",the_file)
            return
        
        print("")
        print("run by file")
        print(the_file)
        
        command_list = []
        cwd = None
        flag_use_mame = False # 如果用了 mame ，cwd 需要考虑原有值
        
        file_content=[]
        with open(the_file,mode="rt",encoding="utf_8_sig") as f:
            for line in f :
                line = line.strip()
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
        

        
        # 以空字符分隔
        # 内容 
        #   不含 \s
        str_1 = r'^([^\s]+)$'
        p=re.compile(str_1,)
        
        # 内容2
        #   含 \s
        str_2 = r'^([^\s]+)\s*([^\s].*)$'
        p2=re.compile(str_2,)
        
        for line in file_content:
            
            # 注释
            if line.startswith("#") : 
                continue
                
            # 内容行 1 
            m=p.search( line )
            if m:
                if m.group(1)   == r"%mame%" :
                    command_list.append(mame_exe)
                    flag_use_mame = True
                elif m.group(1) == r"%machine%" :
                    command_list.append(machine)
                elif m.group(1) == r"%unibios_last%" : # 使用默认 模拟器
                    uni_bios = self.get_uni_bios_last(machine)
                    if uni_bios:
                        command_list.append("-bios")
                        command_list.append(uni_bios)
                elif m.group(1) == r"%unibios_last_other%" :# 使用 其它 mame 模拟器
                    if command_list:
                        uni_bios = self.get_uni_bios_last(machine,cwd=cwd,mame_path=command_list[0])
                        if uni_bios:
                            command_list.append("-bios")
                            command_list.append(uni_bios)
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
        
        #print(command_list)
        #print(cwd)
        
        # start game
        self.start_emu_by_subprocess(
                    command_list,
                    shell=global_variable.user_configure_data["use_shell"],
                    cwd=cwd,
                    hide=hide
                    )
    
    # start_game SL 1 - 9
    def run_by_file_sl(self,file_path,item_id,hide=True):
        
        # item_id 为 xml + name
        # emu_number
        xml      = item_id.split(" ",1)[0]
        software = item_id.split(" ",1)[1]
        print()
        
        mame_exe , mame_working_directory = self.get_mame_path_and_working_directory()
        
        the_file   = file_path
        # xxxxx\nes\1.txt
        # xxxxx\nes\2.txt
        
        print(the_file)
        
        ##############
        
        if not os.path.isfile(the_file):
            print("file not exist : ",the_file)
            return
        
        
        command_list = []
        cwd = None
        flag_use_mame = False # 如果用了 mame ，cwd 需要考虑原有值
        
        
        
        file_content=[]
        with open(the_file,mode="rt",encoding="utf_8_sig") as f:
            for line in f :
                line=line.strip()
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
        
        # 以空字符分隔
        # 内容 
        #   不含 \s
        str_1 = r'^([^\s]+)$'
        p=re.compile(str_1,)
        
        # 内容2
        #   含 \s
        str_2 = r'^([^\s]+)\s*([^\s].*)$'
        p2=re.compile(str_2,)
        
        for line in file_content:
            
            # 注释
            if line.startswith("#") : 
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
                
                elif m.group(1) == r"%unibios_last%" : # 使用默认 模拟器
                    machine = m.group(2)
                    uni_bios = self.get_uni_bios_last(machine)
                    if uni_bios:
                        command_list.append("-bios")
                        command_list.append(uni_bios)
                
                elif m.group(1) == r"%unibios_last_other%" :# 使用 其它 mame 模拟器
                    if command_list:
                        machine = m.group(2)
                        uni_bios = self.get_uni_bios_last(machine,cwd=cwd,mame_path=command_list[0])
                        if uni_bios:
                            command_list.append("-bios")
                            command_list.append(uni_bios)
        
        # 如果用了 mame
        if flag_use_mame == True:
            if not cwd:
                cwd = mame_working_directory
        
        
        if not command_list :return
        
        #print(command_list)
        #print(cwd)
        
        # start game
        self.start_emu_by_subprocess(
                    command_list,
                    shell=global_variable.user_configure_data["use_shell"],
                    cwd=cwd,
                    hide=hide,
                    )
        
    
    # start_game mame 1 - 9
    def get_other_emu_configure(self,item_id,emu_number,hide=True,alt=False):
        
        if alt:
            the_folder_by_source = the_files.emulator_configure_folder_by_source
            
            game_info = global_variable.machine_dict[item_id]
            
            if "sourcefile" not in global_variable.columns_index:
                return
            
            index = global_variable.columns_index["sourcefile"]
            sourcefile = game_info[index]
            sourcefile = sourcefile.replace("\\",os.sep)
            sourcefile = sourcefile.replace("/",os.sep)
            sourcefile = os.path.splitext(sourcefile)[0]
            
            the_folder = os.path.join(the_folder_by_source,sourcefile)
            the_file   = os.path.join(the_folder,str(emu_number)+".txt")
        else:
            the_folder = the_files.emulator_configure_folder
            the_file   = os.path.join(the_folder,str(emu_number)+".txt")
            # xxxxx\1.txt
            # xxxxx\2.txt
        
        self.run_by_file(the_file,item_id,hide=hide)

    
    # start_game SL 1 - 9
    def get_other_emu_configure_sl(self,item_id,emu_number,hide=True):
        
        # item_id 为 xml + name
        # emu_number
        xml      = item_id.split(" ",1)[0]
        software = item_id.split(" ",1)[1]
        print()
        
        the_folder = the_files.emulator_configure_folder_sl
        the_file   = os.path.join(the_folder,xml,str(emu_number)+".txt")
        # xxxxx\nes\1.txt
        # xxxxx\nes\2.txt
        
        self.run_by_file_sl(the_file,item_id,hide=hide)
    
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
        binary_content = []
        p = subprocess.Popen( command_list, 
                            shell=global_variable.user_configure_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            #encoding="utf_8",# python 3.4 不兼容这选项 。同时也不方便检查 gbk
                            cwd=mame_dir,
                            )
        for binary_line in p.stdout:
            binary_content.append( binary_line )
        
        the_encoding = self.check_binary_string_list_encoding(binary_content)
        
        for binary_line in binary_content:
            line = binary_line.decode(encoding=the_encoding, errors='replace')
            #print(line,end='')
            content.append(line)
        
        temp_string = " "
        if len(other_option)>=1:
            try:
                temp_string = str(other_option[0])
            except:
                temp_string = " "
        
        
        self.show_text_winodw(content=content,title=temp_string,)
    
    # 二进制字符串列表，检查 字符编码
    def check_binary_string_list_encoding(self,binary_string_list):
        
        if global_variable.user_configure_data["encoding"] :
            print("user encoding")
            print(global_variable.user_configure_data["encoding"])
            return global_variable.user_configure_data["encoding"]
        
        encoding_list=["utf_8_sig",]
        
        if sys.platform.startswith('win32'):
            encoding_list=["utf_8_sig","mbcs","gbk"]
                # utf_8 、utf_8_sig
                # gbk 其实要比 对应的 ANSI 少一点点，比如欧元符号
                # big5
                # mbcs : Windows 专属：根据 ANSI 代码页（CP_ACP）对操作数进行编码。
        else:
            encoding_list=["utf_8_sig","gbk"]
        
        the_right_encoding = 'utf_8' # 默认值
        
        for the_encoding in encoding_list:
            flag_encoding_is_ok = False
            
            try:
                for binary_line in binary_string_list:
                    line = binary_line.decode(encoding=the_encoding, )
                flag_encoding_is_ok = True
            except:
                flag_encoding_is_ok = False
            
            if flag_encoding_is_ok:
                the_right_encoding = the_encoding
                print("the_right_encoding:{}".format(the_encoding))
                break
        
        return the_right_encoding
    
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
        
        window.transient(global_variable.root_window)
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
        scrollbar_1.grid(row=0,column=1,sticky=tk.N+tk.S,)
        scrollbar_2.grid(row=1,column=0,sticky=tk.W+tk.E,)
        
        ttk.Sizegrip(window).grid(row=1,column=1,sticky=tk.N+tk.S,)
        
        if content:
            for x in content:
                t.insert(tk.END, x, )
        
        t["state"]="disabled"

        window.wait_window()
    ##########
    # font 初始化
    def font_initial(self,):
        print("")
        print("font_initial")
        print("")
        
        all_font = tkfont.families()
        
        # "TkDefaultFont"
        font_defualt = tkfont.nametofont("TkDefaultFont")
        default_name = font_defualt.actual("family")
        default_size = font_defualt.actual("size")
        
        # font size 正整数 
        # font size 负整数 都可以
        
        # gamelist font
        font_name = default_name
        if global_variable.user_configure_data["gamelist_font"] in all_font:
            font_name = global_variable.user_configure_data["gamelist_font"]
        font_size = default_size
        if global_variable.user_configure_data["gamelist_font_size"] != 0: 
            font_size = global_variable.user_configure_data["gamelist_font_size"]
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
        if global_variable.user_configure_data["gamelist_header_font"] in all_font:
            font_name = global_variable.user_configure_data["gamelist_header_font"]
        font_size = the_size
        if global_variable.user_configure_data["gamelist_header_font_size"] != 0:
            font_size = global_variable.user_configure_data["gamelist_header_font_size"]
        # 记录
        global_variable.font_gamelist_header=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_gamelist_font_for_header()
        
        # text font 1
        font_name = default_name
        if global_variable.user_configure_data["text_font"] in all_font:
            font_name = global_variable.user_configure_data["text_font"]
        font_size = default_size
        if global_variable.user_configure_data["text_font_size"] != 0: 
            font_size = global_variable.user_configure_data["text_font_size"]
        # 记录
        global_variable.font_text=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_text_1_font()

        # text font 2
        font_name = default_name
        if global_variable.user_configure_data["text_2_font"] in all_font:
            font_name = global_variable.user_configure_data["text_2_font"]
        font_size = default_size
        if global_variable.user_configure_data["text_2_font_size"] != 0: 
            font_size = global_variable.user_configure_data["text_2_font_size"]
        # 记录
        global_variable.font_text_2=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_text_2_font()
        
        # others font
        font_name = default_name
        if global_variable.user_configure_data["others_font"] in all_font:
            font_name = global_variable.user_configure_data["others_font"]
        font_size = default_size
        if global_variable.user_configure_data["others_font_size"] != 0: 
            font_size = global_variable.user_configure_data["others_font_size"]
        # 记录
        global_variable.font_others=tkfont.Font( font=(font_name, font_size,),)
        # 执行
        self.set_others_font()
    
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
    
    # font others
    def set_others_font(self,):
        
        style = ttk.Style()
        
        if global_variable.font_others : 
            the_font = global_variable.font_others
            
            style.configure('TLabel', font = the_font)
            style.configure('TButton', font = the_font)
            style.configure('TMenubutton', font = the_font)
            style.configure('TCheckbutton', font=the_font)
            style.configure('TCombobox', font=the_font)# 没用，似乎
            style.configure('TNotebook', font=the_font)
            style.configure('TNotebook.Tab', font=the_font)
            
            # TEntry
            the_entry_list = self.find_widget("TEntry")
            for x in the_entry_list:
                x.configure(font=the_font)
            
            global_variable.root_window.option_add("*TCombobox*Listbox.font", the_font)
            global_variable.root_window.option_add("*font", the_font)
            global_variable.root_window.option_add('*Text*font', the_font)
            global_variable.root_window.option_add('*Listbox*font', the_font)            
            
            # combobox
            the_combobox_list = self.find_widget("TCombobox")
            for x in the_combobox_list:
                x.configure(font=the_font)
            
            # menu
            the_menu_list = self.find_widget("Menu")
            for x in the_menu_list:
                x.configure(font=the_font)
    
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
        window.transient(global_variable.root_window)
        
        window.columnconfigure(1,weight=1)
        
        # 字体
        
        ttk.Label(window,text = "",).grid(row=0,column=0,sticky=tk.W+tk.N)
        
        font_name_tkstring = tk.StringVar()

        label_font = ttk.Label(window,text = _("字体选择"),)
        label_font.grid( row=1,column=0,sticky=tk.W+tk.E)
        
        font_choose_box = ttk.Combobox(window, textvariable = font_name_tkstring,state="readonly",)
        font_choose_box.grid( row=1,column=1,sticky=tk.W+tk.E, )
        
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
        label_font_size.grid( row=3,column=0,sticky=tk.W+tk.E, )
        
        font_size_box = ttk.Combobox(window, textvariable = font_size_tkstring,state="readonly")
        font_size_box.grid(row=3,column=1,sticky=tk.W+tk.E,)
        
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
            #print(font_size)
            font_size = int(font_size)
            #print(font_size)
            
            if font_name:
                #print(font_name)
                the_font.config(family=font_name)
            
            if font_size!=0:
                #print(font_size)
                the_font.config(size=font_size)
                #print("xxx")
                #print(the_font.actual("size")) # 负的好像直接被转成正的了
            
        
        ttk.Label(window,text=_("负整数，字体单位是像素；正整数，字体单位是 point"),).grid(row=4,column=0,columnspan=2,sticky=tk.W+tk.N)
        ttk.Label(window,text = "",).grid(row=5,column=0,sticky=tk.W+tk.N)
        
        ttk.Button(window,text=_("确定"),command=for_ok_button).grid( row=6,column=0,sticky=tk.N+tk.E, )
        
        
        
        
        
        ttk.Label(window,text="").grid()
        
        
        window.wait_window()
    
    def for_save_font(self,):
        # 游戏列表字体
        the_font = global_variable.font_gamelist
        global_variable.user_configure_data["gamelist_font"]      = the_font.actual("family")
        global_variable.user_configure_data["gamelist_font_size"] = the_font.actual("size")
        
        # 游戏列表 标题 字体
        the_font = global_variable.font_gamelist_header
        global_variable.user_configure_data["gamelist_header_font"]      = the_font.actual("family")
        global_variable.user_configure_data["gamelist_header_font_size"] = the_font.actual("size")
        
        # 文本字体 一
        the_font = global_variable.font_text
        global_variable.user_configure_data["text_font"]      = the_font.actual("family")
        global_variable.user_configure_data["text_font_size"] = the_font.actual("size")
        
        # 文本字体 二
        the_font = global_variable.font_text_2
        global_variable.user_configure_data["text_2_font"]      = the_font.actual("family")
        global_variable.user_configure_data["text_2_font_size"] = the_font.actual("size")
        
        # others font
        the_font = global_variable.font_others
        global_variable.user_configure_data["others_font"]      = the_font.actual("family")
        global_variable.user_configure_data["others_font_size"] = the_font.actual("size")
        
    # row height
    def use_user_configure_row_height(self,):
        # gamelist row height
            # ttk.Treeview 
            # 自制 table
        # text 
        
        
        style = ttk.Style()
        if global_variable.user_configure_data["row_height"] > 0:
            # Treeview
            style.configure('Treeview', rowheight = global_variable.user_configure_data["row_height"])
            
            # 自制 table
            print(len(global_variable.all_tables))
            for table in global_variable.all_tables:
                
                table.new_func_set_row_height( global_variable.user_configure_data["row_height"] )
        
    # row height for header
    def use_user_configure_row_height_for_header(self,):
        # gamelist row height
            # ttk.Treeview ,header row height ，不知道怎样设置
            # 自制 table 设置
        # text row height
        
        if global_variable.user_configure_data["row_height_for_header"] > 0:

            # 自制 table
            for table in global_variable.all_tables:
                table.new_func_set_row_height_for_header( global_variable.user_configure_data["row_height_for_header"] )
    
    # icon width
    def use_user_configure_icon_width(self,):
        # 自制 table
        for table in global_variable.all_tables:
            table.new_func_set_icon_width( global_variable.user_configure_data["icon_size"] )
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
        window.transient(global_variable.root_window)
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
            
            if global_variable.user_configure_data[key_word]:
                try:
                    label.configure( background = global_variable.user_configure_data[key_word] )
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
                global_variable.user_configure_data[key_word] = widget["background"]
            
            self.use_user_configure_colours()
        
        # ui
        tk.Button(frame,text=_("确定"),background="grey95",foreground="black",command=for_ok_button).grid(row=r,column=0,columnspan=2,sticky=tk.E+tk.N,)
        r+=1
        
        
        window.wait_window()
    
    
    def use_user_configure_colours(self,):
        style = ttk.Style()
        
        if style.theme_use() not in global_variable.internal_themes:
            print("not internal themes,not use colours")
            return
        
        if global_variable.user_configure_data["foreground"]:
            
            cf = global_variable.user_configure_data["foreground"]
            
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
            
            global_variable.root_window.option_add('*Toplevel*foreground', cf)
            global_variable.root_window.option_add('*Text*foreground', cf)
            global_variable.root_window.option_add('*Listbox*foreground', cf)
            global_variable.root_window.option_add("*TCombobox*Listbox.foreground ", cf)

        if global_variable.user_configure_data["background"]:
            
            c = global_variable.user_configure_data["background"]
            
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
            global_variable.root_window.option_add('*Toplevel*background', c)
            global_variable.root_window.option_add('*Listbox*background', c)
            global_variable.root_window.option_add('*Text*background', c)
            global_variable.root_window.option_add('*Canvas*background', c)
    
        if global_variable.user_configure_data["selectforeground"]:
            c_sf = global_variable.user_configure_data["selectforeground"]
            
            style.configure('.',selectforeground = c_sf)
            
            style.map('Treeview', foreground =[ ('selected',c_sf) ] )
            
            for table in global_variable.all_tables:
                table.new_func_set_colour_and_font(selectforeground=c_sf)
            
            for text in (global_variable.tk_text_1,global_variable.tk_text_2):
                text.configure(selectforeground=c_sf)
        
        if global_variable.user_configure_data["selectbackground"]:
            c_sb = global_variable.user_configure_data["selectbackground"]
            
            style.configure('.',selectbackground = c_sb)
            
            style.map('Treeview', background =[ ('selected',c_sb) ] )
            
            for table in global_variable.all_tables:
                table.new_func_set_colour_and_font(selectbackground=c_sb)
            
            for text in (global_variable.tk_text_1,global_variable.tk_text_2):
                text.configure(selectbackground=c_sb)
        
        if global_variable.user_configure_data["background_for_panedwindow"]:
            style.configure('TPanedwindow',background =global_variable.user_configure_data["background_for_panedwindow"])
    
    ##########
    ##########
    ##########
    ##########
    # 周边
    #   建目录
    #  for menu bar 周边文档，建目录
    def extra_docs_make_index(self,):
        print("")
        print("extra_docs_make_index")
        print("waiting......")
        
        root = global_variable.root_window
        
        progressbar = ttk.Progressbar(root)
        progressbar.grid(row=0,column=0,rowspan=2,sticky=tk.W+tk.E+tk.S)
        progressbar.grab_set()
        progressbar.start()
        
        
        def make_index():
            
            # history.xml
            def make_index_of_history_xml():
                
                # 文件路径
                path = global_variable.user_configure_data["history.xml_path"]
                path = path.replace(r'"',"") # 去掉双引号
                
                if os.path.isfile(path) : 
                
                    index_dict = {}
                    if global_variable.gamelist_type == "softwarelist":
                        index_dict = extra_read_history_xml.get_index(path,the_type="softwarelist")
                    else:# mame
                        index_dict = extra_read_history_xml.get_index(path,)
                    
                    if index_dict:
                        global_variable.extra_index_for_histroty_xml = index_dict
                        save_pickle.save(index_dict,the_files.file_pickle_extra_index_history_xml)
                
            # ("history.dat","sysinfo.dat",)
            # history.dat
            def make_index_of_history_dat():
                #if global_variable.gamelist_type == "mame":
                # history.dat
                path = global_variable.user_configure_data["history.dat_path"]
                path = path.replace(r'"',"") # 去掉双引号
                if os.path.isfile(path) : 
                    index_dict = {}
                    # file_pickle_extra_index_history_dat
                    # global_variable.extra_index_for_histroty_dat
                    
                    index_dict = extra_history_dat.get_index( path ,global_variable.gamelist_type)
                    
                    if index_dict:
                        global_variable.extra_index_for_histroty_dat = index_dict
                        save_pickle.save(index_dict,the_files.file_pickle_extra_index_history_dat)
            # sysinfo.dat
            def make_index_of_sysinfo_dat():
                if global_variable.gamelist_type == "mame":
                    # history.dat
                    path = global_variable.user_configure_data["sysinfo.dat_path"]
                    path = path.replace(r'"',"") # 去掉双引号
                    if os.path.isfile(path) : 
                        index_dict = {}
                        # file_pickle_extra_index_history_dat
                        # global_variable.extra_index_for_histroty_dat
                        
                        index_dict = extra_history_dat.get_index( path )
                        
                        if index_dict:
                            global_variable.extra_index_for_sysinfo_dat = index_dict
                            save_pickle.save(index_dict,the_files.file_pickle_extra_index_sysinfo_dat)
            
            
            #("mameinfo.dat","messinfo.dat",)
            # mameinfo.dat
            def make_index_of_mameinfo_dat():
                if global_variable.gamelist_type == "mame":
                    # history.dat
                    path = global_variable.user_configure_data["mameinfo.dat_path"]
                    path = path.replace(r'"',"") # 去掉双引号
                    if os.path.isfile(path) : 
                        index_dict = {}
                        # file_pickle_extra_index_history_dat
                        # global_variable.extra_index_for_histroty_dat
                        
                        index_dict = extra_mameinfo_dat.get_index( path )
                        
                        if index_dict:
                            global_variable.extra_index_for_mameinfo_dat = index_dict
                            
                            save_pickle.save(index_dict,the_files.file_pickle_extra_index_mameinfo_dat)
            # messinfo.dat
            def make_index_of_messinfo_dat():
                if global_variable.gamelist_type == "mame":
                    # history.dat
                    path = global_variable.user_configure_data["messinfo.dat_path"]
                    path = path.replace(r'"',"") # 去掉双引号
                    if os.path.isfile(path) : 
                        index_dict = {}
                        # file_pickle_extra_index_history_dat
                        # global_variable.extra_index_for_histroty_dat
                        
                        index_dict = extra_mameinfo_dat.get_index( path )
                        
                        if index_dict:
                            global_variable.extra_index_for_messinfo_dat = index_dict
                            
                            save_pickle.save(index_dict,the_files.file_pickle_extra_index_messinfo_dat)
            
            #"command.dat","command_english.dat",
            # command.dat
            def make_index_of_command_dat():
                if global_variable.gamelist_type == "mame":
                    # history.dat
                    path = global_variable.user_configure_data["command.dat_path"]
                    path = path.replace(r'"',"") # 去掉双引号
                    if os.path.isfile(path) : 
                        index_dict = {}
                        
                        index_dict = extra_command.get_index( path )
                        
                        if index_dict:
                            global_variable.extra_index_for_command_dat = index_dict
                            
                            save_pickle.save(index_dict,the_files.file_pickle_extra_index_command_dat)
            def make_index_of_command_english_dat():
                if global_variable.gamelist_type == "mame":
                    # history.dat
                    path = global_variable.user_configure_data["command_english.dat_path"]
                    path = path.replace(r'"',"") # 去掉双引号
                    if os.path.isfile(path) : 
                        index_dict = {}
                        
                        index_dict = extra_command.get_index( path )# 和 command.dat 一样
                        
                        if index_dict:
                            global_variable.extra_index_for_command_english_dat = index_dict
                            
                            save_pickle.save(index_dict,the_files.file_pickle_extra_index_command_english_dat)
            
            # "gameinit.dat",
                # 建目录用 history.dat 的
            def make_index_of_gameinit_dat():

                if global_variable.gamelist_type == "mame":
                    # gameinit.dat
                    path = global_variable.user_configure_data["gameinit.dat_path"]
                    path = path.replace(r'"',"") # 去掉双引号
                    if os.path.isfile(path) : 
                        index_dict = {}
                        
                        index_dict = extra_history_dat.get_index( path ) 
                            # 使用 history 中的 建目录函数
                        
                        if index_dict:
                            global_variable.extra_index_for_gameinit_dat = index_dict
                            
                            save_pickle.save(index_dict,the_files.file_pickle_extra_index_gameinit_dat)

            
            make_index_of_history_xml()
            
            make_index_of_history_dat()
            make_index_of_sysinfo_dat()
            
            make_index_of_mameinfo_dat()
            make_index_of_messinfo_dat()
            
            make_index_of_command_dat()
            make_index_of_command_english_dat()
            
            make_index_of_gameinit_dat()
        
        
        thread = threading.Thread(target=make_index,)
        thread.start()
        
        #
        tkvar = tk.StringVar()
        tkvar.set("waiting")
        #
        def wait_threading(thread):
            nonlocal tkvar
            
            if thread.is_alive(): #运行
                root.after(300,wait_threading,thread)
            else: # 停止
                print("threading finish")
                root.after(10,tkvar.set ,("threading finish",))
        
        wait_threading(thread)
        
        if tkvar.get() == "waiting":
            root.wait_variable(tkvar)
        
        print("finish")
        progressbar.stop()
        progressbar.grab_release()
        progressbar.destroy()
    
    
    
    ##########
    ##########
    ##########
    ##########
    # save
    def user_configure_get_window_size(self,):
        # 主窗口大小
        height = global_variable.root_window.winfo_height() 
        width  = global_variable.root_window.winfo_width()
        # 得到的结果不准确，因为 菜单 ？？
        # 在 设置 global_variable.root_window.geometry 之后，马上 global_variable.root_window.update() 一下，就准确了
        # why ?
        # # #
        # 转为字符串 如 800x600
        size = str(width) + "x" + str(height)
        global_variable.user_configure_data["size"] = size
        
        print("")
        print("window size")
        print(global_variable.user_configure_data["size"])
    
    def user_configure_get_window_size_and_position(self,):
        print("")
        print("window size and position")
        
        # windows 
        if sys.platform.startswith("win") : # or sys.platform.startswith("darwin")
            #  global_variable.root_window.geometry() ，
            # 因为这个值在最大化时，反回的位置不太对
            
            if global_variable.root_window.wm_state() == "zoomed" : # 最大化
                global_variable.user_configure_data["zoomed"] = True
            else:
                global_variable.user_configure_data["zoomed"] = False
                
                size  =  global_variable.root_window.geometry() 
                global_variable.user_configure_data["size"] = size
            
            return
        
        # 其它
        size  =  global_variable.root_window.geometry() 
            # windows 最大化时，这个值反回的位置不太对
            # 其它没试过
        global_variable.user_configure_data["size"] = size
        
        
        print(global_variable.user_configure_data["size"])
    
    def user_configure_get_widget_position(self,):
        # 分隔线位置
        if global_variable.PanedWindow is not None:
            # 目录 游戏列表 ，分隔条 位置
            global_variable.user_configure_data["pos1"] = global_variable.PanedWindow.sashpos(0,)
            # 游戏开表 周边 ，分隔条 位置
            global_variable.user_configure_data["pos2"] = global_variable.PanedWindow.sashpos(1,)
        if global_variable.PanedWindow_2 is not None:
            # 图片处还有一条分隔线
            global_variable.user_configure_data["pos3"] = global_variable.PanedWindow_2.sashpos(0,)
    
    def user_configure_get_widget_option(self,):
        
        # 列宽度保存
        if global_variable.the_showing_table is not None:
            top_table = global_variable.the_showing_table
            columns_width = top_table.new_func_get_column_width()
            
            # 转为整数
            for x in columns_width:
                columns_width[x] = int(columns_width[x])
            
            global_variable.user_configure_data["gamelist_columns_width"] = columns_width
            print(global_variable.user_configure_data["gamelist_columns_width"])
        
        # 周边，notebook tab 选择记录
        if global_variable.Notebook_for_extra is not None:
            global_variable.user_configure_data["extra_tab_index"] = global_variable.Notebook_for_extra.index( global_variable.Notebook_for_extra.select() )
        
        # 图片区 是否使用 zip 选项记录
        if global_variable.tkint_flag_for_zip_1 is not None:
            global_variable.user_configure_data["extra_image_usezip"] = global_variable.tkint_flag_for_zip_1.get()
        if global_variable.tkint_flag_for_zip_2 is not None:
            global_variable.user_configure_data["extra_image_usezip_2"] = global_variable.tkint_flag_for_zip_2.get()
        # 文本区 是否使用 建立目录 记录
        if global_variable.tkint_flag_for_text_index_1 is not None:
            global_variable.user_configure_data["extra_text_use_index_1"] = global_variable.tkint_flag_for_text_index_1.get()
        if global_variable.tkint_flag_for_text_index_2 is not None:
            global_variable.user_configure_data["extra_text_use_index_2"] = global_variable.tkint_flag_for_text_index_2.get()
        
        # Combobox 选项记录
        #图片一
        if global_variable.Combobox_chooser_image_1 is not None:
            global_variable.user_configure_data["extra_image_chooser_index"] = global_variable.Combobox_chooser_image_1.current()
        #图片二
        if global_variable.Combobox_chooser_image_2 is not None:
            global_variable.user_configure_data["extra_image_chooser_2_index"] = global_variable.Combobox_chooser_image_2.current()
        #文本一
        if global_variable.Combobox_chooser_text_1 is not None:
            global_variable.user_configure_data["extra_text_chooser_index"] = global_variable.Combobox_chooser_text_1.current()
        #文本二
        if global_variable.Combobox_chooser_text_2 is not None:
            global_variable.user_configure_data["extra_command_type_chooser_index"] = global_variable.Combobox_chooser_text_2.current()
    
    def user_configure_get_index_last_record(self,):
        # 记录 treeview 中的 iid_string ，
        # 方便判断下一打开时，如果是外置目录，此 iid_string 还存不存在
        if global_variable.the_index:
            event_data = global_variable.the_index.new_var_data_for_virtual_event
            iid_string = ""
            if event_data is not None:
                for x in event_data:
                    iid_string += x + "|"
                if iid_string:
                    iid_string=iid_string[0:-1]
            global_variable.user_configure_data["index_be_chosen"] = iid_string
            print(iid_string)

    def user_configure_get_table_option(self,):
        table = global_variable.the_showing_table
        global_variable.user_configure_data["game_be_chosen"] = table.new_var_remember_select_row_id    
        global_variable.user_configure_data["gamelist_sorted_by"] = table.new_var_data_holder.sort_key     
        global_variable.user_configure_data["gamelist_sorted_reverse"] = table.new_var_data_holder.sort_reverse    
    
    def save_user_configure_just_after_initial(self,):
        # 刚初始化之后，
        # 有些选项 不能 读取 ，
        # 仅保存 现有 选项
        try:
            #read_user_config.write_ini(ini_file_name,ini_dict,order = None)
            read_user_config.write_ini(
                    the_files.file_ini_configure,
                    global_variable.user_configure_data,
                    order = global_variable.user_configure_data_order)
            print("")
            print("after initial")
            print("save configure file")
            #print( global_variable.user_configure_data["mame_path"] )
        except:
            pass
    
    def save_user_configure(self,):
        
        self.user_configure_get_widget_option()
        
        self.for_save_font()
        
        self.user_configure_get_table_option()

        self.user_configure_get_index_last_record()
        
        try:
            #read_user_config.write_ini(ini_file_name,ini_dict,order = None)
            read_user_config.write_ini(
                    the_files.file_ini_configure,
                    global_variable.user_configure_data,
                    order = global_variable.user_configure_data_order)
            print("save configure file")
            print( global_variable.user_configure_data["mame_path"] )
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
    ###################
    # save ，目录 编辑后 保存
    def new_func_index_popup_menu_function_save(self,event=None):
        # global_variable.external_index_files_be_edited
        for x in global_variable.external_index_files_be_edited :
            try:
                folders_save.save(x , global_variable.external_index[x])
                print("save",x)
            except:
                pass
        global_variable.external_index_files_be_edited = set() # 重置
    
    #######################
    def find_widget(self,class_name):
        # 查找
        result=[]
        
        def find_childen(window):
            for child in window.winfo_children():
                if child.winfo_class()==class_name:
                    result.append(child)

                find_childen(child)
        
        find_childen(global_variable.root_window)
        
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
        
        #global_variable.available_set
        #global_variable.unavailable_set
        #global_variable.available_hide_set
        
        # 记录 
        # 拥有部分
        global_variable.available_set   = available_items
        global_variable.unavailable_set = global_variable.set_data["all_set"] - available_items
        
        # 保存数据
        if need_save :
            #the_files.file_pickle_gamelist_available
            save_pickle.save(available_items,the_files.file_pickle_gamelist_available)
        
    
    
    
    # 刷新 拥有列表 split
    def gamelist_available_refresh_bak(self,merged = False):
        ""
        print()
        print("gamelist available refresh")
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        if global_variable.gamelist_type == "softwarelist":
            temp_set = self.get_files_names_in_rompath_sl(merged = merged)
        else:
            temp_set = self.get_files_names_in_rompath(merged = merged)
        
        self.set_available_gamelist(temp_set,need_save=True)
        
        global_variable.root_window.event_generate('<<RequestForAvailableGameList>>')
    
    # 不卡 UI
    def gamelist_available_refresh(self,merged = False):
        ""
        print()
        print("gamelist available refresh")
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        # subprocess 
        # 从命令行读取 roms 路径信息
        # subprocess，读取 roms 路径，
        # 如果第一次读取 mame 的话，mame 几百 M ，可能卡一下
        roms_folder_list = self.get_roms_folder_list()
        
        # 进度条
        root = global_variable.root_window
        progressbar = ttk.Progressbar(root)
        progressbar.grid(row=0,column=0,rowspan=2,sticky=tk.W+tk.E+tk.S)
        progressbar.grab_set()
        progressbar.start()
        
        # threading
        
        def func_1():
            
            if global_variable.gamelist_type == "softwarelist":
                temp_set = self.get_files_names_in_rompath_sl(merged = merged,roms_folder_list=roms_folder_list)
            else:
                temp_set = self.get_files_names_in_rompath(merged = merged,roms_folder_list=roms_folder_list)
            
            self.set_available_gamelist(temp_set,need_save=True)

        thread = threading.Thread(target=func_1,)
        thread.start()
        
        #
        tkvar = tk.StringVar()
        tkvar.set("waiting")
        #
        def wait_threading(thread):
            
            if thread.is_alive(): #运行
                root.after(300,wait_threading,thread)
            else: # 停止
                print("threading finish")
                root.after(10,tkvar.set ,("threading finish",))
        
        wait_threading(thread)
        # wait
        if tkvar.get() == "waiting":
            root.wait_variable(tkvar)
        
        print("threading finish")


        # 进度条 取消
        progressbar.stop()
        progressbar.grab_release()
        progressbar.destroy()
        
        global_variable.root_window.event_generate('<<RequestForAvailableGameList>>')

    # 刷新 拥有列表 merged
    def gamelist_available_refresh_2(self,):
        self.gamelist_available_refresh(merged=True)
    
    # 初始化 ui_main.py
    def initial_available_filter_set(self,):
        
        global_variable.available_filter_set.clear()
        
        for x in global_variable.user_configure_data["filter"]:
            # 目前都是 目录 第一层 的
            temp = misc.get_id_list_from_internal_index(x)
            
            global_variable.available_filter_set.update( temp )


    def get_roms_folder_list(self):
        
        roms_folder_list = []
        
        # rompath 里记录的文件，相对位置是相对于模拟器的，这个还得改一下
        rom_path = self.get_rompath_from_command_line()
        
        (mame_exe , mame_dir) = self.get_mame_path_and_working_directory()
        
        if rom_path:
            rom_path = rom_path.replace(r'"',"") # 去掉双引号
        
        for x in rom_path.split(r';'):
            if x:
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
                    roms_folder_list.append( y )
                else: # 如果是，相对路径，转换
                    if mame_dir != None:# 已设置 mame 工作文件夹
                        # mame 所在文件夹 ,绝对路径
                        mame_folders = mame_dir
                        mame_folders = os.path.abspath( mame_folders )
                        
                        # 相对转换路径后的绝对路径
                        y = os.path.join(mame_folders,temp_path)
                        
                        if os.path.isdir(y):
                            y = os.path.abspath( y )
                            roms_folder_list.append( y )
                    else:# 未设置 mame 工作文件夹，且不是默认值
                        #当成与 jjui 同文件夹对待？
                        y = x
                        if os.path.isdir(y):
                            y = os.path.abspath( y )
                            roms_folder_list.append( y )
        return roms_folder_list

    # 刷新列表
    # 找到拥有的 *.zip 、*.7z 、文件夹
    def get_files_names_in_rompath(self,merged = False,roms_folder_list=None):
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        temp=[]
        
        if roms_folder_list is None:
            roms_folder_list = self.get_roms_folder_list()
        print()
        print(roms_folder_list)
        print()
        
        for a_folder in roms_folder_list:
            if not os.path.isdir(a_folder):
                continue
            
            (dirpath, dirnames, filenames) = next( os.walk(a_folder) )
            
            # 文件夹
            for name in dirnames:
                temp.append( name.lower() )
            
            # zip or 7z
            for name in filenames:
                
                name_lower=name.lower()
                
                if name_lower.endswith(r".zip") :
                    temp.append(name_lower[0:-4]) # .zip
                elif name_lower.endswith(r".7z"):
                    temp.append(name_lower[0:-3]) # .7z
                    
        
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
    
    # 刷新列表 sl
    # 找到拥有的 *.zip 、*.7z 、文件夹
    # copy 上面的
    def get_files_names_in_rompath_sl(self,merged = False,roms_folder_list=None):
        # 仅检查文件 存在 与否
        # 不深度检查文件的 正确性、完整性
        # *.zip 、*.7x 、文件夹
        
        # rompath 里记录的文件，相对位置是相对于模拟器的，这个还得改一下            
        
        if roms_folder_list is None:
            roms_folder_list = self.get_roms_folder_list()
        
        temp_set = set()
        
        xml_dict = global_variable.dict_data["xml"]
        
        temp={}
        
        
        # 扫描
        for a_folder in roms_folder_list:
            if not os.path.isdir(a_folder):
                continue
            
            (dirpath, dirnames, filenames) = next( os.walk(a_folder) )
            
            for sub_folder_name in dirnames:
                xml_name = sub_folder_name.lower()
                if xml_name in xml_dict:
                    z=os.path.join(dirpath,sub_folder_name)
                    z=os.path.abspath(z)
                    # z 是 xml 名称的 子文件夹路径
                    
                    print("\t" ,end="")
                    print(z)

                    # z, ????\nes
                    # z, ????\gba
                    # z, ????\.....

                    if os.path.isdir( z ): 
                        
                        if xml_name not in temp:
                            temp[xml_name]= [] # 初始化
                        
                        (dirpath_2, dirnames_2, filenames_2) = next( os.walk(z) )
                        
                        # 文件夹
                        for name in dirnames_2:
                            temp[xml_name].append( xml_name + " " + name.lower())
                        
                        # zip or 7z
                        for name in filenames_2:
                            
                            name_lower=name.lower()
                            
                            if name_lower.endswith(r".zip") :# .zip
                                temp[xml_name].append( xml_name + " " + name_lower[0:-4])
                            elif name_lower.endswith(r".7z"):# .7z
                                temp[xml_name].append( xml_name + " " + name_lower[0:-3])
        
        # 交集
        for xml_name in temp:
            #temp[xml_name] = set( temp[xml_name] )# 转为 set
            temp[xml_name] = set( temp[xml_name] ) & xml_dict[xml_name] 
        
        temp_set = set() 
        
        a_temp_list = []
        for xml_name in temp:
            a_temp_list.extend(temp[xml_name])
        temp_set = set(a_temp_list)
        del a_temp_list
        
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
        
        
        content=[]
        binary_content = []
        sub_process = subprocess.Popen( command_list, 
                            shell=global_variable.user_configure_data["use_shell"],
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            #encoding="utf_8",python 3.4 没有这选项。同时也不方便 检查 gbk
                            cwd=mame_dir,
                            )
        for binary_line in sub_process.stdout:
            binary_content.append( binary_line )
        
        the_encoding = self.check_binary_string_list_encoding(binary_content)
        
        for binary_line in binary_content:
            line = binary_line.decode(encoding=the_encoding, errors='replace')
            #print(line,end='')
            content.append(line)
        
        for line in content:
            print(line)
            m = p.search(line)
            if m :
                rom_path = m.group(1)
                #print("find")
                break
        
        print()
        print()
        print("find rom path:")
        print(rom_path)
        return rom_path
    
    #######################
    #######################
    #######################
    # 翻译
    def gamelist_reload_translation(self,):
        # 翻译
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        size = "400x300"
        window.geometry(size)
        
        window.title(_("导入翻译文件"))
        
        window.lift()
        window.transient(global_variable.root_window)
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
                
                text = _("读取翻译文件，出错。注意将文件的 文本编码 保存为 utf-8-bom")
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
            translation_gamelist.add_translation( 
                translation_dict ,
                global_variable.machine_dict ,
                global_variable.columns,
                )
            
            global_variable.the_showing_table.new_func_refresh_table()
            
            #global_variable.all_data["machine_dict"] = global_variable.machine_dict
            
            # 文件更新
            save_pickle.save(global_variable.all_data , file_pickle_gamelist_data_file_name)
            
            del translation_dict
            del translationed_set
            
            
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
                text = _("读取翻译文件，出错。注意将文件的 文本编码 保存为 utf-8-bom")
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
            translation_gamelist.add_translation( 
                translation_dict ,
                global_variable.machine_dict ,
                global_variable.columns,
                )
            global_variable.the_showing_table.new_func_refresh_table()
            
            #global_variable.all_data["machine_dict"] = global_variable.machine_dict
            
            # 文件更新
            save_pickle.save( global_variable.all_data ,file_pickle_gamelist_data_file_name)
            
            del translation_dict
            del translationed_set
            
            window.destroy()

        n=0
        
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        the_file_name = the_files.file_txt_translation_for_gamelist
        
        ttk.Label(window,text= _("默认翻译文件：") + the_file_name,).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text= _(r"默认翻译文件，文字编码为：utf_8_bom")).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
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
            window.lift(global_variable.root_window)
        
        ttk.Button(window,text=_("选择"),width=-1,command=choose_file).grid(row=n,column=0,sticky=tk.W+tk.N,)
        
        new_file_path = tk.StringVar()
        ttk.Entry(window,textvariable=new_file_path).grid(row=n,column=1,sticky=tk.W+tk.N+tk.E,)
        n+=1
        
        ttk.Button(window,text=_("读取指定翻译文件"),width=-1,command = load_translation_file).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        n+=1
        
        ttk.Label(window,text="").grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text=_("编码提示：")).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        ttk.Label(window,text=_("将文本保存为 utf-8 带 bom ，可以包含多国文字")).grid(row=n,column=0,columnspan=2,sticky=tk.W+tk.N,)
        n+=1
        
        window.wait_window()
    # 翻译
    def ui_select_translation(self,):
        # ui 翻译
        window = tk.Toplevel()
        
        window.resizable(width=True, height=True)
        
        size = "400x300"
        window.geometry(size)
        
        window.title(_(r"界面翻译/UI translation"))
        
        window.lift()
        window.transient(global_variable.root_window)
        
        # filedialog
        #file_path = filedialog.askopenfilename( initialdir="." ,filetypes=[( _(".exe 文件"),"*.exe"),(_("所有文件"),"*")],)
        
        def for_button_use_internal_language():
            global_variable.user_configure_data["ui_language"] = ""
            
            window.destroy()
            
            self.save_user_configure()
        
        def for_button_select_other_translation_file():
            the_folder_path = the_files.folder_language
            file_path = filedialog.askopenfilename( initialdir=the_folder_path ,filetypes=[( _(".txt 文件"),"*.txt"),],)
            
            
            if file_path:
                file_path =  os.path.abspath(file_path) # 绝对
                
                print(file_path)
                
                try:
                    the_path = os.path.relpath(file_path, start=os.curdir) #相对
                except:
                    the_path = file_path # 绝对
                
                print(the_path)
                
                global_variable.user_configure_data["ui_language"] = the_path
                
                window.destroy()
                
                self.save_user_configure()
        
        row=0
        
        ttk.Label(window,text="").grid(row=row,column=0,sticky=tk.W+tk.N)
        row+=1
        
        
        button_chinese = ttk.Button(window,text=_(r"中文 / Chinese"),command=for_button_use_internal_language)
        button_chinese.grid(row=row,column=0,sticky=tk.W+tk.N)
        row+=1
        
        ttk.Label(window,text="").grid(row=row,column=0,sticky=tk.W+tk.N)
        row+=1
        
        button_2 = ttk.Button(window,text=_(r"选择其它翻译文件 / choose other translation file"),command=for_button_select_other_translation_file)
        button_2.grid(row=row,column=0,sticky=tk.W+tk.N)
        row+=1
        
        ttk.Label(window,text="").grid(row=row,column=0,sticky=tk.W+tk.N)
        row+=1
        
        ttk.Label(window,text=_(r"需关闭程序 / need close this application") ).grid(row=row,column=0,sticky=tk.W+tk.N)
        
        
        window.wait_window()
    
    
    
    #
    def use_threading(self,a_func):
    
        # 进度条
        root = global_variable.root_window
        progressbar = ttk.Progressbar(root)
        progressbar.grid(row=0,column=0,rowspan=2,sticky=tk.W+tk.E+tk.S)
        progressbar.grab_set()
        progressbar.start()
        
        #
        tkvar = tk.StringVar()
        tkvar.set("waiting")        
        
        #
        def wait_threading(thread):
            
            if thread.is_alive(): #运行
                root.after(300,wait_threading,thread)
            else: # 停止
                print("threading finish")
                root.after(10,tkvar.set ,("threading finish",))
        
        #
        thread = threading.Thread(target=a_func,)
        thread.start()

        #
        wait_threading(thread)
        # wait
        if tkvar.get() == "waiting":
            root.wait_variable(tkvar)
        
        # 进度条 取消
        progressbar.stop()
        progressbar.grab_release()
        progressbar.destroy()
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
        #print(r"global_variable.root_window.destroy()")
        global_variable.root_window.destroy()
    #################
    #################


misc_funcs = Misc_functions()
