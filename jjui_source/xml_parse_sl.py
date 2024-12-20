﻿# -*- coding: utf-8 -*-
import xml.etree.ElementTree
# import os

# 元素改为 list

# softwarelists

#  softwarelist
#  softwarelist name description        # attrib

#    software
#    software name cloneof supported  # attrib


# xml name cloneof supported description year publisher alt_title
#
# id 改为 → xml + 空格 + name
#
# 这其中 romof 要改一下，
#   原来的 cloneof → name
#   改为   cloneof → xml + 空格 + name
def read_xml( file_name ):

    all_info = {}
    # nes smb
        # name : smb
        # description : Super Mario Bros. (Euro, Rev. A)
        # ......
    # id 为  ： xml 名称 + 一个空格 + 名称
    
    xml_info = {}
    # nes     # key为 xml 名
        # description : "Nintendo Entertainment System cartridges"
        # "gamelist"    : [] ,# 元素列表，初始化
        # .....
    
    print( )
    print( "parsing xml")
    count = 0
    for (event, elem) in xml.etree.ElementTree.iterparse(file_name,events=("end",) ) :#"start"
    
        if elem.tag=="softwarelist":
            
            xml_name        = elem.attrib.get("name","").strip().lower()
            
            #xml_description = elem.attrib.get("description","")
            xml_info[xml_name] = {
                "description" : elem.attrib.get("description","") ,
                "gamelist"    : [] ,# 元素列表，初始化
                }
            
            games_in_xml = xml_info[xml_name][ "gamelist" ]

            for child in elem:
                
                if child.tag=="software" :
                
                    count += 1
                    if count % 1000 == 0:
                        print(count)
                
                    temp_dict = dict()
                    
                    temp_dict["xml"] = xml_name
                    
                    software_name = child.attrib["name"].strip().lower()
                    
                    # id
                    software_id   = "".join( ( xml_name," ",software_name ) )
                    
                    games_in_xml.append(software_id)
                    
                    #
                    #<!ATTLIST software name CDATA #REQUIRED>
                    #<!ATTLIST software cloneof CDATA #IMPLIED>
                    #<!ATTLIST software supported (yes|partial|no) "yes">
                    temp_dict.update( child.attrib )
                    
                    # 这其中 romof 要改一下，
                    #   原来的 cloneof → name
                    #   改为   cloneof → xml + 空格 + name
                    if "cloneof" in temp_dict:
                        temp_parent_id = temp_dict["cloneof"].strip().lower()
                        parent_id      = xml_name + " " +  temp_parent_id
                        temp_dict["cloneof"] = parent_id
                    
                    #
                    for grand_child  in child:
                        
                        # description
                        if   grand_child.tag == "description":
                            temp_dict["description"] = grand_child.text
                        
                        # year
                        elif grand_child.tag == "year":
                            temp_dict["year"] = grand_child.text
                        
                        # publisher
                        elif grand_child.tag == "publisher":
                            temp_dict["publisher"] = grand_child.text
                        
                        # alt_title
                        # <info name="alt_title" value="神宮館'89電脳九星占い"/>
                        # 可能有多个值 用逗号连接
                        elif grand_child.tag == "info":
                            if "name" in grand_child.attrib:
                                if grand_child.attrib["name"]=="alt_title":
                                    if "value" in grand_child.attrib:
                                        if grand_child.attrib["value"]:
                                            
                                            # 已有值，逗号连接
                                            if "alt_title" in temp_dict:
                                                temp_dict["alt_title"] += ","
                                                temp_dict["alt_title"] += str(grand_child.attrib["value"])
                                            # 初始
                                            else:
                                                temp_dict["alt_title"] = str(grand_child.attrib["value"])

                            
                    
                    # 清理
                    # Element.text 的值，有可能是 None
                    # 新版本好像 也没有问题
                    # 0.162 有遇到此问题
                    for the_key in temp_dict:
                        if temp_dict[the_key ] is None:
                            temp_dict[the_key ] = ""
                    
                    all_info[ software_id ] = temp_dict
            

            
            
            elem.clear()

    print(count)

    return all_info,xml_info


