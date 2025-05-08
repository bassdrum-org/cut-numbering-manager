"""
カット情報モデル
Data model for cut information.
"""

import re
from cut_numbering_manager.config import (
    DEFAULT_PART_NAME, 
    DEFAULT_SCENE_NAME, 
    DEFAULT_CUT_NUMBER, 
    DEFAULT_VERSION
)


class CutInfo:
    """Cut information data model"""
    def __init__(self):
        self.part_name = DEFAULT_PART_NAME
        self.scene_name = DEFAULT_SCENE_NAME
        self.cut_number = DEFAULT_CUT_NUMBER
        self.version = DEFAULT_VERSION
    
    def increment_cut(self):
        """Increment cut number and reset version"""
        self.cut_number += 1
        self.version = 1
    
    def increment_version(self):
        """Increment version number only"""
        self.version += 1
    
    def get_formatted_cut_number(self):
        """Get formatted cut number with leading zeros"""
        return str(self.cut_number).zfill(3)
    
    def get_formatted_version(self):
        """Get formatted version with leading v and zeros"""
        return f"v{str(self.version).zfill(2)}"
    
    @staticmethod
    def sanitize_filename(name):
        """Remove invalid characters from filename"""
        return re.sub(r'[\\/*?:"<>|]', "_", name)
