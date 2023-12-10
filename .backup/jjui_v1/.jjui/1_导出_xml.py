# -*- coding: utf_8_sig-*-
import subprocess

def export_xml_from_mame(mame_path,out_put_file_path):
    print()
    
    command_list=[]
    
    command_list.append( mame_path )
    command_list.append( r"-listxml" ) 
    
    print()
    for x in command_list:
        print(x ,end='')
        print(" ",end='')
    print()
    
    file = open(out_put_file_path, 'wb')
    
    subprocess.run( args = command_list , stdout = file )
    
    file.close
    

if __name__ == "__main__":
    
    mame_path = r"..\mame.exe"
    xml_file_name  = r".\roms.xml"
    
    export_xml_from_mame( mame_path , xml_file_name )

