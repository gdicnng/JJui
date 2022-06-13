# -*- coding: utf_8_sig-*-
import xml.etree.ElementTree


def getinfo( file_name ,game_name):

    text = ''
    flag = False
    count = 0
    try:
        for (event, elem) in xml.etree.ElementTree.iterparse(file_name,events=("start","end") ) :
            if event == 'end': # 找到结束标记
                if elem.tag=="entry":
                    count += 1
                    for child in elem:
                        if child.tag == "systems" :
                            game_names =[]
                            for grandchild in child:
                                game_names.append(grandchild.attrib.get("name",""))
                            if game_name in game_names:
                                flag = True
                                print(game_names)
                                
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


if __name__ == "__main__":
    
    # xml 文件
    xml_file_name = "history.xml"
    
    game_name = "kov"

    
    data = getinfo( xml_file_name,game_name )
    
    if data is not None:
        print(data)
    

