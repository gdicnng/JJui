# a=(0 1 2 3 4 4 4 5 5 5 )
# echo ${a[@]}
# a=(a b c d e ${a[@]} )
# echo ${a[@]}

the_command_string=("" )
# echo ${the_command_string[@]}


# jjui_source\images
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
the_command_string=( ${the_command_string[@]} --windowed  )
# --clean
the_command_string=( ${the_command_string[@]} --clean  )


echo python ${the_command_string[@]} --icon jjui_source/images/for-icon.png   JJui.pyw
python ${the_command_string[@]} --icon jjui_source/images/for-icon.png   JJui.pyw

echo ......

echo python ${the_command_string[@]} --icon jjui_source/images/for-icon-2.png JJui_sl.pyw
python ${the_command_string[@]} --icon jjui_source/images/for-icon-2.png JJui_sl.pyw