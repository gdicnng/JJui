# -*- coding: utf_8_sig-*- 
import os
import io
import sys
import string
import re

from . import split_string_to_two_part
from . import the_first_part
from . import the_second_part
from . import multi_space_to_single


def for_print_error_python34():
    import sys
    import io
    # python 3.4.4
    #   命令行模式时，print 函数 兼容，超过 字符集时
    if sys.version_info < (3, 6):
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors= 'backslashreplace',line_buffering=True)
            #print(sys.version_info)
        except:
            pass

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

########################################
#
# 如果标题，由 数字、符号 等组成，似乎没有必要翻译，可能只需要翻译 括号后面部分
#   数字、符号、不超过一个英文字符 ，可以直接翻译 括号后面
#        string.punctuation # ascii 标点
#       \s #空
#       \d #数字
#       勉强吧
#       主要是可能有 超 ascii 字符，不然，简单点
string_find_character="".join(         # [^......] # 非
    [
    r"[",
    r"^",
    re.escape(string.punctuation),  # 非符号
    r"\s",                          # 非空
    r"\d",                          # 非数
    r"]",
    ]
)
p_find_character = re.compile( string_find_character )
string_find_character_ascii=r"[a-zA-Z]"
p_find_character_ascii = re.compile( string_find_character_ascii )
def find_character_at_least_twice(s):
    #print()
    #print(s)
    if is_ascii(s):
        #print("is ascii")
        m=p_find_character_ascii.findall(s)
        if m:
            if len(m) > 1:
                return True
    else:
        #print("is not ascii")
        m=p_find_character.findall(s)
        if m:
            if len(m) > 1:
                return True
    return False
#
##################

# 读取文本
# id \t 英文
def read_id_english_file(file_name):

    id_english_dict ={}
    # id 
        # 英文

    search_str = r'^([^\t]+)\t([^\t]+)'
    p=re.compile( search_str, )
    
    with open(file_name,mode="rt",encoding="utf_8_sig",errors='backslashreplace') as f:
        for line in f:
            
            line=line.strip()
            
            m=p.search( line ) 
            if m:
                the_id  = m.group(1).strip()
                english = m.group(2).strip()
                
                if the_id and english:
                    id_english_dict[ the_id ] = english
    
    return id_english_dict

# 读取文本
# 英文 \t 中文
def read_english_chinese_file(file_name):
    
    temp_dict ={}
    # 英文：中文

    search_str = r'^([^\t]+)\t([^\t]+)'
    p=re.compile( search_str, )
    
    with open(file_name,mode="rt",encoding="utf_8_sig",errors='backslashreplace') as f:
        for line in f:
            #print(line)
            line=line.strip()
            
            m=p.search( line ) 
            if m:
                english = m.group(1).strip()
                chinese = m.group(2).strip()
                
                if english == chinese:
                    continue
                if is_ascii(chinese): # ?? 要不要这样呢
                    continue
                
                english_part_1,english_part_2 = split_string_to_two_part.main( english )
                
                # 处理
                english = the_first_part.main( english_part_1 )
                
                english = english.lower()
                
                chinese_part_1,chinese_part_2 = split_string_to_two_part.main_cn( chinese )
                
                chinese_part_1 = the_first_part.main_cn(chinese_part_1)
                
                if english and chinese_part_1:# 非空
                    temp_dict[ english ] = chinese_part_1
    
    return temp_dict

# 读取文本
# 英文 \t 中文
#   分类目录的翻译
#       不用分成两部分
def read_english_chinese_file_for_folders_translation(file_name):
    
    temp_dict ={}
    # 英文：中文

    search_str = r'^([^\t]+)\t([^\t]+)'
    p=re.compile( search_str, )
    
    with open(file_name,mode="rt",encoding="utf_8_sig",errors='backslashreplace') as f:
        for line in f:
            #print(line)
            line=line.strip()
            
            m=p.search( line ) 
            if m:
                english = m.group(1).strip()
                chinese = m.group(2).strip()
                
                if english == chinese:
                    continue
                if is_ascii(chinese): # ?? 要不要这样呢
                    continue
                
                # 处理
                english = the_first_part.main( english )
                
                english = english.lower()
                
                chinese = the_first_part.main_cn(chinese)
                
                if english and chinese:# 非空
                    temp_dict[ english ] = chinese
    
    return temp_dict

