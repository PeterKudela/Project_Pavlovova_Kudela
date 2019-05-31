# Project

##Project summary

To run the project, just run $ python application.py in your terminal and then open http://127.0.0.1:8050/ in your browser.

##Project data
We worked with two sources of data (see inputs_and_functions.py). The first publicly available inqubu API which provides various demographic, economical variables. Second, TripAdvisor.json file which was created using sraper.py to obtain list of "best things to do" in each country

## application.py
In this file the 'application is defined'. Meaning the layout, its inputs and outputs.

Functions and defined list of inputs(such as list of countries and characteristics) are defined in the file inputs_and_functions.py. The code depends on the way how the inputs are defined (e.g. countries as dict {'country':'code'}).

## inputs_and_functions.py
In this file inputs and function used in application.py are defined. The functions are dependent on the way how input dictionaries are specified.

If the limit of number of data downloads is exceeded, please get a new API key from http://inqubu.com/blog/index.php and change it in functions getData and getDataWorld - namely in the used url change api_key= .