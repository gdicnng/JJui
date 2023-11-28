========================================================
视频选项
========================================================

（游戏截图的话，怕人说侵权什么的。没有游戏截图展示一下的话，这篇文单看起来可能不够人性话。）

当年的街机游戏，图像像素都比较少。
现在的显示器和当年的显示器又不一样。
当年的街机游戏，在现在显示器中，通常都需要放大好多倍。
不同选项，图像放大好多倍后，最后的显示效果，差距非常大。

本篇通常都会用到配置文件 mame.ini ，选项说的都是这个配置文件里的。
如果你喜欢图形界面中，鼠标点一点来修改选项的话，也是一样的，找到对应的选项就是了。
	
	如果整体统一设置的话，在配置文件 mame.ini 修改就行了。
	
	如果不同游戏种类，分别设置的话，你需要稍微了解一下 mame.ini 这一类配置文件，比如 horizont.ini 、 vertical.ini 、……等。

video 选项
===============================

图形界面中：
	
	.. image:: images/video_video.png

配置文件中，比如 0.260 版，默认为::
	
	video                     auto

比如 0.260 版，video 选项的值可以是 d3d, bgfx, gdi, opengl ， none（不使用图像），默认是 auto（自动）
	
	video 默认 auto（自动），按说明 自动选的话 会是 d3d 。
	
	video 普通的话，会选 d3d ，也可以选 opengl。
	
	video 选 bgfx 的话，可以使用内置的一些图像效果，后面会专门说一下。
	
	video 通常不会选 gdi ，说明上提到，这个最慢，但兼容性好，如果 老版本的 windows 或 显卡驱动有问题什么的话，或许有点用。
	
	老版本的话，可能选项略有不同。
	
	其它操作系统的话，情况可能不同，可以去看看官方说明。

filter 选项
=========================

filter 选项 ，双线性过滤

图形界面中：
	
	.. image:: images/video_filter.png

配置文件中，比如 0.260 版，默认值::
	
	filter                    1


双线性过滤效果
==========================

官方原版 MAME 现在，好像默认就是这种画面 。

其它第三方版本的的 MAME ，有的可能默认不是这样的。

| 比如 0.260 版，
| video 选项 值 简单设为 auto（自动）或者 d3d 或者 opengl ；
| filter 选项（双线性过滤），打开。
| 会是 双线性过滤效果
	
	图形界面修改的话，在这里：
		
		.. image:: images/video_filter.png
	
	手动修改配置文件的话::
		
		video                     auto
		filter                    1


马赛克效果
======================

很多人不喜欢这种画面效果，但好像也有人就喜欢这种。

双线性过滤选项 filter 关闭。

| 比如 0.260 版，
| video 选项 简单设为 auto（自动） 或者 d3d 或者 opengl ；
| filter 选项（双线性过滤）， 关闭。
| 会是 马赛克效果
	
	图形界面修改的话，在这里：
		
		.. image:: images/video_nofilter.png
	
	手动修改配置文件的话::
		
		video                     auto
		filter                    0
	
	注意
		
		后文会提到的 HLSL 、GLSL 的开关选项，关闭，
		
		以免误入 HLSL 或 GLSL 模式

prescale 选项
================================


图形界面选项在这里：
	
	.. image:: images/vidoe_prescale.png

配置文件中的话，默认为::
	
	prescale                  1

可以把它的值调大一点 2,3,……

如果不喜欢 双线性过滤效果 ，那可以试试把这个 prescale 选项的值 调大一些，
而不是直接关掉 双线性过滤。

effect 选项
===========================

默认为 空::
	
	effect                    none

打开模拟器 artwork 文件夹，其中应该有一些 .png 格式的效果图片。

选一张图片，把 effect 选项的值，改为图片的文件名，就可以使用这种效果了。

感兴趣的话，我记得第三方的 MAME 可能包含更多此类图片。

BGFX
===============

https://docs.mamedev.org/advanced/bgfx.html

需要比较新的版本。老的版本可能当时没有此功能。

使用方法也比较简单。打开 bgfx 功能，操作如下：

	图形界面操作的话，选项在这里：
		
		.. image:: images/video_bgfx.png

	配置文件中，把 video 选项值改为 bgfx::
		
		video                     bgfx

