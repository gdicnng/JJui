﻿==========================================
游戏文件 roms 下载
==========================================



需要自己搜索资源
==================

由于版权的原因，游戏文件，玩家需要自己找资源。

本页面没有给出资源链接。

在此只是简单说一些基本的事项。

MAME 官方网站 不提供游戏文件
==================================

MAME 官方网站，提供的模拟器是空的，不含游戏文件的。
	
	网址：https://www.mamedev.org
	
	比如 0.260 版，里面有一个古老的街机游戏 pong ，这个倒是不需要游戏文件就可以运行的。
		
		测试一下模拟器的功能，倒是很方便。
		
		不过，这古老的街机游戏，有点太古老，当年在街机厅里我是没见过这种的。

MAME 官方网站，也提供了一个 游戏文件 roms 下载的页面。
	
	https://www.mamedev.org/roms/
		
		但是，这里的数量非常少，勉强超过了个位数。
		
		而且，仅有的几个游戏都非常的古老。
		

建议新玩家先下载别人理好的资源
==============================================

MAME 官方网站，不提供游戏资源。
游戏资源，需要玩家自己整理收集，这对于新玩家来说，就有点难了。

如果能找到资源的话，特别是新玩家，推荐 优先 下载别人整理好的 小合集／大合集／全集 资源，使用起来要简单很多。
跳过了找资源这一个步骤，只需要稍微了解一下 MAME 的使用方法，就可以游戏了，这样就简单很多。

测试、使用后，如果觉得好，再深入了解也不迟。

即使是老用户，也有很多不会自己整理资源的，只是简单的使用了别人整理好的资源。

而且现在网络带宽大，下载速度也快。

初步了解，会用了以后，觉得有必要深入了解一下，再花时间去折腾也不迟。

英文名缩写
==================

MAME 会给每一个游戏分配一个 英文缩写。

比如::
	
	拳皇97
	英文名： The King of Fighters '97 (NGM-2320)
	英文缩写： kof97

游戏文件、游戏周边文件 的保存位置， 通常是和这个 英文缩写 相关的。

游戏文件 roms
======================
游戏文件 ，一般可能被叫做 roms 。

| 游戏文件，默认的保存位置就是 roms 文件夹；
| 当然也是可以修改的，可以修改为其它的文件夹 或者 多个文件夹。
|  （roms 文件夹 和 mame 程序 在同一个文件夹里）
|  （如果你使用的不是 Windows 操作系统，情况可能不太一样，可以通过 mame -showconfig 查看模拟器的设置选项）
|  （如果你使用的不是 官方原版 MAME ，比如 RetroArch 这种大杂烩，它也有 MAME 核心，具体的情况，你就得了解一下 RetroArch 的使用方法了）



.zip 压缩包
	
	比如 MAME 0.267 版本中：
		
		比如 拳皇97 ，英文缩写 kof97：
		它的游戏文件就保存在 kof97.zip 中，其中有十来个文件。
		
		比如  拳皇97 的一个盗版，拳皇 97 - 风云再起 Plus ：
		英文缩写为 kof97pls ，
		它的游戏文件就保存在 kof97pls.zip 中，
		其中有3个文件，
		有很多 在 kof97.zip 中重复的文件，
		在这里被省略掉了，
		以节约空间。
		
		同一个游戏，如果有不同版本，MAME 会指定其中的一个为主版本，上面说的两个，kof97 为主版本。
		
		如上面描述的，两游戏的游戏文件可以分别保存在 kof97.zip 、kof97pls.zip 中。
		
		两游戏的游戏文件也可以都放在  kof97.zip 中 （主版本的位置）。
		
		老用户应该知道，这类游戏需要一个 BIOS 文件 ，
		neogeo.zip ，其中有 三十多个 文件。
		新用户想了解详情的话，可以通过 MAME 的命令行 指令 -verifyroms 、-listroms 、-listxml 、……等，查看具体的 roms 信息。
		
		::
			
			mame kof97 -verifyroms
			mame kof97 -listroms
			mame kof97 -listxml
		

