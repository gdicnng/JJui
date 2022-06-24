# -*- coding: utf_8_sig-*-
import sys
import os
import re

from . import extra_history_dat

# ("gameinit.dat",)

# $mame 
#   复制 extra_history_dat.py ，改一下
#   $bio 改为 $mame 
def gameinit_format(content):

    if content is None:
        return None
        
    new_coutent=[]
    
    # $mame
    # $end
    # 去掉，这开头，结尾的标记
    
    str_sart = r'^\s*\$mame'
    str_end  = r'^\s*\$end'
    
    p_start  = re.compile(str_sart)
    p_end    = re.compile(str_end)
    
    flag = False
    
    for line in content:
        if flag:
            m_end = p_end.search(line) # 配匹 结束 标记
            
            if m_end:
                flag = False # 标记 取消
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
    #content=extra_history_find(file_name,game_name)
    content=extra_history_dat.extra_history_find(file_name,game_name)
    content=gameinit_format(content)
    return content


def get_content_by_file_name_use_index(file_name,game_name,the_index=0):
    content=extra_history_dat.extra_history_find_by_index(file_name,game_name,the_index)
    content=gameinit_format(content)
    return content

if __name__ =="__main__":
    print()
    print("test")
    print()
    
    text_file_name = r'gameinit.dat'
    game_name = r"kof97"
    
    content = get_content_by_file_name(text_file_name,game_name)
    
    for x in content:
        print(x,end="")


