@echo off

rem python in the path
rem make ico
python .windows_pillow_make_icon__py34py36.py

rem pyinstaller in the path


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
pyinstaller %the_command_string_jjui% JJui.pyw
pyinstaller %the_command_string_jjui_sl% JJui_sl.pyw