.7z 压缩包
	
	老版本的 MAME 不支持 .7z 压缩包格式。
	
	新版本的 MAME 支持 .7z 压缩包格式。
	
	.7z 和 .zip 一样的，只是不同的压缩格式。
	
	同样的游戏文件，比如 上面提到的 kof97.zip ，转换为 kof97.7z ，也是可以的。

文件夹
	
	如果把 kof97.zip 中的文件，解压出来，放在 kof97 文件夹中，把 kof97.zip 删了，这样也是可以的。
	
	不推荐使用 文件夹 的形式
		
		| 使用压缩包，可以节约一些空间。
		| 使用压缩包，对它内部文件的 文件名错误，MAME 会有一定的纠错功能。
		| 有一些前端，可能不会识别 文件夹 这种方式。

游戏文件 chds
========================

对于 roms 来说，大多数文件通常是放在 .zip 或 .7z 压缩包里的，前面已经说过了。

有些街机，如果使用了 光盘、硬盘、……等，用来保存游戏文件，对应到 MAME 上，MAME 整了一下 .chd 的格式，用来保存这一类游戏文件。

一个游戏，可能即有 .zip 或 .7z 压缩包 格式的游戏文件，又有 .chd 格式的 游戏文件。

比如 MAME 0.267 版 
	
	| 比如 使用 默认的保存位置 roms 文件夹
	| 比如游戏 街头霸王 III - 三度冲击 未来战斗 (欧版 990608)，sfiii3，
	| 它缩写是 sfiii3
	| 它需要 rom 文件，保存在 ``roms\sfiii3.zip`` 中
	| 它还有一个 chd 文件，文件名是 cap-33s-2 ，.chd文件的保存位置： ``roms\sfiii3\cap-33s-2.chd``
	| 这其中，chd 文件的命名，感觉没有规则，感兴趣的，可以通过 MAME 的命令行 选项 -listroms 、-listxml 、……等选项，查看具体的 roms 信息。

街机部分，从数量上来讲，有 CHD 文件的 游戏不多；
从文件大小来讲，这些少量的文件加起来，体积就很大了。
其中有很多游戏，模拟状态不佳，还运行不了。

我自己的话，曾经在街机厅时代，体验过的游戏，好像都不是这一类的。

游戏文件 samples
========================
默认的保存位置是 samples 文件夹。

需要这类文件的游戏，数量不多。

以前看过一下，时面都是一些音频文件。
不是很了解，可能是部分游戏，某些声音片段模拟的不行，需要另外整一些音频文件。

好像缺了这类文件，游戏也能运行。

版本差异
======================

因为 MAME 一直在更新，不同版本的游戏文件，可能会略有差异。

有的网站，标记得比较清楚，游戏资源具体是适用于某个版本的 MAME ，那么用对应版本的 MAME 兼容性要好一些。

有些网站，提供的游戏资源，没有注明适用于哪个版本的 MAME 。
这种的话，要麻烦一些。有可能会遇到资源不兼容的情况。

因为，MAME 更新，游戏文件 roms 可能会有 更新，所以不同版本的 MAME ，需要的 roms 可能会有些许不同。
	
	文件名称的修改：
		
		1：
			
			MAME 给每一个游戏弄一个 英文缩写，
			这个 英文缩写 通常就是 游戏文件 对应的 压缩包 的 文件名。
			如果 这个 英文缩写 改了，
			那对应的游戏文件所在的 压缩包 也是需要改名的。
			这种情况应该是比较少见的。
		
		2：
		
			具体到某一个游戏，
			压缩包 内部 包含的许多文件，
			如果 这些文件 有改名的，
			这种情况，自己手里的游戏文件也是需要修改文件名的。
			还好，MAME 对 压缩包 内部 的 文件名称 的错误 有一定纠错机制，
			许多此类文件名出错情况，并不会影响到游戏的运行；
			但最好使用正确的文件名，有些错是不可以的，
			比如 两个文件 分别使用了 对方应该使用的文件名、
			再比如 一个错误的文件 占用了 一个正确的文件名。
		
	
	游戏文件 roms 的 更新：
		
		游戏文件是从街机里整出来的，有个英文单词叫 dump ，意思大概就是把街机中的游戏文件 提取 出来。
		
		我的理解是
			
			以前有些 dump 出来的文件 可能有点错误，
			后来 dump 出来了正确的文件，
			那自然就需要更新了；
			
			有些 以前 没有被 dump 出来的文件，
			后来 被 dump 出来了，
			那自然就需要更新了。
			
			如果使用 JJui ，
			内置的目录分类中（分类信息是从 mame.exe -listxml 中提取的），
			有 dump 分类，
			其中 no dump 分类 和 bad dump 分类。
			感兴趣的可以看看。
			游戏文件如果有 no dump、 bad dump 标记，MAME 在运行此类游戏时，还会有专门的提示信息。

