# -*- coding: utf_8_sig-*- 
import re

"""
    以括号 起始处 分割字符串
    返回两部分： 前一部分,后一部分
    
"""

# 英文括号
# () [] {}
    # <> 尖括号这个不管吧

# 中文括号
# （ ）    就这个吧，其它不管
    # 〔 〕 【 】 〖 〗 ｛ ｝
    # 估计还有其这的,还有也不管了

# ()[]{} 开头
separator_string = r"([{" 
#search_str_parentheses = r'^(.*?)([\(\[\{].*)$'  
search_str_parentheses = "".join(
        [
            r'^(.*?)(['                 ,
            re.escape(separator_string) ,
            r'].*)$'                    ,
        ]
            )
p_parentheses=re.compile( search_str_parentheses, )

# ()[]{} 开头
# 一些中文括号，开头 （〔【〖｛
separator_string_cn = r"([{" + r"（〔【〖｛"
# search_str_parentheses_cn = r'^(.*?)([（〔【〖｛\(\[\{].*)$' 
search_str_parentheses_cn = "".join(
        [
            r'^(.*?)(['                    ,
            re.escape(separator_string_cn) ,
            r'].*)$'                       ,
        ]
            )
p_parentheses_cn=re.compile( search_str_parentheses_cn, )

# en
# 返回两部分
def main(s):
    m=p_parentheses.search( s )
    if m:
        s1=m.group(1)
        s2=m.group(2)
        return s1,s2
    else:
        return s,""

# cn
# 返回两部分
def main_cn(s):
    m=p_parentheses_cn.search( s )
    if m:
        s1=m.group(1)
        s2=m.group(2)
        return s1,s2
    else:
        return s,""


if __name__ =="__main__":
    
    # test
    
    some_string = [
            r"abc BBC(sa df)[gggg ]{ sdfsdf} KKK(ggg)",
            r"abc BBC[gggg ](sa df){ sdfsdf} KKK(ggg)",
            r"abc BBC{ sdfsdf}[gggg ](sa df) KKK(ggg)",
            
            # # 〔 〕 【 】 〖 〗 ｛ ｝
            r"测试(abc)（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试[bbc](abc)（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试{ggh}[bbc](abc)（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试 中文括号（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试 中文括号〔 测试一〕（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试 中文括号 【 test2 】〔 测试一〕（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试 中文括号 〖 测试三 〗 【 test2 】〔 测试一〕（人aa）(民bb)[日cc]ccc{报dd}",
            r"测试 中文括号 ｛ 四｝〖 测试三 〗 【 test2 】〔 测试一〕（人aa）(民bb)[日cc]ccc{报dd}",
            
            r"没有括号",
            
            r"(括号在一开始)",
            
            ]
    
    count = 0
    for a_string in some_string:
        print()
        print(count)
        
        
        a,b = main(a_string)
        print("::English split")
        print(a_string)
        print("\t",a)
        print("\t",b)
        
        a,b = main_cn(a_string)
        print("::Chinese split")
        print(a_string)
        print("\t",a)
        print("\t",b)
        
        count += 1
    

