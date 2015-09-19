# crawlStackExchangeDataExplorer
Stack Exchange Data Explorer is a platform for users to query data in Stack Exchange sites.
This is a script written in Python which can crawl the viewCount of questions in Stack Overflow.
As there are 10 million questions in Stack Overflow recently and only 50 thousand results can be returned in Stack Exchange Data exploer, we need to write a program to repeate such steps and get the data automatically.

##Functions
This script can 
* automatically execute the SQL in that platform and download the result file;
* remove the file from default download path to where we want;
* aggregate all data into one file.


##Prerequisites
* Install Python 2.7.* ;
* Install selenium for python ;
* Download Chrome driver and put it into the same path with viewCount.py.
 

##Others
It sucks sometimes and maybe it will be more stable when using phantomjs.
Of course, more excelent solution to this task is to analyze the request and response in the site and then get the data in that way. But you may need to consider the **captcha image** which is rather difficult to recognize.

Of course, you are free to improve this one and enjoy the journey. 

