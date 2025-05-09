# === config.py ===

import os
import sys

# 支持 PyInstaller 下访问资源路径
def resource_path(relative_path):
    """返回运行时或开发环境下的资源路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

config = {
    'image_folder': resource_path("images"),
    'output_base': "result_output",
    'num_old_pairs': 8,
    'num_similar_pairs': 8,
    'num_new_items': 44,
    'min_separation': 10,
    'max_separation': 40,
    'response_keys': {
        'b': 'N',  # press key 'b' means NEW
        'n': 'O',  # press key 'n' means OLD
        'm': 'S'   # press key 'm' means SIMILAR
    },
    'fixed_duration': 2.0, # s
    'isi_duration': 0.5,  # s
}