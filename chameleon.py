#!/usr/bin/env python3
#
# Project     : Chameleon - Website IP Address Seeker
# Author      : Samiux (http://www.infosec-ninjas.com)
# Version     : 0.0.20 (Dated OCT 04, 2019)
#
# License     : GPLv3
#
# Download    : http://www.infosec-ninjas.com/chameleon
#
# Usage       : python3 chameleon.py -s github -f ipaddress.txt -p https -H github.com
#               python3 chameleon.py -h
#
# Dependences : Python 2.7.x and Python 3.7.x
#               Python 2.7.x cookielib.py has bug, so Python 3.7.x is preferred.
#
# Remarks     : Tested on Kali Linux Rolling 2019.3 and Ubuntu 19.04
#
# ChangeLog   : Version 0.0.1 (FEB 22, 2015)
#               [+] First release
#
#               Version 0.0.2 (FEB 25, 2015)
#		[+] Input file for IP addresses comparison option
#		[+] Add timeout option
#		[-] drop the single IP address comparison option
#
#		Version 0.0.3 (FEB 26, 2015)
#		[+] Add exceptional error handling
#		[+] Add threading option
#		[+] Add output file option
#		[+] Add batch of IP address per thread option
#
#		Version 0.0.4 (MAR 5, 2015)
#		[+] Add exceptional error handling
#		[+] Bugs fix
#
#               Version 0.0.5 (SEP 13, 2019)
#               [+] Bug fix
#               [+] Add more broswer user-agent option
#               [+] Add Referer Header option
#
#               Version 0.0.6 (SEP 14, 2019)
#               [+] Bug fix
#
#               Version 0.0.7 (SEP 14, 2019)
#               [+] Performance and resources tuning
#               [+] Add port number option
#               [+] Bug fix
#               [+] Major modification
#
#               Version 0.0.8 (SEP 15, 2019)
#               [+] Add path to the search
#
#               Version 0.0.9 (SEP 16, 2019)
#               [+] Lower the default threads setting to 30
#               [+] Add the IP range of USA and other, Ocean Digital
#               [+] Update the IP range of Singapore, Ocean Digital
#
#               Version 0.0.10 (SEP 16, 2019)
#               [+] Multi-threading bug fix
#
#               Version 0.0.11 (SEP 17, 2019)
#               [+] Multi-threading bug fix
#               [+] Change back to 100 default threads setting
#
#               Version 0.0.12 (SEP 18, 2019)
#               [+] Performance boost
#               [+] Multi-threading bug fix
#
#               Version 0.0.13 (SEP 22, 2019)
#               [+] Major modification
#               [+] Bug fix
#
#               Version 0.0.14 (SEP 23, 2019)
#               [+] Minor improvement
#
#               Version 0.0.15 (SEP 28, 2019)
#               [+] Major improvement
#
#               Version 0.0.16 (SEP 29, 2019)
#               [+] Add the IP range of all and ap-northeast-{1,2,3}, aws
#               [+] Add example
#
#               Version 0.0.17 (OCT 01, 2019)
#               [+] Minor improvement
#
#               Version 0.0.18 (OCT 02, 2019)
#		[+] Minor improvement
#               [+] Bug fix
#
#               Version 0.0.19 (OCT 03, 2019)
#               [+] Fix Python 3 bug
#
#               Version 0.0.20 (OCT 04, 2019)
#               [+] Minor improvement
#
# Remarks     : CTRL + \ to terminate the process
#

import os
import operator
import time
import os.path
import socket
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)
from time import sleep
from sys import stdout
from optparse import OptionParser
from multiprocessing import Pool
from requests.exceptions import HTTPError, ConnectionError, Timeout, TooManyRedirects, SSLError

# disable proxy (it should be here)
os.environ["http_proxy"] = ""

# global variables
version = "0.0.20"
options = ""
num = 0
infile = ""
outfile = ""
timeout = 0
pagetimeout = 0
batch = 0
ipaddress = ""
url = ""
port = 0
proto = ""
searchstring = ""
searchstring2 = ""
referer = ""
path = ""
host = ""
redirect = False

