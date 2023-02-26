# -*- coding: utf_8_sig-*-
#import sys
#import os
import re

from . import extra_history_dat


# def extra_history_find(file_name , game_name):# 逐行读取，节约内存

# 和 history.dat 一样

extra_mameinfo_find = extra_history_dat.extra_history_find_mame


def mameinfo_format(content):

    if content is None:
        return None
        
    new_coutent=[]
    
    # $mame 或 $drv
    # $end
    # 去掉，这开头，结尾的标记
    
    str_sart = r'^\s*\$(mame)|(drv)'
    str_end  = r'^\s*\$end'
    
    p_start  = re.compile(str_sart)
    p_end    = re.compile(str_end)
    
    flag = False
    
    for line in content:
        if flag:
            m_end = p_end.search(line) # 配匹 结束 标记
            
            if m_end:
                #flag = False # 标记 取消
                break
            else:
                new_coutent.append(line)
        else:
            m_start = p_start.search(line) # 配匹 开始 标记
            if m_start:
                flag = True # 标记

    if len(new_coutent) == 0:
        return None
    else:
        return new_coutent

def get_content_by_file_name(file_name,game_name):
    content=extra_mameinfo_find(file_name,game_name)
    content=mameinfo_format(content)
    return content

##################
##################
##################

# 创建目录

# 街机部分
# 驱动部分
# 和 history.dat 一样

get_index = extra_history_dat.get_index_mame
    # def get_index(file_name,):

#################
#################
#################
# 使用目录
#


# def extra_history_find_by_index(file_name , game_name,the_index):# 逐行读取，节约内存

extra_mameinfo_find_by_index = extra_history_dat.extra_history_find_by_index_mame


def get_content_by_file_name_by_index(file_name,game_name,the_index=0):
    content=extra_mameinfo_find_by_index(file_name,game_name,the_index)
    content=mameinfo_format(content)
    return content


if __name__ =="__main__":
    print()
    print("test")
    print()
    
    text_file_name = r'mameinfo.dat'
    #game_name = r"kof97"
    
    
    index_dict = get_index(text_file_name)
    
    with open("out.txt",mode="wt") as f:
        for x in index_dict:
            print(x+"\t"+str(index_dict[x]) ,file = f)


