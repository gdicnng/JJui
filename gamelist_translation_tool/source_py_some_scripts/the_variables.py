# -*- coding: utf_8_sig-*- 


# () [] {} 至少要这几个
# / , &
#string_separators_for_second_part    = r"()[]{}"
#string_separators_for_second_part    = string_separators_for_second_part + r"/,&"

#import string
# 把所有 符号 都加上吧
#string_separators_for_second_part = string.punctuation
# 把数字 0-9 也加上吧
#string_separators_for_second_part = string_separators_for_second_part + string.digits

#
string_separators_for_second_part    = r"()[]{}"
#string_separators_for_second_part    = string_separators_for_second_part + r"/,&"
# & 这个符号 感觉还是不去掉好一些
string_separators_for_second_part    = string_separators_for_second_part + r"/,"


