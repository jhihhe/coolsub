# -*- coding: utf-8 -*-
# Copyright (c) 2026 jhihhe. All rights reserved.
# Project: coolsub

from dataclasses import dataclass
from PySide6.QtGui import QColor

@dataclass
class SubtitleStyle:
    name: str
    font_name: str
    font_size: int
    primary_color: str  # &HBBGGRR
    outline_color: str
    outline_width: float
    shadow_width: float
    bold: bool = False
    margin_v: int = 45
    description: str = ""

    def get_qcolor(self, color_str):
        # &HBBGGRR or &HAABBGGRR
        c = color_str.replace("&H", "")
        if len(c) == 8:
            a, b, g, r = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), int(c[6:8], 16)
        elif len(c) == 6:
            a, b, g, r = 0, int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        else:
            return QColor(255, 255, 255)
        # ASS Alpha is 0-255 where 0 is opaque. QColor Alpha is 0-255 where 255 is opaque.
        return QColor(r, g, b, 255 - a)

STYLES = {
    "immersive_serif": SubtitleStyle(
        name="沉浸宋体 (Immersive Serif)",
        font_name="Source Han Serif SC, 思源宋体 SC, Songti SC",
        font_size=20,
        primary_color="&H00E8E8E8", # 柔和灰白
        outline_color="&H00000000",
        outline_width=0.8,
        shadow_width=0,
        margin_v=50,
        description="极致克制，如阅读纸质书般的电影质感"
    ),
    "modern_minimal": SubtitleStyle(
        name="现代极简 (Modern Minimalist)",
        font_name="PingFang SC, 微软雅黑, sans-serif",
        font_size=18,
        primary_color="&H00FFFFFF",
        outline_color="&H40000000", # 半透明描边
        outline_width=1.0,
        shadow_width=0,
        bold=True,
        margin_v=40,
        description="清爽利落，适合现代剧集与纪录片"
    ),
    "classic_cinema": SubtitleStyle(
        name="经典影院 (Classic Cinematic)",
        font_name="Heiti SC, 黑体",
        font_size=22,
        primary_color="&H0000E6FF", # 经典电影淡黄
        outline_color="&H00000000",
        outline_width=1.5,
        shadow_width=1.0,
        margin_v=35,
        description="怀旧复古，浓郁的胶片电影氛围"
    ),
    "netflix_orange": SubtitleStyle(
        name="网飞橙 (Netflix Orange)",
        font_name="PingFang SC, Helvetica, sans-serif",
        font_size=20,
        primary_color="&H000088FF", # Netflix Orange (BBGGRR: 00 88 FF -> RGB: FF 88 00)
        outline_color="&H00000000",
        outline_width=1.2,
        shadow_width=0,
        bold=True,
        margin_v=45,
        description="Netflix 标志性橙色，高辨识度与现代感"
    ),
    "doc_yellow": SubtitleStyle(
        name="纪实金黄 (Documentary Yellow)",
        font_name="Source Han Sans SC, 思源黑体 SC",
        font_size=19,
        primary_color="&H0000CCFF", # 经典纪录片黄
        outline_color="&H00000000",
        outline_width=1.0,
        shadow_width=1.0,
        margin_v=40,
        description="经典 BBC/国家地理纪录片风格，专业且醒目"
    ),
    "midnight_ghost": SubtitleStyle(
        name="深夜幽灵 (Midnight Ghost)",
        font_name="Source Han Serif SC, 思源宋体 SC",
        font_size=21,
        primary_color="&H00DB7093", # 淡淡的紫色
        outline_color="&H00330033",
        outline_width=0.5,
        shadow_width=3.0,
        margin_v=50,
        description="幽暗深邃的紫色调，适合悬疑或深夜剧集"
    )
}
