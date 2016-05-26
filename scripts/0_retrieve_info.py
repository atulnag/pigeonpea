#import webpages
import urllib2
#System
import os
import re
#Beautiful Soup - parsing HTML
from bs4 import BeautifulSoup

def retrieve_seq(id):
	global errors
	#proxy = urllib2.ProxyHandler({'http': 'http://atul_nag:nag2910@10.0.0.6:8080'})
	#auth = urllib2.HTTPBasicAuthHandler()
	#opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
	#urllib2.install_opener(opener)
	try:
		response = urllib2.urlopen('http://plantgrn.noble.org/LegumeIP/v2/GeneCard.jsp?seq_acc='+id)
		html = response.read().decode("UTF-8")
		response.close()
		fout = open(id+'.html','w')
		fout.write(html)
		fout.close()
	except urllib2.HTTPError as e:
		errors.append(id)
	else:
		pass

def extract_seq(id):
	try:
		err = open("errors.txt","a")
		fh = open(id+'.html')
		html = fh.read()
		soup = BeautifulSoup(html)
		data = []
		for lines in soup.find_all('pre'):
			if len(lines.text) > 1 :
				line = unicode(lines.string)
				line = line.replace('\r\n','')
				data.append(line)
		for lines in soup.find_all('td'):
			line = unicode(lines.string)
			if re.search('&nbsp\[mRNA\]\s+locus=',line):
				data.append(line)
				#	for lines in soup.find_all('li'):
				#		line = lines.text
				#		if re.search('^(IPR|GO|K)',line):
				#			data.append(line)
			fh.close()

		os.remove(id+'.html')
		fh = open("Data/"+id+'.dfa','w')
		fh.write('>'+id+"\n")
		fh.write(data.pop(0))
		fh.close()
		fh = open("Data/"+id+'.profa','w')
		fh.write('>'+id+"\n")
		fh.write(data.pop(0))
		fh.close()
		data.append("\n")
		fh = open("Data/"+id+'.loc','w')
		fh.write(data.pop(0))
		#fh.write(','.join(data))
		fh.close()
	except IOError:
		err.write("Error:"+id+"\n")
	except IndexError:
		err.write("Error:"+id+"\n")
	else:
		pass
	err.close()

errors = []
ids = open("id.txt")
for pid in ids:
	pid = pid.strip()
	print "Processing :"+pid
	retrieve_seq(pid)
	extract_seq(pid)
print errors



