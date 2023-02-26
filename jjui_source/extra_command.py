# -*- coding: utf_8_sig-*-
#import sys
#import os
import re


def extra_command_find(content , game_name):# content 为， 所有文本，readlines 读取的
    #$info=xxx,xxx,xxx
    #^\$info=(\S.*?)\s*$
    
    
    str_1 = r'^\$info=(\S.*?)\s*$'
    p1=re.compile(str_1,)
    
    str_comment= r'^#'
    p_comment=re.compile(str_comment,)
    
    found_flag = False
    
    new_text = []
    
    for line in content:
        
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
                if game_name in m.group(1).split(r","):
                    print(m.group(1).split(r","))
                    found_flag = True
    
    if found_flag:
        return new_text
    else:
        return None

def extra_command_find_2(file_name , game_name):# 逐行读取，节约内存

    #$info=xxx,xxx,xxx
    #^\$info=(\S.*?)\s*$
    
    with open( file_name, 'rt',encoding='utf_8_sig',errors='replace') as text_file:
    
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
                    if game_name in m.group(1).split(r","):
                        print(m.group(1).split(r","))
                        found_flag = True
        
        
        
        if found_flag:
            return new_text
        else:
            return None

def command_replace(content):
    replace_dict={
            r"@A-button" : r"Ａ",
            r"@B-button" : r"Ｂ",
            r"@C-button" : r"Ｃ",
            r"@D-button" : r"Ｄ",
            r"@E-button" : r"Ｅ",
            r"@F-button" : r"Ｆ",
            r"@G-button" : r"Ｇ",
            r"@H-button" : r"Ｈ",
            r"@I-button" : r"Ｉ",
            r"@J-button" : r"Ｊ",
            r"@K-button" : r"Ｋ",
            r"@L-button" : r"Ｌ",
            r"@M-button" : r"Ｍ",
            r"@N-button" : r"Ｎ",
            r"@O-button" : r"Ｏ",
            r"@P-button" : r"Ｐ",
            r"@Q-button" : r"Ｑ",
            r"@R-button" : r"Ｒ",
            r"@S-button" : r"Ｓ",
            r"@T-button" : r"Ｔ",
            r"@U-button" : r"Ｕ",
            r"@V-button" : r"Ｖ",
            r"@W-button" : r"Ｗ",
            r"@X-button" : r"Ｘ",
            r"@Y-button" : r"Ｙ",
            r"@Z-button" : r"Ｚ", 
            # ^s
            
            r"_A"        : r"Ａ",
            r"_B"        : r"Ｂ",
            r"_C"        : r"Ｃ",
            r"_D"        : r"Ｄ",
            
            r"_Z"        : r"Ｚ",

            r"_+"  : r"＋",#gb2312
            r"_."  : r"…",
            r"_1"  : r"↙",
            r"_2"  : r"↓",
            r"_3"  : r"↘",
            r"_4"  : r"←",
            r"_5"  : r"⊕", # gbk  ???
            r"_6"  : r"→",
            r"_7"  : r"↖",
            r"_8"  : r"↑",
            r"_9"  : r"↗",
            r"_N"  : r"Ｎ", # # # # 
            
            r"@BALL"  : r"⊕",# gbk  ???
            
            r"_a" : r"①",# ① gb2312
            r"_b" : r"②",
            r"_c" : r"③",
            r"_d" : r"④",
            r"_e" : r"⑤",
            r"_f" : r"⑥",
            r"_g" : r"⑦",
            r"_h" : r"⑧",
            r"_i" : r"⑨",
            r"_j" : r"⑩",
            
            r"@decrease" : r"＋",
            r"@increase" : r"－",
            
            r"_S":r"开始键",
            r"^S":r"选择键",
            r"_P":r"拳",
            r"_K":r"脚",
            r"_G":r"防",
            r"^E":r"轻拳",
            r"^F":r"中拳",
            r"^G":r"重拳",
            r"^H":r"轻脚",
            r"^I":r"中脚",
            r"^J":r"重脚",
            r"^T":r"三脚同时输入",
            r"^U":r"三拳同时输入",
            r"^V":r"两脚同时输入",
            r"^W":r"两拳同时输入",
            
            r"@start"   : r"开始键",
            r"@select"  : r"选择键",
            r"@punch"   : r"拳",
            r"@kick"    : r"脚",
            r"@guard"   : r"防",
            r"@L-punch" : r"轻拳",
            r"@M-punch" : r"中拳",
            r"@S-punch" : r"重拳",
            r"@L-kick"  : r"轻脚",
            r"@M-kick"  : r"中脚",
            r"@S-kick"  : r"重脚",
            r"@3-kick"  : r"三脚同时输入",
            r"@3-punch" : r"三拳同时输入",
            r"@2-kick"  : r"两脚同时输入",
            r"@2-punch" : r"两拳同时输入",
            
            r"@custom1" : r"自定义①",# ① gb2312
            r"@custom2" : r"自定义②",
            r"@custom3" : r"自定义③",
            r"@custom4" : r"自定义④",
            r"@custom5" : r"自定义⑤",
            r"@custom6" : r"自定义⑥",
            r"@custom7" : r"自定义⑦",
            r"@custom8" : r"自定义⑧",
            r"@up"      : r"↑",
            r"@down"    : r"↓",
            r"@left"    : r"←",
            r"@right"   : r"→",
            r"@lever"   : r"Φ",# gb2312 ?????
            r"@nplayer" : r"Pn",
            r"@1player" : r"P1",
            r"@2player" : r"P2",
            r"@3player" : r"P3",
            r"@4player" : r"P4",
            r"@5player" : r"P5",
            r"@6player" : r"P6",
            r"@7player" : r"P7",
            r"@8player" : r"P8",
            
            r"_`" : r"・",#gb2312
            r"_@" : r"◎",#gb2312
            r"_)" : r"○",#gb2312
            r"_(" : r"●",#gb2312
            r"_*" : r"☆",#gb2312
            r"_&" : r"★",#gb2312
            r"_%" : r"△",#gb2312
            r"_$" : r"▲",#gb2312
            r"_#" : r"",       #gbk 里有 ，没有 ▣ ,▣ 25a3 ,
            r"_]" : r"□",#gb2312
            r"_[" : r"■",#gb2312
            r"_{" : r"▽",       #gbk
            r"_}" : r"▼",       #gbk
            r"_<" : r"◇",#gb2312
            r"_>" : r"◆",#gb2312
            
            r"_|" : r"跳",
            r"_O" : r"按住",
            r"_-" : r"空中",
            r"_=" : r"下蹲",
            r"^-" : r"靠近",
            r"^=" : r"离开",
            r"_~" : r"按住",
            r"^*" : r"连按",
            r"^?" : r"任意键",
            
            r"@jump"  : r"跳",
            r"@hold"  : r"按住", # #
            r"@air"   : r"空中",
            r"@sit"   : r"下蹲",
            r"@close" : r"靠近",
            r"@away"  : r"离开",
            r"@charge": r"按住", # #
            r"@tap"   : r"连按",
            r"@button": r"任意键",
            
            r"_k" : r"→↘↓↙←",
            r"_l" : r"←↖↑↗→",
            r"_m" : r"←↙↓↘→",
            r"_n" : r"→↗↑↖←",
            r"_o" : r"→↘↓",
            r"_p" : r"↓↙←",
            r"_q" : r"←↖↑",
            r"_r" : r"↑↗→",
            r"_s" : r"←↙↓",
            r"_t" : r"↓↘→",
            r"_u" : r"→↗↑",
            r"_v" : r"↑↖←",
            r"_w" : r"从下面顺时针转一圈",
            r"_x" : r"从上面顺时针转一圈",
            r"_y" : r"从上面逆时针旋转一圈",
            r"_z" : r"从下面逆时针旋转一圈",
            r"_L" : r"→→",
            r"_M" : r"←←",
            r"_Q" : r"→↓↘",
            r"_R" : r"←↓↙",
            
            # → ← ↑ ↓↖ ↗ ↘ ↙ 
            r"@hcb" : r"→↘↓↙←",
            r"@huf" : r"←↖↑↗→",
            r"@hcf" : r"←↙↓↘→",
            r"@hub" : r"→↗↑↖←",
            r"@qfd" : r"→↘↓",
            r"@qdb" : r"↓↙←",
            r"@qbu" : r"←↖↑",
            r"@quf" : r"↑↗→",
            r"@qbd" : r"←↙↓",
            r"@qdf" : r"↓↘→",
            r"@qfu" : r"→↗↑",
            r"@qub" : r"↑↖←",
            r"@fdf" : r"从下面顺时针转一圈",
            r"@fub" : r"从上面顺时针转一圈",
            r"@fuf" : r"从上面逆时针旋转一圈",
            r"@fdb" : r"从下面逆时针旋转一圈",
            r"@xff" : r"→→",
            r"@xbb" : r"←←",
            r"@dsf" : r"→↓↘",
            r"@dsb" : r"←↓↙",

            r"_!" : r"→",
            r"^!" : r"└→",
            r"^1" : r"↙.",
            r"^2" : r"↓.",
            r"^3" : r"↘.",
            r"^4" : r"←.",
            r"^6" : r"→.",
            r"^7" : r"↖.",
            r"^8" : r"↑.",
            r"^9" : r"↗.",
            
            r"@-->" : r"→",
            r"@==>" : r"└→",
            }
    
    #for x in replace_dict:
    #    print(x)
    #    print(replace_dict[x])
    
    new_content = []
    
    if content is None:
        return None
    else:
        for line in content:
            #print(line)
            for x in replace_dict: 
                line = line.replace(x,replace_dict[x])
            #print(line)
            new_content.append(line)
        return new_content

