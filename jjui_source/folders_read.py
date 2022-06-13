# -*- coding: utf_8_sig-*-
import sys
import os
import re

# 用的是 read_folder_ini_3()

# 以 uft8 格式 读取 一个文本
# 反回 lines [line,line,……]
# 读取 错语 返回 None
def read_a_text( file_name ):

    encoding_list = ['utf_8_sig',] 
    # 'utf_8','utf_8_sig' 
    # '\ufeff'
    # 用 'utf_8' 读文本，如果 遇到 bom ，会保留。
    # 用 'utf_8_sig' 读文本，如果 遇到 bom ，会跳过。
    # python 各版本 行为 是否 一致 ？
    
    lines = []
    
    mark = False
    
    for x in encoding_list:
    
        lines = []
            # try 模块 对 lines 赋值
            # 如果 try 模块 ，不成功，对 lines 有影响吗 ？
            # 干脆 清空一下 吧
    
        file = open( file_name ,mode = 'rt',encoding = x )
        
        try:
            lines = file.readlines()
            mark = True
        except:
            pass
            
        file.close()
        
        if mark == True: break
        
    if mark == True:
        return lines
    else:
        return None

def read_folder_ini( file_name ):

    temp_dict = {}
    mark = ''
    
    content = read_a_text( file_name )
    
    search_str = r'^\[(.*)\]\s*$'
        # 查找分类标题 [...]
    p=re.compile( search_str, )
    #p=re.compile(search_str, re.IGNORECASE)
    
    search_str_2 = r'^\s*([^\s]+)\s*.*$'
        # 内容
    p2=re.compile( search_str_2, )
    
    search_str_3 = r'^\s*([^\s].*?)\s*$'
        # FOLDER_SETTINGS
        # SubFolderIcon folder 
        # 因为有这种，连空格也读取了
    p3=re.compile( search_str_3, )
    
    search_str_empty =r'^\s*$'
    #空行
    p_empty = re.compile( search_str_empty , )

    if content == None:
        return None # 之前 读取 文本 的错误
    else:
        for line in content:
        
            # 空行测试
            m=p_empty.search( line ) 
            if m : 
                continue
            
            #  标题 行 测试
            m=p.search( line ) 
            if m:
                # 是标题
                #print (m.group())  # The entire match
                #print (m.group(1)) # The first parenthesized subgroup.
                mark = m.group(1)
                if mark not in temp_dict: # 第一次，出始化
                    temp_dict[mark] = set()
                continue
            
            
            if mark == "FOLDER_SETTINGS" :
                m = p3.search( line )
                if m : 
                    temp_dict[mark].add( m.group(1) )
            else :
                # 内容行
                m=p2.search( line )
                if m:
                    if mark == '' : 
                        return None 
                        # 格式出错，内容出现在标题前
                    else:
                        #print(m.group(1))
                        temp_dict[mark].add( m.group(1) )

    if "FOLDER_SETTINGS" not in temp_dict:
        # 格式错误
        return None 
    if "ROOT_FOLDER" not in temp_dict:
        # 主分类 ROOT_FOLDER
        # 如果不在
        # 格式错误
        return None 
    return temp_dict

# 把 read_folder_ini 函数 结果，格式转化一下
def read_folder_ini_2( file_name ):

    # set 格式 比较浪费空间
    # 把格式转为 list

    content = read_folder_ini( file_name )
    
    if content == None:
        return None
    
    temp = {}
    for x in content:
        temp[x] = list( content[x] )
    
    return temp

# ###################
# ###################
# ###################
# 重写：read_folder_ini 与 read_folder_ini_2 内容
def read_folder_ini_3( file_name ):

    temp_dict = {}
    mark = None
    mark_list = []
    
    content = read_a_text( file_name )
    
    #    mameui ，分类名， [] ,后面可以有空格
    #    mameui ，分类名， 可以为空 .* 不用 .+
    #search_str = r'^\[(.*)\]\s*$'
    search_str = r'^\s*\[(.*)\]\s*$'
        # 查找分类标题 [...]
    p=re.compile( search_str, )
    #p=re.compile(search_str, re.IGNORECASE)
    
    #   mameui,游戏名，前后，可以有空格
    # software list 中间正好有 空格
    search_str_2 = r'^\s*(\S.*?)\s*$'
    #search_str_2 = r'^(.+)$' 
        # 内容
    p2=re.compile( search_str_2, )
    
    #search_str_3 = r'^\s*([^\s].*?)\s*$'
    #search_str_3 = r'^(.+)$'
        # FOLDER_SETTINGS
        # SubFolderIcon folder 
        # 因为有这种，连空格也读取了
    #p3=re.compile( search_str_3, )
    
    search_str_empty =r'^\s*$'
    #空行
    p_empty = re.compile( search_str_empty , )

    if content == None:
        return None # 之前 读取 文本 的错误
    else:
        for line in content:
        
            # 空行测试
            m=p_empty.search( line ) 
            if m : 
                continue
            
            #  标题 行 测试
            m=p.search( line ) 
            if m:
                # 是标题
                #print (m.group())  # The entire match
                #print (m.group(1)) # The first parenthesized subgroup.
                mark = m.group(1)
                mark_list.append(mark)
                if mark not in temp_dict: # 第一次，出始化
                    temp_dict[mark] = []
                continue
            
            # 内容行
            m=p2.search( line )
            if m:
                if mark == None : 
                    return None 
                    # 格式出错，内容出现在标题前
                else:
                    #print(m.group(1))
                    temp_dict[mark].append( m.group(1).lower() )
                    # .lower()
                    # 转为小写
    
    # 格式错误
    #
    # 没有 "FOLDER_SETTINGS" ，mameui 也行
    # mameui 大写
    #
    # 没有 "ROOT_FOLDER" ，mameui 也行
    # mameui 大写
    #
    # 没有任何分类，直接列表，kof97、kov……，mameui报错
    #
    # 空文件，mameui 也行，也可以添加新游戏在其中
    #

    
    
    
    # 如果没有
    # 添加一个空的
    if "FOLDER_SETTINGS" not in temp_dict:
        temp_dict["FOLDER_SETTINGS"] =  []
    
    # 如果没有
    # 添加一个空的    
    if "ROOT_FOLDER" not in temp_dict:
        temp_dict["ROOT_FOLDER"] =  []
    
    # 格式转换一下，去重
    # new_dict ={}
    # for x in temp_dict:
    #     new_dict[x] = list( set( temp_dict[x] ) )
    # 
    # temp_dict = new_dict
    #
    # 似乎用不着了
    # 之后，在 ui 里，载入列表时，转化为 set ，自动去重了
    
    return temp_dict

if __name__ == "__main__" :


    file = r'..\folders\gdicnng.ini'
    file = r'..\folders\test.ini'
    a = read_folder_ini( file )
    for x in sorted( a.keys() ):
        for y in sorted(a[x]):
            print(x,end='')
            print('\t',end='')
            print(y)
    
    #for x in sorted( a.keys() ):
    #    print(x)

