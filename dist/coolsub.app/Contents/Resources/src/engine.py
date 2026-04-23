# -*- coding: utf-8 -*-
# Copyright (c) 2026 jhihhe. All rights reserved.
# Project: coolsub

import os
import pysubs2
from src.styles import STYLES, SubtitleStyle

def process_subtitle(input_path, style_key="immersive_serif"):
    """
    Process subtitle file and save as ASS in the same directory.
    """
    if not os.path.exists(input_path):
        return False, f"文件不存在: {input_path}"
    
    try:
        # Load subtitle with encoding detection
        # pysubs2.load supports encoding parameter, but we can try to detect or let it handle
        try:
            subs = pysubs2.load(input_path, encoding="utf-8")
        except UnicodeDecodeError:
            try:
                subs = pysubs2.load(input_path, encoding="utf-16")
            except:
                subs = pysubs2.load(input_path) # Fallback to default detection
        
        # Get style configuration
        style_config = STYLES.get(style_key, STYLES["immersive_serif"])
        
        # Set standard canvas resolution for consistent rendering
        subs.info["PlayResX"] = 1920
        subs.info["PlayResY"] = 1080
        
        # Create new ASS style
        new_style = pysubs2.SSAStyle()
        # Ensure fontname is a single string and handle potential fallback
        font_name = str(style_config.font_name).split(",")[0].strip()
        new_style.fontname = font_name
        new_style.fontsize = float(style_config.font_size)
        def parse_ass_color(color_str):
            # &HAABBGGRR or &HBBGGRR
            c = str(color_str).replace("&H", "")
            if len(c) == 8:
                a, b, g, r = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), int(c[6:8], 16)
            elif len(c) == 6:
                a, b, g, r = 0, int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            else:
                a, b, g, r = 0, 255, 255, 255
            return pysubs2.Color(r, g, b, a)

        new_style.primarycolor = parse_ass_color(style_config.primary_color)
        new_style.outlinecolor = parse_ass_color(style_config.outline_color)
        new_style.outline = float(style_config.outline_width)
        new_style.shadow = float(style_config.shadow_width)
        new_style.bold = bool(style_config.bold)
        new_style.marginv = int(style_config.margin_v)
        
        # Add style to subtitle object
        style_name = "CustomStyle"
        subs.styles[style_name] = new_style
        
        # Apply style to all lines
        for line in subs:
            line.style = style_name
            # Adjust bilingual ratio (assuming newline separates Chinese and English)
            # Scaling English part to 0.75 of Chinese part
            if "\\N" in line.text:
                parts = line.text.split("\\N", 1)
                line.text = f"{parts[0]}\\N{{\\fscx75\\fscy75}}{parts[1]}"
            
        # Generate output path
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_{style_key}.ass"
        
        # Save as ASS
        subs.save(output_path)
        return True, output_path
        
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Test logic removed for production
    pass
