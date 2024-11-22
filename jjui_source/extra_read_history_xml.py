# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree

"""
    规则
    https://www.arcade-history.com
    
    Information for the mainlist entries:
    
    <entry>
     <systems>
      <system name="rom_name">
      <system name="rom_name2">
      <system name="rom_name3">
     </systems>
     <text>information to show</text>
    </entry>
    
    
    
    Information for the softlist entries:
    
    <entry>
     <software>
      <item list="softlist_name" name="rom_name">
      <item list="softlist_name" name="rom_name2">
      <item list="softlist_name2" name="rom_name">
     </software>
     <text>information to show</text>
    </entry>
    
    
    
    
    Special case (when an entry appears in both softlist & mainlist):
    
    <entry>
     <systems>
      <system name="rom_name">
     </systems>
     <software>
      <item list="softlist_name" name="rom_name">
     </software>
     <text>information to show</text>
    </entry>

"""

######################
######################
######################
# 读取一个

def getinfo_mame( file_name ,game_name):

    text = ''
    flag = False
    count = 0
    try:
        for (event, elem) in xml.etree.ElementTree.iterparse(file_name,events=("end",) ) :
            #if event == 'end': # 找到结束标记
            if elem.tag=="entry":
                count += 1
                for child in elem:
                    if child.tag == "systems" :
                        for grandchild in child:
                            if grandchild.attrib["name"] == game_name :
                                flag = True
                                print("found")
                                print(count)
                                print(game_name)
                            
                if flag:
                    for child in elem:
                        if child.tag == "text" :
                            try:
                                text = child.text
                            except:
                                pass
                            
                    break
                
                elem.clear()
    except:
        pass
    print(count)
    if flag:return text
    else: return None

def getinfo_sl( file_name ,sl_id):
    
    
    xml_name,game_name = sl_id.split(sep=" ",maxsplit=1)
    
    text = ''
    flag = False
    count = 0
    try:
        for (event, elem) in xml.etree.ElementTree.iterparse(file_name,events=("end",) ) :
            #if event == 'end': # 找到结束标记
            if elem.tag=="entry":
                count += 1
                for child in elem:
                    if child.tag == "software" :
                        for grandchild in child:
                            if grandchild.attrib["list"] == xml_name :
                                if grandchild.attrib["name"] == game_name :
                                    flag = True
                                    print("found")
                                    print(count)
                                    print(sl_id)
                            
                if flag:
                    for child in elem:
                        if child.tag == "text" :
                            try:
                                text = child.text
                            except:
                                pass
                            
                    break
                
                elem.clear()
    except:
        pass
    print(count)
    if flag:return text
    else: return None

def getinfo( file_name ,item_id ,the_type="mame"):
    if the_type=="mame":
        return getinfo_mame(file_name,item_id)
    elif the_type=="softwarelist":
        return getinfo_sl( file_name ,item_id)

###########################################
###########################################
###########################################
###########################################
# 根据目录，读取一个

# xml.etree.ElementTree.iterparse
#   bug,memroy leak ,python 3.6
# 此方法 python 3.6.8 可能是内存泄露，显示次数越多，内存越涨
# python 3.7 没问题
# python 3.8 没问题
def getinfo_mame_by_index_1( file_name ,game_name,the_index=0):
    
    with open(file_name,mode="rb") as f:
        
        try:
            f.seek(the_index)
        except:
            print("seek error")
            return
        
        text = ''
        flag = False
        count = 0
        #try:
        for (event, elem) in xml.etree.ElementTree.iterparse(f,events=("end",) ) :
            
            if count>1 : break
            
            #if event == 'end': # 找到结束标记
            if elem.tag=="entry":
                count += 1
                for child in elem:
                    if child.tag == "systems" :
                        for grandchild in child:
                            if grandchild.attrib["name"] == game_name :
                                flag = True
                                print("found")
                                print(count)
                                print(game_name)
                            
                if flag:
                    for child in elem:
                        if child.tag == "text" :
                            try:
                                text = child.text
                            except:
                                pass
                            elem.clear()
                    break
                
                elem.clear()
        #except:
        #    pass
        print(count)
        if flag:
            print(type(text))
            return text
        else: return None


# 用于下面的函数中
class The_Target(xml.etree.ElementTree.TreeBuilder):
    
    def __init__(self,):
        
        self.the_found_elem = None
        self.the_count_number = 0
        
        super().__init__()
    
    def end(self, tag):
        
        result = super().end(tag)
        
        if tag == "entry":
            self.the_count_number += 1
            self.the_found_elem   = result
        
        return result

# 因为 python 3.6 的 bug ，重写一个函数，换一个方式
def getinfo_mame_by_index_2( file_name ,game_name,the_index=0):
    
    with open(file_name,mode="rb") as f:
        
        try:
            f.seek(the_index)
        except:
            print("seek error")
            return
        
        text = ''
        flag = False
            
        target=The_Target()
        parser = xml.etree.ElementTree.XMLParser(target=target)
        
        line = f.readline()
        
        while line:
            if target.the_count_number >= 1:
                #print("break")
                break
            parser.feed(line)
            line = f.readline()
            
        elem = target.the_found_elem
        
        if elem is not None:
            for child in elem:
                if child.tag == "systems" :
                    for grandchild in child:
                        if grandchild.attrib["name"] == game_name :
                            flag = True
                            print("found")
                            print(game_name)
                        
            if flag:
                for child in elem:
                    if child.tag == "text" :
                        try:
                            text = child.text
                        except:
                            pass
                        elem.clear()
        
        if flag:
            #print(type(text))
            return text
        else: return None

