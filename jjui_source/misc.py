# -*- coding: utf_8_sig-*-
import os
import sys


from . import save_pickle
from . import global_variable
from . import global_static_filepath as the_files
from . import xml_parse_mame
from . import folders_save

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


#########################
##### 从目录中取值
#####   内置目录
#####   外置目录
#####   外置 xml 目录 (SL) 
#####   外置 source 目录 (MAME) 
#####   拥有列表 与 未拥有列表
# internal_index
def get_id_list_from_internal_index(id_1,id_2=None,):
    
    the_index = global_variable.internal_index
    
    def for_level_1(id_1):
        temp = [] # 可能为 list 也可能为 set
        if id_1 in the_index:
            if "gamelist" in the_index[id_1]:
                temp = the_index[id_1]["gamelist"]
        return temp
    
    def for_level_2(id_1,id_2):
        temp = [] # 可能为 list 也可能为 set
        if id_1 in the_index:
            if "children" in the_index[id_1]:
                if id_2 in the_index[id_1]["children"]:
                    if "gamelist" in the_index[id_1]["children"][id_2]:
                        temp = the_index[id_1]["children"][id_2]["gamelist"]
        return temp
    
    if id_2 is None:
        return for_level_1(id_1)
    else:
        return for_level_2(id_1,id_2)
# external_index
def get_id_list_from_external_index(id_1,id_2=None,):
    
    the_index = global_variable.external_index
    
    # 第一层 "ROOT_FOLDER"
    def for_level_1(id_1):
        temp = [] # 可能为 list 也可能为 set
        if id_1 in the_index:
            if "ROOT_FOLDER" in the_index[id_1]:
                temp = the_index[id_1]["ROOT_FOLDER"]
        return temp
    
    # 第二层
    def for_level_2(id_1,id_2):
        temp = [] # 可能为 list 也可能为 set
        if id_1 in the_index:
            if id_2 in the_index[id_1]:
                temp = the_index[id_1][id_2]
        return temp
    
    if id_2 is None:
        return for_level_1(id_1)
    else:
        return for_level_2(id_1,id_2)
# external_index_by_source      mame
def get_id_list_from_external_index_by_source(id_1,id_2=None):
    the_index = global_variable.external_index_by_source
    
    # 第一层 "ROOT_FOLDER"
    def for_level_1(id_1):
        temp = [] 
        if id_1 in the_index:
            if "ROOT_FOLDER" in the_index[id_1]:
                temp = the_index[id_1]["ROOT_FOLDER"]
        return temp
    
    # 第二层
    def for_level_2(id_1,id_2):
        temp = [] 
        if id_1 in the_index:
            if id_2 in the_index[id_1]:
                temp = the_index[id_1][id_2]
        return temp
    
    if id_2 is None:
        the_source_list = for_level_1(id_1)
    else:
        the_source_list = for_level_2(id_1,id_2)
    
    the_id_list = []
    
    internal_index = global_variable.internal_index
    for the_source in the_source_list :
        if "sourcefile" in internal_index:
            if "children" in internal_index["sourcefile"]:
                if the_source in internal_index["sourcefile"]["children"]:
                    if "gamelist" in internal_index["sourcefile"]["children"][the_source]:
                        the_id_list.extend( internal_index["sourcefile"]["children"][the_source]["gamelist"] )

    return the_id_list
# external_index_by_source      SL
def get_id_list_from_external_index_sl_by_xml(id_1,id_2=None):
    the_index = global_variable.external_index_sl_by_xml
    
    # 第一层 "ROOT_FOLDER"
    def for_level_1(id_1):
        temp = [] 
        if id_1 in the_index:
            if "ROOT_FOLDER" in the_index[id_1]:
                temp = the_index[id_1]["ROOT_FOLDER"]
        return temp
    
    # 第二层
    def for_level_2(id_1,id_2):
        temp = [] 
        if id_1 in the_index:
            if id_2 in the_index[id_1]:
                temp = the_index[id_1][id_2]
        return temp
    
    if id_2 is None:
        the_xml_list = for_level_1(id_1)
    else:
        the_xml_list = for_level_2(id_1,id_2)
    
    the_id_list = []
    
    xml_dict = global_variable.all_data["xml"]
    for xml_name in the_xml_list:
        if xml_name in xml_dict:
            the_id_list.extend(  xml_dict[xml_name]  )
    
    return the_id_list
