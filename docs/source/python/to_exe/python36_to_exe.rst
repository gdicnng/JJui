================================================================
使用 python 3.6 版，打包 exe
================================================================

先看上一篇，在 python 3.6 中使用 JJui 。

打包 exe 需要注意，python3.6.8 可以安装到 win7 sp1 上，最好到 win7 sp1 上去打包，安装个 win7 sp1 的虚拟机。

如果在 win10 上打包，拿到 更早的 操作系统上，可能不兼容，我看说明，好像是这么个意思。

用的是 pyinstaller 打包的，打包为一个文件夹，里面有很多的文件。打包后，在 dist 文件夹里找到，把整个文件夹复制出来。
	
	注意事项：把源代码文件夹复制过去，源代码可以删，图片需要用到。
	
	图片的文件名不要改，图片所在的文件夹名，以及上层源代码的文件夹名，都不要改。
	
	图片，觉得效果不好的话，可以换掉。
	
		.png 格式的图片。
		
		.xbm 格式的图片。
	
	第三方主题包，需要的话，复制到指定位置。
	
	文档，需要的话，复制到指定位置。


安装 pyinstaller 用于打包 exe
==========================================

问题是， python 3.6 已经 停止更新了，不能无脑安装最新版。不然，安装要简单点。

查了一下，4.10 版支持 python 3.6 。

- 安装 python 3.6.8 之前说过了，去看前一篇（考虑到兼容性，用的 python 版本老一点）

- 更新 pip 到 21.3.1 之前说过了，去看前一篇（python 3.6 停止更新了，不能无脑安装最新版）

- 安装 Pillow 库，之前说过了，去看前一篇（python 3.6 停止更新了，不能无脑安装最新版）

- 安装 pyinstaller 4.10 （python 3.6 停止更新了，不能无脑安装最新版） ::
		
		考虑到一个问题，pyinstaller 它依赖几个其它的库的，
		而其它的库指定的一般是最小版本，
		现在新版本，也许，我是说也许，会差得太多，
		所以我每一个，都找了一下时间和 pyinstaller 4.10 差不多的版本，
		先安装其它的依赖，
		最后再安装 pyinstaller 4.10
		
		用中转器的话，如下：
		（不用中转器的话，
		（把 py -3.6 替换为 python.exe 的完整路径 (或者 python.exe，如果它在 path 里 )
		（也可以，
		（把 py -3.6 -m pip 替换为 pip.exe 的完整路径 (或者 pip.exe，如果它在 path 里 )
		
		py -3.6 -m pip install  --prefer-binary future==0.18.2
		py -3.6 -m pip install  --prefer-binary zipp==3.6.0
		py -3.6 -m pip install  --prefer-binary typing-extensions==3.10.0.2
		py -3.6 -m pip install  --prefer-binary pywin32-ctypes==0.2.0
		py -3.6 -m pip install  --prefer-binary pefile==2021.9.3
		py -3.6 -m pip install  --prefer-binary pyinstaller-hooks-contrib==2022.0
		py -3.6 -m pip install  --prefer-binary altgraph==0.17.2
		py -3.6 -m pip install  --prefer-binary setuptools==58.0.4
		py -3.6 -m pip install  --prefer-binary importlib-metadata==4.7.1
		py -3.6 -m pip install  --prefer-binary pyinstaller==4.10
		
		
		如果觉得，安装时，其它依赖自动选择版本，也没有什么问题的话，可以试试直接安装 pyinstaller 4.10：
		py -3.6 -m pip install  --prefer-binary pyinstaller==4.10
		
		
		如果是新版本的 python ，不像 python 3.6 这种停止更新维护的，
		可以无脑安装，
		不用指定版本，默认应该是装上最新的版本
		不用加 --prefer-binary 参数，也不会有问题

打包 exe 
=============================

非常简单。需要的时间，也很短，一小会儿，毕竟是个很小的程序。

到目前为止，python 很干净，更新了 pip ，安装了 Pillow 、pyinstaller ， 没有安装其它的第三方库。
	
	据说呢，如果安装了其它的第三方库，有可能影响到 打包 exe ，体积可能会很大。
	那么。
	如果，你安装了很多其它的第三方库，其实就说明，你是 python 的老用户了。
	这种情况下，如果发现打包出来的 exe 很大，可以考虑创建一个 python 这样，就可以隔离开来，不会受到其它的的影响。
	既然是老用户了，应该不用我再说明如何弄一个 虚拟环境了，python 官方文档里，可以搜索 venv 了解一下

找到 python 所在的文件夹，那里有一个 Scripts 文件夹。

安装 pyinstaller 之后， Scripts 文件夹 里会有 pyinstaller.exe ，用的就是它。

命令行，进入源代码 JJui.pyw 所在的文件夹。

打包指令：
::

	如果在 PATH 里：
	
		pyinstaller.exe JJui.pyw
	
	如果不在 PATH 里
	
		（完整路径可能有一长串）\pyinstaller.exe JJui.pyw

因为 .pyw 的后缀，默认是 有窗口界面的程序。
如果需要带命令行界面的，可以改为 .py ，或者 阅读 pyinstaller 的说明，查看具体指令。

会生成一个 dist 文件夹，生成的新 exe 就在里面。
exe 不是单文件，而是一整个文件夹，一起复制出来。
因为 pyinstaller 打包的单文件的 exe ，需要先解压一堆文件出来到临时文件夹，再执行，麻烦，文件多的话，还有点慢，而使用的 tkinter 库，文件虽然不太，但是文件真的很多。

打包完成以后，把源代码中的图片复制过去，目录结构不变。

第三方主题包，需要的话，复制到指定位置；文档，需要的话，复制到指定位置。