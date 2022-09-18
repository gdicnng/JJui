# -*- coding: utf_8_sig-*-
import xml.etree.ElementTree
import os

# mame_version
def get_mame_version( xml_file_name ):
    print( )
    print( "get mame version")
    
    mame_version = ''
    
    for (event, elem) in xml.etree.ElementTree.iterparse( xml_file_name ,events=("start","end") ) :
        if event == 'start' : # 找到开始标记
            if elem.tag=="mame" : # mame 标签
                if "build" in elem.attrib : # 版本 标签
                    mame_version = elem.attrib["build"]
                break
    if mame_version != '':
        print( "mame_version")
        print( mame_version)
        return mame_version

# machine_dict
# machine_dict_delete
def parse_mame_xml( xml_file_name , mame_type = "mame0162"):
    print( )
    print( "parse mame xml")
    
    machine_dict = {}
        # a dict of dicts
        # a dict , 包含 machine name ，如 kof97 、 kof90 、 knights 等

        # 每一个元素，如 kof97 ，是一个 dict 含：{'name': 'kof97', 'sourcefile': 'neogeo.cpp', 'romof': 'neogeo', 'isbios': 'no', 'isdevice': 'no', 'ismechanical': 'no', 'runnable': 'yes'}    
    print( )
    print( "parsing xml ....")
    
    node="machine"
    if mame_type == "mame0162" : node="machine"
    if mame_type == "mame084"  : node="game"
    
    count = 0
    
    for (event, elem) in xml.etree.ElementTree.iterparse( xml_file_name,
            events=("end",),#"start"
            ) :

        if elem.tag== node : # "machine" or "game"
            
            # elem.attrib 是一个 dict 的类型
            # 直接复制过去，多出来的，之后再处理
            #   比如 kof97 的：
            #   {'name': 'kof97', 'sourcefile': 'neogeo.cpp',........}
            # 有以下内容
            # <!ATTLIST machine name CDATA #REQUIRED>
            # <!ATTLIST machine sourcefile CDATA #IMPLIED>
            # ...
            
            #if elem.attrib["name"]=="kof97" :
            if( "name" in elem.attrib ):
                
                game_name = elem.attrib["name"]
                
                count += 1
                if count % 1000 == 0:
                    print(str(count) + ":" + game_name)
                
                # 个体元素
                temp_dict = {} # 初始化
                
                # 复制 attrib 这一部分
                temp_dict = elem.attrib
                
                
                number_biosset = 0
                # rom 、chd 、saple 数字，
                #   用于 nodump 、 baddump 分类
                #       没有考虑 merged 标签
                number_rom_nodump  = 0
                number_rom_baddump = 0
                number_rom_good    = 0
                
                number_chd_nodump  = 0
                number_chd_baddump = 0
                number_chd_good    = 0
                
                number_sample = 0
                
                # sl
                number_softwarelist = 0
                
                # 多项
                # 多项 初始化
                # 单项的 就直接使用了
                temp_dict["chip cpu"]=[]
                temp_dict["chip audio"]=[]
                temp_dict["input control"]=[]
                temp_dict["softwarelist"]=[]
                
                temp_dict['display number']     =0
                temp_dict['display type']       =[]
                temp_dict['display refresh']    =[]
                temp_dict['display rotate']     =[]
                temp_dict['display resolution'] =[]
                
                for child in elem:
                
                    if   child.tag=="description" :
                        temp_dict["description"] = child.text
                    
                    elif child.tag=="year" :
                        temp_dict["year"] = child.text
                    
                    elif child.tag=="manufacturer" :
                        temp_dict["manufacturer"] = child.text
                    
                    # bios 计数
                    elif   child.tag=="biosset" :
                        number_biosset += 1
                    
                    #   rom number 
                    elif   child.tag=="rom" :
                        if "status" in child.attrib:
                            if   child.attrib["status"] =="nodump":number_rom_nodump  += 1
                            elif child.attrib["status"] =="baddump":number_rom_baddump +=1
                            elif child.attrib["status"] =="good":number_rom_good +=1

                    # chd number
                    elif child.tag=="disk" :
                        if "status" in child.attrib:
                            if   child.attrib["status"] =="nodump":number_chd_nodump +=1
                            elif child.attrib["status"] =="baddump":number_chd_baddump +=1
                            elif child.attrib["status"] =="good":number_chd_good +=1
                    
                    # sample
                    elif child.tag=="sample" :
                        number_sample += 1
                    
                    # "chip"
                    elif   child.tag=="chip" :
                        if "type" in child.attrib:
                            if "name" in child.attrib:
                                if child.attrib["type"] == "cpu":
                                    temp_dict["chip cpu"].append(child.attrib["name"])
                                elif child.attrib["type"] == "audio":
                                    temp_dict["chip audio"].append(child.attrib["name"])
                    # display
                    # 如果有一个 display
                    # 如果有多个呢，？？？？？？？ 就不是这样子了
                    elif   child.tag=="display" :
                        temp_dict['display number'] += 1
                        
                        if "type" in child.attrib:
                            temp_dict["display type"].append( child.attrib["type"] )
                        if "refresh" in child.attrib:
                            temp_dict["display refresh"].append(child.attrib["refresh"])
                        if "rotate" in child.attrib:
                            temp_dict["display rotate"].append(child.attrib["rotate"])
                        if "width" in child.attrib:
                            if "height" in child.attrib:
                                if "rotate" in child.attrib:
                                    temp_dict["display resolution"].append( child.attrib["width"] +'x'+ child.attrib["height"] + r" (" + child.attrib["rotate"] + r")" )
                                else:
                                    temp_dict["display resolution"].append(child.attrib["width"] +'x'+ child.attrib["height"])
                    
                    #<sound channels="2"/>
                    elif   child.tag=="sound" :
                        if "channels" in child.attrib:
                            temp_dict["sound channels"]=child.attrib["channels"] 

                    # input
                    elif   child.tag=="input" :
                        if "players" in child.attrib:
                            temp_dict["input players"]=child.attrib["players"] 
                        for grand_child in child:
                            if grand_child.tag=="control":
                                if "type" in grand_child.attrib:
                                    temp_dict["input control"].append(grand_child.attrib["type"])
                    
                    # driver
                    elif child.tag=="driver" :
                        if "status" in child.attrib:
                            temp_dict["status"] = child.attrib["status"] 
                        if "savestate" in child.attrib:
                            temp_dict["savestate"] = child.attrib["savestate"]

                    elif child.tag=="softwarelist" :
                        number_softwarelist += 1
                        if "name" in child.attrib :
                        
                            ####
                            xml_file_name_sl  = child.attrib["name"] + r".xml"
                            #xml_file_name_sl  = os.path.join("hash",xml_file_name_sl)
                            temp_dict["softwarelist"].append( xml_file_name_sl )
                            
                    

                ##
                temp_dict["number_biosset"]     = number_biosset
                
                temp_dict["number_rom_nodump"]  = number_rom_nodump
                temp_dict["number_rom_baddump"] = number_rom_baddump
                temp_dict["number_rom_good"]    = number_rom_good
                
                temp_dict["number_chd_nodump"]  = number_chd_nodump
                temp_dict["number_chd_baddump"] = number_chd_baddump
                temp_dict["number_chd_good"]    = number_chd_good
                
                temp_dict["number_sample"]      = number_sample
                temp_dict["number_softwarelist"]= number_softwarelist
                
                machine_dict[ game_name ] = temp_dict

            elem.clear()


    print(count)
    return( machine_dict  )