# 拥有列表 未拥有列表
def get_id_list_for_available_or_unavailable(the_type="available_set"):
    the_id_list = [] # 可能为 list 也可能为 set
    
    if the_type == "available_set":
        if global_variable.available_hide_set or global_variable.available_filter_set:
            the_id_list = global_variable.available_set - global_variable.available_hide_set - global_variable.available_filter_set
        else:
            the_id_list = global_variable.available_set
    elif the_type=="unavailable_set":
        if global_variable.available_hide_set:
            the_id_list = global_variable.unavailable_set | global_variable.available_hide_set
        else:
            the_id_list = global_variable.unavailable_set
    
    return the_id_list
# 外部目录编辑
def set_id_list_for_external_index(the_id_list,id_1,id_2=None):
    if type(the_id_list) != list:
        the_id_list = list( the_id_list )
    
    the_index = global_variable.external_index
    
    # 第一层 "ROOT_FOLDER"
    def for_level_1(the_id_list,id_1):
        if id_1 in the_index:
            the_index[id_1]["ROOT_FOLDER"] = the_id_list
    
    # 第二层
    def for_level_2(the_id_list,id_1,id_2):
        if id_1 in the_index:
            the_index[id_1][id_2] = the_id_list
    
    if id_2 is None:
        for_level_1(the_id_list , id_1)
    else:
        for_level_2(the_id_list , id_1 , id_2)


# 导出内置目录到 .jjui\out 文件夹
def export_all_internal_index():
    the_out_folder = the_files.folder_export
    if os.path.isdir(the_out_folder):
        pass
    else:
        if os.path.isfile(the_out_folder):
            os.remove(the_out_folder)
        os.makedirs(the_out_folder)

    the_index = global_variable.internal_index

    for id_1 in the_index:

        print()
        print(id_1)

        file_name = os.path.join(the_out_folder,id_1 + ".ini")

        with open( file_name,mode="wt",encoding="utf_8") as f:
            print(file_name)
            # 文件头
            f.write("[FOLDER_SETTINGS]\n")
            f.write("RootFolderIcon golden\n")
            f.write("SubFolderIcon golden\n")
            f.write("\n")
            
            # 主分类
            # 标题
            f.write("[ROOT_FOLDER]\n")
            # 内容
            id_list = get_id_list_from_internal_index(id_1)
            for x in sorted( set(id_list) ):
                f.write(x)
                f.write("\n")
            f.write("\n")

            # 子分类
            if "children" in the_index[id_1]:
                for id_2 in sorted( the_index[id_1]["children"] ):
                    id_list = get_id_list_from_internal_index(id_1,id_2)
                    if id_list:
                        # 标题 
                        f.write("[" + id_2 + "]" + "\n")
                        # 内容
                        for x in sorted( set(id_list) ):
                            f.write(x)
                            f.write("\n")
                        f.write("\n")

# 导出外置目录到 .jjui\out 文件夹，并清理超出范围的项目
def export_all_external_index_and_clean():
    the_out_folder = the_files.folder_export
    if os.path.isdir(the_out_folder):
        pass
    else:
        if os.path.isfile(the_out_folder):
            os.remove(the_out_folder)
        os.makedirs(the_out_folder)

    the_index = global_variable.external_index

    def clean_the_id(the_id_set):
        if type(the_id_set) != set:
            the_id_set = set(the_id_set)
        the_id_set = global_variable.set_data["all_set"] & the_id_set
        return the_id_set

    for file_path_old in the_index:

        print()
        print(file_path_old)

        base_name = os.path.basename(file_path_old)
        file_name = os.path.join(the_out_folder,base_name)
        file_name_not_used = os.path.join(the_out_folder,base_name + ".txt")

        print(file_name)

        # 清理
        data = the_index[file_path_old]
        new_data = {}
        data_not_used={}
        for x in data:
            if x != "FOLDER_SETTINGS":
                new_data[x] = clean_the_id( data[x] )
                temp = set(data[x]) - new_data[x]
                if temp:
                    data_not_used[x] = temp
            else:
                new_data[x] = data[x]
                data_not_used[x] = data[x]
        
        # 写
        folders_save.save(file_name,new_data)
        #
        if "FOLDER_SETTINGS" not in data_not_used:
            data_not_used["FOLDER_SETTINGS"] = []
        if len(data_not_used)>1: # 至少有 "FOLDER_SETTINGS"
            folders_save.save(file_name_not_used,data_not_used)


