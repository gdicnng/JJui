# -*- coding: utf_8_sig-*-

gamelist_type = "mame"
# 主脚本中确定
    # "mame"
    # "softwarelist"
    # if global_variable.gamelist_type == "softwarelist":

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
tk_text_1 = None
    #文本一
    #文本二
the_index = None # 退出时，需要记录 目录 的选项


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
columns_index = {} # 
    # {"name":0,……，……，……，}
    # 方便对得到 columns 数字 index

machine_dict = {} # game list data，dict 格式，
    # 在读取基本数据后，赋值
    # 状态栏得到 id
    #   然后
set_data={}
dict_data={}
    # 周边用到
internal_index={}
##
external_index={}
#
external_index_files_editable =set()
external_index_files_be_edited=set()

# 拥有列表
available_set = set()
# 过滤列表
available_hide_set = set()
# 拥有列表 其它过滤项
available_filter_set = set()





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
#font_gamelist_header = "TkDefaultFont"
#font_label           = "TkDefaultFont"
#font_button          = "TkDefaultFont"
#font_menu            = "TkDefaultFont"
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