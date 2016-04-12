import urllib
import urllib2
import time

#Scrapping search engines
hosts = ["https://ia800300.us.archive.org/27/items/amusementsinmath16713gut/16713-8.txt","https://ia800300.us.archive.org/27/items/amusementsinmath16713gut/16713.txt",
		"https://ia802605.us.archive.org/18/items/beetonsbookofnee15147gut/15147-8.txt","https://ia802605.us.archive.org/18/items/beetonsbookofnee15147gut/15147.txt",
		"https://ia801405.us.archive.org/18/items/alicesadventures19033gut/19033-8.txt","https://ia801405.us.archive.org/18/items/alicesadventures19033gut/19033.txt",
		"https://ia800504.us.archive.org/23/items/littlebrother30142gut/30142-8.txt","https://ia800504.us.archive.org/23/items/littlebrother30142gut/pg30142.txt",
		"https://ia600501.us.archive.org/27/items/theadventuresofs01661gut/1661-8.txt","https://ia600501.us.archive.org/27/items/theadventuresofs01661gut/1661.txt","https://ia800501.us.archive.org/27/items/theadventuresofs01661gut/pg1661.txt"]

#Start timer
start = time.time()

#Collection of files
C = []

def downloadFiles():
	#grabs urls of hosts and prints first 1024 bytes of page
	for host in hosts:
		#Fetch file name from url
		file_name = host.split('/')[-2]+host.split('/')[-1]
		f = open(file_name, 'wb')
		#Read file
		url = urllib2.urlopen(host)
		f.write(url.read())
		f.close()
		C.append(file_name)

#Call function
downloadFiles()

print "Downloaded file:"
print C

end = time.time()
#print finish time
print "Time Taken: %s" % (end - start)

