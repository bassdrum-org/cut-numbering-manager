"""
ファイル名ユーティリティ
Utilities for filename generation and handling.
"""

from cut_numbering_manager.models.cut_info import CutInfo
from cut_numbering_manager.models.filename_config import FilenameConfig


def generate_filename(cut_info, element_order=None):
    """Generate a filename from cut information"""
    part = CutInfo.sanitize_filename(cut_info.part_name)
    scene = CutInfo.sanitize_filename(cut_info.scene_name)
    cut = cut_info.get_formatted_cut_number()
    version = cut_info.get_formatted_version()
    
    elements = {
        FilenameConfig.PART: part,
        FilenameConfig.SCENE: scene,
        FilenameConfig.CUT: cut,
        FilenameConfig.VERSION: version
    }
    
    if element_order is None:
        element_order = FilenameConfig.DEFAULT_ORDER
    
    filename_parts = [elements[element] for element in element_order]
    return "_".join(filename_parts)
