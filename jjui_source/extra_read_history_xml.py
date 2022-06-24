# -*- coding: utf_8_sig-*-
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

def getinfo_mame_by_index( file_name ,game_name,the_index=0):
    
    with open(file_name,mode="rb") as f:
        
        try:
            f.seek(the_index)
        except:
            return
        
        text = ''
        flag = False
        count = 0
        try:
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
                                
                        break
                    
                    elem.clear()
        except:
            pass
        print(count)
        if flag:return text
        else: return None

def getinfo_sl_by_index( file_name ,sl_id,the_index=0):
    
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
    

