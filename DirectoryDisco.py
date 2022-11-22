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

# Adding Arguments
parser = argparse.ArgumentParser(
     description='''Description: This program helps you with finding hidden folders/directories in http/https websites''',
     usage="""python3 DirectoryDisco.py -u <url> -w <wordlist>""")
parser.add_argument('-u', '--url', type=str, metavar='', help='URL. Example: -u/--url http://tesla.com/ ')
parser.add_argument('-w', '--wordlist', type=str, metavar='', help='Wordlist. Example: -w/--wordlist /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt')
parser.add_argument('-x', '--extentions', type=str, metavar='', help='File Extentions. Example: -x/--extentions php,login,js,etc.')
parser.add_argument('-t', '--threads', type=int, metavar='', default=60, help='When incrementing the amount of threads the program will do a couple things at once this can rush the process of the program but maybe not as much stealthy or reliable Example: -s/--threads 60 (Default: 60) ')
parser.add_argument('-o', '--output', type=str, metavar='', help='Output file. Example: -o/--output DirectorySearch.out')

args = parser.parse_args()
# End Arguments

# Assigning arguments to variables
url = args.url
wordlist = args.wordlist
output = args.output
threads = args.threads
extentions = args.extentions
# End Assigning

if(url == None or wordlist == None):
    print("usage: python3 DirectoryDisco.py -u <url> -w <wordlist>")
    print("for help: python3 DirectoryDisco.py --help")
    sys.exit()

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
    # End extention list

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


#Combining the url with every word in the wordlist into a url list like so: url/word 
for x in range(len(new_wordlist_array)):
    url_dir = f"{url}/{new_wordlist_array[x]}"
    url_list.append(url_dir)
# End Url list.

original_wordlist = list(url_list)

# If the getStatusCode Function returns -1 it means that there is not status code for the site which means it doesn't exist so it errors out.
if(getStatuscode(url) == -1):
    print("Error: can not connect to Site/IP.")
    sys.exit()
# End Error.

if(extentions is not None):
    # Adding every extention into the url list.
    for x in range(len(extentions_list)):
        for i in range(len(new_wordlist_array)):
            url_dir_extention = f"{url}/{new_wordlist_array[i]}.{extentions_list[x]}"
            url_list.append(url_dir_extention)
    # End url list.

def wordlistOrientation(url_list, original_wordlist, new_url_list):
    # this function sorts the url_list to a word and all of it's extentions
    i = 0
    j = 0
    for i in range(len(original_wordlist)):
        for j in range(i, len(url_list), len(original_wordlist)):
            new_url_list.append(url_list[j])

print('url, status_code \n')
def urlChecking(url):
    # Returns a url with a status code that's not 404 because 404 is a "not found" error and it's not needed.
    if(getStatuscode(url) != 404):
        check = f'{url}, Status Code: {getStatuscode(url)}'
        print(check)
        return check
    # End.


new_url_list = []
if(extentions is not None):
    wordlistOrientation(url_list, original_wordlist, new_url_list)
    pool = ThreadPool(threads)

    result = pool.map(urlChecking, new_url_list)

    new_result = []
    for i in result:
        if(i != None):
            new_result.append(i)
else:
    pool = ThreadPool(threads)

    result = pool.map(urlChecking, url_list)

    new_result = []
    for i in result:
        if(i != None):
            new_result.append(i)


if(output != None):
    outFile = open(output, 'a')
    for item in new_result:
        outFile.write(item + "\n")

print("\nFinished!!! " + current_time)
