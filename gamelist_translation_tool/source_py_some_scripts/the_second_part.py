# -*- coding: utf_8_sig-*- 
import re

###
from . import multi_space_to_single
from . import the_variables

"""
    将，以括号 起始处 分割字符串 之后，得到的 第二段 字符
    分隔成 更小元素，
        比如 English / French / German / Spanish 
            这样的分开来，
            单个单词，
            最方便 批量翻译 了
        
        可惜，有的内容，里面信息比较混乱，
        有 把主版本的 英文名 写进去的，
        有 pirate 这个单词，不分隔，写进去的，
        其它的，还得仔细看看
    
    分隔符号 1
    括号
        英文括号
        () [] {}
            # <> 尖括号这个不管吧
        
        以 括号 开始的
        可能有 多个括号、多种括号
            比如 (abc)[bbc]{ccc}
        可能有 一些 在括号之间，但 没有 包含在 括号之内的 字符
            比如 bbc : (abc)bbc(ccc)
    
    分隔符号 2
    其它符号，主要是很有可能 用于 分隔 文字的 符号
        , 这个是的，主要是这个
        / 1278 ，可能是的
        & 这个要不要呢
        
        其它不要了吧 . - ?!'+#* : ~ ; $^
        
        比如：
            逗号分开的：
                36 Great Holes starring Fred Couples (Europe, prototype, 19941221-B)
            / 分开的：
                Arquimedes XXI (128K, English / French / German / Spanish)
    
    
"""

# () [] {}
# / , &
string_separator_s    = the_variables.string_separators_for_second_part

string_separator_s_re = re.escape( string_separator_s )             # 转为 正则 字符 表达

string_for_keep_separator     = r"[" + string_separator_s_re + r"]"    # 匹配其中一个
string_for_keep_separator     = r"(" + string_for_keep_separator + r")"
    # 圆括号，有括号的内容，re.split() 分割时，内容保留
string_for_not_keep_separator = r"[" + string_separator_s_re + r"]"    # 匹配其中一个
    # 不保留，不要 圆括号

p_keep_separator     = re.compile( string_for_keep_separator )
p_not_keep_separator = re.compile( string_for_not_keep_separator )

# 返回一个 list
# 将原始字符串切割后的结果
#   (Europe, prototype, 19941221-B,just for a test)
#       结果为：['', '(', 'Europe', ',', ' prototype', ',', ' 19941221-B', ',', 'just for a test', ')', '']
#       # 之后的话：翻译 其中的 每一项，再拼起来就行
def split(a_string,keep_separator=True):
    
    # True 保留分隔符，翻译后，方便 把 翻译好的内容 ，再 拼接起来
    
    # False 不保留，用于，创建 需要 翻译 的 词条
    
    s = a_string.strip()
    
    s = multi_space_to_single.main( s )
    
    # Pattern.split(string, maxsplit=0)
    # re.split(pattern, string, maxsplit=0, flags=0)
    
    if keep_separator:
        list_of_string_s = p_keep_separator.split(s)
    else:
        list_of_string_s = p_not_keep_separator.split(s)
    
    # # 清理 前、后 空格
    # for n in range( len( list_of_string_s ) ):
    #     list_of_string_s[n] =  list_of_string_s[n].strip()
    # 还是不清理了吧，用到的时候，再清理
    #   如果只有一部分翻译了，
    #   剩余的部分 还没有翻译，还能保持原有的格式
    
    return list_of_string_s
    


if __name__ =="__main__":
    
    s=  r"(Europe, prototype, 19941221-B,just for           a test & test b)(OK)[HELLO]"
    
    temp=split(s,True)
    temp2=split(s,False)
    
    print()
    print(s)
    
    
    print()
    print("keep separator")
    print(temp)
    print()
    for x in temp:
        if x :
            print("\t",x)

    print()
    print("not keep separator")
    print(temp2)
    print()
    for x in temp2:
        if x :
            print("\t",x)
