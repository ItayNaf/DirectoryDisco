#!/usr/bin/env python3
import sys
import argparse
import urllib.request
import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

parser = argparse.ArgumentParser(
     description='''Description: This program helps you with finding hidden folders/directories and files or hunt for hidden subdomains in http/https websites''',
     usage="""python3 MainDisco.py [command]""")

subparser = parser.add_subparsers(dest='command')
DIR = subparser.add_parser('Dir', help="files/directories")
SUB = subparser.add_parser('Subdomain', help="subdomains")

DIR.add_argument('-u', '--url', type=str, metavar='', help='URL. Example: -u/--url http://tesla.com/ ')
DIR.add_argument('-w', '--wordlist', type=str, metavar='', help='Wordlist. Example: -w/--wordlist /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt')
DIR.add_argument('-x', '--extentions', type=str, metavar='', help='File Extentions. Example: -x/--extentions php,html,js,etc.')
DIR.add_argument('-t', '--threads', type=int, metavar='', default=60, help='When incrementing the amount of threads the program will do a couple things at once this can rush the process of the program but maybe not as much stealthy or reliable Example: -s/--threads 60 (Default: 60) ')
DIR.add_argument('-o', '--output', type=str, metavar='', help='Output file. Example: -o/--output DirectorySearch.out')
# DIR.add_argument('-c', '--cookie', type=str, metavar='', help='Cookie. This flag take the cookie you give the and sets it as the cookie for the request. Example: -c/--cookie "PHPSSID=lnol1ulh0kolcges6iha52h8r0"')

args = parser.parse_args()

if args.command == 'Dir':
	# Assigning arguments to variables
	url = args.url
	wordlist = args.wordlist
	output = args.output
	threads = args.threads
	extentions = args.extentions
	# cookie = args.cookie
	
	if(url == None or wordlist == None):
		# checking if input is legel
	     print("usage: python3 DirectoryDisco.py -u <url> -w <wordlist>")
	     print("for help: python3 DirectoryDisco.py --help")
	     sys.exit()

	if(url[-1] == '/'):
		url = url[:-1]

	# Printing the arguments to the screen.
	print(f"""
	    -------------------------------------------------
	    Url:                    {url} 
	    Wordlist:               {wordlist}
	    Extentions              {extentions}
	    Threads:                {threads}
	    Output File:            {output}
	    -------------------------------------------------
	    """)

	if(extentions is not None):
	    # Assigning every extention into a list.
	    erase_space = extentions.replace(" ", "")
	    extentions_list = erase_space.split(',')

	url_list = []

	def getStatuscode(url):
	    # Function that returns the status code of the specified URL.
	    try:
	        r = requests.head(url,verify=False,timeout=5) # it is faster to only request the header
	        return (r.status_code)
	    except:
	        return -1
	    # End Function

	def loadingScreen():
	    # Loading Screen.
	    loading = "Searching...🧐"
	    for char in loading:
	        sys.stdout.flush()
	        time.sleep(0.1)
	        print(char,end='') 
	    # End Loading Screen

	loadingScreen()
	print("\n")

	# Appending every word from the wordlist into a list and removing every unneccery new line and a word that starts with a '#'.
	wordlist_file = open(wordlist, "r")

	wordlist_array = []
	for line in wordlist_file:
	    if(line[0] != '#'):
	        wordlist_array.append(line)

	new_wordlist_array = [item.rstrip() for item in wordlist_array]
	# End wordlist.

	# Removing all empty space in the list.
	while("" in new_wordlist_array):
    		new_wordlist_array.remove("")

	def wordlistCombination(new_wordlist_array, url, url_list):
		#Combining the url with every word in the wordlist into a url list like so: url/word 
		for x in range(len(new_wordlist_array)):
			url_dir = f"{url}/{new_wordlist_array[x]}"
			url_list.append(url_dir)
		# End Url list.
	

	# If the getStatusCode Function returns -1 it means that there is not status code for the site which means it doesn't exist so it errors out.
	if(getStatuscode(url) == -1):
	    print("Error: can not connect to Site/IP.")
	    sys.exit()
	# End Error.

	def addExtention(extentions, extentions_list, new_wordlist_array, url, url_list):
		if(extentions is not None):
		# Adding every extention into the url list.
			for x in range(len(extentions_list)):
				for i in range(len(new_wordlist_array)):
					url_dir_extention = f"{url}/{new_wordlist_array[i]}.{extentions_list[x]}"
					url_list.append(url_dir_extention)
		# End url list.

	def wordlistOrientation(url_list, original_wordlist, orianted_url_list):
	    # this function sorts the url_list to a word and all of it's extentions
	    i = 0
	    j = 0
	    for i in range(len(original_wordlist)):
	        for j in range(i, len(url_list), len(original_wordlist)):
	            orianted_url_list.append(url_list[j])

	folder_list = []
	print('url, status_code \n')
	def urlChecking(url):
		# Prints a url with a status code that's not 404 because 404 is a "not found" error and it's not needed.
			if(getStatuscode(url) < 403):
				for extention in extentions_list:
					extention = f".{extention}"
					if(extention in url == False or getStatuscode(url) == 301):
						folder_list.append(url)

				check = f"{url}, Status Code: {getStatuscode(url)}"
				#print(check)
				return check
	    # End.

	orianted_url_list = []
	#new_folder_list = []
	orianted_folder_list = []
	recyle_folder_list = []
	def threadFunction(url, str_list, orianted_list):

		if(extentions is not None):
			wordlistCombination(new_wordlist_array, url, str_list)
			original_wordlist = str_list.copy()
			addExtention(extentions, extentions_list, new_wordlist_array, url, str_list)
			wordlistOrientation(str_list, original_wordlist, orianted_list)

			pool = ThreadPool(threads)
			result = pool.map(urlChecking, orianted_list)
			new_folder_list = list(set(folder_list))

			global recyle_folder_list

			#print(f"str_list:\n {str_list}\n")
			print(f"orianted_list:\n {orianted_list}\n")
			print(f"new_folder_list:\n {new_folder_list}\n")
			print(f"recyle_folder_list:\n {recyle_folder_list}\n")

			print(f"does recyle_folder_list equal to new_folder_list: {new_folder_list == recyle_folder_list}\n\n")
			
			#print(id(new_folder_list))
			#print(id(recyle_folder_list))

			if(new_folder_list != recyle_folder_list):
				recyle_folder_list = new_folder_list.copy()
				for url in new_folder_list:
					threadFunction(url, new_folder_list, orianted_folder_list)
					#Work on it Something not working with the recursive function(it gets into a infinite loop.
			new_result = []
			for i in result:
				if(i != None):
					new_result.append(i)
		else:
			wordlistCombination(new_wordlist_array, url, str_list)
			#Check if working
			pool = ThreadPool(threads)
			result = pool.map(urlChecking, url_list)
			new_result = []
			for i in result:
				if(i != None):
					new_result.append(i)

	threadFunction(url, url_list, orianted_url_list)

	if(output != None):
	    outFile = open(output, 'a')
	    for item in new_result:
	        outFile.write(item + "\n")

	print("\nFinished!!! " + current_time)

elif args.command == 'Subdomain':
	print("Working")
else:
	print("Picking a command is REQUIRED!")
	print("usage: python3 MainDisco.py [command]")
	print("for help: python3 MainDisco.py -h/--help")
