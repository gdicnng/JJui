# -*- coding: utf_8_sig-*-
# import sys
# import os
# import re

all_dict={} 
# 第三方的目录有点占用体积
# 都是重复的字符串，game_id
# 从已有数据过一遍，看看能不能省一点空间
# 确实省了一点空间
    # 使用时，赋值 all_dict ={ game_id:game_id for game_id in global_variable.set_data["all_set"] }
    # 使用完，清理一下，节省空间

# 以 uft8 格式 读取 一个文本
# 反回 lines [line,line,……]
# 读取 错语 返回 None
def read_a_text( file_name ):

    # 'utf_8','utf_8_sig' 
    # '\ufeff'
    # 用 'utf_8' 读文本，如果 遇到 bom ，会保留。
    # 用 'utf_8_sig' 读文本，如果 遇到 bom ，会跳过。
    # python 各版本 行为 是否 一致 ？

    lines = None

    try:
        file = open( file_name , mode = 'rt', encoding = 'utf_8_sig', )
        lines = file.readlines()
        file.close()
    except:
        lines = None
    
    return lines

def read_folder_ini(file_name):
    
    global all_dict
    
    temp_dict = {}
    mark = None # 分类 标题
    mark_list = []
    
    content = read_a_text( file_name )


    if content == None:
        return None # 之前 读取 文本 的错误
    
        
    #index_counter = 0
    for line in content:
        
        line=line.strip()
        
        # 空行
        if not line:
            continue
        
        # 标题 行
        # [ 开头, ]结尾
        if line.startswith(r"[") and line.endswith(r"]"):

                mark = line[1:-1]

                # FOLDER_SETTINGS
                if mark.strip().lower() == "folder_settings":
                    mark="FOLDER_SETTINGS"
                
                # ROOT_FOLDER
                if mark.strip().lower() == "root_folder":
                    mark="ROOT_FOLDER"
                
                mark_list.append(mark)
                if mark not in temp_dict: # 第一次，出始化
                    temp_dict[mark] = []
                continue
        
        # 内容行
        if mark==None:
            return None
            # 格式出错，内容出现在标题前
        else:
            game_id =line.lower() # 转为小写
            
            if game_id in all_dict: 
                temp_dict[mark].append( all_dict[game_id] )
            else:
                temp_dict[mark].append( game_id )
    
    # 格式错误
    #
    # 没有 "FOLDER_SETTINGS" ，mameui 也行
    # mameui 大写
    #
    # 没有 "ROOT_FOLDER" ，mameui 也行
    # mameui 大写
    #
    # 空文件，mameui 也行，也可以添加新游戏在其中
    #
    # 没有任何分类，直接列表，kof97、kov……，mameui报错
    #   
    
    # 如果没有
    # 添加一个空的
    if "FOLDER_SETTINGS" not in temp_dict:
        temp_dict["FOLDER_SETTINGS"] =  []
    
    # 如果没有
    # 添加一个空的    
    if "ROOT_FOLDER" not in temp_dict:
        temp_dict["ROOT_FOLDER"] =  []
        
    return temp_dict

if __name__ == "__main__" :
    pass
