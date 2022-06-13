# -*- coding: utf_8_sig-*-
import sys
import os
import re

# 复制 extra_history_dat.py ，改一下
# $bio 改为 $mame 

def extra_history_find(file_name , game_name):# 逐行读取，节约内存

    #$info=xxx,xxx,xxx
    #^\$info=(\S.*?)\s*$
    
    # $mame
    # $end
    
    text_file = open( file_name, 'rt',encoding='utf_8_sig')
    
    str_1 = r'^\$info=(\S.*?)\s*$'
    p1=re.compile(str_1,)
    
    str_comment= r'^#'
    p_comment=re.compile(str_comment,)
    
    found_flag = False
    
    new_text = []
    
    for line in text_file:
        
        # 注释
        m_comment = p_comment.search(line)
        if m_comment:
            continue
        
        if found_flag:
            m=p1.search(line)
            if m:# 已经找到另一个游戏了
                break
            new_text.append(line)
        else:
            m=p1.search(line)
            if m:
                if game_name in m.group(1).split(","):
                    print( m.group(1).split(",") )
                    found_flag = True
    
    text_file.close()
    
    if found_flag:
        return new_text
    else:
        return None

def history_format(content):

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
    content=extra_history_find(file_name,game_name)
    content=history_format(content)
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


