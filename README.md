#### Prerequisites
- Python 3.10
- PIP

#### Installation:
`git clone "repo_link" or unpack the archive`  
`pip install --upgrade pip`
+ Create and activate virtual environment:
  + Linux / macOS  
  `python3 -m venv /path_to_virtual_environment/venv`  
  `source /path_to_virtual_environment/venv/bin/activate`  
  + Windows:  
  `python -m venv \path_to_virtual_environment\venv`  
  `\path_to_virtual_environment\venv\bin\activate.bat`
+ Install requirements:  
`python -m pip install -r requirements.txt`
+ Install precompiled ta-lib (indicators):  
  + To avoid issues place downloaded file at the toot of the project and then install  
  + Linux - Download cp310 x64 version lib from: 
  https://www.wheelodex.org/projects/ta-lib-precompiled/  
  `python -m pip install TA_Lib_Precompiled-0.4.25-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`  
  + Windows - Download cp310 x64 version lib from:  
  https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib   
  `python -m pip install TA_Lib‑0.4.24‑cp310‑cp310‑win_amd64.whl`
+ Sometimes it may happen, that matplotlib will not draw the graphic window. To fix this install this package under with activated venv:  
`python -m pip install PyQt5`
