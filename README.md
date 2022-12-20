# DirectoryDisco
DirectroyDisco(very) is a python program for discovering hidden directories and soon subdomains. The program is ran on your Linux terminal and can be download as easy as just copying the mainDisco.py file or downloading it. This program is for learning purpose only and is used for CTFs.


## Usage
basic:
`$ python3 mainDisco.py -u http://1.1.1.1 -w wordlist.txt -x php,txt`

advanced:
`$ python3 mainDisco.py -u http://1.1.1.1 -w wordlist.txt -x php,txt -t 40` 

## Note:
mainDisco.py for now directory busting only haven't had a chance to add subdomains to hunt but gonna add them soon. For now everything everything looks good with the threading and the recursion, thinking of adding more arguments/flags soon.  
