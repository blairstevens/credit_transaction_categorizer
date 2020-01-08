# credit_transaction_categorizer



#### About

Credit_transaction_categorizer is a cli that scrapes transaction information from saved html pages.

#### Why

Often your credit card transaction history will show you your spending category with each transaction when you are logged into their web interface. However when you download all of your transactions most firms will not provide those spending categories. This tool looks through the saved web pages, peels out the transaction information including the spending category, and returns one combined .xlsx file.

#### Caveats

This was quickly built to pull down the data for one user. It therefore is only optomized for that users bank/credit card combination. It was not designed to work for all institiuitons, but with some adaptation it is likely you will be able to use much of the base for your own case.

This also only works upon html pages you have saved already. If you would like to integrate this into a crawler that will download your pages for you go right ahead, but I imagined the possible hassle of dealing with your bank if they detect your crawler outweighs the effort required to manually save the pages (approx 6 pages per year of data).

#### How to

Clone down the convert.py file. 

Place it within a folder with a data and output folders beside it.

Save the html pages that show the transactions you would like to scrape within the data folder.

In your command line run:

```
​```
python convert.py convert
​```
```

If successful the .xlsx file will be in the output folder.