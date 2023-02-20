# baysil
To create Json opbject for baysil data ingestion

1. Manual clean up raw data accordingly. Save the data files into raw_data folder.

2. Execute data_clean_up.py. This script will further clean up the data, such as formatting datetime, postal code and assemble birth log and blue heron baby into one file.

3. Execute Baysil_Engine.py. In main() function, there are two parameters: a. volumn of Json object to create b. if json object will be actually created. 
Default is volumn = 10, create_json = False. To create all Json object, put volumn = -1.