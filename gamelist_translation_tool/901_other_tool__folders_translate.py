# -*- coding: utf_8_sig-*-
import os

from source_py_some_scripts import misc
from source_py_some_scripts import the_first_part

folder_path_old = "folders_old"
folder_path_new = "folders"
english_chinese_folder = "folders_resources_for_translation"
log_file_for_not_translate = "out_folders_not_translate.txt"

if os.path.isfile(folder_path_new):
    os.remove(folder_path_new)
if not os.path.isdir(folder_path_new):
    os.makedirs(folder_path_new)


def get_files_old(folder_path):
    if not os.path.isdir(folder_path):
        return []
    
    file_list = []

    dirpath, dirnames, filenames=next( os.walk(folder_path) )

    for file_name in filenames:
        if file_name.lower().endswith(".ini"):
            file_list.append(file_name)

    return file_list




# english chinese dict
english_chinese_dict = dict()
the_txt_file_list = misc.search_txt_files_in_a_folder( english_chinese_folder )
for a_txt_file in the_txt_file_list:
    print()
    try:temp=os.path.relpath(a_txt_file)
    except:temp=a_txt_file
    print("\t",temp)
    temp = misc.read_english_chinese_file_for_folders_translation( a_txt_file )
    english_chinese_dict.update( temp )
del the_txt_file_list

english_not_translated=[]
def translate(line):
    English = the_first_part.main(line)
    english = English.lower()
    if english in english_chinese_dict:
        chinese = english_chinese_dict[english]
        return chinese
    else:
        english_not_translated.append(English)
        return line

file_list = get_files_old(folder_path_old)
for file_name in file_list:
    old_file_path = os.path.join(folder_path_old,file_name)
    new_file_path = os.path.join(folder_path_new,file_name)

    lines_old=[]
    with open(old_file_path,mode="rt",encoding="utf_8_sig") as f:
        lines_old = f.readlines()

    with open(new_file_path,mode="wt",encoding="utf_8") as f:
        for line in lines_old:
            line_content = line.strip()

            # 翻译
            if line_content.startswith(r"["):
                if line_content.endswith(r"]"):
                    
                    # 去头 去尾
                    line_content = line_content[1:-1] 

                    # FOLDER_SETTINGS 不用译
                    # ROOT_FOLDER 不用译
                    if line_content.strip().lower() not in [
                            "FOLDER_SETTINGS".lower(),
                            "ROOT_FOLDER".lower(),
                            ]:
                        
                        translate_content = translate(line_content)
                        if translate_content != line_content:
                            
                                line = r"[" + translate_content + r"]" + "\n"

            f.write(line)

# 未翻译的
temp_set =set()
with open(log_file_for_not_translate,mode="wt",encoding="utf_8_sig") as f:
    for english in english_not_translated:
        if english not in temp_set:
            temp_set.add(english)
            f.write(english)
            f.write("\n")