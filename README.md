# web-crawler-experiment

An experiment where an automated script continuously read the page and scrap data from it, this was slightly altered to check if a "new entry" was added post the first initialization of the script.

Does this task every 30 seconds and save everything into a log documenting all changes that occured.

Note: Web Crawler as a whole is pretty grey, their purpose can be good or bad depending on how utilized, for good reasons they are used to create search engines and search results, without em companies like Google will not be known for their search engine back in the old days, for bad reasons it can be utilized to extract private info that is extremely sensitive.

# Packages Used

* `requests | pip install requests` for requesting the website.
* `BeautifulSoup | pip install BeautifulSoup` to read it in plain HTML and get exactly the specific data from the requested content
* Rest are default Python libraries (Note: This is mainly for Windows because of "winsound").

![](https://i.imgur.com/9IGfjq1.png)
