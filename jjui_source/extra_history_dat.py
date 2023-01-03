# -*- coding: utf_8_sig-*-
import sys
import os
import re




def extra_history_find_mame(file_name , game_name):# 逐行读取，节约内存

    #$info=xxx,xxx,xxx
    #^\$info\=(\S.*?)\s*$
    
    # $bio
    # $end
    
    with open( file_name, 'rt',encoding='utf_8_sig',errors='replace') as text_file:
        
        str_1 = r'^\$info\=(\S.*?)\s*$'
        p1=re.compile(str_1,)
        
        str_comment= r'^#'
        p_comment=re.compile(str_comment,)
        
        str_end = r'^\$end'
        p_end=re.compile(str_end,)
        
        found_flag = False
        
        new_text = []
        
        for line in text_file:
            
            # 注释
            m_comment = p_comment.search(line)
            if m_comment:
                continue
            
            if found_flag:
                m=p_end.search(line)# 找到结束点
                if m:
                    break
                else:
                    new_text.append(line)
            else:
                m=p1.search(line)
                if m:
                    if game_name in m.group(1).split(","):
                        print( m.group(1).split(",") )
                        found_flag = True
        
        
        if found_flag:
            return new_text
        else:
            return None

def extra_history_find_sl(file_name , sl_id):# 逐行读取，节约内存
    
    xml_name,game_name = sl_id.split(sep=" ",maxsplit=1)
    print("xx yy")
    print(xml_name,game_name)
    
    # $info=kof97,kof97k, 
    #   街机
    # $neogeo=kof97,kof97k,
        # neogeo
    # $vgmplay=kof97,
        # vgmplay
    
    #$XXXX=xxx,xxx,xxx
    #^\$info\=(\S.*?)\s*$
    
    # $bio
    # $end
    
    with open( file_name, 'rt',encoding='utf_8_sig',errors='replace') as text_file:
        
        # 街机
        # str_1 = r'^\$info\=(\S.*?)\s*$' 
        
        # sl
        # #$XXXX=xxx,xxx,xxx
        str_1 = r'^\$' + xml_name
        str_1 = str_1 + r'\=(\S.*?)\s*$'
        p1=re.compile(str_1,)
        
        str_comment= r'^#'
        p_comment=re.compile(str_comment,)
        
        str_end = r'^\$end'
        p_end=re.compile(str_end,)
        
        found_flag = False
        
        new_text = []
        
        for line in text_file:
            
            # 注释
            m_comment = p_comment.search(line)
            if m_comment:
                continue
            
            if found_flag:
                m=p_end.search(line)# 找到结束点
                if m:
                    break
                else:
                    new_text.append(line)
            else:
                m=p1.search(line)
                if m:
                    if game_name in m.group(1).split(","):
                        print( line.strip() )
                        print( m.group(1).split(",") )
                        found_flag = True
        
        
        if found_flag:
            return new_text
        else:
            return None

def history_format(content):

    if content is None:
        return None
        
    new_coutent=[]
    
    # $bio
    # $end
    # 去掉，这开头，结尾的标记
    
    str_sart = r'^\$bio'
    str_end  = r'^\$end'
    
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

def get_content_by_file_name(file_name,game_name,the_type="mame"):
    content = None
    if the_type=="mame":
        content=extra_history_find_mame(file_name,game_name)
        content=history_format(content)
        return content
    elif the_type=="softwarelist":
        content=extra_history_find_sl(file_name,game_name)
        content=history_format(content)
        return content


###########################
# 建目录

# 仅街机部分
def get_index_mame(file_name,):
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

# sl
def get_index_sl(file_name,):
    index_dict = {}
    
    start_position = 0
    
    #$XXXX=xxx,xxx,xxx
    # 非 info
    #^\$(.+)\=(\S.*?)\s*$
    
    str_1 = r'^\$(.+)\=(\S.*?)\s*$'
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
                xml_name = m.group(1) 
                if xml_name != "info" :
                    for game_name in m.group(2).split(","):
                        #the_id = game_name.strip()
                        if game_name:
                            the_id = xml_name + " " + game_name
                            index_dict[ the_id ] = start_position
            
            start_position = f.tell()
            
            bin_line = f.readline()
    
    return index_dict

########
def get_index(file_name,the_type="mame"):
    if the_type=="mame":
        return get_index_mame(file_name)
    elif the_type=="softwarelist":
        return get_index_sl(file_name)