############################
# Browser User Agent Strings
# Firefox on Ubuntu Linux (default)
useragent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"

# Chrome on Android
#useragent = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"

# Chrome on iOS
#useragent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
#useragent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1"

# Chrome on MacOS
#useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"

# Firefox on Windows
#useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/69.0"

# Crawler and Bot of Google
#useragent = "Googlebot/2.1 (+http://www.google.com/bot.html)"
############################


# main routine for main menu
def main(num, infile, timeout, url, searchstring, searchstring2, outfile, batch, pagetimeout, proto, referer, port, path, host, redirect):
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)

	parser = OptionParser()
	parser.add_option("-s", "--string", dest="searchstring",
			  help="specify the unique string to search, case sensitive")
	parser.add_option("-S", "--string2", dest="searchstring2", default="",
			  help="specify the unique 2nd string to search, case sensitive, default is None")
	parser.add_option("-f", "--file", dest="infile",
			  help="input file contains ip addresses for comparison")
	parser.add_option("-p", "--proto", dest="proto", default="http",
			  help="protocol to use, http or https, default is http")
	parser.add_option("-o", "--timeout", dest="timeout", default=3,
			  help="timeout for connection, default 3 seconds")
	parser.add_option("-t", "--thread", dest="numthread", default=100,
			  help="number of thread, default is 100")
	parser.add_option("-w", "--write", dest="outfile", default="find.txt",
			  help="output file for findings, default is find.txt")
	parser.add_option("-b", "--batch", dest="batch", default=10,
			  help="number of IP address per thread, default is 10")
	parser.add_option("-l", "--pagetimeout", dest="pagetimeout", default=3,
			  help="timeout for web page loading, default is 3 seconds")
	parser.add_option("-r", "--referer", dest="referer", default="",
			  help="Referer header for the request, default is None")
	parser.add_option("-P", "--port", dest="port", default=80,
			  help="desired port number, default is 80")
	parser.add_option("-a", "--path", dest="path", default="",
			  help="path to the url, default is None")
	parser.add_option("-H", "--host", dest="host", default="",
			  help="host name for the header, default is None")
	parser.add_option("-R", "--redirect", dest="redirect", default=False,
			  help="allow redirect, default is False")
	(options, args) = parser.parse_args()

	if not options.proto:
		parser.error("protocol should be specified.")
		sys.exit()

	if not options.searchstring:
		parser.error("search string should be specified.")
		sys.exit()

	if not options.infile:
		parser.error("input file should be specified.")
		sys.exit()
	else:
		if not os.path.isfile(options.infile):
			print ("input file " + options.infile + " not exist.")
			sys.exit()

	if options.outfile:
		if os.path.isfile(options.outfile):
			print ("output file " + options.outfile + " exist, or rename it.")
			sys.exit()

	if "https" in options.proto and not options.host:
		parser.error("host name should be specified.")
		sys.exit()

        # specify the url
	if "https" in options.proto:
		url = "https://"
		port = 0
	else:
		url = "http://"
		port = 0

	# specify the desired port number
	if options.port is not 80:
		port = int(options.port)

	# specify the referer
	if options.referer != None:
		referer = options.referer
	else:
		referer = ""

	return options.numthread, options.infile, options.timeout, url, options.searchstring, options.searchstring2, options.outfile, options.batch, \
		options.pagetimeout, options.proto, options.referer, port, options.path, options.host, options.redirect