def xml_info_change(xml_info):
    # 转为 set 格式
    
    # nes     # key为 xml 名
        # description : "Nintendo Entertainment System cartridges"
        # "gamelist"    : [] ,# 元素列表，初始化
        # .....
    
    for xml_name in xml_info:
        temp = set( xml_info[xml_name]["gamelist"] )
        
        xml_info[xml_name]["gamelist"]  = temp

# 大量重复字符串，处理一下
#   相同的字符串，占用了不同的空间，
#   重新赋值一下，可能会 节约 些空间
def about_some_same_strings(machine_dict):
    
    # 游戏名： 
    #
    # sl
    # 'cloneof' ,所有内容，都是 游戏名 id ，重复的
    def func_1(original_data):
        #['xml', 'name', 'supported', 'translation', 'year', 'publisher', 'description','alt_title', 'cloneof']
        the_key_list = ['cloneof',]
        
        # dict 游戏名→游戏名
        game_name_dict = { game_name : game_name for game_name in original_data }
        
        for the_key in the_key_list:
            print()
            print(the_key)
            
            for game_name,game_info in original_data.items() :
                if the_key in game_info:
                    # 原始值
                    the_old_value = game_info[the_key]
                    
                    # 重新赋值
                    game_info[the_key] = game_name_dict.get(the_old_value,the_old_value)
        
        return original_data
    
    # 某个key中，有（大量/一些）重复的 字符串，
    # sl
    def func_2(original_data):
        #['xml', 'name', 'supported', 'translation', 'year', 'publisher', 'description','alt_title', 'cloneof']
        the_key_list = [ 
                'xml',# 重复的特别多
                'name',
                'supported',# 重复的特别多
                'year',
                'publisher',
                ]
        
        for the_key in the_key_list:
            print()
            print(the_key)
            
            # 原来的值
            the_value_list = []
            
            for game_name,game_info in original_data.items() :
                if the_key in game_info:
                    the_value_list.append( game_info[the_key] )
            
            the_value_set = set( the_value_list )
            
            the_value_dict = { x : x for x in the_value_set}
            
            # 重新赋值
            for game_name,game_info in original_data.items() :
                if the_key in game_info:
                    the_value = game_info[ the_key ]
                    game_info[ the_key ] = the_value_dict[ the_value ]
        
        return original_data
    
    
    
    #if "nes smb1" in machine_dict:
    #    print(machine_dict["nes smb1"])
    
    machine_dict = func_1(machine_dict)
    
    #if "nes smb1" in machine_dict:
    #    print()
    #    print(machine_dict["nes smb1"])
    
    machine_dict = func_2(machine_dict)
    
    #if "nes smb1" in machine_dict:
     #   print()
     #   print(machine_dict["nes smb1"])
    return machine_dict




# set_data = {}
# set_data["all_set"] = set()
# set_data["clone_set"] = set()
# set_data["parent_set"] = set()
#############
def make_set_data(machine_dict,):
    print( )
    print( "make set data")
    
    set_data = {}
    set_data["all_set"] = set()
    set_data["clone_set"] = set()
    set_data["parent_set"] = set()
    
    set_data["all_set"] = set( machine_dict.keys() )
    
    temp = []
    for game_name,temp_dict in machine_dict.items():
        if "cloneof" in temp_dict : 
            
            temp.append(game_name)
    set_data["clone_set"]  = set( temp )
    
    set_data["parent_set"] = set_data["all_set"] - set_data["clone_set"]
    
    return set_data

