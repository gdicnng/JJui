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
	在此文件夹里，以 hash 文件夹中的 *.xml 的文件名 建立一个文件夹，
	比如 nes.xml 就用 nes 作为文件夹 名称，里面可以有:
		.jjui\emu_sl\nes\1.txt
		.jjui\emu_sl\nes\2.txt
		.jjui\emu_sl\nes\3.txt
		.jjui\emu_sl\nes\...
		.jjui\emu_sl\nes\9.txt
		.jjui\emu_sl\nes\0.txt
	对于这一类型来说
	其中 1.txt 保存的指令，用来，鼠标双击游戏 或 选中游戏按回车键运行游戏，或者 按数字 1 运行游戏。
	2.txt ，按数字键 2，运行游戏。
	3.txt ，按数字键 3，运行游戏。
	……
	……

比如对于 nes.xml 中的游戏：

``.jjui\emu_sl\nes\1.txt``

::

	%mame%
	command nes
	command -cart
	%xml:software%
	
	command -statename
	command %g/%d_cart

``.jjui\emu_sl\nes\2.txt``
::

	%mame%
	command nespal
	command -cart
	%xml:software%
	
	command -statename
	command %g/%d_cart

简单说明
	
	1.txt 是美版 游戏机 nes 运行游戏的指令。
	
	2.txt 是欧版 游戏机 nespal 运行游戏的指令。
	
	其中
	
	%mame% ，代表 mame 模拟器。
	
	%xml:software% ， xml名称:rom名称。（这是一个变量，不同的游戏，值不同，比如 nes:smb1）
	
	command 后面跟普通指令，普通指令一般有多条
		
		-statename %g/%d_cart 是 nes 存档指令，
			
			| -statename %g/%d_cart
			| 是一组指令，但有两条指令
			| 分开来，写两行
			| -statename 写一行
			| %g/%d_cart 写一行
			
			| 默认的话，所有 nes 游戏存档都放在一个位置，nes 有几千个游戏，太乱了
			| nes 以外，其它的游戏机，不同类型的游戏可能不太一样，但大致有几大类，具体参考 mame 官方说明
	
	| 命令行指令对比：
	|   美版游戏机 nes ，运行 nes.xml 中的 smb1 (超级马里奥 世界版)
	|   mame.exe nes -cart nes:smb1 -statename %g/%d_cart
	| 命令行指令对比：
	|   欧版游戏机 nespal ，运行 nes.xml 中的 smb (超级马里奥 欧版)
	|   mame.exe nespal -cart nes:smb -statename %g/%d_cart
	
	| 命令行解释一下
	| mame.exe nes -cart nes:smb1 -statename %g/%d_cart
	| 	mame.exe 模拟器程序
	| 	nes 表示 游戏机 nes
	| 	-cart 表示 游戏卡带 类型，和 游戏卡带类型 有关，不同情况下，值不同
	| 	nes:smb1 ，写的比较详细，表示 nes.xml 中 的 游戏 smb1
	| 	-statename %g/%d_cart ，存档位置，
	| 		%g 表示游戏机种名称，此处就是指 游戏机 nes
	| 		%d_cart 游戏名称，和 游戏卡带类型 有关，不同情况下，值不同
	| 		这时 用 Shift + F7 存档功能的话，会在 存档文件中，建一个 nes 文件夹，其中再建一个 smb1 文件夹，然后存档文件放入其中。
	| 		具体可以去 MAME 官方网站上查看一下 statename 这个选项的说明。
	| mame.exe nes -cart nes:smb1 -statename %g/%d_cart
	| 这样的指令写得比较详细
	| 如果不考虑存档位置的话，指令短一点看起来方便：
	| 	mame.exe nes -cart nes:smb1
	| 	甚至
	| 	mame.exe nes -cart smb1
	| 	mame.exe nes nes:smb1
	| 	mame.exe nes smb1
	| 	0.255版本中试过，都能运行游戏
	| 	如果是其它 游戏机
	| 	如果有多种游戏卡带类型的，省略类型，就可能表达不准确
	| 	如果能同时使用多个xml文件中记录的游戏，省略xml种类，就可能表达不准确

参数
::
	
	%mame% ，jjui_sl 中 设置的 mame 模拟器 程序
	%xml:software% ，xml名称:游戏名称，比如上面的 nes:smb1
	%xml% ， xml名称
	%software% ，游戏名称
	
	command 普通指令
	
	%cwd% ，工作文件夹，（如果使用 jjui_sl 中 设置的 mame 模拟器 程序，无需额外设置此项）
	

游戏卡带类型
::
	
	1
	命令行 -listmedia 查看
	比如 查看 游戏机 nes 的卡带类型
	mame.exe nes -listmedia
	显示结果：
	SYSTEM           MEDIA NAME       (brief)    IMAGE FILE EXTENSIONS SUPPORTED
	---------------- --------------------------- -------------------------------
	nes              cartridge        (cart)     .nes  .unf  .unif
	上面这种显示了一种 cartridge （缩写 cart），比较好区分。
	如果显示多种的，就比较麻烦了。
	
	2
	打开 xml 文件查看
	比如 打开 nes.xml 文件查看
	同一个 .xml 文件里的，应该是一个类型的

游戏机 与 .xml 文件
::
	
	software list ，子列表，其中记录的游戏，是 显示在 JJui_sl 中的。
	然而，游戏机的列表 却是和 街机列表 在一起，显示在 JJui 主列表当中的。
	就是说，在 JJui_sl 中能看到 nes 的几千个游戏，但 nes 游戏机本身的信息在 JJui 中查看。
	
	
	打开 JJui ，在 JJui 中查看，有一个分类，software list ，如果游戏机有 software list ，就会在这个分类中。
	
	1，某个.xml 文件，有哪些相关联的游戏机：
	JJui 中，software list 分类中，子分类：比如 nes.xml 分类，可以看到和 nes.xml 有关的游戏机。
	
	2，某个游戏机，有哪些相关联的 .xml 文件
	在 JJui 列表中，找到游戏机，比如 nes 或 gba 等：
	鼠标右键，查看 -listxml 信息，里面的内容比较多、比较杂，其中也会有 software list 信息；
	或者，
	查看 周边 文档，messinfo.dat (文档需要额外下载)，也会显些一些信息，其中有 software list 信息。
	
