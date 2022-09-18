==========================================
PATH
==========================================

环境变量中的 PATH ，指定可执行文件的搜索路径。
	
	在 CMD 命令行当中输入 ``PATH`` 指令，查看
	
	PowerShell 命令行中输入 ``echo $env:PATH`` 指令，查看

比如，命令行里输入指令 ``ping baidu.com`` ，
	
	我现在电脑上，这里的 ping 是指 ``C:\Windows\System32\PING.EXE``
	
	不用输入完整的 ping.exe 的路径 ``C:\Windows\System32\PING.EXE``
	
	输入 ping.exe 或 ping 就行
	
	因为 它 所在的文件夹 在 PATH 中

安装 python 的时候，有个选项，添加到 PATH，其实如果你仅打算安装 python 来运行 JJui ，完全可以不管这个。

打开 命令行 cmd 。
输入一条指令 ，随意进入一个文件夹，输入 python.exe (或者省略为 python)。
如果不在 PATH 环境变量里，并且当前文件夹里也没有 同名的程序，那么命令行会给出错信息,因为它找不到 python.exe 在哪里。
如果能执行 python ，说明，它在环境变量里，这样，你在命令行里使用它比较方便，输入 python.exe 就行了，而不用输入完整的可能很长很长的路径，比如 ``C:\xxx\yyy\zzz\???\python.exe`` 这种。

如果只安装一个版本的 python ，选上也是方便的。

如果安装多个版本的 python ，建议不要选上，添加太多文件夹到 环境变量 PATH 里，显得太乱。

安装 python ，如果你选择了 添加到 PATH ，应该会添加以下两个文件夹到环境变量里：
	
	一个是 python.exe、 pythonw.exe 所在的文件夹。

	另一个是 此文件夹下面的 Scripts 文件夹（里包应该有一个 pip.exe ，以及其它(如果安装其它许多的第三方库，这个文件夹里会有更多东西)）。

