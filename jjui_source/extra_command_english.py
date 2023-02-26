# -*- coding: utf_8_sig-*-
#import sys
#import os
import re


from . import extra_command


# 中文 command ,每一个片段被 $cmd $end 包起来

# 英文 command ,全部内容被 $cmd $end 包起来，分隔符号用的 ──────────── 


# 去掉 $cmd $end
def command_format_1(content):

    # 去掉 $cmd $end
    
    if content is None:
        return None
        
    str_sart = r'^\$cmd'
    str_end  = r'^\$end'
    
    p_start  = re.compile(str_sart)
    p_end    = re.compile(str_end)
    
    new_content=[]
    
    flag = False
    
    for line in content:
        if flag:
            m_end = p_end.search(line) # 配匹 结束 标记
            
            if m_end:
                flag = False # 标记 取消
            else:
                new_content.append(line)
        else:
            m_start = p_start.search(line) # 配匹 开始 标记
            if m_start:
                flag = True # 标记

    if len(new_content) == 0:
        return None
    else:
        return new_content    

# 分段 
def command_format_2(content):
    
    if content is None:
        return None

    #- CONTROLS -
    #───────
    
    # ******************
    # r"^\- .+ \-$" ，备注，原来用 $ ，这种对行尾 \n 、\r\n 效果不一样
    #   从文件读的，默认转为 \n
    #   从二进制读的，解码后为 \r\n ，
    #   把 $ 换为了 \r\n
    
    str_heading = r"^\- .+ \-[\r\n]" # 小标题
    str_separator = r"─{8,}" # 分隔线 # 暂时设定，超过 8个 重复字符吧
        # 小标题 下一行，就是分隔线行
   
    p_heading   = re.compile(str_heading)
    p_separator = re.compile(str_separator)
       
    remember_1 = set() # 标题数量 记录
    remember_2 = set() # 分隔线数量，记录
    # 标题数量 + 1，如果也在 分隔线里，那么就符合了
    
    #
    count = 0
    for line in content:
    
        m1 = p_heading.search(line)

        if m1 : 
            remember_1.add( count )

        count += 1
    del count
    
    #
    count = 0
    for line in content:
    
        m2 = p_separator.search(line)

        if m2 : 
            remember_2.add( count )

        count += 1
    del count
    
    #print()
    #print("a:")
    #print(remember_1)
    #print()
    #print("b:")
    #print(remember_2)
    #print()
    
    #
    remember =  set()
    
    for x in remember_1:
        y = x+1 # 小标题行，下一行就是分隔线行
        if y in remember_2:
            remember.add(x)
    
    #
    new_content = {}
    count_dict = 1 # for new_content ,从 1 开始 ,做为 key
    count_line = 0 # 行计数
    
    for line in content :
    
        if count_line in remember:
            if count_line > 0: 
                # 如果第0行，开始，就是小标题 ，不增加计数
                count_dict += 1
    
        if count_dict in new_content:
            new_content[count_dict].append(line)
        else: # 初始化为 list
            new_content[count_dict] = []
            new_content[count_dict].append(line)

        count_line += 1
        # 行计数
    
    if len(new_content) == 0:
        return None
    else:
        return new_content

# 文本，不读到 内存
def get_content_by_file_name(file_name,game_name):
    
    content = extra_command.extra_command_find_2( file_name,game_name )
        # 调用 中文版 command 函数
        # 找到内容
    content = extra_command.command_replace(content)
        # 调用 中文版 command 函数
        # 替换 标记
    content = command_format_1(content)
        # 去掉 $cmd $end
    content = command_format_2(content)
        # 分段
    return content


#########################
#使用目录

def get_content_by_file_name_use_index(file_name,game_name,the_index=0):
    
    content = extra_command.extra_command_find_2_use_index( file_name,game_name,the_index )
        # 调用 中文版 command 函数
        # 找到内容
    content = extra_command.command_replace(content)
        # 调用 中文版 command 函数
        # 替换 标记
    content = command_format_1(content)
        # 去掉 $cmd $end
    content = command_format_2(content)
    
    return content


if __name__ =="__main__":
    print()
    print("test")
    print()
    
    text_file_name = r'command_english.dat'

    game_name=r'kof97'
    
    content = get_content_by_file_name(text_file_name,game_name)
    
    #for x in content:
    #    for y in content[x]:
    #        print(y,end='')
    
    count = 3
    
    for y in content[count]:
        print(y,end='')
