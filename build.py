import PyInstaller.__main__
import os
import shutil

def build():
    # Application name
    app_name = "coolsub"
    
    # Entry point
    entry_point = "src/main.py"
    
    # Arguments for PyInstaller
    args = [
        entry_point,
        '--name=%s' % app_name,
        '--windowed',        # No console for macOS .app
        '--onefile',         # Bundle into a single executable (or directory)
        '--noconfirm',
        '--clean',
        '--add-data=src/styles.py:src',
        '--add-data=src/engine.py:src',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print(f"\nBuild Success! The .app is located in dist/{app_name}.app")

if __name__ == "__main__":
    build()
