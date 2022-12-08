# DirectoryDIsco
DirectroyDisco(very) is a python program for discovering hidden directories and soon subdomains. The program is ran your Linux terminal. This program is for learning purpose only and is used for CTFs or stuff.


## Usage
basic:
`$ python3 DirectoryDisco -u http://1.1.1.1 -w wordlist.txt -x php,txt`

advanced:
`$ python3 DirectoryDisco -u http://1.1.1.1 -w wordlist.txt -x php,txt -t 100` 

## Note:
MainDisco.py is a work in progress the main differance between the two files is that the mainDisco is going to be a subdomain and directory, and that the mainDisco is going to be doing recursive searching meaning after finding a folder it's going to run the progam on that folder to find the files in theat folder too.
