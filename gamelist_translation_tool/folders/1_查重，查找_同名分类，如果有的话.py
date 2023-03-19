import os
import sys

file_out = "out_查重_结果.txt"
f_out = open(file_out,mode="wt",encoding="utf_8_sig")

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

# 搜索 .ini 文件
search_folder = "."
# 单层搜索
dirpath, dirnames, filenames = next(  os.walk(search_folder)  )
file_list =[]
for file_name in filenames:
    if file_name.lower().endswith(".ini"):
        file_list.append(  file_name  )


for file_name in file_list:
    file_path = os.path.join(search_folder,file_name)
    with open(file_path,mode="rt",encoding="utf_8_sig") as f:
        header_dict={}
        for line in f:
            line = line.strip()
            if line.startswith(r"["):
                if line.endswith(r"]"):
                    header = line[1:-1]
                    header = header.strip()
                    if header not in header_dict:
                        header_dict[header] = 1
                    else:
                        header_dict[header] += 1

        if header_dict:
            print()
            print("",file=f_out)
            print(file_path)
            print(file_path,file=f_out)
            for header,count in header_dict.items():
                if count > 1:
                    print(count,"\t",header)
                    print(count,"\t",header,file=f_out)


f_out.close()