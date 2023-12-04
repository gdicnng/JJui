==============================================
NEOGEO
==============================================

MAME 0.260 里，这一类游戏，源代码 分类是 neogeo/neogeo.cpp，其它版本可能略有差异，你可以在游戏列表中把这一类找出来看一看。

有 拳皇系列、合金弹头系列、侍魂系列、月华剑士系列、炸弹人机皇版、双截龙格斗、……

这类游戏，当年在街机厅里还是很常见的。

AES 家用机
====================

你可能需要额外下载一个游戏文件： aes.zip
	
	AES 中的游戏，和，街机 neogeo 一类的游戏 ，大量重复
	
	几乎不用 另外 下载别的游戏文件，就可以体验一下 aes 
	
	只有少量几个游戏 可能不一样
	
	同样的游戏，在 家用机 AES 中，可能有一些不同的地方
		
		| 比如 拳皇97 vs 对战模式，比较方便两人 PK
		| 比如 拳皇98 有练习模式，
		| ……
		| 感兴趣的可以体验一下
		
比如 官方原版 MAME 0.260 ，游戏列表中有个 Neo-Geo AES (NTSC)，缩写为 aes 。
	
	.. image:: images/neogeo_aes.png

游戏列表，进入下一层，显示的 AES 所拥有的 子游戏列表。
	
	此时，可以在 子游戏列表 中，找到熟悉的游戏，比如 kof97
		
		.. image:: images/neogeo_aes_sl.png


如上所说，官方原版的话，现在简单体验一下家用机 AES 还是挺简单的。

注：
	
	家用机游戏，如果使用 Shift + F7 存档，
	你可能需要设置一下存档位置，
	不然，这一款游戏机里，所有的游戏都用同一个位置，挺麻烦。
	
	可以查看说明文件 statename 选项。

BIOS
===================

这类游戏，一般有多个 bios 版本，比如 欧版的、美版的、亚洲版、日版、uni-bios 加强版、……。

这一类不管是 街机 还是 家用机AES 都可以切换 BIOS 。
	
	街机 可选的 bios 版本要多一些；家用机AES 可选的 bios 版本要少一些。
	
	街机，默认是选的 欧版 bios
	
	使用日版 bios ，可能游戏中会有更多日文元素，比如 侍魂、月华剑士 这样的。
	懂日语的可能会更喜欢。
	另外，日语中可能使用一些字汉，不懂日语的，也可能会用这种。
	
	比如 街机 kof97 ，默认 bios ，不方便 游戏一开始就在 玩家2 的方向玩。
	用 美版 bios ，玩家2 单独投币的，可以 游戏一开始就在 玩家2 的方向玩。
	
	uni-bios，UNIVERSE BIOS。
	这种的话，是属于加强版 bios ，应该是第三方出的 bios 。
	功能增强型的。
	可以选择不同地区。
	可以切换 街机模式/家用机模式 。
	游戏中可以调出 作弊菜单。
	以及其它的功能。

比如 0.260 版，官方原版 MAME 
	
	进入街机 kof97 时，会有一个 bios 选择框，方便选择不同的 bios 版本。
		
		.. image:: images/neogeo_bios_select.png
	

如上所说，官方原版的话，现在简单体验一下不同版本的 bios ，还是很方便的。（以前的版本不是这样的）
	
	当然你如果觉得这个 bios 选择器，有点碍事，可以选择关掉。

第三方版本的 MAME ，可能设置的方式有点不同。

如果要手动编辑配置文件的话
	
	首先，命令行中查看 kof97 各版本 bios 的名称，比如 euro 、us 、japan 、unibios40 、…… 等::
		
		mame.exe kof97 -listbios
			
			新版本才支持 -listbios
		
		或者
		
		mame.exe kof97 -listxml
			
			这种显示的内容太多，不光有 bios 信息，还有一大堆其它信息
		
		mame 版本不同，名称可能不一致。
	
	配置文件中，bios 这一项，默认未设置
	
	上面命令行查出来的 bios 的名称，可以设置到配置文件中，比如::
		
		bios                   unibios40
	
	自己设置的话，不建议设置到全局配置文件 mame.ini 中，因为不同的游戏，可能这个值设置的不一样。
		
		单个游戏可以设置到 单个游戏的 配置文件中，比如 kof97.ini 
		
		按 bios 类型的话，比如它的 bios 为 neogeo,可以设置到 neogeo.ini 中
		
		注意和 全局 mame.ini 相同的选项，都删除，仅保留不同的选项。
		此处仅设置了 bios 一项，那仅保留这一项就行了，其它的都删了。
		

使用家用机 AES
==================

此类游戏，使用家用机 AES 的话，可以直接使用 AES （你可能需要下载一个 aes.zip 文件），前文已经说了。

