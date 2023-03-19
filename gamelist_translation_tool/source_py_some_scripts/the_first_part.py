# -*- coding: utf_8_sig-*- 
import re

###
from . import multi_space_to_single

"""
    如果是 英文 字符串
        
        去掉 前、后 空格 .strip()
        
        多重空格，换单个空格
        
        大小写，不在这里处理
            因为，如果之前 需保留大写的、或需全小写的，在之前处理
        
        ？
        对于 符号 怎样 处理 ？
            . , ？ 这样的，可以统一 添加 前、后 的空格；或者 统一删除 前、后 的空格
            - 这种不好搞，连字符 a-b 这种的，不方便 随便 添加 空格；有空格的 也 不方便 随便删空格
        以后再说
        . 句号，最后，应不应该 删掉
        
"""

# 英文
def main( a_string ):
    
    string_english = a_string.strip() 
    # 去掉 前、后 空格 .strip()
    
    string_english = multi_space_to_single.main( string_english )
    # 多重空格，换单个
    
    return string_english 


def main_cn( a_string ):
    
    string_cn = a_string.replace(r"　",r" ") 
    # 中文空格，换英文空格
    
    string_cn = string_cn.strip() 
    # 去掉 前、后 空格 .strip()
    
    string_cn = multi_space_to_single.main( string_cn )
    # 多重空格，换单个
    
    return string_cn 


if __name__ =="__main__":
    
    s = " D         D D       DJJ JJab bc vvvvvvvvvvvvvvv     "
    
    en = main(s)
    
    print(s  + "::")
    print(en + "::")
    