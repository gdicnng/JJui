# -*- coding: utf_8_sig-*- 
import re

# windows 非法 文件名 字符 
reserved_characters_replace_dict={
    r"<"   :  r"＜",
    r">"   :  r"＞",
    r":"   :  r"∶",
    r'"'   :  r"＂",
    r"/"   :  r"／",
    "\\"   :  r"＼",
    r"|"   :  r"｜",
    r"?"   :  r"？",
    r"*"   :  r"＊",
            }

#for x,y in reserved_characters_replace_dict.items():
#    print()
#    print(x,"\t:",y)
#    try:
#        encoding="gb2312"
#        y.encode(encoding=encoding, errors='strict')
#        print( y,encoding)
#    except:
#        pass

reserved_characters = "".join( [x for x in reserved_characters_replace_dict] )
#print(reserved_characters)

reserved_characters_re = re.escape(reserved_characters)
reserved_characters_re = r"[" + reserved_characters_re + r"]" # 单选
#print(reserved_characters_re)

p_reserved_characters  = re.compile(reserved_characters_re)

def replace_func(m):
    temp = m.group(0)
    
    if temp in reserved_characters_replace_dict:
        return reserved_characters_replace_dict[temp]
    else:
        return temp

def replace_reserved_characters(a_string):
    a_string = a_string.strip()
    
    a_string = p_reserved_characters.subn(replace_func,a_string,)[0]
    
    return a_string

if __name__ == "__main__" :
    s='''abc bbc eed?"|\/////\\\\||||****<<..>>::::""""'''
    
    a=replace_reserved_characters(s)
    print(s)
    print(a)