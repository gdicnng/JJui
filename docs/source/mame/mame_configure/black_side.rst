==========================================
去黑边
==========================================

有些游戏的话，游戏周围会有少量的黑边。

先把游戏调成 窗口模式，这样更容易看清楚黑边。

方法一.参数调整
	
	进入游戏后，按 Tab 键，弹出菜单，有个选项【参数调整】
		
		.. image:: images/black_side_1.png
	
	菜单进入下一层，下面这些选项，可以把 游戏画面 扩大 ，黑边就没有了
		
		.. image:: images/black_side_2.png

方法二.视频选项
	
	仅一部分游戏，可能会有这样子的选项，比上面方便一点。
	
	0.260 版本中，比如 《拳皇97》 
	
	进入游戏后，按 Tab 键，弹出菜单，有个选项【视频选项】
		
		.. image:: images/black_side_3.png
	
	菜单进入下一层，屏幕0# 
		
		.. image:: images/black_side_4.png
	
	菜单进入下一层，可以看到有好多个选项，下图中的这个选项，正好去掉了黑边。
		
		.. image:: images/black_side_5.png

方法三.BGFX 中的 crt-geom 等
	
	如果 视频模式 设置为 bgfx ，如果使用了 crt-geom 等 效果。
	
	进入游戏后，按 Tab 键，弹出菜单，有个选项【参数调整】
		
		.. image:: images/black_side_1.png
		
	
	菜单进入下一层，可以看到 crt-geom 这个效果，有很多的选项，
	其中的 overscan (过扫描) 选项，可以用来去除黑边
		
		.. image:: images/black_side_overscan.png