# id_translated_dict
def translate(id_english_dict,english_chinese_dict,english_chinese_dict_second_part=None):
    
    if english_chinese_dict_second_part is None:
        english_chinese_dict_second_part = dict()
    
    #separators = set( the_variables.string_separators_for_second_part )
    
    id_translated_dict = {}

    for game_id,english in id_english_dict.items():
        
        english_part_1,english_part_2 = split_string_to_two_part.main(english)
        
        # 之间的空格
        # 翻译后，加回去
        space_between = ""
        if english_part_1.endswith(" "):
            space_between=" "
        
        # 括号前的部分
        the_string_need_to_be_translate = the_first_part.main( english_part_1 )
        
        the_string_need_to_be_translate = the_string_need_to_be_translate.lower()
        
        def translate_part_2(english_part_2):
            second_part_translated_flag = False
            if english_chinese_dict_second_part and english_part_2:
                
                english_part_2 = english_part_2.strip()
                
                if english_part_2:
                    the_split_english_list = the_second_part.split( english_part_2 , keep_separator = True )
                    
                    for n in range( len(the_split_english_list) ):
                        
                        temp_string = the_split_english_list[n]
                        
                        # 记录 左 右 的空格，翻译后，把空格加回去,基本保持原有格式
                        empty_left  = ""
                        empty_right = ""
                        if temp_string.startswith(" ") : empty_left  =" "
                        if temp_string.endswith(" ")   : empty_right =" "
                        
                        temp_string = temp_string.strip()#
                        
                        if not temp_string : # 空字符
                            continue
                        
                        # 算了吧
                        #if not misc.find_character_at_least_twice(temp_string):# 英文字符 没有 或 就一个，
                        #    continue
                        
                        temp_string = multi_space_to_single.main( temp_string )
                        
                        if len(temp_string) == 1 :# 单字符，不译
                            continue
                        
                        temp_string = temp_string.lower() # 全转小写
                        
                        if temp_string in english_chinese_dict_second_part:
                            second_part_translated_flag = True
                            the_split_english_list[n] = "".join(
                                        [
                                        empty_left,
                                        english_chinese_dict_second_part[temp_string],
                                        empty_right,
                                        ]
                                            )
                    
                    if second_part_translated_flag:
                        english_part_2="".join( the_split_english_list )
            
            return english_part_2
        
        # 第一部分有翻译，翻译第二部分
        if the_string_need_to_be_translate in english_chinese_dict:
            
            english_part_2 = translate_part_2(english_part_2)
            
            id_translated_dict[game_id] = english_chinese_dict[the_string_need_to_be_translate] + space_between + english_part_2
        
        ## 第一部分 英文字母太少，不到两个，无需翻译；仅 翻译第二部分
        #elif not misc.find_character_at_least_twice(the_string_need_to_be_translate):
        #    
        #    english_part_2 = translate_part_2(english_part_2)
        #    
        #    id_translated_dict[game_id] = the_string_need_to_be_translate + space_between + english_part_2
        else:
            pass
    
    return id_translated_dict


# id_translated_dict
# 比如 1943 ，这种，可以只翻译 第2部分
# 翻译完成以后，可以追加这个功能
def translate_only_part_2(id_english_dict,english_chinese_dict,english_chinese_dict_second_part=None):
    # 仅翻译 第2部分
    
    if english_chinese_dict_second_part is None:
        english_chinese_dict_second_part = dict()
    
    #separators = set( the_variables.string_separators_for_second_part )
    
    id_translated_dict = {}

    for game_id,english in id_english_dict.items():
        
        # 仅翻译 第2部分，括号前面不管
        english_part_1,english_part_2 = split_string_to_two_part.main(english)
        
        # 之间的空格
        # 翻译后，加回去
        # space_between = ""
        # if english_part_1.endswith(" "):
        #     space_between=" "
        
        # 括号前的部分
        the_string_need_to_be_translate = the_first_part.main( english_part_1 )
        
        #the_string_need_to_be_translate = the_string_need_to_be_translate.lower()
        
        def translate_part_2(english_part_2):
            second_part_translated_flag = False
            if english_chinese_dict_second_part and english_part_2:
                
                english_part_2 = english_part_2.strip()
                
                if english_part_2:
                    the_split_english_list = the_second_part.split( english_part_2 , keep_separator = True )
                    
                    for n in range( len(the_split_english_list) ):
                        
                        temp_string = the_split_english_list[n]
                        
                        # 记录 左 右 的空格，翻译后，把空格加回去,基本保持原有格式
                        empty_left  = ""
                        empty_right = ""
                        if temp_string.startswith(" ") : empty_left  =" "
                        if temp_string.endswith(" ")   : empty_right =" "
                        
                        temp_string = temp_string.strip()#
                        
                        if not temp_string : # 空字符
                            continue
                        
                        # 算了吧
                        #if not misc.find_character_at_least_twice(temp_string):# 英文字符 没有 或 就一个，
                        #    continue
                        
                        temp_string = multi_space_to_single.main( temp_string )
                        
                        if len(temp_string) == 1 :# 单字符，不译
                            continue
                        
                        temp_string = temp_string.lower() # 全转小写
                        
                        if temp_string in english_chinese_dict_second_part:
                            second_part_translated_flag = True
                            the_split_english_list[n] = "".join(
                                        [
                                        empty_left,
                                        english_chinese_dict_second_part[temp_string],
                                        empty_right,
                                        ]
                                            )
                    
                    if second_part_translated_flag:
                        english_part_2="".join( the_split_english_list )
            
            return english_part_2
        

        
        # 第一部分 英文字母太少，不到两个，无需翻译；仅 翻译第二部分
        if not find_character_at_least_twice(the_string_need_to_be_translate):
            
            english_part_2 = english_part_2.strip()
            
            if english_part_2:# 非空
            
                english_part_2_translated = translate_part_2(english_part_2)
                
                if english_part_2 != english_part_2_translated :# 如相等，代表没有翻译
                
                    id_translated_dict[game_id] = english_part_1 + english_part_2_translated
        else:
            pass
    
    return id_translated_dict

# 结果写出
def write_to_text__id_chinese(
            out_text_file_name,
            id_translated_dict,
            double_chinese=False,
            id_english_dict=None,
            english=False
            ):
    
    if id_english_dict is None:
        id_english_dict=dict()
    
    with open(out_text_file_name,mode="wt",encoding="utf_8_sig") as f:
        for game_id in sorted( id_translated_dict.keys() ):
            translated_string = id_translated_dict[game_id]
            f.write(game_id)
            f.write("\t")
            f.write(translated_string)
            if double_chinese:
                f.write("\t")
                f.write(translated_string)
            if english:
                f.write("\t")
                f.write(id_english_dict.get(game_id,""))
            f.write("\n")





if __name__ == "__main__":
    for x in [
            "abc",
            "abc \t efgh",
            "abc 中文",
            ]:
        print(x,", is_ascii :",is_ascii(x))


