==========================================
python 与 JJui
==========================================

用 python 运行 JJui
===================================

Python：
	
	https://www.python.org/

JJui 是用 python 语言写的。

可以用 python 3 运行 JJui ： 
	
	鼠标双击运行： ::
		
		（需要安装好第三方库 Pillow）
		
		鼠标双击 JJui.pyw ，应该能打开并运行程序。
		
		如果没能正常打开：
			
			检查一下 Pillow
			  检查一下你所用的 Python 有没安装好第三方 Pillow 库。
			
			检查一下文件关联
			  检查一下 *.py  文件，有没有正确关联到 启动器 py.exe  或者 某个版本的 python.exe 。
			  检查一下 *.pyw 文件，有没有正确关联到 启动器 pyw.exe 或者 某个版本的 pythonw.exe 。

	命令行中运行： ::
		
		（需要安装好第三方库 Pillow）
		
		命令行进入 JJui.pyw 所在的文件夹。
			
			（如果没有进入此文件夹：下面的 JJui.pyw 文件，替换为文件的完整路径）
		
		py.exe JJui.pyw
		
		或者
		
		python.exe JJui.pyw
			
			（有的版本的命令行，默认，鼠标点一下就暂停了）
			（如果遇到这种情况，觉得碍事，可以自己稍微设置一下命令行）
			需要注意，不要让命令行暂停了，
			GUI 主程序 一般是单线程的，前面命令行暂停了，GUI 程序 就卡死了。
		
		
		pyw.exe JJui.pyw
		
		或者
		
		pythonw.exe JJui.pyw
			
			这个会屏蔽掉所有命令行中显示的文字内容，不显示任何消息。
			感觉这个不是在命令行里用的。
			感觉这种就是专门给 GUI 程序做的，适合 鼠标双击 *.pyw 运行程序。
		
		上面命令行中 用 python.exe ，是假设它所在的位置，已正确设置到 环境变量 PATH 里。
		环境变量 PATH 不了解，或者不想管，可以用 py.exe ，这个简单一点。
		
		py.exe 是启动器，现在 官方 Python 安装包，安装时的选项，默认都有选上这个。
		我看到启动器直接安装到了 C:\Windows 文件夹，一般不用担心 环境变量 PATH 的设置。
		命令行中 用启动器 ，可能方便一点；
		安装多个版本 Python 时，也方便切换 不同版本的 Python 。
		py.exe  会跳转到 默认版本的 python.exe
		pyw.exe 会跳转到 默认版本的 pythonw.exe
		指定 Python 版本的话，比如：
			py.exe -3.9 JJui.pyw
			py.exe -3.12 JJui.pyw
		


UI 库 用的是 tkinter 。
	
	windows 版，python 官网的安装包，默认已经包含了 tkinter，安装时有选项默认已经选上了。
	
	windows 版，python 官网 还提供一种 免安装的，嵌入式发行版（文件名里有 embed ），这个不包含 tkinter 。
	所以不用这个。

使用了第三方库 Pillow 。图片的缩放功能用的这个库。这个需要自己额外安装一下。
	
	| https://pypi.org/project/Pillow
	| https://python-pillow.org
	
	Pillow 可以通过 pip 安装。
		
		如果 Python 版本比较新，还在更新维护，安装还是很方便的： ::
			
			如果需要更新 pip （按 pip 的说明，pip setuptools wheel 最好一起更新）
				
				python.exe -m pip install --upgrade pip setuptools wheel
			
			安装更新 Pillow
				
				python.exe -m pip install --upgrade Pillow
				
				可以指定使用二进制的安装包（免得自动下载到源代码的安装包）：
				
					python.exe -m pip install --only-binary :all: --upgrade Pillow
					
					或
					
					python.exe -m pip install --prefer-binary --upgrade Pillow
		
		如果用 老版本的 Python ，已经停止更新维护的版本： ::
			
			pip
				最新版本的 pip 可能不支持 老版本的 Python 。
				如果 pip 需要更新的话，得先去了解一下兼容性，可以去查看一下 pip 更新记录，看看哪些版本能用。
				如果需要更新 pip ，估计得指定更新到合适的版本。
			
			Pillow
				
				得去看看 Pillow 对各版本 Python 的兼容性情况。
				安装时指定一个合适的版本。或者 指定 版本范围。
				安装时指定使用二进制的安装包（免得自动下载到源代码的安装包）。


将 JJui 源代码转为 .exe 格式的程序
=======================================

可以用 pyinstaller 。
	
	https://pypi.org/project/pyinstaller
	
	用 pip 安装 pyinstaller
		
		python.exe -m pip install pyinstaller
	
	用 pyinstaller 将 JJui.pyw 转换为 .exe ：
		
		转换为 单个 .exe 文件
			
			python.exe -m PyInstaller -F JJui.pyw
			
			注意：
			生成 .exe 文件后，需要 把 源代码中的图片 复制过去。图片的路径不变。
			
			这种的话，其实是假的单个 exe 文件，
			运行时，
			还需要先将所有东西解压缩到系统的临时文件夹中，
			效率不行。
			
			效率不行，最好不用这种。
		
		转换为 文件夹
			
			python.exe -m PyInstaller JJui.pyw
			
			注意：生成 .exe 文件后，需要 把 源代码中的图片 复制过去。图片的路径不变。
			
			一个文件夹里，除了 .exe 文件，还有它所的依赖的一些文件。
			
			| 这种缺点是一大堆文件，比较乱。
			| 试了一下， pyinstaller 新版本，似乎好了一点，大堆文件移到了子文件夹中。
			

如果用其它的工具转为 .exe 程序，也是可以的。
	
	可能需要改一点点，不同的工具，定位 .exe 程序的位置，可能方法不一样：
	
		以下这段代码
			
			如果，
			用 python 运行 JJui.pyw 的话，
			当前工作文件夹 切换到 JJui.pyw 所在的文件夹。
			
			如果，
			用 pyinstaller 成生的 exe 程序。
			运行 exe 的时候，
			当前工作文件夹 切换到 .exe 所在的文件夹。
			
			| 因为我程序里是以 当前工作文件夹 为基准点，定位程序需要的其它的文件，比如配置文件、内置的几张小图片等；
			| 以及 MAME程序、MAME周边图片、MAME周边文档等，在设置路径时，可能会使用相对路径，相对路径也使用它作为基准点。
			
			如果你用其它的工具转 exe ，可能要改一下这地方
			
			方便你查找的话，这段代码如下：
			
			::
				
				def change_working_directory():
				    if getattr(sys, "frozen", False):
				        # pyinstaller 生成的 exe 程序，在运行
				        # 这判断的方式是 pyinstaller 用的，其它的工具，可能不同
				        executable_path = os.path.dirname(sys.executable)
				        executable_path = os.path.abspath(executable_path)
				        os.chdir( executable_path )
				    else:
				        # python 在运行 源代码 文件
				        the_script_path = os.path.dirname(__file__)
				        the_script_path = os.path.abspath(the_script_path)
				        os.chdir( the_script_path )