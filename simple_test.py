"""
Simple test to verify our Windows modifications.
"""

import os

def test_files_exist():
    """Test that Windows-specific files exist."""
    files = [
        'Makefile.bat',
        'WINDOWS_SUPPORT.md',
        'test_windows.py',
        'uvloop/includes/compat_win.h'
    ]
    
    missing = []
    for file_path in files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    else:
        print("✅ All Windows-specific files exist")
        return True

def test_setup_modified():
    """Test that setup.py has been modified to remove Windows restriction."""
    try:
        with open('setup.py', 'r') as f:
            content = f.read()
        
        # Check if the Windows restriction is commented out
        if '# raise RuntimeError(\'uvloop does not support Windows at the moment\')' in content:
            print("✅ Windows restriction is commented out in setup.py")
            return True
        elif 'uvloop does not support Windows at the moment' not in content:
            print("✅ Windows restriction has been removed from setup.py")
            return True
        else:
            print("❌ Windows restriction still active in setup.py")
            return False
    except Exception as e:
        print(f"❌ Error checking setup.py: {e}")
        return False

def test_pyproject_updated():
    """Test that pyproject.toml includes Windows classifier."""
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
        
        if 'Operating System :: Microsoft :: Windows' in content:
            print("✅ pyproject.toml includes Windows classifier")
            return True
        else:
            print("❌ pyproject.toml missing Windows classifier")
            return False
    except Exception as e:
        print(f"❌ Error checking pyproject.toml: {e}")
        return False

def test_readme_updated():
    """Test that README.rst mentions Windows support."""
    try:
        with open('README.rst', 'r') as f:
            content = f.read()
        
        if 'Windows Support' in content:
            print("✅ README.rst mentions Windows support")
            return True
        else:
            print("❌ README.rst doesn't mention Windows support")
            return False
    except Exception as e:
        print(f"❌ Error checking README.rst: {e}")
        return False

if __name__ == '__main__':
    print("Testing uvloop Windows modifications...")
    print("=" * 50)
    
    tests = [
        test_files_exist,
        test_setup_modified,
        test_pyproject_updated,
        test_readme_updated
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} checks passed")
    
    if passed == len(tests):
        print("\n🎉 All checks passed! The modifications look good.")
    else:
        print("\n❌ Some checks failed. Please review the issues above.")