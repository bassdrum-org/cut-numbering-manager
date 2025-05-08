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
from cut_numbering_manager.models.filename_config import FilenameConfig


class CutInfo:
    """Cut information data model"""
    def __init__(self):
        self.part_name = DEFAULT_PART_NAME
        self.scene_name = DEFAULT_SCENE_NAME
        self.cut_number = DEFAULT_CUT_NUMBER
        self.version = DEFAULT_VERSION
        self.filename_config = FilenameConfig()
    
    def increment_cut(self):
        """Increment cut number and reset version"""
        self.cut_number += 1
        self.version = 1
    
    def increment_version(self):
        """Increment version number only"""
        self.version += 1
    
    def get_formatted_cut_number(self, prefix=None):
        """Get formatted cut number with custom prefix or default"""
        if prefix is None:
            prefix = self.filename_config.get_prefix(FilenameConfig.CUT)
        
        if not prefix:
            return str(self.cut_number).zfill(3)
        return f"{prefix}{str(self.cut_number).zfill(3)}"
    
    def get_formatted_version(self, prefix=None):
        """Get formatted version with custom prefix or default"""
        if prefix is None:
            prefix = self.filename_config.get_prefix(FilenameConfig.VERSION)
        
        if not prefix and prefix != "":  # Check if None, not empty string
            return f"v{str(self.version).zfill(2)}"
        return f"{prefix}{str(self.version).zfill(2)}"
    
    def get_formatted_part(self, prefix=None):
        """Get formatted part name with custom prefix or default"""
        if prefix is None:
            prefix = self.filename_config.get_prefix(FilenameConfig.PART)
        
        if not prefix:
            return self.part_name
        return prefix
    
    def get_formatted_scene(self, prefix=None):
        """Get formatted scene name with custom prefix or default"""
        if prefix is None:
            prefix = self.filename_config.get_prefix(FilenameConfig.SCENE)
        
        if not prefix:
            return self.scene_name
        return prefix
    
    @staticmethod
    def sanitize_filename(name):
        """Remove invalid characters from filename"""
        return re.sub(r'[\\/*?:"<>|]', "_", name)
