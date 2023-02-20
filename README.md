# baysil
To create Json opbject for baysil data ingestion

1. Manual clean up raw data accordingly. Save the data files into raw_data folder.

2. Execute data_clean_up.py. This script will further clean up the data, such as formatting datetime, postal code and assemble birth log and blue heron baby into one file.

3. Execute Baysil_Engine.py. In main() function, there are two parameters: a. volumn of Json object to create b. if json object will be actually created. 
Default is volumn = 10, create_json = True. To create all Json object, put volumn = -1.

4. Json object will be created in sample folder. In addition, several reports will also be generated in check_list folder. This is only for reference.

    a. baby with out mother.csv indicates baby whose mother is missing because the mother name in blue heron baby doesn't exist in client list.

    b. number of episode for each mother is how many episode are there for each mother.