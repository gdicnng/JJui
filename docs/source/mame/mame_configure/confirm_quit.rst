====================================
退出时确认
====================================

游戏时，按一下 Esc 键，就退出了，可能容易误按。

可以把 confirm_quit（退出时确认）这个选项打开来。

这样游戏时，按一下 Esc 键，会有一个菜单，再按回车键确认退出。
	
	.. image:: images/confirm_quit.png

图形界面修改的话
	
	在进入游戏之前 的 游戏列表界面，选项中，找一找，找到这个选项 【退出时确认 Confirm quit from emulation 】，改一下就行了。

手动编辑配置文件的话
	
	mame.ini 配置文件中的 confirm_quit 这一项
		
		原来为::
			
			confirm_quit              0
		
		改为::
			
			confirm_quit              1