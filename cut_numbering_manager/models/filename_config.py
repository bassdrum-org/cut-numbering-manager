"""
ファイル名設定モデル
Data model for filename configuration.
"""

class FilenameConfig:
    """Filename configuration data model"""
    
    PART = "part"
    SCENE = "scene"
    CUT = "cut"
    VERSION = "version"
    
    DEFAULT_ORDER = [PART, SCENE, CUT, VERSION]
    DEFAULT_PREFIXES = {
        PART: "",
        SCENE: "",
        CUT: "",
        VERSION: "v"
    }
    
    def __init__(self):
        self.element_order = self.DEFAULT_ORDER.copy()
        self.prefixes = self.DEFAULT_PREFIXES.copy()
    
    def get_element_order(self):
        """Get current element order"""
        return self.element_order
    
    def set_element_order(self, new_order):
        """Set new element order"""
        if sorted(new_order) == sorted(self.DEFAULT_ORDER):
            self.element_order = new_order
            return True
        return False
    
    def move_element_up(self, element):
        """Move element up in the order"""
        if element in self.element_order:
            idx = self.element_order.index(element)
            if idx > 0:
                self.element_order[idx], self.element_order[idx-1] = self.element_order[idx-1], self.element_order[idx]
                return True
        return False
    
    def move_element_down(self, element):
        """Move element down in the order"""
        if element in self.element_order:
            idx = self.element_order.index(element)
            if idx < len(self.element_order) - 1:
                self.element_order[idx], self.element_order[idx+1] = self.element_order[idx+1], self.element_order[idx]
                return True
        return False
    
    def get_element_name(self, element):
        """Get display name for element"""
        names = {
            self.PART: "パート",
            self.SCENE: "シーン",
            self.CUT: "カット",
            self.VERSION: "バージョン"
        }
        return names.get(element, element)
    
    def get_prefix(self, element):
        """Get prefix for element"""
        return self.prefixes.get(element, "")
    
    def set_prefix(self, element, prefix):
        """Set prefix for element"""
        if element in self.DEFAULT_ORDER:
            self.prefixes[element] = prefix
            return True
        return False
    
    def get_all_prefixes(self):
        """Get all prefixes"""
        return self.prefixes
    
    def set_all_prefixes(self, prefixes):
        """Set all prefixes"""
        for element, prefix in prefixes.items():
            if element in self.DEFAULT_ORDER:
                self.prefixes[element] = prefix
