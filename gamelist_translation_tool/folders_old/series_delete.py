import sys
import os
# 切换工作目录
def change_working_directory():

    if getattr(sys, "frozen", False):
        # cx_Freeze 
        # pyinstall 
        
        # The application is frozen
        executable_path = os.path.dirname(sys.executable)
        executable_path = os.path.abspath(executable_path)
        os.chdir( executable_path )
    else:
        # 以 python 脚本模式 运行
        
        # The application is not frozen
        # Change this bit to match where you store your data files:
        the_script_path = os.path.dirname(__file__)
        the_script_path = os.path.abspath(the_script_path)
        os.chdir( the_script_path )

change_working_directory()


file_in = "series.ini"
file_out = "series_delete.ini"

lines=[]
with open(file_in,mode="rt",encoding="utf_8_sig") as f:
    lines=f.readlines()

with open(file_out,mode="wt",encoding="utf_8") as f:

    keep_this_header=True

    for line in lines:
        line_content = line.strip()
        if line_content.startswith(r"["):

            header=line_content.strip()
            header=header.strip(r"[]")
            header=header.strip()
            #print(header)

            if header.lower().endswith( "* Slot".lower() ):
                keep_this_header=False
                print(header)
            elif header.lower().endswith( "* Pinball".lower() ):
                keep_this_header=False
                print(header)
            else:
                keep_this_header=True
        
        if keep_this_header:
            f.write(line)