############
# 删除 列表中 指定的 行
def delete_current_rows_in_game_list(event=None,reverse=False):
    the_table = global_variable.the_showing_table
    
    the_index = global_variable.internal_index
    
    if the_table is None:
        return
    
    the_id_list = the_table.new_var_data_holder.get_current_list_all_id()
    
    if reverse:
        id_list_to_delete = global_variable.set_data["all_set"] - set(the_id_list)
    else:
        id_list_to_delete = the_id_list
    
    if not id_list_to_delete:
        return
    
    the_id_will_be_deleted = set(id_list_to_delete) & global_variable.set_data["all_set"]
    
    ###############
    ###############
    ##
    ##全删了
    if len(the_id_will_be_deleted) == len(  global_variable.set_data["all_set"]  ):
        print()
        print("delete all")
        print()
        if os.path.isfile(the_files.file_pickle_gamelist_data):
            os.remove(the_files.file_pickle_gamelist_data)
            sys.exit()
    
    ###############
    ###############
    ##
    ##只删部分
    
    # 1
    # 清理 行
    machine_dict = global_variable.machine_dict
    for the_id in the_id_will_be_deleted:
        del machine_dict[the_id]
    
    
    # 清理 set_data
    new_all_set    = set( machine_dict.keys() )
    new_clone_set  = new_all_set & global_variable.set_data["clone_set"]
    new_parent_set = new_all_set - new_clone_set
    
    global_variable.set_data["all_set"].clear()
    global_variable.set_data["all_set"].update(new_all_set)
    global_variable.set_data["clone_set"].clear()
    global_variable.set_data["clone_set"].update(new_clone_set)
    global_variable.set_data["parent_set"].clear()
    global_variable.set_data["parent_set"].update(new_parent_set)
    
    
    # dict_data
    # global_variable.dict_data["clone_to_parent"]
    temp_delete = set( global_variable.dict_data["clone_to_parent"].keys() ) - new_clone_set
    for the_id in temp_delete:
        del global_variable.dict_data["clone_to_parent"][the_id]
    # global_variable.dict_data["parent_to_clone"]
    # parent_to_clone
    global_variable.dict_data["parent_to_clone"].clear() # 先清理
    for clone_game,parent_game in global_variable.dict_data["clone_to_parent"].items():
        if parent_game not in global_variable.dict_data["parent_to_clone"]:
            global_variable.dict_data["parent_to_clone"][parent_game] = []
        global_variable.dict_data["parent_to_clone"][parent_game].append( clone_game )
    
    # xml
    if global_variable.gamelist_type == "softwarelist":
        xml_dict = global_variable.all_data["xml"]
        for xml_name in xml_dict:
            xml_dict[xml_name] = set(xml_dict[xml_name]) & new_all_set
        # 空项目清理
        empty_list = []
        for xml_name in xml_dict:
            if not xml_dict[xml_name]:
                empty_list.append(xml_name)
        for xml_name in empty_list:
            del xml_dict[xml_name]
    
    # 2
    # 再 清理 一下 内置目录
    the_index = global_variable.internal_index
    def delete_items_in_internal_index():
        #new_all_set
        
        the_index = global_variable.internal_index
        
        def for_level_1():
            temp = [] # 可能为 list 也可能为 set
            for id_1 in the_index:
                if "gamelist" in the_index[id_1]:
                    if   type(the_index[id_1]["gamelist"])==list:
                        the_index[id_1]["gamelist"] = list(set(the_index[id_1]["gamelist"]) & new_all_set)
                    elif type(the_index[id_1]["gamelist"])==set:
                        the_index[id_1]["gamelist"] = the_index[id_1]["gamelist"] & new_all_set
        
        def for_level_2():
            for id_1 in the_index:
                if "children" in the_index[id_1]:
                    for id_2 in the_index[id_1]["children"]:
                        if "gamelist" in the_index[id_1]["children"][id_2]:
                            if   type(the_index[id_1]["children"][id_2]["gamelist"])==list:
                                the_index[id_1]["children"][id_2]["gamelist"] = list(  set( the_index[id_1]["children"][id_2]["gamelist"] )  & new_all_set )
                            elif type(the_index[id_1]["children"][id_2]["gamelist"])==set:
                                the_index[id_1]["children"][id_2]["gamelist"] = the_index[id_1]["children"][id_2]["gamelist"] & new_all_set

        for_level_1()
        for_level_2()
    #
    delete_items_in_internal_index()
    #
    # 目录 空项目：
    #xml_parse_mame.clean_internal_index(the_index)
    xml_parse_mame.clean_internal_index(the_index)
    
    
    ##
    ##
    ##
    save_pickle.save(global_variable.all_data , the_files.file_pickle_gamelist_data)
    
    # 退出
    sys.exit()

if __name__ == "__main__" :
    pass