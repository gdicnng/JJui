==========================================
版本 2.0 测试
==========================================

列表部件换了
=========================
原来使用的 列表部件，比较慢，换了一个列表部件。因为 sl 列表部分有 十几万，原来的列表本来就慢，估计压力太大，干脆换了。

新增 JJui_sl
===========================
JJui 
	显示 MAME 街机部分列表
	
	主要是换了一个列表部件
	
	翻译文件位置为 ``.jjui\translation.txt``
	
	可以自行添加翻译

JJui_sl 新增
	显示 MAME 非街机部分 software list 软件列表
	
	翻译文件位置为 ``.jjui\translation_sl.txt``
	
	可以自行添加翻译
	
	和街机部分不一样，每一个机种，运行指令都不相同。每一个机种都得单独设置运行参数。



分类文件
=========================

JJui 街机部分，分类文件 ``*.ini`` ，和其它的 MxUI ,MAMEUI 一样的，就是格式需要 utf-8 带 bom 。
	utf-8 有没有 bom 应该都能读取
	
	没有 bom 的话，修改过后，保存的时候，会添一个 bom
	
	MAMEUI 这样的，添加了 bom 以后，它可能不认，你自己去掉 bom 就行了
	
	如果你不想修改分类文件，把它属性设置为只读

JJui 街机部分，新增分类文件 ``*.source_ini`` ，
	格式和之前的一样，
	
	元素为源代码名，比如 cps1.cpp
	
	这样方便把常见的，以源代码分类的类型列出来，
	
	这一类，只能手动编辑，不能在 UI 里编辑


JJui_sl 非街机部分，分类文件 ``*.sl_ini``
	格式和之前的一样
	
	元素 为 xml名称 加 一个(英文)空格 加 rom缩写

JJui_sl 非街机部分，分类文件 ``*.xml_ini``
	格式和之前的一样
	
	元素 xml 名称，这样方显把常见的 xml 选出来
	
	这一类，只能手动编辑，不能在 UI 里编辑


JJui_sl (非街机部分) 运行参数设置
===========================================

::

	.jjui 文件夹里，新建 emu_sl 文件夹。
	在此文件夹里，以 xml名 建立一个文件夹，里面可以有:
		1.txt
		2.txt
		3.txt
		...
		9.txt
	其中 1.txt 保存的指令，用来，鼠标双击时运行游戏，或者 按数字 1 运行游戏。
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
	其中 %mame% ，代表 mame 模拟器
	%xml:software% 代表 xml名称:rom名称
	
	command 后面跟普通指令，普通指令一般有多条
	
	最后 -statename %g/%d_cart 是 nes 存档指令，不然的话，所有游戏存档都放在一个位置乱了

JJui 街机部分，用其它模拟器打开游戏
======================================================

可以定义多个其它模拟器
::

	鼠标双击，用默认的模拟器打开游戏
	
	.jjui\emu\1.txt
	.jjui\emu\2.txt
	.jjui\emu\3.txt
	......
	.jjui\emu\9.txt
	
	按数字键 1 - 9 ，用对应的指令打开游戏


比如用 fba 模拟器，它的位置为 ``d:\temp\fba_029743\fba.exe``

比如把 1.txt 编辑为：
::

	command   d:\temp\fba_029743\fba.exe
	%machine%
	%cwd%     d:\temp\fba_029743
	command   -window

说明:
::

	其中 
	第一条指令是模拟器本身，表示调用 模拟器
	%machine% 为 rom缩写 ，比如 kof97
	%cwd% 为工作目录，一般指定模拟器所在的文件夹
		这一条指定工作目录，不是传给模拟器的指令，
		所以位置无所谓，写在哪一行都行。
	command 后面为普通指令
	command 后面为普通指令
		普通指令可以写很多条
	-window 指令，传给 fba ，fba 的这条指令表示用窗口模式打开游戏