此类游戏，使用家用机 AES 的话，街机 可以使用 uni-bios ，并且在游戏启动时，切换为 家用机 AES ，后文附了 uni-bios 的说明。

如果用的是 MamePlus:
	
	MamePlus 的 bios 中，也有一样有 uni-bios ，还有一个 家用机 的 bios 
		
		后期的 MamePlus 这个 家用机 的 bios 有点 bug ，游戏没有声音。
			
			官方原版 MAME ，没有这个 bios 。
		
		早期版本的 MamePlus 没有 bug 无所谓用哪个 bios ；
		后期版本的 MamePlus 如果遇到 bug ，就使用 uni-bios 切换到 AES .



uni-bios
=====================

如果 bios 使用 uni-bios ,这个 bios 提供了许多功能。

使用说明，可以到这里看一下：
	
	http://unibios.free.fr/
	
	http://unibios.free.fr/howitworks.html

这个 bios ，可以切换 街机、家用机 模式。在游戏启动时设置。

这个 bios ，游戏中，弹出菜单后，可以使用一些作弊功能，以及其它功能。

说明如下
	
	HOW IT WORKS
	
	它是怎样工作的
	 
	The UNIVERSE BIOS is a patched version of the original SNK BIOS. Most code is the same as the original BIOS with the new code being worked into it. To access features of the UNIVERSE BIOS you will need to use button codes.
	
	UNIVERSE BIOS 是原始 SNK BIOS 的修补版本。大多数代码与原始BIOS相同，其中包含新代码。要访问 UNIVERSE BIOS 的功能，您需要使用按钮代码。
	 
	For the Neo Geo CD system please visit the dedicated CD Systems page.
	
	对于 Neo-Geo CD 系统，请访问专用 CD 系统页面。
	 
	The following codes should be used on the 1up controller while the splash screen is showing or held during power up if the splash screen is disabled;
	
	当启动画面显示时，玩家1 按以下 组合键 ；如果启动画面被禁用，启动时按住 组合键；
	
	::
	
		(A)+(B)+(C)       UNIVERSE BIOS Menu
		ABC               UNIVERSE BIOS 菜单
		
		(A)+(B)+(C)+(D)   Memory Card Manager
		ABCD              记忆卡管理器
		
		(B)+(C)+(D)       Test Mode (MVS only)
		BCD               测试模式 (仅街机 MVS)
		
		(B)+(C)+(D)       Hardware Test (AES only)
		BCD               硬件测试 (仅家用机 AES)
		
		(Use 2up controller for the following code)
		(以下玩家2按组合键)
		
		(A)+(B)+(C)+(D)    Controller Test (AES only)
		ABCD               控制器测试 (仅家用机 AES)
	
	此处补充::
		
		A 、B 、C 、D 表示 第一个按键、第二个按键、第三个按键、第四个按键
		
		启动时，同时按 ABC ，弹出菜单（如果错过了刚启动那段时间，游戏关闭，重新打开一次就行了）
			
			如果要切换 街机 与 家用机AES ，就是在这个菜单里操作的
				
				比如 uni-bios 4.0 的菜单，
				
				Region Setup（地区设置），选中这一项，菜单进入下一层
					
					Region 地区 ,选 A 或 B 或 C ： (A) 日、(B) 美、(C) 欧
					
					Mode 模式，选 A 或 B： (A) Arcade 街机 、(B) Console AES 家用机
					
					选完以后，它会回到主菜单
				
				主菜单，按 C ，退出菜单，进入游戏

	The following codes are available in game only, they will not work if you have disabled the in game menu (general bios settings);
	
	以下 组合键 仅在游戏中可用，如果您禁用了游戏中的菜单（常规bios设置），它们将不起作用；
	
	::
	
		(START)+(SELECT)    In Game Menu
		开始键+选择键        游戏内菜单
		
		(START)+(COIN)      In Game Menu
		开始键+投币键        游戏内菜单
		
		(START)+(A)+(B)+(C)   In Game Menu
		开始键+ABC            游戏内菜单

	此处补充::
		
		比如 uni-bios 4.0
		
		游戏中，按 上面提到的 组合键 ，可以弹出菜单
		
		按 C ，可以退出菜单
		
		其中菜单的第一项是作弊功能
			
			当然 MAME 使用作弊码也可以作弊，不一定要用这里的作弊功能
			
			可以对比一下 MAME 作弊功能中的选项，和，uni-bios 作弊功能的选项


	Further information on using the UNIVERSE BIOS is provided in the manual that came with the UNIVERSE BIOS or in the readme.txt included with the image. 
	
	有关使用 UNIVERSE BIOS 的更多信息，请参阅 UNIVERSE BIOS 附带的手册或映像附带的 readme.txt。