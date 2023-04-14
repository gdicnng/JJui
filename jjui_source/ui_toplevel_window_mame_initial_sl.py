# -*- coding: utf_8_sig-*-
import sys
import os

import subprocess
import threading

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog

from . import global_static_filepath as the_files
from . import global_variable

from .save_pickle import save as save_pickle

# from .ui__window import Window_with_scrollbar
from .ui__text_with_scrollbar import Text_with_scrollbar
from . import xml_parse_mame
from . import xml_parse_sl
from . import translation_gamelist


# new_var_
# new_func_
# new_ui_

# initial_window
class Toplevel_Window(tk.Toplevel):
    def __init__(self,
            #global_variable.user_configure_data,
            #root_window = None,
            #type_mame    = True, # xml 类型
            #type_mame_sl = False,
            #type_fbn     = False,
            *args,
            **kwargs
            ):
        super().__init__(*args,**kwargs)
        
        self.new_var_version = None # 命令行导出的 version
        
        self.new_var_after_remember = None
        
        self.new_var_tkvar_for_wait = tk.StringVar()
        
        self.new_var_mame_path=tk.StringVar()
        self.new_var_mame_path.set( global_variable.user_configure_data["mame_path"] )
        
        #self.new_var_type_mame = type_mame
        
        self.new_var_type = tk.StringVar()
        self.new_var_type.set("mame0162")
        ######################
        self.new_var_type.set("SoftwareList")
        
        self.new_func_ui()
        self.new_func_bindings()

    def new_func_ui(self,):
        self.title( _("初始化 / initialization") )
        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        
        parent=self
        
        n=0
        ttk.Label(parent,text=_("初始化，从模拟器读取游戏列表数据 / initialization,get info from emulator") ).grid(row=n,column=0,columnspan=3,sticky=tk.W+tk.N);n+=1
        
        # MAME 路径选择
        #
        self.new_ui_button_choose = ttk.Button(parent,text=_("选择 MAME 程序 / choose MAME executable program"),command=self.new_func_for_button_choose)
        self.new_ui_button_choose.grid(row=n,column=0,sticky=tk.W+tk.N,)
        n+=1
        # 路径显示在 Entry 中
        self.new_ui_entry = ttk.Entry(parent,width=40,textvariable=self.new_var_mame_path)
        self.new_ui_entry.grid(row=n,column=0,columnspan=3,sticky=tk.W+tk.E,)
        n+=1
        
        # 模拟器种类选择区
        frame=ttk.LabelFrame(parent,text=_("-getsoftlist"),)
        frame.grid(row=n,column=0,columnspan=3,sticky=tk.W+tk.N+tk.E)
        n+=1
        #
        r=0;c=0
        def make_a_radiobutton(row_number,column_number,the_value,the_text,columnspan_number=1,state="normal"):
            temp = ttk.Radiobutton(frame,
                variable = self.new_var_type,
                value    = the_value     ,
                text     = the_text,
                state    = state,
                        )
            temp.grid(  row       = row_number,
                        column    = column_number,
                        columnspan= columnspan_number,
                        sticky    = tk.W,
                                )
            return temp
        #
        #ttk.Label(frame,text= _("mame 0.162 之后：") ).grid(row=r,column=c,columnspan=2,sticky=tk.W+tk.N)
        #r+=1;c=0
        #
        self.new_var_radiobutton_s = []
        #
        # "mame0162" 不能改了,解析 xml 处用了
        #a_radiobutton = make_a_radiobutton(r,c,"mame0162",      _("主列表，mame版本 >= 0.162，用 -listxml 命令导出数据"));c+=1
        #self.new_var_radiobutton_s.append( a_radiobutton )
        #r+=1;c=0

        # "mame084" 不能改了,解析 xml 处用了
        #a_radiobutton =make_a_radiobutton(r,c,"mame084",_("0.162 > mame版本 >= 0.84，用 -listxml 命令导出数据，xml 中标签为 game"),3);c+=1
        #self.new_var_radiobutton_s.append( a_radiobutton )
        #r+=1;c=0
        
        #a_radiobutton = make_a_radiobutton(r,c,"mame00",_("mame版本 < 0.84，用 -listinfo 命令导出数据"),3,state="disabled");c+=1
        #self.new_var_radiobutton_s.append( a_radiobutton )
        #r+=1;c=0
        
        
        # mame -getsoftlist >roms_sl.xml
        a_radiobutton = make_a_radiobutton(r,c,"SoftwareList",_("MAME 版本>=0.162 / MAME version>=0.162"),3,);c+=1
        self.new_var_radiobutton_s.append( a_radiobutton )
        r+=1;c=0
        
        #
        #r+=1;c=0
        #make_a_radiobutton(r,c,"mame_very_old",_("mame 更早,主列表 -listinfo"),3);c+=1
        #
        #r+=1;c=0
        #make_a_radiobutton(r,c,"fbn",_("FBNeo 街机部分"),3);c+=1
        
        
        # 确定 按钮
        self.new_ui_button_ok = ttk.Button(parent,text=_("确定 / OK"),command = self.new_func_for_button_ok)
        self.new_ui_button_ok.grid(row=n,column=0,columnspan=3,sticky=tk.E)
        n+=1
        
        # 进度条
        self.new_ui_progressbar=ttk.Progressbar(parent,orient=tk.HORIZONTAL)
        self.new_ui_progressbar.grid(row=n,column=0,columnspan=3,sticky=tk.W+tk.E,)
        n+=1
        
        # 文本
        #   消息提示
        parent.rowconfigure(n,weight=1)
        self.new_ui_text_frame = Text_with_scrollbar(parent,wrap=tk.NONE,horizontal=True,sizegrip=True,)
        self.new_ui_text_frame.grid(row=n,column=0,columnspan=3,sticky=(tk.W+tk.N+tk.E+tk.S) )
        n+=1

    def new_func_bindings(self,):
        # alt 键，会打断 进度条
        # 所以重新 bind 一下
        self.bind('<KeyPress-Alt_L>',lambda event : "break")
        self.bind('<KeyPress-Alt_R>',lambda event : "break")
        
        
    
    # button call back function
    def new_func_for_button_choose(self,):
        if sys.platform.startswith('win'):
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,filetypes=[( _(".exe 文件"),"*.exe"),(_("所有文件"),"*")],)
        else:
            file_path = tkinter.filedialog.askopenfilename( initialdir="." ,)
        
        if not file_path:
            self.lift()
            return
        
        file_path = os.path.abspath( file_path ) # 统一格式，不然  / \ 混乱
        print(file_path)
        
        self.new_var_mame_path.set( file_path )
        self.lift()

    # button call back function
    def new_func_for_button_ok(self,):
        
        # 让一些 ui 部件 失效 ，在 任务中 不需要 操作，仅等待
        self.new_func_disable_some_ui()
        
        # 清理，删除一些文件
        
        
        xml_type =  self.new_var_type.get()
        
        # 导出 xml
        self.new_func_export_xml(xml_type)
        
        # 命令行 -help ，版本信息
        self.new_func_export_version_info()
        
        # 解析 xml 并 翻译
        self.new_func_parse_xml(xml_type)
        
        
        global_variable.user_configure_data["mame_path"] = self.new_var_mame_path.get()
        
        # 删除文件
        if xml_type=="SoftwareList":
            if os.path.isfile( the_files.file_xml_mame_softwarelist ):
                try:
                    os.remove( the_files.file_xml_mame_softwarelist )
                except:
                    pass
        elif xml_type=="mame":
            if os.path.isfile( the_files.file_xml_mame ):
                os.remove( the_files.file_xml_mame )
        
        self.destroy()

    # 导出版本信息
    #   -version
    #   或者
    #   -help
    def new_func_export_version_info(self,):
        
        mame_path      = self.new_var_mame_path.get()
        
        command = "-help"
        
        flag_use_shell = global_variable.user_configure_data["use_shell"]
        
        p=subprocess.Popen( args   = [mame_path,command,] ,
                                # command = "-listxml"
                            shell  = flag_use_shell, 
                            stdout=subprocess.PIPE , 
                            stderr=subprocess.STDOUT ,
                            stdin=subprocess.PIPE,
                            )
        
        binary_content = []
        
        for binary_line in p.stdout:
            binary_content.append( binary_line )
        
        if binary_content:
            
            version_info = binary_content[0].decode(encoding="utf_8", errors='replace')
            
            self.new_var_version = version_info.strip()
            
            print(version_info)


    def new_func_export_xml(self,xml_type="mame0162"):
        command=""
        if xml_type=="mame0162":
            command = "-listxml"
        elif xml_type== "mame084":
            command = "-listxml"
        elif xml_type=="SoftwareList":
            command = "-getsoftlist" 
                # 一部分，roms_sl.xml
                # 还有主列表一部分 roms.xml
        
        
        self.new_func_text_insert_string( _("导出 xml") )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( _("请耐心等待......") )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( "\n" )
        
        xml_file_name  = the_files.file_xml_mame
        if xml_type=="SoftwareList":
            xml_file_name  = the_files.file_xml_mame_softwarelist
        
        mame_path      = self.new_var_mame_path.get()
        flag_use_shell = global_variable.user_configure_data["use_shell"]
        
        try:
            if os.path.isfile(xml_file_name):
                os.remove(xml_file_name)
        except:
            pass
        
        
        self.new_func_text_insert_string( _("模拟器：") )
        self.new_func_text_insert_string( str(mame_path) )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( _("提取 roms 信息 到文件：") )
        self.new_func_text_insert_string( str(xml_file_name) )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( "\n" )
        
        file_object = open(xml_file_name, 'wb')
        
        #
        self.new_func_export_xml_mame(xml_type,file_object,mame_path,command,flag_use_shell)
        
        print("close file")
        file_object.close()
        
        self.new_func_text_insert_string( _("导出结束") )
        self.new_func_text_insert_string( "\n" )
    
    def new_func_export_xml_mame(self,xml_type,file_object,mame_path,command,flag_use_shell):
        
        self.new_var_tkvar_for_wait.set("wait_for_subprocess")
        
        if xml_type=="SoftwareList":
            if os.path.isfile( mame_path ):
                temp                   = os.path.dirname( mame_path )
                mame_working_directory = os.path.abspath( temp )
            else:
                mame_working_directory=None
                
            p=subprocess.Popen( args   = [mame_path,command,] ,
                                    # command = "-listxml"
                                shell  = flag_use_shell, 
                                stdout = file_object ,
                                stderr = subprocess.PIPE,
                                stdin  = subprocess.PIPE,
                                cwd    = mame_working_directory,
                                )
                
        else:
            
            p=subprocess.Popen( args   = [mame_path,command,] ,
                                    # command = "-listxml"
                                shell  = flag_use_shell, 
                                stdout = file_object ,
                                stderr = subprocess.PIPE,
                                stdin  = subprocess.PIPE,)
        
        
        self.new_func_progressbar_for_subprocess(p,)
        
        # wait
        if self.new_var_tkvar_for_wait.get() == "wait_for_subprocess":
            self.wait_variable(self.new_var_tkvar_for_wait)
    

    
            
    # parse xml and translation
    def new_func_parse_xml(self,xml_type):
        if xml_type=="mame0162":
            pass
        elif xml_type== "mame084":
            pass
        elif xml_type=="SoftwareList":
            pass
        
        
        translation_file_name = the_files.file_txt_translation_for_gamelist
        
        xml_file_name    = the_files.file_xml_mame
        if xml_type=="SoftwareList":
            xml_file_name  = the_files.file_xml_mame_softwarelist
        
        
        
        save_to_file_name = the_files.file_pickle_gamelist_data
        
        try:
            if os.path.isfile(save_to_file_name):
                os.remove(save_to_file_name)
        except:
            pass
        
        print(xml_file_name)
        print(save_to_file_name)
        print(translation_file_name)

        
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( _("解析 xml") )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( _("导入翻译文件") )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( _("请耐心等待......") )
        self.new_func_text_insert_string( "\n" )
        self.new_func_text_insert_string( "\n" )
        
        self.new_var_tkvar_for_wait.set("wait_for_threading")
        
        if xml_type=="SoftwareList":
            thread = threading.Thread(
                    target=self.new_func_parse_xml_mame, 
                    args=(xml_file_name,translation_file_name,save_to_file_name), 
                    kwargs={"xml_type":xml_type},
                    )        
        else:
            thread = threading.Thread(
                    target=self.new_func_parse_xml_mame, 
                    args=(xml_file_name,translation_file_name,save_to_file_name), 
                    kwargs={"xml_type":xml_type},
                    )
        
        thread.start()
        
        self.new_func_progressbar_for_threading(thread)
        
        # wait
        if self.new_var_tkvar_for_wait.get() == "wait_for_threading":
            self.wait_variable(self.new_var_tkvar_for_wait)
        
        self.new_func_text_insert_string( _("完成") )
        self.new_func_text_insert_string( "\n" )

    def new_func_parse_xml_mame(self,xml_file_name,translation_file_name,save_to_file_name,xml_type="mame0162"):
        if xml_type=="mame0162":
            pass
        elif xml_type== "mame084":
            pass
        elif xml_type=="SoftwareList":
            pass
            
        # 解析 xml
        # from . import xml_parse_mame
        data = {}
        if xml_type=="mame0162":
            try:
                data = xml_parse_mame.main(xml_file_name,xml_type)
            except:
                pass
        
        elif xml_type=="SoftwareList":
            print("sl")
            print(xml_file_name)
            print(xml_type)
            #try:
            #    data = xml_parse_sl.main(xml_file_name)
            #except:
            #    pass
            
            data = xml_parse_sl.main(xml_file_name)
        
        #print(len( data ) )
        print()
        print( data.keys() )
        
        if len( data ) == 0:
            return None
        
        if "machine_dict" not in data :
            return None
            
        if len( data["machine_dict"] ) == 0 : 
            return None
        
        # sl ，补充版本信息
        if xml_type=="SoftwareList":
            if not data["mame_version"]:
                if self.new_var_version is not None:
                    data["mame_version"] = self.new_var_version
        
        
        # 翻译
        # from . import translation_gamelist
        translation_dict={}
        if os.path.isfile(translation_file_name):
            try:
                translation_dict = translation_gamelist.read_translation_file( translation_file_name )
            except:
                translation_dict={}
        
        if len( translation_dict ) > 0 :
            translation_gamelist.add_translation( translation_dict , data["machine_dict"] ,data["columns"])
        
        # 保存
        # from .save_pickle import save as save_pickle
        save_pickle(data,save_to_file_name)
        
        del data
        del translation_dict

    def new_func_progressbar_for_subprocess(self,p):# p subprocess.Popen
        #self.new_var_after_remember
        #self.new_var_tkvar_for_wait
        #self.new_ui_progressbar
        if p.poll() != None: #停止
            print("subprocess finish")
            
            #self.new_var_tkvar_for_wait.set("subprocess finish")
            
            # widget.wait_variable 留点时间,延迟，不然，等待之前就设好了怎么搞
            self.after(3,self.new_var_tkvar_for_wait.set ,("subprocess finish",))
        else: # 没停止
            self.new_ui_progressbar.step(2.0)
            self.new_var_after_remember = self.after(300,self.new_func_progressbar_for_subprocess,p,)
    
    def new_func_progressbar_for_threading(self,thread):# threading.Thread
        #self.new_var_after_remember
        #self.new_var_tkvar_for_wait
        #self.new_ui_progressbar
        if thread.is_alive(): #运行
            self.new_ui_progressbar.step(2.0)
            self.new_var_after_remember = self.after(300,self.new_func_progressbar_for_threading,thread)
        else: # 停止
            print("threading finish")
            
            #self.new_var_tkvar_for_wait.set("threading finish")
            
            # widget.wait_variable 留点时间, 延迟，不然，等待之前就设好了怎么搞
            self.after(3,self.new_var_tkvar_for_wait.set ,("threading finish",))

    def new_func_text_insert_string(self,a_string=''):
        self.new_ui_text_frame.new_func_insert_string(a_string)

    def new_func_disable_some_ui(self,):
        self.new_ui_entry.configure(state="disable")
        self.new_ui_button_choose.configure(state="disable")
        self.new_ui_button_ok.configure(state="disable")
        for radiobutton in self.new_var_radiobutton_s:
            radiobutton.configure(state="disable")    
    

    
    # def exit_for_window():

    #window.protocol("WM_DELETE_WINDOW", exit_for_window)



def main(root_window):
    
    top=Toplevel_Window(root_window)
    


if __name__ == "__main__":
    root = tk.Tk()
    
    
    top=Toplevel_Window()
    root.mainloop()