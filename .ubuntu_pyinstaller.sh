the_command_string=("" )
# echo ${the_command_string[@]}

# jjui_source/images
the_command_string=( ${the_command_string[@]} --add-data ./jjui_source/images:jjui_source/images)

# if
# jjui_source/ui_translation
if [ -d ./jjui_source/ui_translation ];then
the_command_string=( ${the_command_string[@]} --add-data ./jjui_source/ui_translation:jjui_source/ui_translation)
fi

# if
# .jjui
if [ -d ./.jjui ];then
the_command_string=( ${the_command_string[@]} --add-data ./.jjui:.jjui )
fi

# if
# folders
if [ -d ./folders ];then
the_command_string=( ${the_command_string[@]} --add-data ./folders:folders )
fi

# --windowed 
# This option is ignored on *NIX systems.
# the_command_string=( ${the_command_string[@]} --windowed  )

# --clean
the_command_string=( ${the_command_string[@]} --clean  )

# ???????
the_command_string=( ${the_command_string[@]} --hidden-import='PIL._tkinter_finder' )


# no option for icon

echo python -m PyInstaller ${the_command_string[@]} JJui.pyw
python -m PyInstaller ${the_command_string[@]} JJui.pyw

echo ......

echo python -m PyInstaller ${the_command_string[@]} JJui_sl.pyw
python -m PyInstaller ${the_command_string[@]} JJui_sl.pyw