# dict_data
# dict_data["clone_to_parent"]
# dict_data["parent_to_clone"]
# 添加
# dict_data["xml"]
def make_dict_data(machine_dict,xml_info):
    print( )
    print( "make dict data")
    
    dict_data = {}

    dict_data["clone_to_parent"] = {}
        # 一对一,子元素为 字符
    dict_data["parent_to_clone"] = {}
        # 一对多，子元素为 字符 组成 的 list
    #dict_data["romof"] ={} 
        # 一对一,子元素为 字符
        # 这个要还是不要？
        #   似乎不重要，
        #   在后面的 分类 bios 里用一下，然后就可以删了
    
    
    # romof
    # clone_to_parent
    for game_name,game_info in machine_dict.items():
        if "cloneof" in game_info : 
            
            dict_data["clone_to_parent"][game_name] = game_info["cloneof"]
        #if "romof" in game_info :
        #    dict_data["romof"][game_name] = game_info["romof"]
    
    # parent_to_clone
    for clone_game,parent_game in dict_data["clone_to_parent"].items():
        if parent_game not in dict_data["parent_to_clone"]:
            dict_data["parent_to_clone"][parent_game] = []
        dict_data["parent_to_clone"][parent_game].append( clone_game )


    # xml
    dict_data["xml"] = {}
    
    for xml_name in xml_info:
        dict_data["xml"][xml_name] = xml_info[xml_name]["gamelist"]
    return dict_data


#   internal_index
def make_internal_index(machine_dict,set_data,dict_data,xml_info):
    print( )
    print( "make internal index")
    internal_index = {}
    # 目录
    # 内部元素为 {}
    # 单层，双层，         ?三层，?更多层
    # 
    # 子元素, 1 层 
    #   gamelist:[],游戏列表
    #       children:{} 为空  
    #       或者 干脆没有 children:{}
    #
    # 子元素, 2 层 
    #   gamelist:[],游戏列表

    # 单层
    #{"gamelist":[],}
    
    # all_set
    # clone_set
    # parent_set    
    def func_for_index_1( internal_index ):
        internal_index["all_set"   ]      = {"gamelist":[],"children":{},}
        internal_index["clone_set" ]      = {"gamelist":[],"children":{},}
        internal_index["parent_set"]      = {"gamelist":[],"children":{},}
        #
        internal_index["all_set"   ]["gamelist"]    = set_data["all_set"]
        internal_index["clone_set" ]["gamelist"]    = set_data["clone_set"]
        internal_index["parent_set"]["gamelist"]    = set_data["parent_set"]
    print("index - all_set clone_set parent_set")
    func_for_index_1( internal_index )
    
    # 按 xml 文件分类
    def func_for_index_2( internal_index ):
        
        # 初始化
        internal_index[ "xml" ]      = {"gamelist":[],"children":{},}
        
        for xml_name in xml_info:
            
            temp_dict = internal_index[ "xml" ]["children"]
            temp_dict[xml_name + r".xml"] = {"gamelist":[],}
            temp_dict[xml_name + r".xml"]["gamelist"] = xml_info[xml_name]["gamelist"]
    
    # 按 xml 文件分类
    func_for_index_2( internal_index )
    

    #  machine_dict[ game_name ][ the_key ] 为一个 单一的元素
    # 比如 year 年代分类
    def func_for_index_level_2( the_key, temp_dict=None):
        #反回一个二级分类，
        #   但，分类第一层，为空
        #   比如 year 分类
    
        # machine_dict
        # set_data
        games_range = set_data["all_set"]
        
        # 初始化
        if temp_dict == None:
            temp_dict = {"gamelist":[],"children":{},}
            #   添加第二层内容，也就是 temp_dict[ "children" ]
        
        # 已 year 为例
        # year 空
            # 1997  ---> [kof97 ,sfiii, ....]
            # 1998  ---> [kof98,.....]
            # 1999
            #
        # the_key 是 ：比如 "year" 在 machine_dict[game_name] 中
        #   且 每个游戏 此项 只有一个元素
        #   并 以 子元素 作为 子分类 group_name
        # 如 group_name 为 1997 1998 这样子
        
        for game_name in games_range:
            if the_key in machine_dict[game_name]:
                group_name = machine_dict[game_name][the_key]
                if group_name not in temp_dict["children"]:
                    # 初始化
                    temp_dict["children"][group_name]={"gamelist":[],} # "children":{},
                temp_dict["children"][group_name]["gamelist"].append( game_name )
        
        return temp_dict
    # year
    print("year")
    internal_index["year"]= func_for_index_level_2("year") 
    # publisher
    print("publisher")
    internal_index["publisher"]= func_for_index_level_2("publisher")
    # supported
    print("supported")
    internal_index["supported"] = func_for_index_level_2("supported")

    
    return internal_index