##################################
##################################
##################################
# 根据目录搜索
def extra_history_find_by_index_mame(file_name , game_name,the_index):# 逐行读取，节约内存
    print("docs use index")
    print(file_name)
    print(game_name)
    print(the_index)
    
    #$info=xxx,xxx,xxx
    #^\$info\=(\S.*?)\s*$
    
    # $bio
    # $end
    
    # with open( file_name, 'rt',encoding='utf_8_sig',errors='replace') as text_file:
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
        
        str_end = r'^\$end'
        p_end=re.compile(str_end,)
        
        found_flag = False
        
        new_text = []
        

        bin_line=f.readline()
        first_line = bin_line.decode(encoding='utf-8', errors='replace')
        print("first line:{}".format(first_line.strip()))
        
        while bin_line:
            
            if count > 1 : 
                print(r"count > 1,break")
                break # ###
            
            line = bin_line.decode(encoding='utf-8', errors='replace')
            
            # 注释
            m_comment = p_comment.search(line)
            if m_comment:
                bin_line=f.readline() #############
                continue
            
            m=p1.search(line)
            if m:
                count += 1
                
                if game_name in m.group(1).split(","):
                    print( m.group(1).split(",") )
                    found_flag = True
                else:
                    break
            
            else:
                if found_flag:
                    new_text.append(line)
            
            bin_line=f.readline() ############
        
        if found_flag:
            return new_text
        else:
            return None

def extra_history_find_by_index_sl(file_name , sl_id,the_index):# 逐行读取，节约内存
    print("docs use index")
    print(file_name)
    print(sl_id)
    print(the_index)
    
    xml_name,game_name = sl_id.split(sep=" ",maxsplit=1)
    
    # $XXXX=xxx,xxx,xxx
    # r'^\$(.+)\=(\S.*?)\s*$'
    
    # $bio
    # $end
    
    # with open( file_name, 'rt',encoding='utf_8_sig',errors='replace') as text_file:
    with open( file_name, 'rb',) as f:
        
        try:
            f.seek(the_index)
        except:
            print("seek error")
            return 
        
        #str_1 = r'^\$info\=(\S.*?)\s*$'
        str_1 = r'^\$(.+)\=(\S.*?)\s*$'
        p1=re.compile(str_1,)
        
        str_comment= r'^#'
        p_comment=re.compile(str_comment,)
        
        str_end = r'^\$end'
        p_end=re.compile(str_end,)
        
        found_flag = False
        
        new_text = []
        

        bin_line=f.readline()
        first_line = bin_line.decode(encoding='utf-8', errors='replace')
        print("first line:{}".format(first_line))
        
        
        count = 0
        
        while bin_line:
            
            if count >= 1 : 
                print(r"count >= 1,break")
                break 
            
            line = bin_line.decode(encoding='utf-8', errors='replace')
            
            
            # 找到注释行
            m_comment = p_comment.search(line)
            if m_comment:
                
                bin_line=f.readline() #############
                continue
            
            # 找到结束点
            m_end = p_end.search(line)
            if m_end:
                count += 1
                
                if found_flag:
                    new_text.append(line)
                
                bin_line=f.readline()
                continue
            
            # 找到起点,目录处
            # $XXXX=xxx,xxx,xxx
            m=p1.search(line)
            if m:
                if xml_name == m.group(1):
                    if game_name in m.group(2).split(","):
                        found_flag = True
                
                bin_line=f.readline()
                continue
            
            if found_flag:
                new_text.append(line)
            
            bin_line=f.readline() ############
        
        if found_flag:
            return new_text
        else:
            return None

def get_content_by_file_name_by_index(file_name,game_name,the_index=0,the_type="mame"):
    if the_type=="mame":
        content=extra_history_find_by_index_mame(file_name,game_name,the_index)
        content=history_format(content) # 没变
        return content
    elif the_type=="softwarelist":
        content=extra_history_find_by_index_sl(file_name,game_name,the_index)
        content=history_format(content) # 没变
        return content

if __name__ =="__main__":
    print()
    print("test")
    print()
    
    text_file_name = r'history.dat'
    
    index_dict = get_index(text_file_name)
    
    with open("out.txt",mode="wt",encoding="utf_8_sig",errors='replace') as f:
        for x in index_dict:
            print(x,end="",file=f)
            print("\t",end="",file=f)
            print(index_dict[x],end="",file=f)
            print("",file=f)
    


