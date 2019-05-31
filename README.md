# Project

## Project summary
In this project, we tried to create an interactive tool, similar to the one of inqubu.com. The user selects a country of interest and the tool returns its capital, top places to visit in this country based on tripadvisor rating, graph of location of the country. Further, the user can select some demographic characteristic. The tool then returns scatterplot of this characteristic in the selected country over the period between 1990 and 2016. Moreover, next to this scatterplot a world map for this given characteristic is displayed, so that the user can compare the selected country with rest of the world. Below the world map, the user can choose for which year between 1990 adn 2016 he wants the world map.

To run the project, download files application.py, input_and_funcitons.py and data Tripadvisor.json. Then just run $ python application.py in your terminal and then open http://127.0.0.1:8050/ in your browser. We do not use Jupyter Notebook as it was not convenient in our case. However, we provide it for the scraper and inputs_and_function files. In case of inputs_and_functions, functions for graph do not make much sense, as they are constracted to work in our application. The code is not objected oriented and does not have its own class defined. This is again because it was more suitable for us to use functions to connect it with the app (inputs and outputs of html).

It can happen that an error occurs, in this case please just refresh the page and try again (maybe several times) and it should work. The error might occure due to the data downloading behind the application as good internet connection is needed and also the inqubu page sometimes takes some while to respond.

It can happen that the limit for API download is exceeded, then please go to http://inqubu.com/blog/index.php and ask for a new key. Then in change this key in file input_and_data.py in functions getData() and getDataWorld (in both cases in url change the part after api_key=).

If you wish to download the Tripadvisor.json yourself, use scraper.py or scraper.ipynb. It will take several minutes. As the scraper is based on google, it might happen that some changes to the scraper might be needed in order for it to work as the pages on which it is build might change.

## Project data
We worked with two sources of data (see inputs_and_functions.py). The first publicly available inqubu.com API which provides various demographic and economical variables. Second, TripAdvisor.json file which was created using sraper.py to obtain list of "best things to do" in each country.

### application.py
In this file the 'application' is defined. Meaning the layout, its inputs and outputs.

Functions and defined list of inputs(such as list of countries and characteristics) are defined in the file inputs_and_functions.py. The code depends on the way how the inputs are defined (e.g. countries as dict {'country':'code'}).

### inputs_and_functions.py
In this file inputs and function used in application.py are defined. The functions are dependent on the way how input dictionaries are specified.

Most importantly, the functions used for data download are defined here alongside with the inputs user can choose.

If the limit of number of data downloads is exceeded, please get a new API key from http://inqubu.com/blog/index.php and change it in functions getData and getDataWorld - namely in the used url change api_key= .

### scraper.py and Tripadvisor.py

Web scraper that gets TOP things to visit in every country based on TripAdvisor rating. To get the TripAdvisor websites special TripAdvisor country codes are needed. As we did not find any list of them, we went around using google. The scraper first googles top places to visit in country x - gets the corresponding link and then scrapes the corresponding page for titles of most favoured attractions.