# 大量重复字符串，处理一下
#   相同的字符串，占用了不同的空间，
#   重新赋值一下，可能会 节约 些空间
def about_some_same_strings(machine_dict):
    
    # 游戏名： 
        # 'name' 和 id 应该是一样的
        # 生成 id 时,用 'name' 复制的
    # 'cloneof' ,所有内容，都是 游戏名 id ，重复的
    # 'romof',所有内容，都是 游戏名 id ，重复的
    def func_1(original_data):
        #['name', 'status', 'translation', 'description', 'year', 'sourcefile', 'manufacturer', 'cloneof', 'savestate', 'romof']
        the_key_list = ['cloneof','romof']
        
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
    def func_2(original_data):
        #['name', 'status', 'translation', 'description', 'year', 'sourcefile', 'manufacturer', 'cloneof', 'savestate', 'romof']        
        the_key_list = [ 
                'status',# 重复的特别多
                'year',
                'sourcefile',
                'manufacturer',
                'savestate',# 重复的特别多
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
    
    
    
    if "kof97k" in machine_dict:
        print(machine_dict["kof97k"])
    
    machine_dict = func_1(machine_dict)
    
    if "kof97k" in machine_dict:
        print()
        print(machine_dict["kof97k"])
    
    machine_dict = func_2(machine_dict)
    
    if "kof97k" in machine_dict:
        print()
        print(machine_dict["kof97k"])
    return machine_dict


# set_data = {}
# set_data["all_set"] = set()
# set_data["clone_set"] = set()
# set_data["parent_set"] = set()
def make_set_data(machine_dict):
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
            temp.append( game_name )
    set_data["clone_set"]  = set( temp )
    
    set_data["parent_set"] = set_data["all_set"] - set_data["clone_set"]

    return set_data

# dict_data
# dict_data["clone_to_parent"]
# dict_data["parent_to_clone"]
def make_dict_data(machine_dict):
    print( )
    print( "make dict data")
    
    dict_data = {}

    dict_data["clone_to_parent"] = {}
        # 一对一,子元素为 字符
    dict_data["parent_to_clone"] = {}
        # 一对多，子元素为 字符 组成 的 list or set ?
        # 嗯，改成 set ,方便后面用
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
        
    # parent_to_clone
    # 子元素改成 set
    #for parent_name in dict_data["parent_to_clone"]:
    #    temp = set( dict_data["parent_to_clone"][parent_name] )
    #    dict_data["parent_to_clone"][parent_name] = temp
    return dict_data

#   internal_index
#   改：
#   一部分，分类，用 set 格式
#   一部分，分类，用 list  格式
#   已改 all_set clone_set parent_set
def make_internal_index(machine_dict,set_data,dict_data):
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
    
    
    # 值为 yes 类型的，isbios == yes
    # bios        第一层，有两层，此处设置 第一层
    # device
    # mechanical
    def func_for_index_2( internal_index ):
        internal_index["bios"]          = {"gamelist":[],"children":{},}
        internal_index["device"]        = {"gamelist":[],"children":{},}
        internal_index["mechanical"]    = {"gamelist":[],"children":{},}
        #internal_index["sampleof"]      = {"gamelist":[],"children":{},}
        #
        for game_name,game_info in machine_dict.items():
            if game_info.get("isbios","")=="yes":
                internal_index["bios"      ]["gamelist"].append(game_name)
            if game_info.get("isdevice","")=="yes":
                internal_index["device"    ]["gamelist"].append(game_name)
            if game_info.get("ismechanical","")=="yes":
                internal_index["mechanical"]["gamelist"].append(game_name)
    print("index - bios-1 device mechanical")
    func_for_index_2( internal_index )
    
    # bios 第二层 补全
    #   根据 romof 大致分类，不一定十分准确
    #   或者，精确一点，先计算有 bios 的，再分类 ???
    def func_for_index_bios_level_2(internal_index):
        temp_dict = {}
        new_dict  = {}
        
        # internal_index["bios"] = {"gamelist":[],"children":{},}
        bios_dict      = internal_index["bios"]        
        bios_list = internal_index["bios"]["gamelist"]
        
        # dict
        #   key     value
        #   neogeo   [kof97,kof98……]
        
        # romf 倒过来
        # bios - parent_game_name 
        # bios - parent_game_name - clone_game_name
        #    dict_data["parent_to_clone"] ，用这个
        # bios - clone_game_name 有没有这种 ？？,就当有吧
        

        # game_name --> romof_name
        # 倒过来
        # temp_dict[romof_name] = [game_name_1,game_name_2,.....]
        for game_name in set_data["all_set"]:
            if "romof" in machine_dict[game_name]:
                romof_name = machine_dict[game_name]["romof"]
                
                if romof_name not in temp_dict :
                    temp_dict[romof_name]=[]
                temp_dict[romof_name].append(game_name)
        
        # 提取 在 bios 范围 中的
        #   temp_dict[romof_name] = [game_name1,game_name2,.....]
        #       仅提取 romof_name 在 bios 范围 中的
        for bios_set_name in bios_list:
            if bios_set_name in temp_dict:
                new_dict[bios_set_name]=temp_dict[bios_set_name]
        
        # 补充克隆版本
        for bios_set_name in new_dict:
            temp_list = []
            
            # 原始的
            temp_list.extend( new_dict[bios_set_name] )
            
            # 找到克隆版本，补充
            for game_name in new_dict[bios_set_name]:
                if game_name in dict_data["parent_to_clone"] :
                    temp_list.extend( dict_data["parent_to_clone"][game_name] )
            
            # 去重
            temp_list = list( set(temp_list) )
            
            new_dict[bios_set_name] = temp_list

        #{"gamelist":[],"children":{},}
        #{"gamelist":[],"children":{},}
        
        # 第二层
        for bios_set_name in bios_list:
            
            # 初始化 []
            if bios_set_name not in bios_dict["children"]:
                bios_dict["children"][bios_set_name] = {"gamelist":[],}#"children":{},
            
            # 复制数据
            if bios_set_name in new_dict:
                bios_dict["children"][bios_set_name]["gamelist"] = new_dict[bios_set_name]
    
    print("index - bios level 2")
    func_for_index_bios_level_2(internal_index)
    
    # 计数类型的
    # chd
    # sample
    # softwarelist 第一层 *
    def func_for_chd_sample_softwarelist(internal_index):
        # machine_dict
        internal_index["chd"]         = {"gamelist":[],"children":{},}
        internal_index["sample"]      = {"gamelist":[],"children":{},}
        internal_index["softwarelist"]= {"gamelist":[],"children":{},}
        
        temp_chd=[]
        temp_sample=[]
        temp_softwarelist=[]
        
        for game_name,game_info in machine_dict.items():
            # game_info["number_chd_nodump"]  = number_chd_nodump
            if game_info["number_chd_baddump"] or game_info["number_chd_good"]:
                temp_chd.append(game_name)
            if game_info["number_sample"]:
                temp_sample.append(game_name)
            if game_info["number_softwarelist"]:
                temp_softwarelist.append(game_name)
        
        internal_index["chd"         ]["gamelist"] = temp_chd
        internal_index["sample"      ]["gamelist"] = temp_sample
        internal_index["softwarelist"]["gamelist"] = temp_softwarelist
    print("index - chd sample softwarelist-(1)")
    func_for_chd_sample_softwarelist(internal_index)
    
    ####
    print("index - dump")
    # dump
    #   nodump
    #   baddump
    internal_index["dump"] = {"gamelist":[],"children":{},}
    internal_index["dump"]["children"]["nodump"] = {"gamelist":[],}#"children":{},
    internal_index["dump"]["children"]["baddump"] = {"gamelist":[],}#"children":{},
    for game_name,game_info in machine_dict.items():
        # nodump
        if game_info["number_rom_nodump"] or game_info["number_chd_nodump"] :
            internal_index["dump"]["children"]["nodump"]["gamelist"].append( game_name )
        # baddump
        if game_info["number_rom_baddump"] or game_info["number_chd_baddump"] > 0:
            internal_index["dump"]["children"]["baddump"]["gamelist"].append( game_name )


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
    # manufacturer
    print("manufacturer")
    internal_index["manufacturer"]= func_for_index_level_2("manufacturer")
    # status 模拟状态
    print("status")
    internal_index["status"] = func_for_index_level_2("status")
    # savestate 存盘
    print("savestate")
    internal_index["savestate"] = func_for_index_level_2("savestate")
    # sourcefile
    print("sourcefile")
    internal_index["sourcefile"] = func_for_index_level_2("sourcefile")
    print("sound channels") # 单
    internal_index["sound channels"] = func_for_index_level_2("sound channels")

    # 
    # machine_dict[ game_name ][ the_key ] 为一个列表
    def func_for_index_level_2_another( the_key ,temp_dict=None ):
        # machine_dict
        # set_data
        
        games_range = set_data["all_set"]
        
        # 初始化
        if temp_dict==None :
            temp_dict = {"gamelist":[],"children":{},}
        
        # group_name
        # group_name_s
        
        # 找出分组 名
        group_name_s = []
        for game_name in games_range:
            if the_key in machine_dict[game_name]:
                the_result = machine_dict[game_name][the_key]
                for x in the_result:
                    group_name_s.append(x)
                    
        # 分组名，去重
        temp = set(group_name_s)
        group_name_s = list(temp)
        
        # 初始化
        # 每个二级分类，都初始化
        for group_name in group_name_s:
            temp_dict["children"][group_name]={"gamelist":[],} # "children":{},
        
        # 赋值
        for game_name in games_range:
            if the_key in machine_dict[game_name]:
                #the_result = machine_dict[game_name][the_key]
                the_result = set(machine_dict[game_name][the_key])#去重
                for group_name in the_result:
                    temp_dict["children"][group_name]["gamelist"].append( game_name )
        
        return temp_dict
    print("chip cpu") # 多
    internal_index["chip cpu"] = func_for_index_level_2_another("chip cpu",)
    print("chip audio") # 多
    internal_index["chip audio"] = func_for_index_level_2_another("chip audio")
    
    print('input players') # 单
    internal_index["input players"] = func_for_index_level_2("input players")    
    print('input control') # 多
    internal_index["input control"] = func_for_index_level_2_another("input control")
    
    print('display number') # 单
    print('display type') # 多
    print('display refresh') # 多
    print('display rotate') # 多
    print('display resolution') # 多
    
    # 转为 字符串
    for game_info in machine_dict.values():
        if "display number" in game_info:
            temp = game_info["display number"]
            game_info["display number"] = str(temp)

    internal_index["display number"] = func_for_index_level_2("display number")
    internal_index["display type"] = func_for_index_level_2_another("display type")
    internal_index["display refresh"] = func_for_index_level_2_another("display refresh")
    internal_index["display rotate"] = func_for_index_level_2_another("display rotate")
    internal_index["display resolution"] = func_for_index_level_2_another("display resolution")
    
    print("softwarelist - 2")# 多
    temp = internal_index["softwarelist"]["gamelist"] 
        # 备份 之前已计算过的数据
    internal_index["softwarelist"]= func_for_index_level_2_another("softwarelist")
    internal_index["softwarelist"]["gamelist"] = temp
    

    
    return internal_index

# 清理 game list data
def clear_game_list_data(game_list_data):
    machine_dict = {}
    
    
    # "translation"
    the_key_s =  [
                    "name",
                    "year",
                    "sourcefile",
                    "description",
                    "manufacturer",
                    "cloneof",
                    "savestate",
                    "status",
                    #"isbios",
                    #"isdevice",
                    #"ismechanical",
                    "romof",
                    #"runnable",
                    #"softwarelist",
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
    temp=[]
    for x in the_key_s:
        if x in all_keys:
            temp.append(x)
    the_key_s=temp
    
    for game_name,game_info in game_list_data.items():
        machine_dict[game_name]={} # 初始化
        for the_key in the_key_s:
            if the_key in game_info:
                machine_dict[game_name][the_key] = game_info[the_key]
    return machine_dict


# dict_to_list
def dict_to_list(game_list_data):
    print()
    print("\t dict to list")
    # return columns,machine_dict
    
    
    #第一项 "name"         ，id ，高频使用
    #第二项 "status"       ，决定图标颜色，也是高频使用
    the_key_s =  [
                    "name",
                    "status",
                    
                    "translation",
                    "description",
                    
                    "year",
                    "sourcefile",

                    "manufacturer",
                    
                    "cloneof",
                    "savestate",
                    "romof",
                    
                    #"isbios",
                    #"isdevice",
                    #"ismechanical",

                    #"runnable",
                    #"softwarelist",
                    
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
    columns.append("name")
    columns.append("status")
    for x in the_key_s:
        if x in all_keys:
            if x not in ("name","status"):
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


def prepare_for_gamelist_translation(machine_dict):
    for game_name,game_info in machine_dict.items():
        game_info["translation"]=game_info.get("description","")
    return machine_dict




def main(xml_file_name,mame_type="mame0162"):
    
    # version
    mame_version   = get_mame_version(xml_file_name)
    # game list 
    game_list_data = parse_mame_xml(xml_file_name,mame_type)
    
    # 大量重复字符串，处理一下
    game_list_data = about_some_same_strings(game_list_data)
    
    
    # set data ,
    #   all_set parent_set clone_set
    set_data       = make_set_data(game_list_data)
    # dict_data
    #   clone_to_parent parent_to_clone
    dict_data      = make_dict_data(game_list_data)
    # 内置分类
    internal_index = make_internal_index(game_list_data,set_data,dict_data)
    
  #  # 清理 game_list_data 多余的内容
  # 不需要了，之后转为 list
  #  machine_dict = clear_game_list_data(game_list_data)
  
  
    # 翻译准备 ，将原 英文内容复制过去
    machine_dict = prepare_for_gamelist_translation(game_list_data)
    
    
    # 格式，转为 list
    # 第0项："name" ，这个是 id
    # 第2项："status" ，这个决定图标颜色，也是高频使用的
    columns,machine_dict = dict_to_list(machine_dict)

    temp_dict = {}
    temp_dict["mame_version"]   = mame_version
    
    temp_dict["columns"]        = columns
    temp_dict["machine_dict"]   = machine_dict
    
    temp_dict["set_data"]       = set_data
    temp_dict["dict_data"]      = dict_data
    temp_dict["internal_index"] = internal_index
    
    return temp_dict

if __name__ == "__main__":

    # xml 文件
    xml_file_name = "roms.xml"
    #xml_file_name = "roms_0168.xml"    
    #xml_file_name = "roms_0241.xml"    
    
    data = main(xml_file_name)
    
    new_file_name = "cache_data.bin"
    
    import pickle
    with open( new_file_name , 'wb' ) as file:
        pickle.dump( data , file )

