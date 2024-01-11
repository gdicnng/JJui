# -*- coding: utf_8_sig-*-

gamelist_type = "mame"
# 主脚本中确定
    # "mame"
    # "softwarelist"
    # if global_variable.gamelist_type == "softwarelist":

flag_setlocale_LC_COLLATE = False
# locale.setlocale(locale.LC_COLLATE,locale="???") 
# 无效的设置，# locale.Error: unsupported locale setting
# 如果设置 成功，记录改为 True

# 程序初始化，读取配置文件，然后，再 赋值

user_configure_data = {}
# 主脚本中就复制过来

user_configure_data_order = []
# 主脚本中就复制过来

user_configure_data_default = {}
# 主脚本中就复制过来

root_window = None

internal_themes = tuple()  # style.theme_names() 返回的是 tuple 
other_themes    = set()    # 第三方主题，用集合

tk_scaling_number_0 = 0 # 启动时 tk_scaling_number 记录

# ttk.Notebook 周边框架
Notebook_for_extra = None
# ttk.PanedWindow 分隔线位置
PanedWindow   = None # 主窗口，两条分隔线
PanedWindow_2 = None # 周边，图片，一条分隔线
    # ttk.PanedWindow 分隔线位置
Combobox_chooser_image_1 = None
Combobox_chooser_image_2 = None
Combobox_chooser_text_1  = None
Combobox_chooser_text_2  = None
#flag tkvar
tkint_flag_for_zip_1 = None
tkint_flag_for_zip_2 = None
tkint_flag_for_text_index_1 = None
tkint_flag_for_text_index_2 = None

#flag bool
flag_mark_unavailable_game = False


#
the_showing_table = None # tk table widget
    # 三个列表，记录哪一个列表，正在显示
all_tables=[]
    # 记录全部，方便设置
tk_text_1 = None
tk_text_2 = None
    #文本一
    #文本二
the_index = None 
    # 记录 目录 ui 
    # 退出时，需要记录 目录 的选项
    # 目录瘦身时，


#状态栏 等 
#remember_id_of_last_choice_tk_var=None
    # tk 初始化，之后，设置 为 tk.StringVar()


#data_from_xml = {}
    # temp_dict["mame_version"]   = mame_version
    # 
    # temp_dict["columns"]        = columns
    # temp_dict["machine_dict"]   = machine_dict
    # 
    # temp_dict["set_data"]       = set_data
    # temp_dict["dict_data"]      = dict_data
    # temp_dict["internal_index"] = internal_index
# 
all_data = {}
mame_version =""
columns      = [] 
    # 所有列，范围
    # 在读取基本数据后，赋值
machine_dict = {}
set_data={}
dict_data={}
    # 周边用到
internal_index={}
#####
columns_index = {} ##
    # {"name":0,……，……，……，}
    # 方便对得到 columns 数字 index
    # 在读取基本数据后，赋值
icon_column_index=None ## 如果列表被删空了，用 None
    # 每个元素中，保存图标颜色相关信息，的项目
    # 在读取基本数据后，赋值
search_columns_set=set()##
    # 列表，搜索设置，选择 搜索哪些 列
    # 每一初始化为全部
    # 在读取基本数据后，初始化
search_ignorecase = 1 # 0
    # 列表，搜索设置，
    # 默认忽略大小写,每次初始化为1

##
external_index={} 
# 外置目录,根据 id 分类
#   读取外置目录，初始化目录时，用一下
#   接收目录信号时，刷新列表时，用一下
#   编辑外部目录时，用一下（在列表右键菜单功能里）
# .ini .sl_ini
############################

# 拥有列表
available_set = set()

# 未拥有列表
unavailable_set = set()

# 屏蔽列表，一直不显示
available_hide_set = set()
    # hide_list.txt      拥有列表 屏蔽项目
all_hide_list = list()
    # hide_list_all.txt  全局列表 屏蔽项目

# 拥有列表 过滤项 （在菜单中选择的过滤项目）
available_filter_set = set() 
    # 仅 mame
    # 程序启动时，从配置文件，读取选项，初始化 赋值
    # 配置文件 "filter" 中，记录 项目 ： ['device', 'bios', 'chd', 'softwarelist', 'mechanical']

filter_set = set() 
    # 全局过滤，不保存
    # 程序启动时 应 更新到 all_hide_set
    # 每一次 变化时 （菜单→游戏列表→全局过滤），应清空，更新到 all_hide_set
filter_list = set() 
    # 记录 全局过滤的项目
    # 不保存
#################################
# 外置目录，只读
external_index_sl_by_xml     = {} 
# sl 外置目录,根据 xml 分类,wip
# 只读目录,不使用编辑功能
#   读取外置目录，初始化目录时，用一下
#   接收目录信号时，刷新列表时，用一下
#   编辑外部目录时，不用这个，不使用编辑功能
#       这样子，简单一点，只需要改前边两处
# .xml_ini
################
# 街机部分，按 source 分类
external_index_by_source = {}
# 未完成
external_index_sl_by_machine = {} # sl 外置目录，根据 machine 分类，wip
#
external_index_files_editable =set()
external_index_files_be_edited=set()







column_group_counter = 1
    # 使用 3 组，用以快速切换，常用显示的项目
    # 1组、2组 方便 中英文 切换显示；
    # 第3组，显示整体


#external_index = {}

#available_gamelist = set()

#filter_set         = set()
#filter_set_for_available = set()


#####
current_item = None
    # 用于记录 当前选中的 游戏 id


# user_configure_data 重复 ？
# 或者用 font_name ???
font_gamelist        = "TkDefaultFont"
font_gamelist_header = "TkDefaultFont"

font_text            = "TkDefaultFont"
font_text_2          = "TkDefaultFont"

font_others           = "TkDefaultFont"
#font_button          = "TkDefaultFont"
#font_menu            = "TkMenuFont"
#font_menu_button     = "TkDefaultFont"
#


# user_configure_data 中已有
# colour
#background         = None
#foreground         = None
#selecetbackground  = None
#selecetforeground  = None
# button 高亮色
# 其它，
#   应该 查看一下第三方主题 ？？

# 周边 文档 建目录 以 加速
extra_index_for_histroty_xml = {}

# ("history.dat","sysinfo.dat",)
extra_index_for_histroty_dat = {}
extra_index_for_sysinfo_dat  = {}

#("mameinfo.dat","messinfo.dat",)
extra_index_for_mameinfo_dat = {}
extra_index_for_messinfo_dat = {}

#"command.dat",
#"command_english.dat",
extra_index_for_command_dat = {}
extra_index_for_command_english_dat = {}

# "gameinit.dat",
extra_index_for_gameinit_dat = {}

# 范围 稍微限制一下
#   哪些游戏，周边图片 使用 4:3 或 3:4 的比例
#   MAME 稍微限制一下
#   MESS 完全没有限制
set_extra_image_keep_aspect_ratio = set()