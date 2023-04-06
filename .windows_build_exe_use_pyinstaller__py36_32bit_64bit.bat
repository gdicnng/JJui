@echo off

rem py.exe in the path
	rem py -3.6    ,py -3.6-64 "-64"not work before 3.7 
	rem py -3.6-32 ,
	
	rem pillow installed
	rem pyinstaller installed


rem make ico
rem 	delete old  .ico
IF EXIST jjui.ico del jjui.ico
IF EXIST jjui_sl.ico del jjui_sl.ico
rem make ico
py -3.6 .windows_pillow_make_icon__py36.py



rem jjui_source\images
set the_command_string=--add-data jjui_source\images;jjui_source\images

rem jjui_source\ui_translation
IF EXIST jjui_source\ui_translation (
	set the_command_string=--add-data jjui_source\ui_translation;jjui_source\ui_translation %the_command_string%
	)

rem .jjui
IF EXIST .jjui (
	set the_command_string=--add-data .jjui;.jjui %the_command_string%
	)

rem folders
IF EXIST folders (
	set the_command_string=--add-data folders;folders %the_command_string%
	)

rem windowed
set the_command_string=--windowed %the_command_string%
rem others
set the_command_string=--clean %the_command_string%

rem icon 
IF EXIST jjui.ico (
	set the_command_string_jjui=%the_command_string% --icon jjui.ico
	) else (
	set the_command_string_jjui=%the_command_string%
	)
IF EXIST jjui_sl.ico (
	set the_command_string_jjui_sl=%the_command_string% --icon jjui_sl.ico
	) else (
	set the_command_string_jjui_sl=%the_command_string%
	)

echo on

rem pyinstaller
rem 64
py -3.6    -m PyInstaller %the_command_string_jjui%    --distpath dist\python36_64bit JJui.pyw
py -3.6    -m PyInstaller %the_command_string_jjui_sl% --distpath dist\python36_64bit JJui_sl.pyw
rem 32
py -3.6-32 -m PyInstaller %the_command_string_jjui%    --distpath dist\python36_32bit JJui.pyw
py -3.6-32 -m PyInstaller %the_command_string_jjui_sl% --distpath dist\python36_32bit JJui_sl.pyw

rem delete
IF EXIST jjui.ico del jjui.ico
IF EXIST jjui_sl.ico del jjui_sl.ico

rem jjui_source\_log.txt
IF EXIST jjui_source\_log.txt (
	IF EXIST dist (
		copy /Y jjui_source\_log.txt dist\log.txt
		)
	)