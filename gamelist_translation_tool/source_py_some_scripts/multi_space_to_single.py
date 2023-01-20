# -*- coding: utf_8_sig-*- 
import re

"""
    
    去掉多重空格，换单个
    
    英文空格
    
    中文空格
        删掉 前、后 的 中、英文 空格
        英文空格去重
        中文空格去重
        如果同时出现 中文空格 、英文空格 ，替换为 中文空格
"""

string_for_search_empty = r" +"
p = re.compile(string_for_search_empty)

def main(a_string):
    s = a_string.strip()
    s = re.subn(p," ",s) [0]
    return s
    
if __name__ =="__main__":
    
    s="   abc bbc eec  kkkd   gggp   l              o   "
    #s="bbc"
    #s=""
    
    
    temp = main( s )
    

    print()
    print(s    + "::")
    print(temp + "::")
