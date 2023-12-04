@echo off
	rem python in the path
		rem pillow installed
		rem pyinstaller installed
			rem pyinstaller >= 6.0.0




rem jjui_source\images
rem set the_command_string=--add-data jjui_source\images;jjui_source\images

rem jjui_source\ui_translation
rem IF EXIST jjui_source\ui_translation (
rem 	set the_command_string=--add-data jjui_source\ui_translation;jjui_source\ui_translation %the_command_string%
rem 	)

rem .jjui
rem IF EXIST .jjui (
rem 	set the_command_string=--add-data .jjui;.jjui %the_command_string%
rem 	)

rem folders
rem IF EXIST folders (
rem 	set the_command_string=--add-data folders;folders %the_command_string%
rem 	)


rem --distpath DIR:Where to put the bundled app (default: ./dist)
set the_command_string=--distpath dist
rem windowed
set the_command_string=--windowed %the_command_string%
rem others
set the_command_string=--clean %the_command_string%




rem icon 
set the_command_string_jjui=%the_command_string% --icon jjui_source\images\for-icon.png
set the_command_string_jjui_sl=%the_command_string% --icon jjui_source\images\for-icon-2.png

rem --contents-directory CONTENTS_DIRECTORY
set the_command_string_jjui=%the_command_string_jjui% --contents-directory _jjui
set the_command_string_jjui_sl=%the_command_string_jjui_sl% --contents-directory _jjui_sl

echo on

rem pyinstaller
python -m PyInstaller %the_command_string_jjui% JJui.pyw
python -m PyInstaller %the_command_string_jjui_sl% JJui_sl.pyw

rem copy files
set path_JJui=dist\JJui
set path_JJui_sl=dist\JJui_sl

rem important files
rem jjui_source\images
xcopy jjui_source\images %path_JJui%\jjui_source\images /E /H /C /I
xcopy jjui_source\images %path_JJui_sl%\jjui_source\images /E /H /C /I

rem jjui_source\ui_translation
IF EXIST jjui_source\ui_translation (
	xcopy jjui_source\ui_translation %path_JJui%\jjui_source\ui_translation /E /H /C /I
	xcopy jjui_source\ui_translation %path_JJui_sl%\jjui_source\ui_translation /E /H /C /I
)

rem .jjui
IF EXIST .jjui (
	xcopy .jjui %path_JJui%\.jjui /E /H /C /I
	xcopy .jjui %path_JJui_sl%\.jjui /E /H /C /I
)

rem folders
IF EXIST folders (
	xcopy folders %path_JJui%\folders /E /H /C /I
	xcopy folders %path_JJui_sl%\folders /E /H /C /I
)


rem jjui_source\_log.txt
IF EXIST jjui_source\_log.txt (
	IF EXIST dist (
		copy /Y jjui_source\_log.txt dist\log.txt
		)
	)

rem LICENSE
IF EXIST LICENSE (
	IF EXIST dist (
		copy /Y LICENSE dist\LICENSE
		)
	)
