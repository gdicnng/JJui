====================================
cheat 作弊码
====================================

下载作弊码
===============

Pugsy's cheats
	http://www.mamecheat.co.uk
	
	主要的是这个，作弊码非常的多。

Wayder
	http://nekoziman.s601.xrea.com/cheat/
	
	这一款作弊码可以为补充

两款作弊码，稍微设置一下，就可以同时使用。

中文版本
	
	| 如果需要中文版本的作弊码，可以多关注一下 街机模拟器 相关的网站、论坛，
	| 偶尔会有大佬翻译一下。
	
	老版本的中文作弊码
		
		| 网址： https://www.ppxclub.com/forum.php?mod=viewthread&tid=130735
		| jjsnake 整理的 中文出招表 ： command.dat
		| 还附带了 mame 老版本 的 中文作弊码
		| ( 注 mame 0.126 以前用的是 mame.dat 这种作弊码文件 )
		| ( 注 老版本的 mame 的话，官方原版中文支持不太友好，可以用第三方的 mameplus 或 mame32more 等 )

文件格式
=========================================

新版本
	
	默认文件名为：cheat.7z 或者 cheat.zip
	
	默认的存放位置为 模拟器 相同的文件夹。
	
	使用的时候，可以直接使用压缩包，不用解压。
		
		其实解压也可以，解压缩到 同名 的文件夹中。
	
	注意：
		
		资源为了节约体积，可能使用多层压缩。
		如果是多重压缩的，不能用，要先解压为单层的压缩包。
	
	.7z 和 .zip 都是压缩包文件，只是格式不同。
	以前的一些版本用的 .zip ，
	现在 Pugsy 的作弊码，都喜欢用 .7z 格式的了。
	模拟器先支持的 .zip 格式的，后来才添加了 .7z 格式的支持，如果用的 模拟器版本比较老的话，可能当时还不支持 .7z 格式的。
	
	cheat.7z （或者 cheat.zip ）内部，主要是 .xml 文件。
	
	街机：
		
		作弊码文件名，和街机游戏的英文缩写一一对应。
		比如 cheat.7z 中的 kof97.xml 是 街机 kof97 的 作弊码。
	
	非街机：
		
		每一类作弊码放在一个子文件夹里的，文件夹名 与 hash\\*.xml 文件名对应；
		子文件夹中，作弊码文件名 与 此类游戏的 英文名缩写 对应。
		比如 cheat.7z 中的 nes/sbm1.xml 对应于 hash\\nes.xml 中记录的游戏 smb1 。
	

老版本
	
	默认文件名为 cheat.dat
	
	默认的存放位置为 模拟器 相同的文件夹
	
	0.126 以及之前的版本，是这种格式的。
	
	cheat.dat 可以用文本编辑器 打开查看。


开启作弊功能
========================

下载 Pugsy 作弊码 cheat.7z ，默认的存放位置在 mame.exe 相同的文件夹。

MAME 默认没有开启作弊功能的，需要自己开启作弊功能。
	
	图形界面修改的话
		
		打开 MAME ，在进入游戏之前 的 游戏列表界面，选项中，找一找，找到这个选项 【Cheats 作弊】，改一下就行了。
	
	手动编辑配置文件的话
		
		mame.ini 配置文件中的 cheat 这一项
		
		原来为::
			
			cheat                     0
		
		改为::
			
			cheat                     1


开启作弊功能以后，进入一个常见的游戏，比如 kof97 ，
按 Tab 菜单弹出菜单，菜单中多出了一个 作弊码 的选项，
如下图：

.. image:: images/cheat_1.png

进入下一层子菜单，就可以看到具体的作弊码的各种作弊选项了，如下图：

.. image:: images/cheat_2.png


两份作弊码同时使用
=============================

首先前面说的作弊码功能的开关，要打开。

比如第一份作弊码：cheat.7z

比如第二份作弊码：cheat_wayder.7z

比如我们把两份作弊码文件同时放在 模拟器相同的文件夹 中。

两份作弊码同时使用：
	
	MAME 模拟器中，进入游戏之前，游戏列表界面，设置选项里，找一找，路径设置的选项，作弊码的路径，原来为 cheat ，添加一个 cheat_wayder 就可以了。
	
	如果手动编辑配置文件的话
		
		mame.ini 配置文件中的 cheatpath 这一项
		
		原来为::
			
			cheatpath                 cheat
	
		改为（英文分号间隔一下）::
			
			cheatpath                 cheat;cheat_wayder