def prepare_for_gamelist_translation(machine_dict):
    for game_id,game_info in machine_dict.items():
        game_info["translation"]=game_info.get("description","")
    return machine_dict


# dict_to_list
def dict_to_list(game_list_data):
    print()
    print("\t dict to list")
    # return columns,machine_dict
    
    # xml name translation cloneof supported description year publisher alt_title
    # "translation"
    the_key_s =  [
                    "supported",
                    
                    "xml",
                    "name",
                    "description",
                    
                    "year",
                    "publisher",
                    
                    
                    "alt_title",
                    "cloneof",
                    "translation",

                    
                    ]
    
    
    
    #所有的 key
    def get_all_keys(data):
        all_keys=[]
        for game,game_info in data.items():
            all_keys.extend(  game_info.keys() )
        all_keys= sorted ( set(all_keys) )
        return all_keys
    all_keys = get_all_keys(game_list_data)
    
    # 去掉选错的
    columns=[]
    for x in the_key_s:
        if x in all_keys:
            columns.append(x)

    
    machine_dict = {}
    empty_string = ""
    # 格式 转为 list
    for game_name in sorted( game_list_data ):
        game_info = game_list_data[game_name]
        
        temp=[] # 初始化
        for the_key in columns:
            temp.append( game_info.get(the_key,empty_string) )
        machine_dict[game_name] = temp
    
    print("\t dict to list,columns : {}".format(columns))
    if machine_dict:
        print(len(machine_dict))

    
    return columns,machine_dict


def get_xml_dict(xml_info):
    xml_dict={}
    
    for xml_name in xml_info:
        xml_dict[xml_name]=xml_info[xml_name]["gamelist"]
    
    return xml_dict

def main( file_name ,mame_version=""):
    
    #
    #mame_version 

    all_info,xml_info = read_xml(file_name)
    #
    machine_dict = all_info
    
    # 大量重复字符串，处理一下
    machine_dict = about_some_same_strings(machine_dict)
    
    #
    xml_info_change(xml_info) # 转为 set
    
    # 在转换格式之后
    xml_dict = get_xml_dict(xml_info)
    
    # set data ,
    #   all_set parent_set clone_set
    set_data       = make_set_data( machine_dict ,) #
    # dict_data
    #   clone_to_parent parent_to_clone
    dict_data      = make_dict_data( machine_dict ,xml_info)# 添加 dict_data["xml"]
    # 内置分类
    internal_index = make_internal_index( machine_dict,set_data,dict_data,xml_info)

    # 清理 game_list_data 多余的内容
    # 不用了，等会要转为 list
    #  machine_dict = clear_game_list_data(game_list_data)

    # 翻译准备 ，将原 英文内容复制过去
    machine_dict = prepare_for_gamelist_translation(machine_dict)
    
    # 格式，转为 list
    # 第0项：xml ，第1项：name ，这样方便得到 id : xml + 空格 + name
    columns,machine_dict = dict_to_list(machine_dict)
    
    
    
    temp_dict = {}
    temp_dict["mame_version"]   = mame_version
    
    temp_dict["columns"]        = columns
    temp_dict["machine_dict"]   = machine_dict
    temp_dict["xml"]   = xml_dict
    
    temp_dict["set_data"]       = set_data
    temp_dict["dict_data"]      = dict_data
    temp_dict["internal_index"] = internal_index
    
    return temp_dict

if __name__ == "__main__":

    pass
