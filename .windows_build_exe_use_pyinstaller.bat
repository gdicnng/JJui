@echo off
rem python in the path
	rem pillow installed
	rem pyinstaller installed


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
set the_command_string_jjui=%the_command_string% --icon jjui_source\images\for-icon.png
set the_command_string_jjui_sl=%the_command_string% --icon jjui_source\images\for-icon-2.png

echo on

rem pyinstaller
python -m PyInstaller %the_command_string_jjui% JJui.pyw
python -m PyInstaller %the_command_string_jjui_sl% JJui_sl.pyw


rem jjui_source\_log.txt
IF EXIST jjui_source\_log.txt (
	IF EXIST dist (
		copy /Y jjui_source\_log.txt dist\log.txt
		)
	)