完了以后，找个游戏对比一下：
	
	比如 kof97 使用一个作弊码时，最后一项为 Infinite Credits ：
		
		.. image:: images/cheat_multi_1.png
	
	使用两组作弊码后，后面多出来了一些：
		
		.. image:: images/cheat_multi_2.png


老版本
=====================================

老版本 mame 的作弊作弊码 文件名默认 cheat.dat ，一般 0.126 之前的版本。

老版本 mame 相关的功能，看菜单，似乎功能更多一些，如下图：
	
	.. image:: images/cheat_old_mame.png

差别
	
	使用现成的作弊码，使用体验上，似乎也没有什么差别。
	
	| 如果是老版本的的用户，用过其它的功能，比如 搜索作弊码什么的，新版本估计已经不一样了
	|   新版本，没有 上面 图片中 这么多 选项
	|   后文中提到的 插件中 有 cheat (作弊)、cheatfind (作弊搜索)，但似乎不太一样
	|   新版本，比如 0.260 ,模拟器可以打开 debug 选项，搜索作弊码之类的可能会用到这个功能
	|   我自己不会整作弊码，只会拿来用现成的，这些其它的功能，都不会用
	|   会自己整作弊码的，应该是个高手，比我更懂，上面如有说错的，可以指点一下


快捷键 切换作弊
=====================


| 如果 MAME 打开了 作弊功能，游戏 中 使用了 作弊，可以使用快捷键，打开/关闭 已使用的作弊项。
| 0.263 版本开始，快捷键默认是 Shift + F8 键。
| 0.263 版本之前，快捷键默认是 F6 键。
|   （ 0.263 版本，MAME 调整了一些快捷键的默认值 ）

| 友情提示：
|   如果不小心按到了 此快捷键 ，会把作弊功能给关掉。
|   再按一下就好了。
| 
|   有些作弊码，打开以后，即使关掉了作弊功能，可能效果还在。
|   开启作弊码时，游戏关闭，作弊码选项会清空。
|   开启作弊码时，按 Shift + F3 ，游戏重启，作弊码选项会清空。
|   开启作弊码时，按 F3 ，游戏软重启，作弊码选项不会清空（ 但可能需要 按一下 此快捷键，暂时关闭 作弊码，因为有些作弊码打开后游戏重启不了）。


如果你需要 更精细 一点 的 快捷键，下文中提到的插件中的作弊功能中，可以设置快捷键。


插件 作弊相关
========================

比如 0.260 版本。

打开插件功能 总开关。

插件各功能中有两个和作弊有关的： cheat 、 cheatfind ，打开。

进入游戏，比如 kof97 ，按 Tab 键，弹出菜单，有【插件】这一项，如下图：	
	
	.. image:: images/cheat_plugin_1.png

进入【插件】后，看到我们打开的两个项目，cheat（作弊） 、cheatfind（作弊查找）：
	
	.. image:: images/cheat_plugin_2.png

其中的 cheatfind（作弊查找）这个选项，不了解，感兴趣的可以试试。

另一个选项 cheat（作弊）。
	
	第一：
		
		打开一看，和前面说的作弊码功能重复了？
		
		确实有点重复了。
		不过，菜单最后面，有一个【设定热键】的选项，如下图：
			
			.. image:: images/cheat_plugin_3.png
		
		
		这个【设定热键】选项，
		是原作弊功能中没有的，
		如果有高频使用的作弊码功能，可以设置一个热键，开启关闭更方便。
	
	第二：
		
		仔细看 作弊码 压缩包 cheat.7z 中，除了有很多 ``*.xml`` 文件，
		还有少量的 ``*.json`` 文件
			
			比如就有 sf2.json 文件
			
			看了一下游戏 sf2 ，插件的作弊 比 原始的作弊 多出了第一项 【Hitbox viewer】，如下图
				
				.. image:: images/cheat_plugin_hitbox.png
				   :alt: 此处应显示图片

家用机作弊码 Software List 
=======================================

Software List ，软件列表。

对于一些家用机等，一款游戏机，可能支持很多的游戏，比如 nes 、snes、gba 、……等，它们的 Software List （软件列表）中，都有好几千游戏。

