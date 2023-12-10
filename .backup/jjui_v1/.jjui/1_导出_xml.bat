CD /D "%~dp0"

set mame_path=..\mame.exe

%mame_path% -listxml > .\roms.xml
