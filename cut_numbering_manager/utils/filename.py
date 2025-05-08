"""
ファイル名ユーティリティ
Utilities for filename generation and handling.
"""

from cut_numbering_manager.models.cut_info import CutInfo


def generate_filename(cut_info):
    """Generate a filename from cut information"""
    part = CutInfo.sanitize_filename(cut_info.part_name)
    scene = CutInfo.sanitize_filename(cut_info.scene_name)
    cut = cut_info.get_formatted_cut_number()
    version = cut_info.get_formatted_version()
    
    return f"{part}_{scene}_{cut}_{version}"
