# -*- coding: utf_8_sig-*- 
import sys
import os
import re
import string

from source_py_some_scripts import the_files
from source_py_some_scripts import split_string_to_two_part
from source_py_some_scripts import multi_space_to_single


file_id_to_english = the_files.file__id_to_english
out_file           = the_files.file__word_frequency_in_part_2


# id \t 英文
def read_id_english_file(file_name):

    gamelist_dict ={}
    # id 
        # 英文

    search_str = r'^([^\t]+)\t([^\t]+)'
    p=re.compile( search_str, )
    
    with open(file_name,mode="rt",encoding="utf_8_sig") as f:
        for line in f:
            #print(line)
            line=line.strip()
            
            m=p.search( line ) 
            if m:
                the_id  = m.group(1)
                english = m.group(2)
                
                gamelist_dict[ the_id ] = english
    
    return gamelist_dict


# string.ascii_letters
# string.digits # 0-9
# string.punctuation 
    #   由在 C 区域设置中被视为标点符号的 ASCII 字符所组成的字符串: 
    #   !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~.
# string.whitespace 

string_separator_s    = string.digits + string.punctuation + string.whitespace

string_separator_s_re = re.escape( string_separator_s )             # 转为 正则 字符 表达

string_for_keep_separator     = r"[" + string_separator_s_re + r"]"    # 匹配其中一个
string_for_keep_separator     = r"(" + string_for_keep_separator + r")"
    # 圆括号，有括号的内容，re.split() 分割时，内容保留
string_for_not_keep_separator = r"[" + string_separator_s_re + r"]"    # 匹配其中一个
    # 不保留，不要 圆括号

p_keep_separator     = re.compile( string_for_keep_separator )
p_not_keep_separator = re.compile( string_for_not_keep_separator )

def split(a_string,keep_separator=True):
    
    # True 保留分隔符，翻译后，方便 把 翻译好的内容 ，再 拼接起来
    
    # False 不保留，用于，创建 需要 翻译 的 词条
    
    s = a_string.strip()
    
    s = multi_space_to_single.main( s )
    
    if keep_separator:
        list_of_string_s = p_keep_separator.split(s)
    else:
        list_of_string_s = p_not_keep_separator.split(s)
    
    return list_of_string_s




def count_english_word_in_part_2(id_english_dict):
    
    # 用于保存，被切割后的 英文 小片段
    temp_string_counter = dict() 
    # key 为 英文小段片
    # value 为 计数
    
    for english_string in id_english_dict.values():
        
        english_first_part , english_second_part = split_string_to_two_part.main(english_string)
        
        # 切割 english_second_part
        
        the_split_english_list = split( english_second_part , keep_separator = False )
        
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


#
id_english_file = read_id_english_file( file_id_to_english )
counter_dict = count_english_word_in_part_2(id_english_file)
with open(out_file,mode="wt",encoding="utf-8") as f:
    for english_word ,count in sorted(
            counter_dict.items(),
            key=lambda x : x[1],
            reverse = True,
    ):
        f.write(english_word)
        f.write("\t")
        f.write(str(count))
        f.write("\n")