==========================================
使用 python 比较新的版本
==========================================

如果使用的 python 版本比较新，还在更新维护，那么在线安装 Pillow 库要简单得多。

pip 可以直接更新到最新版，不用 特意 去指定某个版本  通常也不会有问题。

Pillow 库：
	可以直接更新到最新版，不用 特意 去指定某个版本。（需要的话同样也可以指定某个版本 ==版本号)
	
	不用在 选项 里强调要安装二进制的版本。（需要的话也可以加上 --only-binary :all: 参数，表示要安装 二进制 的版本）

::

	使用中转器的话，指令如下
	
	更新 pip 的指令：
	py -m pip install --upgrade pip
	
	安装 Pillow 的指令：
	py -m pip install Pillow
	
		如果安状了多个版本的 python ，不是使用默认的版本,可以加上版本号，比如：
		py -3.9 -m pip install --upgrade pip
		py -3.9 -m pip install Pillow
	
	
	然后，进入 JJui.pyw ，所在的文件夹，运行：
	命令行运行：
	py JJui.pyw
		（会多显示一个命令行窗口）
	pyw JJui.pyw
		（隐藏命令行窗口）
	也可以直接鼠标双击运行（喜欢有命令行窗口的，把 JJui.pyw 改个文件名为 JJui.py 就行了）
	