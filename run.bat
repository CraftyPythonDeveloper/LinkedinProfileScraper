@echo off    
set PATH=%PATH%; C:\Users\%USERNAME%\Anaconda3\Scripts
call C:\Users\%USERNAME%\Anaconda3\Scripts\activate.bat linkedin_scraper
echo Welcome %USERNAME%
echo Which profiles do you want to scrape?
set /p query=
scrapy crawl linkedin -a search="%query%"