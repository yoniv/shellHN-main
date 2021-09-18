# ShellHN - Command line utility for Hacker News

## Installation:
1. clone the git repository: git clone  https://github.com/yoniv/shellHN-main.git

2. Create a virtual environment that includes the following directories:
 'Click','requests','aiohttp','html2text','aiohttp','asyncio','logging'
 
  You can see the requirements.txt.
 
3. From the command line cd the project directory and activate the virtual environment.

##Usage:

To get the 40 top HN stories, run:
```
hn top
```

To get the comments thread of a story by its rank, run:
```
hn comments
```

##Tests:

To run the unittest run:

```
pytest
```

Note: This program was created on windows