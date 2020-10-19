import cx_Freeze


cx_Freeze.setup(
	name="GUI client",
	version = "3.8.6",
	options={"build_exe": {"packages":["pygame"],
				"include_files":["Image/",
				"Connect4Logo.png", "EuchreLogo.png", "MellowLogo.png", "ReversiLogo.png", "versNumber.png", "versNumber1.png", "versNumber2.png"]}},
	description = "Program with which the Tardibuono family can play mellow",
	executables = [cx_Freeze.Executable("start.py", base ="Win32GUI")]
	)

#python setup.py build

#Bug fix:had to take away all prints in serverListener functions to make it work.
# I don't know why that was a problem
#https://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6

#You could delete scipy to make more room

#Recent install notes:

#sites used:
#https://cx-freeze.readthedocs.io/en/latest/installation.html
#https://www.youtube.com/watch?v=GSoOwSqTSrs&t=386s
#https://www.youtube.com/watch?v=DoHWJV8iVTQ (not used)

#C:\Users\Michael\Desktop\cardGamePython\MellowPyGUI>pip install cx_Freeze --upgrade
#Collecting cx_Freeze
#  Downloading cx_Freeze-6.2-cp38-cp38-win_amd64.whl (206 kB)
#     |████████████████████████████████| 206 kB 939 kB/s
#Installing collected packages: cx-Freeze
#Successfully installed cx-Freeze-6.2
#WARNING: You are using pip version 20.2.3; however, version 20.2.4 is available.
#You should consider upgrading via the 'c:\users\michael\appdata\local\programs\python\python38\python.exe -m pip install --upgrade pip' command.

#C:\Users\Michael\Desktop\cardGamePython\MellowPyGUI>c:\users\michael\appdata\local\programs\python\python38\python.exe -m pip install --upgrade pip
#Collecting pip
#  Downloading pip-20.2.4-py2.py3-none-any.whl (1.5 MB)
#     |████████████████████████████████| 1.5 MB 315 kB/s
#Installing collected packages: pip
#  Attempting uninstall: pip
#    Found existing installation: pip 20.2.3
#    Uninstalling pip-20.2.3:
#      Successfully uninstalled pip-20.2.3
#Successfully installed pip-20.2.4

#GOOD NEWS!
#This worked!
#python setup.py build