# compare the search string with response
def check_request(response, ipaddress):
	# get the encoding
	en_code = str(response.encoding)

	# (experimental)
	#if (response.text is not None) and (("text/html" or "text/plain") in response.headers["Content-Type"]):
	if (response.text is not None):
		# everything is fine
		# find the unqiue string
		stdout.write("\r".ljust(100))
		stdout.flush()
		stdout.write("\r" + ipaddress + " is reachable, now comparing ...")
		stdout.flush()

		# case sensitive and same as target encoding
		# works for both Python 2.7.x and Python 3.7.x
		if searchstring2 is "":
			if (searchstring.encode(en_code).decode(en_code) in response.text):
				f = open(outfile, "a")
				f.write(ipaddress + " matches " + searchstring + "\n")
				f.flush()
				f.close()
				stdout.write("\r".ljust(100))
				stdout.flush()
				stdout.write("\r\033[92m" + ipaddress + " matches " + searchstring)
				stdout.flush()
				return True
		else:
			if (searchstring.encode(en_code).decode(en_code) in response.text) and (searchstring2.encode(en_code).decode(en_code) in response.text):
				f = open(outfile, "a")
				f.write(ipaddress + " matches " + searchstring + " and " + searchstring2 + "\n")
				f.flush()
				f.close()
				stdout.write("\r".ljust(100))
				stdout.flush()
				stdout.write("\r\033[92m" + ipaddress + " matches " + searchstring + " and " + searchstring2)
				stdout.flush()
				return True

	return False


# process input file line by line and do the comparison
def process_line(line):
	# remove the "\n" from the line just read
	ipaddress = line.rstrip("\n")

	if ipaddress is not None:
		# make url simple
		if port == 0:
			newurl = url + ipaddress
		else:
			newurl = url + ipaddress + ":" + str(port)

		# path exists?
		if path != "":
			newurl = newurl + "/" + path

		stdout.write("\r ".ljust(100))
		stdout.flush()
		stdout.write("\rTrying " + newurl + " ....")
		stdout.flush()

		# custom headers
		if referer != "" and host == "":
			new_referer = referer
			headers = {"User-Agent" : useragent, "Referer" : new_referer, "Origin" : new_referer}
		elif referer != "" and host != "":
			new_referer = referer
			headers = {"Host" : host, "User-Agent" : useragent, "Referer" : new_referer, "Origin" : new_referer}
		elif referer == "" and host == "":
			new_referer = url + ipaddress
			headers = {"User-Agent" : useragent, "Referer" : new_referer, "Origin" : new_referer}
		elif referer == "" and host != "":
			#new_referer = url + ipaddress
			new_referer = url + host
			headers = {"Host" : host, "User-Agent" : useragent, "Referer" : new_referer, "Origin" : new_referer}

		try:
			# to avoid scanning too fast (experimental)
			#sleep(int(timeout))

			# https://www.w3schools.com/python/ref_requests_head.asp
			# check the headers first
			# allow_redirects should be False, verify should be False, stream should be False
			head = requests.head(newurl, headers=headers, allow_redirects=False, timeout=(int(timeout), \
					int(pagetimeout)), verify=False, stream=False)

			# if the response was successful, no Exception will be raised
			head.raise_for_status()

			# The max. size for the Content-Length
			# 1Mbytes
			#max_size = 1048576
			# 5Mbytes
			max_size = 5242880

			# to avoid to download media file when connected
			# some sites do not have this Content_length header
			if (("Content-Length" in head.headers) and (int(head.headers["Content-Length"]) < max_size)) or \
					("Content-Length" not in head.headers):
				# conduct requests now
				# stream should be False
				if redirect is False:
					response = requests.get(newurl, headers=headers, allow_redirects=False, timeout=(int(timeout), \
						int(pagetimeout)), verify=False, stream=False)
				else:
					response = requests.get(newurl, headers=headers, allow_redirects=True, timeout=(int(timeout), \
						int(pagetimeout)), verify=False, stream=False)

				result = check_request(response, ipaddress)
				return result
			return False

		except HTTPError:
			pass
		except ConnectionError:
			pass
		except Timeout:
			pass
		except TooManyRedirects:
			pass
		except SSLError:
			pass
		except requests.exceptions.ProxyError:
			pass
		except requests.exceptions.ConnectionError:
			pass
		except requests.exceptions.Timeout:
			pass
		except requests.exceptions.ConnectTimeout:
			pass
		except requests.exceptions.ReadTimeout:
			pass
		except requests.exceptions.URLRequired:
			pass
		except requests.exceptions.TooManyRedirects:
			pass
		except requests.exceptions.MissingSchema:
			pass
		except requests.exceptions.InvalidSchema:
			pass
		except requests.exceptions.InvalidURL:
			pass
		except requests.exceptions.InvalidHeader:
			pass
		except requests.exceptions.InvalidProxyURL:
			pass
		except requests.exceptions.ChunkedEncodingError:
			pass
		except requests.exceptions.ContentDecodingError:
			pass
		except requests.exceptions.StreamConsumedError:
			pass
		except requests.exceptions.RetryError:
			pass
		except requests.exceptions.UnrewindableBodyRrror:
			pass
		except requests.exceptions.RequestException as err:
			print (err)
		except Exception:
			pass

	return False


