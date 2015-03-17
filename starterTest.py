
import mellowGUI
from threading import Thread
import time

#mellowGUI.main('Michael')
'''
try:
	#threading.start_new_thread( mellowGUI.main, ('Michael', ) )
	t = Thread(name = 'Testing', target=mellowGUI.main, args=('Michael', ))
	t.start()
except:
	print "Error: unable to start thread"

while 1==1:
	time.sleep(1)
	print 'Tick tock'
'''

def main(name):
	while 1==1:
		time.sleep(1)
		print 'Tick tock'