进入游戏后，按 Tab 键，弹出菜单，有个【参数调整】的选项
	
	.. image:: images/video_bgfx_1.png

进入下一层菜单，看底部，可以 按 左、右 切换不同的视觉效果
	
	.. image:: images/video_bgfx_2.png

如下图，切换 到 另一种 视觉效果，这种的话，自身还有很多选项（其它的一些视觉效果可能没有什么选项）
	
	.. image:: images/video_bgfx_3.png

不同的视觉效果，都可以试试，或许就有喜欢的一款。

建议使用较新的版本，老一点的版本，游戏中的调整， BGFX 可能很多选项不会自动保存，不是那么方便。
现在新一点的版本，可能稍好一点。
如果仍然遇到有选项不能自动保存的话，可能需要手动设置。

bgfx 整体的选项不多，具体含义可以去看看说明::
	
	bgfx_path                 bgfx
	bgfx_backend              auto
	bgfx_debug                0
	bgfx_screen_chains
	bgfx_shadow_mask          slot-mask.png
	bgfx_lut                  lut-default.png
	bgfx_avi_name             auto

bgfx 个体的话，某些视觉效果，各能还会有自己的许多选项。

HLSL
======

https://docs.mamedev.org/advanced/hlsl.html

打开 HLSL 功能，需要把 video 设为 d3d、把 filter 关闭，再把 开关 hlsl_enable 打开
	
	图形界面操作的话，选项在这里：
		
		.. image:: images/video_hlsl.png
	
	配置文件的话::
		
		video                     d3d
		filter                    0
		hlsl_enable               1

进入游戏后，应该可以看到画面效果变了。

打开这功能，很简单，但是，这个 HLSL 功能，有非常多的 选项。

自己不会调节的话，可以网上搜索了解一下，复制一份参数过来也是可以的。

如果需要自己调节选项：
	
	按 Tab 键，弹出菜单，有个【参数调整】的选项
		
		.. image:: images/video_hlsl_1.png

	进入下一层菜单
		
		菜单底部，可以 看到多出来很多选项
		
			.. image:: images/video_hlsl_2.png
		
		你可以手动调节一下这些参数
		
		（好像这些参数不会自动保存，可能需要你手动修改一下）
		
	
	手动 在配置文件中 修改这些参数 的话，
	关于配置文件的优先级：
		
		比如 0.260 版，
		
		当我们把 HLSL 功能打开了以后，需要对 HLSL 参数调整时，
		
		有几个预设的配置文件，其中的 ``ini\presets\raster.ini``
			
			``ini\presets\raster.ini``
			
			raster.ini 这个配置文件的优先级别高于 mame.ini
			
			而且街机游戏应该都属于这一类的
			
			看了一下，里面的参数 好像是关于 HLSL 的
			
			如果修改 mame.ini 无效，可以试试修改 raster.ini
			
			raster.ini 
				
				https://docs.mamedev.org/advanced/multiconfig.html
				
				如果对 不同 显示器种类，需要 分别设置的话，可以使用以下这几类配置文件，优先级都高于 mame.ini
				
					vector.ini
						for vector monitors, 
					
					raster.ini
						for CRT raster monitors，CRT 显示器，一般街机貌似都是这种
					
					lcd.ini
						for LCD/EL/plasma matrix monitors，LCD 显示器


GLSL
========

https://docs.mamedev.org/advanced/glsl.html

这功能需要一些额外的文件，
而官方原版 MAME ，似乎没有包含这类文件，需要自己先去找资源。

不方便使用的话，这里就不说了。

如果是第三方的 MAME ，可能附带了一些 GLSL 需要的文件，使用起来可能更方便。


附：MamePlus 的图像增强选项
===================================

如果使用 MamePlus 的话，MamePlus 停止更新了，可能当时没有 BGFX 、HLSL 、GLSL 这类功能。
具体可以自己试试。

MamePlus 预设的几个视觉效果：
	
	注意这功能 官方原版 MAME 是没有的（新版 MAME 的话，可以使用 前文提到的 BGFX 等 代替）
	
	进入游戏，按 Tab 键，弹出菜单，有个【图像增强】的选项，如下：
		
		.. image:: images/video_mameplus_1.png
	
	菜单进入一下层，可以看到有几个不同的 效果 可以选择
		
		.. image:: images/video_mameplus_2.png