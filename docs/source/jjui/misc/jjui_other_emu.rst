==========================================
JJui 用其它模拟器打开游戏
==========================================

可以定义多个其它模拟器
::

	鼠标双击，用默认的模拟器打开游戏
	
	.jjui\emu\1.txt
	.jjui\emu\2.txt
	.jjui\emu\3.txt
	......
	.jjui\emu\9.txt
	
	按数字键 1 - 9 ，用对应的指令打开游戏

fba 模拟器
======================
比如用 fba 模拟器，它的位置为 ``d:\temp\fba_029743\fba.exe``

比如把 1.txt 编辑为：
::

	command   d:\temp\fba_029743\fba.exe
	%machine%
	%cwd%     d:\temp\fba_029743
	command   -window

命令行指令对比:
::

	首先，打开命令行，进入 fba.exe 所在文件夹，( 下面的 %cwd% 的功能 )
	然后，运行 游戏 knights
	
	windows 的 cmd 命令行 指令：
		cd /d d:\temp\fba_029743
		fba.exe knights -window
	windows 的 powershell 命令行 指令：
		cd d:\temp\fba_029743
		.\fba.exe knights -window


说明:
::

	其中 
	command 后面为普通指令
		普通指令可以写很多条,写在什么位置依命令行 顺序 来
		第一条指令是模拟器本身，用模拟器的路径，表示调用 模拟器
	%machine% 为 游戏名的英文缩写 ，比如 kof97
	%cwd% 为工作目录，一般指定模拟器所在的文件夹
		这一条指定工作目录，不是传给模拟器的指令，
		所以位置无所谓，写在哪一行都行。
	command 后面为普通指令
		普通指令可以写很多条
		普通指令可以写很多条,写在什么位置依命令行 顺序 来
		-window 指令，( fba 的这条指令表示用窗口模式打开游戏 )


mameplus 模拟器
=============================
比如把 2.txt 编辑为：
::

	command d:\temp\mameplus_bin_x86-0.138r4674-20100518\mamep.exe
	%machine%
	%cwd%     d:\temp\mameplus_bin_x86-0.138r4674-20100518

说明:
::

	其中 
	command 后面为普通指令
		第一条指令是模拟器本身
	%machine% 为 游戏名英文缩写 ，比如 kof97
	%cwd% 为工作目录，一般指定模拟器所在的文件夹
		这一条指定工作目录，不是传给模拟器的指令，
		所以位置无所谓，写在哪一行都行。
	
	命令行对比：
	  首先，打开命令行，进入 mamep.exe 所在文件夹，( 上面的 %cwd% 的功能 )
	  然后，运行 游戏 knights
		windows 的 cmd 命令行：
				cd /d "d:\temp\mameplus_bin_x86-0.138r4674-20100518"
				mamep.exe knights
		或者：
		windows 的 powershell 命令行：
				cd 'd:\temp\mameplus_bin_x86-0.138r4674-20100518'
				.\mamep.exe knights


mame 模拟器 本身
==============================

正常来说，使用默认的模拟器打开游戏，
直接鼠标双击 或者 选中游戏后按回车键，进入游戏即可。
没有必要另外整一个。

但如果一个游戏有多种选项，
不想老是去 修改 设置，
也可以调用 默认的 模拟器。

比如 拳皇97，可以切换 多个 BIOS ；还可以使用 家用机 aes 运行 kof97 。

以下，使用 家用机 aes 打开 kof97 。

::
	
	mame 0.162 以上，合并了 mess ，添加了很多 非街机 机种。
	很常见的 neogeo 一类的 街机，它的 家用机 为 aes 。
		包含：拳皇94-2003 、合金弹头 1-5,x 、侍魂、……

以 街机模式 运行 kof97: 
	
	mame.exe kof97

以 家用机模式 运行 kof97: 
	
	mame.exe aes kof97

比如把 3.txt 编辑为：
::

	%mame%
	command   aes
	%machine%
	command -statename 
	command %g/%d_cart

说明:
::

	仅用于 neogeo 其中的一些游戏，既可以普通街机运行，也可以在 家用机 aes 中运行。
	%mame% 表示 mame 模拟器 本身，从 JJui 设置里读取
	command 后面为普通指令
		此处为 aes
	%machine% 为 游戏名的英文缩写 ，比如 kof97
	( %cwd% 工作目录，不需要指定了，使用 JJui 里的设置 )
	command 后面为普通指令
		statename %g/%d_cart 是 存档指令，不然的话，所有游戏存档都放在一个位置乱了，不同类型的游戏可能不太一样，具体参考 mame 官方说明
		两条指令分开来写

其它
=============
略 ……