def command_format(content):

    if content is None:
        return None
    
    count = 0
    
    new_coutent={}
    # 以数量为 key
    # 从 1 开始
    # 把 0 留作 全部 用，
    # ttk.Combobox  .current()
    
    # 目录 全部 : 全部。
    
    # 目录 1 ： 内容 ，从这里开始
    # 目录 2 ： 内容
    # 目录 3 ： 内容
    # 目录 4 ： 内容
    # 目录 ……
    # {1:"lines",2:"lines",……}
    
    #$cmd
    #$end
    
    str_sart = r'^\s*\$cmd'
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
                if count in new_coutent:
                    new_coutent[count].append(line)
                else:
                    new_coutent[count]=[]  # 初始化
                    new_coutent[count].append(line)
            
        else:
            m_start = p_start.search(line) # 配匹 开始 标记
            if m_start:
                flag = True # 标记
                count += 1
                
    
    
    if len(new_coutent) == 0:
        return None
    else:
        return new_coutent

# 文本 已 readlines 读取 到内存
def get_content(file_content,game_name):
    content=extra_command_find(file_content,game_name)
    content=command_replace(content)
    content=command_format(content)
    return content

# 文本，不读到 内存
###################################################
##### 用的这个#####################################
###################################################
def get_content_by_file_name(file_name,game_name):
    content=extra_command_find_2(file_name,game_name)
    content=command_replace(content)
    content=command_format(content)
    return content
    