if __name__ == "__main__":
	# main routine
	numthread, infile, timeout, url, searchstring, searchstring2, outfile, batch, pagetimeout, proto, referer, port, path, host, redirect = \
		main(num, infile, timeout, url, searchstring, searchstring2, outfile, batch, pagetimeout, proto, referer, port, path, host, redirect)
	localtime = time.asctime( time.localtime(time.time()) )

	# the port number to be displayed
	if port == 0 and proto == "http":
		dport = 80
	elif port == 0 and proto == "https":
		dport = 443
	else:
		dport = port

	# total number of line in input file
	count = len(open(infile).readlines( ))

	if redirect is False:
		redir = "No"
	else:
		redir = "Yes"

	print ("\n")
	print ("Chameleon - Website IP Address Seeker")
	print ("Version " + version + " - by Samiux (http://www.infosec-ninjas.com)")
	print ("\n")
	print ("You may need to wait for a while after the scanning is completed!")
	print ("\n")
	print ("CTRL + \ to interrupt the running script when necessary,")
	print ("or you may need to reboot your box!")
	print ("\n")
	print ("Search string       : " + str(searchstring))
	print ("Search string (2nd) : " + str(searchstring2))
	print ("Threads             : " + str(numthread))
	print ("Timeout (sec)       : " + str(timeout))
	print ("Input file          : " + infile)
	print ("Total # of IP       : " + str(count))
	print ("Output file         : " + outfile)
	print ("IP per thread       : " + str(batch))
	print ("Page timeout (sec)  : " + str(pagetimeout))
	print ("Host                : " + str(host))
	print ("Referer             : " + str(referer))
	print ("Protocol            : " + str(proto))
	print ("Port                : " + str(dport))
	print ("Path                : " + str(path))
	print ("Redirect            : " + str(redir))
	print ("Start at            : " + localtime)
	print ("\n")

	stdout.write("\rInitialing ......")
	stdout.flush()

	# multiprocessing pool
	# (default)
	pool = Pool(processes=int(numthread))
	# (experimental)
	#pool = Pool(processes=int(numthread), maxtasksperchild=int(batch))

	with open(infile) as lines:
		# *** OLD CODE *** use less memory with reduce()
		#result = reduce(operator.add, pool.map(process_line, lines, int(batch)))

		# https://docs.python.org/2/library/multiprocessing.html#module-multiprocessing.pool
		# Section 16.6.2.9 Process Pools

		# normal (default)
		#result = pool.map(process_line, lines, int(batch))

		# async (preferred)
		result = pool.map_async(process_line, lines, int(batch))

	# when using read line by line (experiment) - very slow (NOT USE, for reference only)
	#with open(infile) as fp:
	#	for counter, line in enumerate(fp):
	#		process_line(line)

	# when using pool.map (default)
	#pool.close()

	# when using pool.map_async (preferred)
	pool.close()
	pool.join()

	# print the result
	if os.path.isfile(outfile):
		stdout.write("\r".ljust(100))
		stdout.flush()
		stdout.write("\rPlease check " + outfile + " to see if there is any finding!")
		stdout.flush()
	else:
		stdout.write("\r".ljust(100))
		stdout.flush()
		if searchstring2 is "":
			stdout.write("\r" + searchstring + " not found!")
		else:
			stdout.write("\r" + searchstring + " and " + searchstring2 + " not found!")
		stdout.flush()

	# reset the colour
	localtime = time.asctime( time.localtime(time.time()) )
	print ("\033[0m")
	print ("\n")
	print ("End at          : " + localtime)
