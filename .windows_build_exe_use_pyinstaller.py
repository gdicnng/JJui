import sys,os,subprocess,shutil


python_is_32bit = False
if sys.maxsize==2**31-1:
    python_is_32bit = True

if sys.executable:
    python_path = sys.executable
else:
    python_path = "python"

print(python_path)


command_list = []

command_list.extend(  (python_path ,"-m","PyInstaller")  )

command_list.extend(  ("--distpath" ,"dist")  )

command_list.append("--windowed")
command_list.append("--clean")
command_list.append("--noconfirm")
command_list.append("--noupx")


command_list_jjui   =command_list.copy()
command_list_jjui_sl=command_list.copy()

if python_is_32bit:
    command_list_jjui.extend(     ("--name" ,"JJui_32")  )
    command_list_jjui.extend(     ("--contents-directory" ,"_jjui_32")  )
    
    command_list_jjui_sl.extend(  ("--name" ,"JJui_sl_32")  )
    command_list_jjui_sl.extend(  ("--contents-directory" ,"_jjui_sl_32")  )
    
    
    path_JJui   =os.path.join("dist","JJui_32")
    path_JJui_sl=os.path.join("dist","JJui_sl_32")
else:
    command_list_jjui.extend(     ("--name" ,"JJui")  )
    command_list_jjui.extend(     ("--contents-directory" ,"_jjui")  )
    
    command_list_jjui_sl.extend(  ("--name" ,"JJui_sl")  )
    command_list_jjui_sl.extend(  ("--contents-directory" ,"_jjui_sl")  )
    
    
    path_JJui   =os.path.join("dist","JJui")
    path_JJui_sl=os.path.join("dist","JJui_sl")

command_list_jjui.extend(      ("--icon" ,os.path.join("jjui_source","images","for-icon.png"),)  )
command_list_jjui_sl.extend(   ("--icon" ,os.path.join("jjui_source","images","for-icon-2.png"),)  )

command_list_jjui.append("JJui.pyw")
command_list_jjui_sl.append("JJui_sl.pyw")

print(command_list_jjui)
print(command_list_jjui_sl)

# exe
print()
p1=subprocess.run(command_list_jjui,)
print()
print()
p2=subprocess.run(command_list_jjui_sl,)

######
# copy images files
# jjui_source\images
shutil.copytree( os.path.join("jjui_source","images") , os.path.join(path_JJui,   "jjui_source","images") ,dirs_exist_ok=True )
shutil.copytree( os.path.join("jjui_source","images") , os.path.join(path_JJui_sl,"jjui_source","images") ,dirs_exist_ok=True )

# jjui_source\ui_translation
ui_translation_folder = os.path.join("jjui_source","ui_translation")
if os.path.isdir(ui_translation_folder):
    shutil.copytree( ui_translation_folder, os.path.join(path_JJui,    "jjui_source","ui_translation") ,dirs_exist_ok=True )
    shutil.copytree( ui_translation_folder, os.path.join(path_JJui_sl, "jjui_source","ui_translation") ,dirs_exist_ok=True )

# .jjui
if os.path.isdir(".jjui"):
    shutil.copytree( ".jjui", os.path.join(path_JJui,    ".jjui") , dirs_exist_ok=True )
    shutil.copytree( ".jjui", os.path.join(path_JJui_sl, ".jjui") , dirs_exist_ok=True )

# folders
if os.path.isdir("folders"):
    shutil.copytree( "folders", os.path.join(path_JJui,    "folders") , dirs_exist_ok=True )
    shutil.copytree( "folders", os.path.join(path_JJui_sl, "folders") , dirs_exist_ok=True )

# jjui_source\_log.txt
log_file = os.path.join("jjui_source","_log.txt")
if os.path.isfile(log_file):
    shutil.copyfile(log_file,os.path.join("dist",   "log.txt"))

# LICENSE
if os.path.isfile("LICENSE"):
    shutil.copyfile("LICENSE",os.path.join("dist",   "LICENSE"))