if sys.version_info < (3, 7):
    #print("python 3.6 or less")
    getinfo_mame_by_index = getinfo_mame_by_index_2
else:
    #print("python 3.7 or higher")
    getinfo_mame_by_index = getinfo_mame_by_index_1


######################
# sl

# xml.etree.ElementTree.iterparse
#   bug ,memroy leak ,python 3.6
def getinfo_sl_by_index_1( file_name ,sl_id,the_index=0):
    
    xml_name,game_name = sl_id.split(sep=" ",maxsplit=1)
    
    with open(file_name,mode="rb") as f:
        
        try:
            f.seek(the_index)
        except:
            pass
        
        text = ''
        flag = False
        count = 0
        
        try:
            for (event, elem) in xml.etree.ElementTree.iterparse(f,events=("end",) ) :
                
                if count > 1 : break
                
                #if event == 'end': # 找到结束标记
                if elem.tag=="entry":
                    count += 1
                    for child in elem:
                        if child.tag == "software" :
                            for grandchild in child:
                                if grandchild.attrib["list"] == xml_name :
                                    if grandchild.attrib["name"] == game_name :
                                        flag = True
                                        print("found")
                                        print(count)
                                        print(sl_id)
                                
                    if flag:
                        for child in elem:
                            if child.tag == "text" :
                                try:
                                    text = child.text
                                except:
                                    pass
                                
                        break
                    
                    elem.clear()
        except:
            pass
        print(count)
        if flag:return text
        else: return None

# 因为 python 3.6 的 bug ，重写一个函数，换一个方式
def getinfo_sl_by_index_2( file_name ,sl_id,the_index=0):
    
    
    xml_name,game_name = sl_id.split(sep=" ",maxsplit=1)
    
    with open(file_name,mode="rb") as f:
        
        try:
            f.seek(the_index)
        except:
            print("seek error")
            return
        
        text = ''
        flag = False
            
        target=The_Target()
        parser = xml.etree.ElementTree.XMLParser(target=target)
        
        line = f.readline()
        
        while line:
            if target.the_count_number >= 1:
                #print("break")
                break
            parser.feed(line)
            line = f.readline()
            
        elem = target.the_found_elem
        
        if elem is not None:
            for child in elem:
                if child.tag == "software" :
                    for grandchild in child:
                        if grandchild.attrib["list"] == xml_name :
                            if grandchild.attrib["name"] == game_name :
                                flag = True
                                print("found")
                                print(sl_id)
                        
            if flag:
                for child in elem:
                    if child.tag == "text" :
                        try:
                            text = child.text
                        except:
                            pass
                        elem.clear()
        
        if flag:
            #print(type(text))
            return text
        else: return None


if sys.version_info < (3, 7):
    #print("python 3.6 or less")
    getinfo_sl_by_index = getinfo_sl_by_index_2
else:
    #print("python 3.7 or higher")
    getinfo_sl_by_index = getinfo_sl_by_index_1


def getinfo_by_index( file_name ,item_id ,the_index=0,the_type="mame"):
    if the_type=="mame":
        return getinfo_mame_by_index(file_name,item_id,the_index)
    elif the_type=="softwarelist":
        return getinfo_sl_by_index( file_name ,item_id,the_index)

#################################
#################################
#################################
# 创建目录
class For_XMLParser:
    
    def __init__(self,file_object):
        
        self.file_object = file_object
        
        self.index_dict_mame ={}
        self.index_dict_sl   ={}
        
        self.temp_item_list_mame = []
        self.temp_itme_list_sl = []
        
        self.start_position = 0
    
    def start(self, tag, attrib):
        if tag =="system":
            if "name" in attrib:
                self.temp_item_list_mame.append(attrib["name"])
        elif tag =="item":
            if "list" in attrib:
                if "name" in attrib:
                    self.temp_itme_list_sl.append( attrib["list"] + " " +attrib["name"] )
    
    def end(self, tag):
        if tag=="entry":
            for name in self.temp_item_list_mame:
                self.index_dict_mame[name] = self.start_position
            
            for sl_id  in self.temp_itme_list_sl:
                self.index_dict_sl[sl_id] = self.start_position
            
            self.temp_item_list_mame.clear()
            self.temp_itme_list_sl.clear()
            
            self.start_position = self.file_object.tell()
    
    def data(self, data):
        pass
    
    def close(self):
        return self.index_dict_mame,self.index_dict_sl

def get_index_both( file_name ):
    
    with  open(file_name,mode="rb",) as f:
        
        target=For_XMLParser(f)
        
        parser = xml.etree.ElementTree.XMLParser(target=target)
        
        line = f.readline()
        while line:
            parser.feed(line)
            line = f.readline()
        
        # 按字节读，太慢了点
        #a_byte = f.read(1)
        #while a_byte:
        #    parser.feed(a_byte)
        #    a_byte = f.read(1)
        
        
        index_dict_mame,index_dict_sl = parser.close()
        
        return index_dict_mame,index_dict_sl

def get_index(file_name,the_type="mame"):
    index_dict_mame,index_dict_sl = get_index_both(file_name)
    
    if the_type=="mame":
        return index_dict_mame
    elif the_type=="softwarelist":
        return index_dict_sl




if __name__ == "__main__":
    
    # xml 文件
    xml_file_name = "history.xml"
    
    game_name = "kov"

    
    data = getinfo( xml_file_name,game_name )
    
    if data is not None:
        print(data)
    

