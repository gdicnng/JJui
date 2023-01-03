# -*- coding: utf_8_sig-*-

if __name__ == "__main__" :
    import builtins
    from .translation_ui  import translation_holder
    builtins.__dict__['_'] = translation_holder.translation


from . import global_variable

# 游戏列表 列标题
columns_translation = {
        # "#0":"",
        "name"        :_("缩写"),
        "year"        :_("年代"),
        "sourcefile"  :_("源代码"),
        "manufacturer":_("制造商"),
        "cloneof"     :_("主版本"),
        "translation" :_("游戏名(译)"),
        "description" :_("游戏名英文"),
        "status"      :_("模拟状态"),
        "savestate"   :_("存档状态"),
        }
if global_variable.gamelist_type == "softwarelist":
    columns_translation = {
            # "#0":"",
            #"xml"         :_(""),
            "name"        :_("缩写"),
            "year"        :_("年代"),
            "publisher"   :_("出版商"),
            "cloneof"     :_("主版本"),
            "translation" :_("游戏名(译)"),
            "description" :_("游戏名英文"),
            "alt_title"   :_("备注名"),
            "supported"   :_("支持"),
            }

# 目录列表，
index_translation = {
        'all_set'           :_('所有列表'),
        'available_set'     :_('拥有列表'),
        'unavailable_set'   :_('未拥有列表'),
        'parent_set'        :_('主版本'),
        'clone_set'         :_('副版本'),
        'bios'              :_('bios'),
        'device'            :_('device'),
        'mechanical'        :_('mechanical'),
        'softwarelist'      :_('software list'),
        'chd'               :_('chd'),
        'sample'            :_('sample'),
        'year'              :_('年代'),
        'manufacturer'      :_('制造商'),
        'sourcefile'        :_('源代码'),
        'status'            :_('模拟状态'),
        'savestate'         :_("存盘状态"),
        'dump'              :_("dump 问题"),
        'sound channels'    :_("声音 通道"),
        'chip cpu'          :_("芯片 cpu"),
        'chip audio'        :_("芯片 audio"),
        'input players'     :_("输入 玩家"),
        'input control'     :_("输入 控制"),
        'display number'    :_("显示 数量"),
        'display type'      :_("显示 种类"),
        'display refresh'   :_("显示 刷新率"),
        'display rotate'    :_("显示 旋转"),
        'display resolution':_("显示 分辨率"),

        #'only_sample_set':'仅需 sample，无需 rom、chd',
        #'no_roms':'无需 rom、chd',
        #'no_rom_chd_sample':'无需 rom、chd、sample',
                    }
if global_variable.gamelist_type == "softwarelist":
    # 目录列表，
    index_translation = {
        'all_set'           :_('所有列表'),
        'available_set'     :_('拥有列表'),
        'unavailable_set'   :_('未拥有列表'),
        'parent_set'        :_('主版本'),
        'clone_set'         :_('副版本'),
        'supported'         :_('支持'),

        #'chd'               :_('chd'),
        #'sample'            :_('sample'),
        'year'              :_('年代'),
        'publisher'         :_('出版商'),
        #'sourcefile'        :_('源代码'),
        #'status'            :_('模拟状态'),
        #'savestate'         :_("存盘状态"),
        #'dump'              :_("dump 问题"),
        #'sound channels'    :_("声音 通道"),
        #'chip cpu'          :_("芯片 cpu"),
        #'chip audio'        :_("芯片 audio"),
        #'input players'     :_("输入 玩家"),
        #'input control'     :_("输入 控制"),
        #'display number'    :_("显示 数量"),
        #'display type'      :_("显示 种类"),
        #'display refresh'   :_("显示 刷新率"),
        #'display rotate'    :_("显示 旋转"),
        #'display resolution':_("显示 分辨率"),

                    }


# ui ,extra ，图片
extra_image_types_translation = {
        "snap"  : _("snap 游戏截图")    ,
        "titles": _("titles 游戏标题图"),
        "flyers": _("flyers 游戏海报")  ,
        
        "cabinets"  :_("图片 cabinets"),
        "cpanel"    :_("图片 cpanel"),
        "devices"   :_("图片 devices"),
        "marquees"  :_("图片 marquees"),
        "pcb"       :_("图片 pcb"),
        "artpreview":_("图片 artpreview"),
        "bosses"    :_("图片 bosses"),
        "ends"      :_("图片 ends"),
        "gameover"  :_("图片 gameover"),
        "howto"     :_("图片 howto"),
        "logo"      :_("图片 logo"),
        "scores"    :_("图片 scores"),
        "select"    :_("图片 select"),
        "versus"    :_("图片 versus"),
        "warning"   :_("图片 warning"),
        "other_image_1"   :_("图片 其它1"),
        "other_image_2"   :_("图片 其它2"),
        "other_image_3"   :_("图片 其它3"),
        #"other_image_4"   :_("图片 其它 4"),
        #"other_image_5"   :_("图片 其它 5"),
        #"other_image_6"   :_("图片 其它 6"),
        
        
                        }


extra_text_types_translation = {
        "history.xml"  : _("历史(xml格式)：history.xml"),
        "history.dat"  : _("历史(dat格式)：history.dat"),
        "mameinfo.dat" : _("文档：mameinfo.dat"),
        "messinfo.dat" : _("文档：messinfo.dat"),
        "gameinit.dat" : _("文档：gameinit.dat"),
        "sysinfo.dat"  : _("文档：sysinfo.dat"),
                        }

extra_text_types_2_translation =  {
        "command.dat"        : _("出招表 中文版 command.dat"),
        "command_english.dat": _("出招表 英文版 command_english.dat"),
                        }

if __name__ =="__main__":
    
    
    pass