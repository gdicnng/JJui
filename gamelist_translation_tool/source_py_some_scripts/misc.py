# -*- coding: utf_8_sig-*- 
import os
import sys

import re

from . import split_string_to_two_part
from . import the_second_part
from . import multi_space_to_single


def search_txt_files_in_a_folder( the_folder ):
    """
        搜索一个文件夹中的 .txt 文件
        返回文件列表
        顺序排列
    """
    txt_file_list = []
    
    if os.path.isdir( the_folder ):
        
        the_folder = os.path.abspath( the_folder )
        
        for (dirpath, dirnames, filenames) in sorted( os.walk( the_folder ) ):
            for file_name  in sorted(filenames):
                if file_name.lower().endswith(".txt"):
                    txt_file_list.append( os.path.join(dirpath,file_name) )
    
    return txt_file_list


string_ascii_re = r"[\x00-\x7f]*"
p_ascii = re.compile(string_ascii_re)
def is_ascii( a_string ):
    """ 
        # python 3.7 以上有 str.isascii()
        # 低版本 没有
    """
    m = p_ascii.fullmatch(a_string)
    
    if m:
        return True
    else:
        return False


# dict { id : english }
# english 两部分：括号前 与 括号后
# 第二部分，再分割，得到 小片段
# 统计 各小片段 出现的次数
def get_second_part_english_counter(id_english_dict):
    
    # 用于保存，被切割后的 英文 小片段
    temp_string_counter = dict() 
    # key 为 英文小段片
    # value 为 计数
    
    for english_string in id_english_dict.values():
        
        english_first_part , english_second_part = split_string_to_two_part.main(english_string)
        
        # 切割 english_second_part
        
        the_split_english_list = the_second_part.split( english_second_part , keep_separator = False )
        
        for x in the_split_english_list:
            temp_english = x.strip() # 去掉 前、后 空格 .strip()
            temp_english = multi_space_to_single.main( temp_english )# 多重空格，换单个
            #temp_english = temp_english.lower() # 用原始的吧，计数文本，可以小写输出
            if temp_english:
                if len(temp_english)>1:# 单字符，不译
                    if temp_english in temp_string_counter:
                        temp_string_counter[temp_english] += 1
                    else:
                        # 第一次出现， 计数 1
                        temp_string_counter[temp_english] = 1
                    
    return temp_string_counter
# 转，小写
def get_second_part_english_counter_lower_case(id_english_dict):
    
    second_part_english_counter = get_second_part_english_counter(id_english_dict)
    
    new_dict = dict()
    
    for english,count in second_part_english_counter.items():
        
        english_lower = english.lower()
        
        if english_lower in new_dict:
            new_dict[english_lower] += count
        else:
            new_dict[english_lower] = count
    
    return new_dict

#
def write__second_part_english_count(file_name,dict_for_second_part_english_counter):
    temp_dict = {} # 这个全用小写
    
    for temp_string,count in dict_for_second_part_english_counter.items():
    
        temp_string_lower = temp_string.lower()
        
        if temp_string_lower in temp_dict:
            temp_dict[ temp_string_lower ] += count
        else:
            # 初始 计数 
            temp_dict[ temp_string_lower ] = count
    
    with open(file_name,mode="wt",encoding="utf_8_sig") as f:
        temp_list = list( temp_dict.items() )
        temp_list.sort( key = lambda x : x[1] ,reverse=True)
        
        for temp_string,count in temp_list :
            f.write(temp_string)
            f.write("\t")
            f.write(str(count))
            f.write("\n")



if __name__ == "__main__":
    for x in [
            "abc",
            "abc \t efgh",
            "abc 中文",
            ]:
        print(x,", is_ascii :",is_ascii(x))


