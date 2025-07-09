#!/usr/bin/env python3
"""
Test script to verify prefix functionality works correctly
"""

from cut_numbering_manager.models.cut_info import CutInfo
from cut_numbering_manager.utils.filename import generate_filename
from cut_numbering_manager.models.filename_config import FilenameConfig

def test_prefix_functionality():
    """Test that prefixes are properly applied to filenames"""
    print("Testing prefix functionality...")
    
    cut_info = CutInfo()
    cut_info.part_name = 'TestPart'
    cut_info.scene_name = 'TestScene'
    cut_info.cut_number = 1
    cut_info.version = 1
    
    prefixes = {
        FilenameConfig.PART: 'P_',
        FilenameConfig.SCENE: 'S_',
        FilenameConfig.CUT: 'C',
        FilenameConfig.VERSION: 'v'
    }
    
    filename_with_prefix = generate_filename(cut_info, None, prefixes)
    print(f'Generated filename with prefixes: {filename_with_prefix}')
    
    filename_no_prefix = generate_filename(cut_info, None, {})
    print(f'Generated filename without prefixes: {filename_no_prefix}')
    
    filename_default = generate_filename(cut_info, None, None)
    print(f'Generated filename with default prefixes: {filename_default}')
    
    expected_with_prefix = "P_TestPart_S_TestScene_C001_v01"
    if filename_with_prefix == expected_with_prefix:
        print("✓ Prefix functionality working correctly!")
        return True
    else:
        print(f"✗ Expected: {expected_with_prefix}, Got: {filename_with_prefix}")
        return False

if __name__ == "__main__":
    success = test_prefix_functionality()
    exit(0 if success else 1)
