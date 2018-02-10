import os, errno
import glob
# create directories
if not os.path.exists('data'):
	os.makedirs('data')
if not os.path.exists('graphs'):
	os.makedirs('graphs')

#delete files in the 
files = glob.glob('graphs/*')
for f in files:
    os.remove(f)
files = glob.glob('data/*')
for f in files:
	os.remove(f)
print 'the application initialized.'