==========================================
JJui_sl 运行参数设置
==========================================

sl 是 softwre list (软件列表) 的缩写。

JJui_sl 用来显示 software list 列表的。

由于，每个 机种 的运行 参数 不同，
所以，
需要先设置一下运行参数，
然后，才能运行。

::

	.jjui 文件夹里，新建 emu_sl 文件夹。
	在此文件夹里，以 xml名（比如 nes） 建立一个文件夹，里面可以有:
		.jjui\emu_sl\nes\1.txt
		.jjui\emu_sl\nes\2.txt
		.jjui\emu_sl\nes\3.txt
		.jjui\emu_sl\nes\...
		.jjui\emu_sl\nes\9.txt
	对于这一类型来说
	其中 1.txt 保存的指令，用来，鼠标双击游戏 或 选中游戏按回车键运行游戏，或者 按数字 1 运行游戏。
	2.txt ，按数字键 2，运行游戏。
	3.txt 到 9.txt ，同上。

比如对于 nes.xml 中的游戏：

``.jjui\emu_sl\nes\1.txt``

::

	%mame%
	command nes
	%xml:software%
	
	command -statename
	command %g/%d_cart

``.jjui\emu_sl\nes\2.txt``
::

	%mame%
	command nespal
	%xml:software%
	
	command -statename
	command %g/%d_cart

简单说明
::

	1.txt 美版 nes 运行游戏的指令。
	2.txt 欧版 nespal 运行游戏的指令。
	
	其中
	
	%mame% ，代表 mame 模拟器。
	
	%xml:software% ， xml名称:rom名称。（这是一个变量，不同的游戏，值不同）
	
	command 后面跟普通指令，普通指令一般有多条
		-statename %g/%d_cart 是 nes 存档指令，不然的话，所有游戏存档都放在一个位置乱了，不同类型的游戏可能不太一样，具体参考 mame 官方说明
		两条指令分开来写，一行写一条
	
	
	命令行指令对比：
		美版游戏机 nes ，运行 nes.xml 中的 smb1 (超级马里奥 世界版)
		mame.exe nes nes:smb1 -statename %g/%d_cart
	命令行指令对比：
		欧版游戏机 nespal ，运行 nes.xml 中的 smb (超级马里奥 欧版)
		mame.exe nespal nes:smb -statename %g/%d_cart


