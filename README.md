# dyn zone info

A small script to gather the following information from your dyn account:
- approximate number of monthly queries
- number of zones
- number of records

The results will be printed to STDOUT in readable text and added to a 'dynfetch-out.csv' with Excel dialect.

## Setup/install

You will need the [dyn module](https://github.com/dyninc/dyn-python) but a simple `pip install dyn` should get you sorted.
Also you will need to create a 'dynfetch.ini' file with your account credentials for the API access. Please take a look into the provided example file.


