# crawlStackExchangeDataExplorer

##Functions
Stack Exchange Data Explorer is a platform for users to query data in Stack Exchange sites.
This is a script written in Python that can 
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

