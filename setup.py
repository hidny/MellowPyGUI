import cx_Freeze


cx_Freeze.setup(
	name="GUI client",
	version = "2.7",
	options={"build_exe": {"packages":["pygame"],
				"include_files":["Image/",
				"Connect4Logo.png", "EuchreLogo.png", "MellowLogo.png", "ReversiLogo.png", "versNumber.png", "versNumber1.png", "versNumber2.png"]}},
	executables = [cx_Freeze.Executable("start.py", base ="Win32GUI")]
	)

#python setup.py build

#Bug fix:had to take away all prints in serverListener functions to make it work.
# I don't know why that was a problem
#https://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6

#I think you could delete scipy to make more room