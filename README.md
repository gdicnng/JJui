# JJui

![Image](docs/source/jjui/images/001_preview_1.png)

JJui 是一款功能简陋的前端，用于显示 MAME 的游戏列表。
>所以，  
首先得下载一个 MAME ，  
然后再打开 JJui ，  
选择 MAME 程序，  
从 MAME 中读取数据，完成初始化……

----

JJui 用来显示 MAME 主列表。（主要是街机部分）

JJui_sl 用来显示 MAME Software List 。 (这个使用起来麻烦点，得先设置运行参数，否则运行不了，具体先查看一下说明)

----

如果使用的是 已经 打包好的 可执行程序，将程序从压缩包中，解压缩出来，放在某个文件夹中（不要放在权限比较特殊的文件夹中），运行程序。

>生成的 exe ，没有数字签名什么的，杀毒软件容易报毒

----

如果使用源代码的话，因为程序是用 Python 语言写的，可以用 Python 3 打开 JJui.pyw 或者 JJui_sl.pyw 。需要安装第三方库 pillow 。
>pillow ：第三方库  
>>需要在 Python 中 安装上 pillow 。  

>tkinter : 属于标准库  

>>Windows 操作系统，官网的 Python 安装包程序已经包含了 tkinter ，安装时，默认已经勾选了这个。

>>Windows 操作系统，有免安装的版本（文件名有 embed ），此版本不包含 tkinter ，这个不行。

关于源代码中的文件

>JJui.pyw 文件，源代码，可以用 python 运行此脚本 ，用于显示 MAME 游戏列表

>JJui_sl.pyw 文件，源代码，可以用 python 运行此脚本，用于显示 MAME Software List 游戏列表（这个使用麻烦，先看说明）

>jjui_source 文件夹，用于存放 其它 源代码，以及 内置的几个小图片

>.jjui 文件夹，用于存放：配置文件 jjui.ini 、游戏列表翻译文件、第三方主题包、……等

>docs 文件夹，说明文件的源代码

>folders 文件夹，放了几个第三方目前的模板文件，不需要的话，删了就行

>其它可以忽略

----
PPXCLUB 发布页面:
>https://www.ppxclub.com/forum.php?mod=viewthread&tid=705838

----

在线说明：
>https://jjui.readthedocs.io/

>https://jjui.rtfd.io/

----

releases 程序发布页面：

>https://github.com/gdicnng/JJui/releases

>自动将 python 源代码 转为 exe 文件

>这里有自动编译的生成的 exe 

>操作系统比较新，生成的 exe 在老版本的操作系统上，可能兼容性不好

>下面百度网盘中，有手动编译的 exe 文件，在老版本操作系统（虚拟机）上 生成 的 exe ，对老系统兼容性更好。

----

第三方主题包：
>https://github.com/gdicnng/JJui_themes

将 .jjui 文件夹，复制过去

----

百度网盘：
>不知道百度网盘的链接能活多久

>链接：https://pan.baidu.com/s/1guTSDIWr66S6ewIdyMQPjA

>提取码：r9b9 

----
