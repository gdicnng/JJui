# -*- coding: utf_8_sig-*-
import re



def read_ini( ini_file_name ):
    
    temp_dict = {}
    
    text_file = open( ini_file_name , 'rt',encoding='utf_8_sig')
    lines = text_file.readlines()
    text_file.close()
    
    #temp_srt = r'^\s*(\S+)\s+(\S+)\s*$'
    temp_srt = r'^\s*(\S+)\s+(\S.*?)\s*$'
        # 选项 值
    p=re.compile(temp_srt)
    
    #temp_srt_2 = r'^(")(.+)(")$'
    #先不管这个
        # 选项 值，
        # 值 为路径的话，里面有空格
        # sanp "xxx\ yyy"
        # "xxx\ yyy"
        # 去掉 引号
    #p2=re.compile(temp_srt_2)
    
    count = 0
    for line in lines:
        str_1 = ''
        str_2 = ''
        m=p.search(line)
        if m:
            str_1 = m.group(1)
            str_2 = m.group(2)
            #m2 = p2.search(m.group(2))
            #if m2:
            #    str_2 = m2.group(2)
        temp_dict[str_1] = str_2
    return temp_dict

    
def write_ini(ini_file_name,ini_dict,order = None):
    
    # order 顺序
    # keys 组成的 list 或 tuple
    # 新版本的 dict 会保持 原有的 顺序
    # 但老版本的 dict 不会保持 原有的 顺序

    text_file = open(ini_file_name, 'wt',encoding='utf_8_sig')
    
    
    if order == None:
        for x in ini_dict:
            print( x.ljust(29) , end='',file = text_file )
            print( " "         , end='',file = text_file )# 增加一个空格，万一长度超了也不影响
            print( ini_dict[x] ,        file = text_file )

    else:
        for x in order:
            if x in ini_dict:
                print( x.ljust(29) , end='',file = text_file )
                print( " "         , end='',file = text_file )# 增加一个空格，万一长度超了也不影响
                print( ini_dict[x] ,        file = text_file )
        for x in ini_dict:
            if x not in order:
                    print( x.ljust(29) , end='',file = text_file )
                    print( " "         , end='',file = text_file )# 增加一个空格，万一长度超了也不影响
                    print( ini_dict[x] ,        file = text_file )
                
                
    
    text_file.close()
    

if __name__ == '__main__' :

    ini_file = r'..\yyui.ini'

    ini_default = {
        "mame_path":r".\mame.exe",      

        "size":"",            

        "font":"",
        "fontsize":"" ,

        "colour":"" ,
        "colour_bg":"" ,

        "folders_path":r".\folders",

        "snap_path":r".\snap",       
        "titles_path":r".\titles",       
        "flyers_path" :r".\flyers",      

        "history_dat_path":r".\history.dat",  
        "command_dat_path":r".\command.dat",  
    }
    
    print()
    print("type(ini_default)")
    print(type(ini_default))
    print()
    #for x in ini_default:
    #    print(x,end='')
    #    print('\t',end='')
    #    print(ini_default[x])
        
    temp = read_ini(ini_file)
    for x in ini_default:
        if x in temp:
            ini_default[x] = temp[x]
    
    for x in ini_default:
        print(x + '\t' + ini_default[x])
            
    write_ini("2.ini",ini_default)