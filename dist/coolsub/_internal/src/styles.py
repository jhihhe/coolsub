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
        name="沉浸苹方 (Immersive PingFang)",
        font_name="PingFang SC",
        font_size=75,
        primary_color="&H00E8E8E8", # 柔和灰白
        outline_color="&H00000000",
        outline_width=2.5,
        shadow_width=0,
        margin_v=45,
        description="极致克制，苹方字体带来的现代电影感"
    ),
    "modern_minimal": SubtitleStyle(
        name="现代极简 (Modern Minimalist)",
        font_name="PingFang SC",
        font_size=70,
        primary_color="&H00FFFFFF",
        outline_color="&H40000000", # 半透明描边
        outline_width=3.0,
        shadow_width=0,
        bold=True,
        margin_v=40,
        description="清爽利落，适合现代剧集与纪录片"
    ),
    "classic_cinema": SubtitleStyle(
        name="经典影院 (Classic Cinematic)",
        font_name="PingFang SC",
        font_size=82,
        primary_color="&H0000E6FF", # 经典电影淡黄
        outline_color="&H00000000",
        outline_width=4.5,
        shadow_width=3.0,
        margin_v=35,
        description="怀旧复古，浓郁的胶片电影氛围"
    ),
    "netflix_orange": SubtitleStyle(
        name="网飞橙 (Netflix Orange)",
        font_name="PingFang SC",
        font_size=75,
        primary_color="&H000088FF", # Netflix Orange
        outline_color="&H00000000",
        outline_width=3.5,
        shadow_width=0,
        bold=True,
        margin_v=45,
        description="Netflix 标志性橙色，高辨识度与现代感"
    ),
    "doc_yellow": SubtitleStyle(
        name="纪实金黄 (Documentary Yellow)",
        font_name="PingFang SC",
        font_size=72,
        primary_color="&H0000CCFF", # 经典纪录片黄
        outline_color="&H00000000",
        outline_width=3.0,
        shadow_width=2.5,
        margin_v=40,
        description="经典 BBC/国家地理纪录片风格，专业且醒目"
    ),
    "midnight_ghost": SubtitleStyle(
        name="深夜幽灵 (Midnight Ghost)",
        font_name="PingFang SC",
        font_size=78,
        primary_color="&H00DB7093", # 淡淡的紫色
        outline_color="&H00330033",
        outline_width=1.5,
        shadow_width=10.0,
        margin_v=55,
        description="幽暗深邃的紫色调，适合悬疑或深夜剧集"
    )
}
