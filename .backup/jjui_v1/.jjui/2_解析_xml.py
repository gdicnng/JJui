# -*- coding: utf_8_sig-*-
import xml.etree.ElementTree
import os

# datas={ {}、{} }
#   mame_version
#   machine_dict
#       "kof97":
#       {"name":"kof97",…………}
#   set_data
#   dict_data
#   internal_index

def read_xml( file_name ):
    count = 0

    mame_version = ''
    
    #index_list_data=[]
    
    set_data = {}
    set_data["all_set"] = set()
    set_data["clone_set"] = set()
    set_data["parent_set"] = set()

    # 删
    #set_data["device_set"] = set()
    #set_data["bios_set"] = set()
    
    #set_data["mechanical_set"] = set()
    
    #set_data["all_set_2"] = set()
    
    #set_data["softwarelist_set"] = set()
    #set_data["chd_set"] = set()
    #set_data["sample_set"] = set()
    #set_data["rom_set"] = set()
    
    #set_data["no_roms"] = set()
    #set_data["no_roms_2"] = set()
    
    internal_index = {}
    # 目录
    # 内部元素为 {}
    # 单层，双层，三层？，更多层？
    # 
    # 子元素, 1 层 
    #   gamelist:[],游戏列表
    #   children:{} 空
    #
    # 子元素, 2 层 
    #   gamelist:[],游戏列表
    #   children:{}
    #       子元素
    #       gamelist:[],游戏列表
    #       children:{}
    
    # 单层
    #{"gamelist":[],"children":{},}
    
    internal_index["bios"]      = {"gamelist":[],"children":{},}
    internal_index["device"]    = {"gamelist":[],"children":{},}
    
    internal_index["mechanical"]    = {"gamelist":[],"children":{},}
    
    #internal_index["rom"]= {"gamelist":[],"children":{},}    
    internal_index["chd"]= {"gamelist":[],"children":{},}    
    internal_index["sample"]= {"gamelist":[],"children":{},}
    
    internal_index["softwarelist"]= {"gamelist":[],"children":{},}   
    
     
    
    
    
    dict_data = {}
    dict_data["romof"] = {}
    dict_data["clone_to_parent"] = {}
        # 一对一,子元素为 字符
    dict_data["parent_to_clone"] = {}
        # 一对多，子元素为 字符 组成 的 list
    
    
    
    
    machine_dict = {}
        # a dict of dicts
        # a dict , 包含 machine name ，如 kof97 、 kof90 、 knights 等

        # 每一个元素，如 kof97 ，是一个 dict 含：{'name': 'kof97', 'sourcefile': 'neogeo.cpp', 'romof': 'neogeo', 'isbios': 'no', 'isdevice': 'no', 'ismechanical': 'no', 'runnable': 'yes'}
        
    machine_dict_delete = {} 
        # 存放其它信息，用来计算内部分类列表的
        # 之后，不保存
        
    print( )
    print( "读取 xml ，读取 mame 版本")
    for (event, elem) in xml.etree.ElementTree.iterparse(file_name,events=("start","end") ) :
        if event == 'start' : # 找到开始标记
            if elem.tag=="mame" : # mame 标签
                if "build" in elem.attrib : # 版本 标签
                    mame_version = elem.attrib["build"]
                break
    if mame_version != '':
        print( "mame_version")
        print( mame_version)    


    print( )
    print( "读取 xml")
    for (event, elem) in xml.etree.ElementTree.iterparse(file_name,events=("start","end") ) :
        if event == 'end': # 找到结束标记
            if elem.tag=="machine":
                
                # elem.attrib 是一个 dict 的类型
                
                # 比如 kof97 的：
                # {'name': 'kof97', 'sourcefile': 'neogeo.cpp',........}
                
                # <!ATTLIST machine name CDATA #REQUIRED>
                # <!ATTLIST machine sourcefile CDATA #IMPLIED>
                # <!ATTLIST machine isbios (yes|no) "no">
                # <!ATTLIST machine isdevice (yes|no) "no">
                # <!ATTLIST machine ismechanical (yes|no) "no">
                # <!ATTLIST machine runnable (yes|no) "yes">
                # <!ATTLIST machine cloneof CDATA #IMPLIED>
                # <!ATTLIST machine romof CDATA #IMPLIED>
                # <!ATTLIST machine sampleof CDATA #IMPLIED>
                
                #if elem.attrib["name"]=="kof97" :
                if( "name" in elem.attrib ):
                    
                    count += 1
                    if count % 1000 == 0:
                        print(str(count) + ":" + game_name)
                        
                    game_name = elem.attrib["name"]
                    
                    temp_dict = {} # 初始化
                    temp_dict_delete = {}
                    
                    temp_dict = elem.attrib

                    # rom 、chd 、saple 数字，
                    # 仅记录有没有
                    # 没有考虑 merged 标签  
                    
                    number_rom_nodump  = 0
                    number_rom_baddump = 0
                    number_rom_good    = 0
                    
                    number_chd_nodump  = 0
                    number_chd_baddump = 0
                    number_chd_good    = 0
                    
                    number_sample = 0
                    
                    number_softwarelist = 0
                    
                    # 多项
                    temp_dict_delete["chip cpu"]=[]
                    temp_dict_delete["chip audio"]=[]
                    temp_dict_delete["input control"]=[]
                    temp_dict_delete["softwarelist"]=[]
                    
                    
                    for child in elem:
                    
                        if   child.tag=="description" :
                            temp_dict["description"] = child.text
                            
                        elif child.tag=="year" :
                            temp_dict["year"] = child.text
                            
                        elif child.tag=="manufacturer" :
                            temp_dict["manufacturer"] = child.text
                        
                        #elif   child.tag=="biosset" :
                        elif   child.tag=="rom" :
                            if "status" in child.attrib:
                                if   child.attrib["status"] =="nodump":number_rom_nodump  += 1
                                elif child.attrib["status"] =="baddump":number_rom_baddump +=1
                                elif child.attrib["status"] =="good":number_rom_good +=1

                        
                        # chd
                        # <!ATTLIST disk status (baddump|nodump|good) "good">
                        # 查 nodump 
                        # set_data["chd_set"] = set()
                        elif child.tag=="disk" :
                            if "status" in child.attrib:
                                if   child.attrib["status"] =="nodump":number_chd_nodump +=1
                                elif child.attrib["status"] =="baddump":number_chd_baddump +=1
                                elif child.attrib["status"] =="good":number_chd_good +=1
                        
                        #elif   child.tag=="device_ref" :
                        
                        
                        elif child.tag=="sample" :
                            number_sample += 1
                        
                        
                        elif   child.tag=="chip" :
                            if "type" in child.attrib:
                                if "name" in child.attrib:
                                    if child.attrib["type"] == "cpu":
                                        temp_dict_delete["chip cpu"].append(child.attrib["name"])
                                    elif child.attrib["type"] == "audio":
                                        temp_dict_delete["chip audio"].append(child.attrib["name"])

                        elif   child.tag=="display" :
                            if "type" in child.attrib:
                                temp_dict_delete["display type"]=child.attrib["type"] 
                            if "refresh" in child.attrib:
                                temp_dict_delete["display refresh"]=child.attrib["refresh"]
                            if "rotate" in child.attrib:
                                temp_dict_delete["display rotate"]=child.attrib["rotate"]
                            if "width" in child.attrib:
                                if "height" in child.attrib:
                                    if "rotate" in child.attrib:
                                        temp_dict_delete["display resolution"]=child.attrib["width"] +'x'+ child.attrib["height"] + r" (" + child.attrib["rotate"] + r" )"
                                    else:
                                        temp_dict_delete["display resolution"]=child.attrib["width"] +'x'+ child.attrib["height"]
                        
                        elif   child.tag=="sound" :
                            if "channels" in child.attrib:
                                temp_dict_delete["sound channels"]=child.attrib["channels"] 
                        #elif   child.tag=="condition" :
                        elif   child.tag=="input" :
                            if "players" in child.attrib:
                                temp_dict_delete["input players"]=child.attrib["players"] 
                            for grand_child in child:
                                if grand_child.tag=="control":
                                    if "type" in grand_child.attrib:
                                        temp_dict_delete["input control"].append(grand_child.attrib["type"])
                        #elif   child.tag=="dipswitch" :
                        #elif   child.tag=="configuration" :
                        #elif   child.tag=="port" :
                        #elif   child.tag=="adjuster" :
                        

                        elif child.tag=="driver" :
                            if "status" in child.attrib:
                                temp_dict["status"] = child.attrib["status"] 
                            if "savestate" in child.attrib:
                                temp_dict["savestate"] = child.attrib["savestate"]

                        #elif   child.tag=="feature" :
                        #elif   child.tag=="device" :
                        #elif   child.tag=="slot" :
                        
                        elif child.tag=="softwarelist" :
                            number_softwarelist += 1
                            if "name" in child.attrib :
                            
                                ####
                                xml_file_name  = child.attrib["name"] + r".xml"
                                xml_file_name  = os.path.join("hash",xml_file_name)
                                temp_dict_delete["softwarelist"].append( xml_file_name )
                                
                        
                        #elif   child.tag=="ramoption" :
                    
                    #   internal_index["rom"]= {"gamelist":[],"children":{},}
                    #if number_rom > 0:
                    #    internal_index["rom"]["gamelist"].append( game_name )
                    if number_chd_good + number_chd_baddump >0:
                        internal_index["chd"]["gamelist"].append( game_name )
                    if number_sample > 0:
                        internal_index["sample"]["gamelist"].append( game_name )
                    if number_softwarelist >0 :
                        internal_index["softwarelist"]["gamelist"].append( game_name )
                    
                    
                    
                    machine_dict[ game_name ] = temp_dict
                    
                    ####
                    temp_dict_delete["number_rom_nodump"]  = number_rom_nodump
                    temp_dict_delete["number_rom_baddump"] = number_rom_baddump
                    temp_dict_delete["number_rom_good"]    = number_rom_good
                    
                    temp_dict_delete["number_chd_nodump"]  = number_chd_nodump
                    temp_dict_delete["number_chd_baddump"] = number_chd_baddump
                    temp_dict_delete["number_chd_good"]    = number_chd_good
                    
                    machine_dict_delete[ game_name ] = temp_dict_delete
                
                    
                elem.clear()
                
    print(count)
    
    print( )
    print( )
    print( "读取 xml 结束")
    
    print( )
    print( "set_data")
    print( "dict_data")
    print("internal_index")
    

    
    for game_name in machine_dict:
        # all_set
        set_data["all_set"].add( game_name )
        if "cloneof" in machine_dict[game_name] : 
            # clone_set
            set_data["clone_set"].add( game_name )
            dict_data["clone_to_parent"][game_name] = machine_dict[game_name]["cloneof"]
        if machine_dict[game_name].get("isbios","")=="yes":
            # bios
            internal_index["bios"]["gamelist"].append( game_name )
        if machine_dict[game_name].get("isdevice","")=="yes":
            # device
            internal_index["device"]["gamelist"].append( game_name )
        if machine_dict[game_name].get("ismechanical","")=="yes":
            # mechanical
            internal_index["mechanical"]["gamelist"].append( game_name )
            
    set_data["parent_set"] = set_data["all_set"]  - set_data["clone_set"]
    
    print()
    print(r'dict_data["parent_to_clone"]')
    for clone_game in dict_data["clone_to_parent"]:
        parent_game = dict_data["clone_to_parent"][clone_game]
        if parent_game not in dict_data["parent_to_clone"]:
            dict_data["parent_to_clone"][parent_game] = []
        dict_data["parent_to_clone"][parent_game].append( clone_game )
        
    print()
    print(r'dict_data["romof"]')
    for game_name in machine_dict:
        if "romof" in machine_dict[game_name]:
            dict_data["romof"][game_name] = machine_dict[game_name]["romof"]
    
    # 翻译的前期准备，先读取原始英文
    # 等以后再翻译
    print()
    print("copy description")
    the_keys = list(machine_dict.keys())
    for x in the_keys :
        try:
            machine_dict[x]["translation"] = machine_dict[x]["description"]
        except:
            pass
    del the_keys
    
    
    #################
    #################
    #################
    
    # 从 machine_dict
    def make_2_level_internal_folders_1( games_range ,the_key ):
    
        temp_dict = {"gamelist":[],"children":{},}
        
        for game_name in games_range:
            if the_key in machine_dict[game_name]:
                group_name = machine_dict[game_name][the_key]
                if group_name not in temp_dict["children"]:
                    # 初始化
                    temp_dict["children"][group_name]={"gamelist":[],} # "children":{},
                temp_dict["children"][group_name]["gamelist"].append( game_name )
        
        return temp_dict

    # 从 machine_dict_delete
    def make_2_level_internal_folders_2( games_range ,the_key ):
    
        temp_dict = {"gamelist":[],"children":{},}
        
        for game_name in games_range:
            if the_key in machine_dict_delete[game_name]:
                group_name = machine_dict_delete[game_name][the_key]
                if group_name not in temp_dict["children"]:
                    # 初始化
                    temp_dict["children"][group_name]={"gamelist":[],} # "children":{},
                temp_dict["children"][group_name]["gamelist"].append( game_name )
        
        return temp_dict
    
    # 从 machine_dict_delete
    # 值 是一个 list
    def make_2_level_internal_folders_2_1( games_range ,the_key ):
    
        temp_dict = {"gamelist":[],"children":{},}
        
        # 找出分组 名
        group_names = []
        for game_name in games_range:
            if the_key in machine_dict_delete[game_name]:
                the_result = machine_dict_delete[game_name][the_key]
                for x in the_result:
                    group_names.append(x)
                    
        # 分组名，去重
        temp = set(group_names)
        group_names = list(temp)
        
        # 初始化
        for group_name in group_names:
            temp_dict["children"][group_name]={"gamelist":[],} # "children":{},
        
        # 赋值
        for game_name in games_range:
            if the_key in machine_dict_delete[game_name]:
                the_result = machine_dict_delete[game_name][the_key]
                for group_name in the_result:
                    temp_dict["children"][group_name]["gamelist"].append( game_name )
        
        return temp_dict        
    
    
    
    the_games = set_data["all_set"] - set(internal_index["device"]["gamelist"])
    the_all   = set_data["all_set"]
    
    # year
    print("year")
    internal_index["year"]= make_2_level_internal_folders_1(the_games,"year") 

    # manufacturer
    print("manufacturer")
    internal_index["manufacturer"]= make_2_level_internal_folders_1(the_games,"manufacturer")
    
    # status 模拟状态
    print("status")
    internal_index["status"] = make_2_level_internal_folders_1(the_games,"status")
    
    # savestate 存盘
    print("savestate")
    internal_index["savestate"] = make_2_level_internal_folders_1(the_games,"savestate")
    
    # sourcefile
    print("sourcefile")
    internal_index["sourcefile"] = make_2_level_internal_folders_1(the_games,"sourcefile")    
    
    ####
    
    print("sound channels") # 单
    internal_index["sound channels"] = make_2_level_internal_folders_2(the_all,"sound channels")
    
    print("chip cpu") # 多
    internal_index["chip cpu"] = make_2_level_internal_folders_2_1(the_all,"chip cpu")
    
    print("chip audio") # 多
    internal_index["chip audio"] = make_2_level_internal_folders_2_1(the_all,"chip audio")
    
    print('input players') # 单
    internal_index["input players"] = make_2_level_internal_folders_2(the_all,"input players")
    
    print('input control') # 多
    internal_index["input control"] = make_2_level_internal_folders_2_1(the_all,"input control")
    
    print('display type') # 单
    print('display refresh') # 单
    print('display rotate') # 单
    print('display resolution') # 单
    internal_index["display type"] = make_2_level_internal_folders_2(the_all,"display type")
    internal_index["display refresh"] = make_2_level_internal_folders_2(the_all,"display refresh")
    internal_index["display rotate"] = make_2_level_internal_folders_2(the_all,"display rotate")
    internal_index["display resolution"] = make_2_level_internal_folders_2(the_all,"display resolution")
    
    print("softwarelist 补全")# 多
    temp = internal_index["softwarelist"]["gamelist"] # 之前已计算过的数据
    internal_index["softwarelist"]= make_2_level_internal_folders_2_1(the_all,"softwarelist")
    internal_index["softwarelist"]["gamelist"] = temp 
    
    # dump (nodump baddump)
    internal_index["dump"] = {"gamelist":[],"children":{},}
    internal_index["dump"]["children"]["nodump"] = {"gamelist":[],}#"children":{},
    internal_index["dump"]["children"]["baddump"] = {"gamelist":[],}#"children":{},
    for game_name in machine_dict_delete:
        if machine_dict_delete[game_name]["number_rom_nodump"] + machine_dict_delete[game_name]["number_chd_nodump"] > 0:
            internal_index["dump"]["children"]["nodump"]["gamelist"].append( game_name )
            
        if machine_dict_delete[game_name]["number_rom_baddump"] + machine_dict_delete[game_name]["number_chd_baddump"] > 0:
            internal_index["dump"]["children"]["baddump"]["gamelist"].append( game_name )
    
    
    # bios 补全
    print("bios 补全")
    # internal_index["bios"]
    #   {"gamelist":[],"children":{},}
 
    # 主版 romof → bios ，副版 romof  → 主版
    
    temp_bios_list = internal_index["bios"]["gamelist"]
    
    def find_bios_relationship():
        # 上层变量
        # temp_bios_list
        # machine_dict
        # set_data["parent_set"]
        # set_data["clone_set"]
    
        #"romof"
        
        temp_dict = {}
        # dict
        #   key     neogeo
        #   value   [kof97,kof98……]
        
        # 先主版本
        for game_name in set_data["parent_set"]:
            if "romof" in machine_dict[game_name]:
                the_key = machine_dict[game_name]["romof"]
                if the_key not in temp_dict:
                    temp_dict[the_key]=[]
                temp_dict[the_key].append( game_name )
        # 然后，克隆版本
        for game_name in set_data["clone_set"]:
            if "romof" in machine_dict[game_name]:
                the_result = machine_dict[game_name]["romof"] # romof ，应该是主版本名
                
                if the_result == machine_dict[game_name]["cloneof"] :# 主版本名
                    parent_name = the_result
                    if "romof" in machine_dict[parent_name]:
                        the_key = machine_dict[parent_name]["romof"]
                        if the_key not in temp_dict:
                            temp_dict[the_key]=[]
                        temp_dict[the_key].append( game_name )
                else:
                    # romof 不是主版本，有这种情况吗？？?
                    # 如果有这种情况，romof 是 bios 吗，就当是吧。
                    the_key = the_result
                    if the_key not in temp_dict:
                        temp_dict[the_key]=[]
                    temp_dict[the_key].append( game_name )
                    
        # 清理 ,list 格式有 重复 的，清理一下
        # 好像不需要清理
        # for x in temp_bios_list:
        #     if x in temp_dict:
        #         temp = set( temp_dict[x] )
        #         temp = list( temp )
        #         temp_dict[x] = temp
                    
        bios_dict = {"gamelist":[],"children":{},}
        
        # 第一层
        bios_dict["gamelist"] = temp_bios_list 
        
        # 第二层
        for x in temp_bios_list:
        
            group_name = x
            
            if group_name not in bios_dict["children"]:
                bios_dict["children"][group_name] = {"gamelist":[],}#"children":{},
            
            if group_name in temp_dict:
                bios_dict["children"][group_name]["gamelist"] = temp_dict[group_name]

        return bios_dict
            
    internal_index["bios"] = find_bios_relationship()
    

    
    
    
    print()
    print( "set_data")
    for x in set_data:
        print(x,end="")
        print("\t",end="")
        print( len( set_data[x] ))
    
    print()
    print( "dict_data")
    for x in dict_data:
        print(x,end="")
        print("\t",end="")
        print( len( dict_data[x] ))  
    print()        
    
    print("internal_index")
    for x in internal_index:
        print(x,end="")
        print("\t",end="")
        print(len(internal_index[x]["gamelist"]) )
        
        for y in internal_index[x]["children"]:
            print("\t",end="")
            print("包含子元素数量",end="")
            print( len(internal_index[x]["children"]) )
            break # 仅显示子元素数量
            
    print()
    
    
    temp_dict={}
    temp_dict["mame_version"] = mame_version
    temp_dict["machine_dict"] = machine_dict
    temp_dict["set_data"] = set_data
    temp_dict["dict_data"] = dict_data
    temp_dict["internal_index"] = internal_index
    
    return temp_dict


if __name__ == "__main__":
    import pickle
    import time
    
    # xml 文件
    xml_file_name = "roms.xml"
    
    data = read_xml( xml_file_name )
    
    print("将结果写入文件")
    
    # 写到 data_1.bin
    # 写到 data_2_gamelist.bin
    f1 = open(r'cache_data_1.bin', 'wb')
    f2 = open(r'cache_data_2_gamelist.bin', 'wb')
    
    pickle.dump( data["machine_dict"] , f2 )
    f2.close()
    
    del data["machine_dict"]
    
    pickle.dump( data , f1 )
    f1.close()

    print("结束")
    
    
    time.sleep(2)
    