整理游戏文件有一些专用的 roms 管理软件，
比如 ClrMamePro https://mamedev.emulab.it/clrmamepro/ 。

自己整理的话，
比较麻烦，
尤其是还不会用 一些 roms 管理软件的用户。

新玩家，
可以尝试找一找大佬整理并分享出来的资源，
直接测试、使用。

BIOS 、Device
========================
| 老版本 MAME 可能只有 BIOS 一类 。
| 后来 版本的 MAME 还添加了 Device 一类 。

游戏文件中的特殊类型。

其中的一个文件，可能会被多个游戏使用。

具体到某一个游戏，它到底需不需要 BIOS 、Device 文件，需要的话 又 需要哪些 BIOS 、Device 文件，新玩家可能分不清楚。

如果下载的全套游戏文件，那已经包含了 BIOS 、Device 这些特殊的文件，就不必在意。

如果下载少量游戏，对于新玩家来说，如果有 适用于 某个 MAME 版本的 BIOS 、Device 合集，
最好一起下载了。免得总是分不清楚需要依赖哪些 BIOS 、Device 文件。

新用户想了解详情的话，可以通过 MAME 的命令行 指令 -verifyroms、-listroms 、-listxml 、……等，查看具体的 roms 信息。比如：

::
	
	mame kof97 -verifyroms
	mame kof97 -listroms
	mame kof97 -listxml

主版本 克隆版本
===========================

如果自己下载少量游戏的话，优先下载 主版本 游戏文件

同一个游戏，MAME 会选择其中的一个作为主版本，剩下的叫 副版本、克隆版本。
	
	当然了，这只是 MAME 的分类方式

因为是同一个游戏的不同版本，所以有很多游戏文件是重复的。
	
	克隆版本的游戏文件，为了节省空间，可能会省略掉 主版本中已有的相同的文件。
	
	所以要优先下载 主版本 的游戏文件。


	
资源大小
======================

街机部分：0.267 版，roms 有七十多 G ；chds 有九百多 G 。
	
	其中有很多游戏是还没有模拟好的，不能运行的。
	
	对于我来说，曾经在街机厅时代，体验过的游戏，好像都是无需 CHD 一类的。

非街机部分： 0.267 版，roms 有 九十多 G ；chds 有 两个多 T 。
	
	其中有很多游戏是还没有模拟好的，不能运行的。
	
	0.162 版本之后，MAME 合并了 MESS 项目，之前的 MAME 是没有这一部分的。
	
	很多用户，可能对这一部分，没有什么兴趣。

游戏周边 extras
	
	作弊码，文档，游戏截图，海报，照片，视频，…… 等等。

split 、 merged 、 non-merged 
========================================

查找资源的时候，
有可能会看到大佬分享的 用不同方式整理的 roms 。

| 一个游戏，尤其是比较热门的游戏，可能会有许多版本。不同地区的版本、盗版、…… 。
| MAME 会把其中的一个作为 主版本，其它 作为 克隆版本（当然了，这只是 MAME 的分类方式）。

split
	
	| 主版本的游戏文件、副版本的游戏文件 分开存放；
	| 副版本的游戏文件，如果在 主版本的游戏文件 中 已经有相同的了，就可省略掉了，这样可以节约一些空间。
	| 所以，有时候可以看到，有的 克隆版本的游戏，游戏文件数量很少，因为主版本中有重复的文件。
	

merged
	
	主版本的游戏文件、其它版本的游戏文件 都 放在一起，都放在 主版本游戏文件 的 保存位置。

non-merged
	
	主版本的游戏文件、其它版本的游戏文件 都 单独存放在自己的位置；
	重复的文件，也都保留。
		

