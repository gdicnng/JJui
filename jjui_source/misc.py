# -*- coding: utf_8_sig-*-
import sys


from . import global_variable

# 二进制字符串列表，检查 字符编码
def check_binary_string_list_encoding(binary_string_list):
    user_configure = global_variable.user_configure_data
    
    if user_configure["encoding"] :
        print("user encoding")
        print(user_configure["encoding"])
        return user_configure["encoding"]
    
    encoding_list=["utf_8_sig",]
    
    if sys.platform.startswith('win32'):
        encoding_list=["utf_8_sig","mbcs","gbk"]
            # utf_8 、utf_8_sig
            # gbk 其实要比 对应的 ANSI 少一点点，比如欧元符号
            # big5
            # mbcs : Windows 专属：根据 ANSI 代码页（CP_ACP）对操作数进行编码。
    else:
        encoding_list=["utf_8_sig","gbk"]
    
    the_right_encoding = 'utf_8' # 默认值
    
    for the_encoding in encoding_list:
        flag_encoding_is_ok = False
        
        try:
            for binary_line in binary_string_list:
                line = binary_line.decode(encoding=the_encoding, )
            flag_encoding_is_ok = True
        except:
            flag_encoding_is_ok = False
        
        if flag_encoding_is_ok:
            the_right_encoding = the_encoding
            print("the_right_encoding:{}".format(the_encoding))
            break
    
    return the_right_encoding
