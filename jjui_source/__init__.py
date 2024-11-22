# -*- coding: utf-8 -*-
import builtins

if "_" not in builtins.__dict__:
    from . import translation_ui
    builtins.__dict__["_"] = translation_ui.translation_holder.translation
    #
    # _
    #
    # 翻译函数名 _
    # 和 gettext 学的，用这个符号。
    # 这样，用 gettext 的工具，也方便提取翻译词条
    #
    # 导入全局
    # 在这里先确保导入全局，方便调用 python -m xxx?.yyy? ，因为其它文件里，使用了 _
    #
    # 先导入 global_variable ，记录表格类型 mame 或者 mame software list
    # 再导入 global_static_filepath ，找到翻译文件位置
    # 找到翻译文件位置，之后，马上读取翻译文件
    #   导入翻译文件之后，才调用其它的包
    #       因为，有些包，导入时，就使用了 _ 函数