####################
####################
####################

# 和 history.dat 一样
def get_index(file_name,):
    index_dict = {}
    
    start_position = 0
    
    str_1 = r'^\$info\=(\S.*?)\s*$'
    p1=re.compile(str_1,)    
    
    
    
    with open( file_name, 'rb',) as f:
        #$info=xxx,xxx,xxx
        #^\$info\=(\S.*?)\s*$
        
        # encoding='utf_8_sig',errors='replace'
        
        start_position = f.tell()
        
        bin_line = f.readline()
        
        while bin_line :
            
            line = bin_line.decode(encoding='utf-8', errors='replace')
            line = line.strip()
            
            m=p1.search(line)
           
            if m:
                for game_name in m.group(1).split(","):
                    the_id = game_name.strip()
                    if the_id:
                        index_dict[ the_id ] = start_position
            
            
            
            
            
            
            start_position = f.tell()
            
            bin_line = f.readline()
            
            
        
    return index_dict

######################
######################
######################

# 和 history.dat 有一点不一样
    # 结束标记不一样
    # 这个，每一段 都有 结束结标记
    # history.dat 改了一下，不和结束标记了，好像一样了
def extra_command_find_2_use_index(file_name , game_name,the_index):# 逐行读取，节约内存
    #$info=xxx,xxx,xxx
    #^\$info=(\S.*?)\s*$
    
    
    with open( file_name, 'rb',) as f:
        
        try:
            f.seek(the_index)
        except:
            print("seek error")
            return 
        
        count = 0
        
        
        str_1 = r'^\$info\=(\S.*?)\s*$'
        p1=re.compile(str_1,)
        
        str_comment= r'^#'
        p_comment=re.compile(str_comment,)
        
        
        found_flag = False
        
        new_text = []
        
        
        bin_line=f.readline()
        print("first line")
        print(bin_line.decode(encoding='utf-8', errors='replace'))
        
        while bin_line:
            
            if count > 1 : 
                break # ###
            
            line = bin_line.decode(encoding='utf-8', errors='replace')
            
            # 注释
            m_comment = p_comment.search(line)
            if m_comment:
                bin_line=f.readline() #######################
                continue
            
            m=p1.search(line)
            if m:
                count += 1
                
                if game_name in m.group(1).split(","):
                    #print( m.group(1).split(",") )
                    found_flag = True
                else:
                    break
            else:
                if found_flag:
                    new_text.append(line)
            
            bin_line=f.readline() #######################
        
        if found_flag:
            return new_text
        else:
            return None


def get_content_by_file_name_use_index(file_name,game_name,the_index=0):
    content=extra_command_find_2_use_index(file_name,game_name,the_index)
    content=command_replace(content)
    content=command_format(content)
    return content
    #print(content)

if __name__ =="__main__":
    print()
    print("test")
    print()
    
    text_file_name = r'command.dat'
    lines = None
    new_content = None
    try:
        text_file = open( text_file_name, 'rt',encoding='utf_8_sig',errors='replace')
        lines = text_file.readlines()
        text_file.close()
    except:
        pass
    
    game_name=r'kof97'
    
    content = get_content(lines,game_name)
    
    #for x in content:
    #    for y in content[x]:
    #        print(y,end='')
    
    count = 1
    for y in content[count]:
        print(y,end='')
