==========================================
拼音排序 笔画排序
==========================================

游戏列表中，仅 游戏名（译）这一列，其它的列，不影响。

默认的 字符排序 的 顺序 是 按照 字符编码 来的。
我这里，源代码用的 utf-8 ，默认的 排序 应该是 Unicode 字符 的顺序 。

添加功能：
	
	菜单中，游戏列表，选择（或者取消选择） 本地排序。

默认的 排序 速度要快一些。
本地 排序 速度要慢一些。

配置文件  ``jjui.ini`` 中有个选项  ``locale_name``，值没有设置。
	
	locale_name 的值，可以不用设置，默认留空也可以。

电脑操作系统，如果没有选国外的地区，使用本地排序后，默认是拼音排序的。

配置文件  ``jjui.ini`` 中 ``locale_name`` 的值： ::
	
	windows 操作系统的话，值参照:
	  https://learn.microsoft.com/en-us/windows/win32/Intl/sort-order-identifiers
	
		拼音排序：默认，空着不填就行。
		  也可以设为：zh-CN
	
		笔画排序，值可以填：zh-CN_stroke
	
	上面提到的值，zh-CN、zh-CN_stroke 都不是完整的值。
	不过没有关系，设置这一部分就能用了。
	
	locale_name 的值，用于
		locale.setlocale(locale.LC_COLLATE,值 ) 
	排序使用的函数：
		locale.strxfrm()