| Pugsy's 的作弊码，新一点的版本，已包含了一些家用机的作弊码。
| 与街机部分的作弊码在一起。
| 街机游戏的作弊码在第一层；Software List 中 游戏 的 作弊码在 对应的子文件夹中。

使用的方法还是挺简单的，和街机部分一样的。
	
	如果街机已开启过作弊码，那么无需再重复操作。
	
	| 如果还没有开启作弊码：
	|   看看前面的说明
	|   下载作弊码，放在默认的位置；
	|   开启 MAME 作弊功能；
	|   进入游戏，查看 Tab 菜单，【作弊】这一项。
	|   ( 游戏数量太多，有很多游戏没有添加作弊码的，可以查看作弊码文件 并 按大小排列，文件比较大的作弊码内容比较多，运行对应的游戏 )

游戏对应的 作弊码文件
	
	| 比如 作弊码文件为：压缩包 cheat.7z ，
	| 比如 hash\\nes.xml 中记录的游戏 smb1 （Super Mario Bros. (World)，超级马里奥），
	| 此游戏的对应的作弊码文件为 压缩包 cheat.7z 中的文件 nes/smb1.xml

家用机作弊码 自己收集的游戏
=====================================

如果是自己收集的游戏文件，而没有使用 Software List 。

以前看到别人说，可以使用游戏文件的 crc 值作为作弊码的文件名
	
	这操作比较麻烦
	
	官方文档好像没有提到这方面的（我搜索了一下关键词 cheat ，没有看到相关内容，也可能是我看得不够仔细）
	
	找个别游戏试过，确实可以
		
		注意，nes 文件一般有 header ，需要跳过 header ，计算 crc 值。
		
		比如 SNES SFC :
			
			Software List 对应的文件：hash\\snes.xml
			
			对比了个别文件，Software List 中记录的游戏文件，和平常别的地方下载的游戏文件，其实是一样的。 
				
				Software List 中，文件名需要使用指定的名称
				
				Software List 中，游戏文件需要放在指定的路径中，默认比如 roms\\snes\\\*.zip
			
			如果运行的 Software List 中的游戏，Pugsy 的作弊码中已有许多的 snes 游戏的作弊码，比如 cheat.7z 中 snes/smwu.xml 。
			
			如果使用 MAME 载入一个 .sfc 文件，运行游戏，怎样使用作弊码呢？
				
				如果是同款游戏的话，可以复制 Software List 中同款游戏的作弊码文件；
				
				把文件名改为 crc 值。
				
				比如 0.261 版本中
					
					原来的作弊码 snes/smwu.xml 复制一份，改名为 snes/b19ed489.xml
					
					| 不用去编辑原始的 cheat.7z 或 cheat.zip
					| 压缩包中文件数量太多，编辑文件可能比较麻烦
					| cheat 文件夹中的同名文件优先级更高
					| 直接在文件夹中操作更方便一些
		
		比如 NES :
			
			( 跳过 header ，计算 CRC 值 )
			
			Software List 对应的文件：hash\\nes.xml
			
			对比了个别文件，Software List 中记录的游戏文件，和平常别的地方下载的 .nes 游戏文件，区别：
				
				Software List 中，文件名需要使用指定的名称
				
				Software List 中，游戏文件需要放在指定的路径中，默认比如 roms\\nes\\\*.zip
				
				别的地方下载的 .nes 通常是一个单独的文件
				
				Software List 中的 nes ，可能是多个文件
					
					如果把多个文件 拼接起来，能还原一个 .nes 文件（无 header ）。
			
			如果运行的 Software List 中的游戏，Pugsy 的作弊码 中 已有许多 nes 游戏的作弊码，比如 cheat.7z 中 nes/smb1.xml 。
			
			如果使用 MAME 载入一个 .nes 文件，运行游戏，怎样使用作弊码呢？
				
				如果是同款游戏的话，可以复制 Software List 中同款游戏的作弊码文件；
				
				计算 .nes 文件 ( 去掉 header ) 的 crc 值，把文件名改为此 crc 值。
				
				比如 0.261 版本中
					
					原来的作弊码 nes/smb1.xml 复制一份，改名为 nes/d445f698.xml
					
					| 不用去编辑原始的 cheat.7z 或 cheat.zip
					| 压缩包中文件数量太多，编辑文件可能比较麻烦
					| cheat 文件夹中的同名文件优先级更高
					| 直接在文件夹中操作更方便一些