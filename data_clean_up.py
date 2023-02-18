import pandas as pd 
import json
import numpy as np
# process data first and create a new clean csv file

def clean_up_client_list():
# data read and clean up for client list
    data = pd.read_csv('raw_data/Client List.csv',encoding='cp1252')
    # clean up the data by removing the 0x92 byte
    data = data.replace('’', "'", regex=True)

    # format the DoB column to be in the format of month day, year
    data['DoB'] = pd.to_datetime(data['DoB']).dt.strftime('%B %d, %Y')

    # format the phone number as xxx-xxx-xxxx
    for item in ['Mobile Phone','Home Phone','Work Phone','Work Phone Extension']:
        data[item] = data[item].astype(str)
        # remove the decimal point
        data[item] = data[item].str.replace(r'\.0', '',True)
        data[item] = data[item].str.replace(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3',True)

    # create a new column with work phone and work phone extension
    # if extension is null, then it is just work phone. if work phone is null, then it is just null
    data['Work Phone and Extension'] = data['Work Phone'] + ' x' + data['Work Phone Extension']
    data['Work Phone and Extension'] = data['Work Phone and Extension'].str.replace(r'nan xnan', '',True)
    #regex anything berfore xnan
    data['Work Phone and Extension'] = data['Work Phone and Extension'].str.replace(r' xnan', '',True)
    # change the may contact to True or False instead of 1 or 0
    data['May Contact'] = data['May Contact'].astype(str)
    data['May Contact'] = data['May Contact'].str.replace(r'1', 'True',True)
    data['May Contact'] = data['May Contact'].str.replace(r'0', 'False',True)

    # clean up the OHIP Number column
    data['OHIP Number'] = data['OHIP Number'].astype(str)
    data['OHIP Number'] = data['OHIP Number'].replace('-', ' ', regex=True)


    data.to_csv('cleaned_data/Client List.csv',index=False)

    del data

def clean_up_Blue_Heron_Babies_and_Birth_Log():
# data read both Blue Heron Babies and Birth Log to join and clean up 

    data = pd.read_csv('raw_data/Blue Heron Babies.csv',encoding='cp1252')
    data_2 = pd.read_csv('raw_data/Birth Log.csv',encoding='cp1252')
    # join 2 table on CoC ID
    data = pd.merge(data,data_2,on='CoC ID',how='outer')
    del data_2
    # clean up the data by removing the 0x92 byte
    data = data.replace('’', "'", regex=True)


    # format the Delivery Date column to be in the format of month day, year
    data['Delivery Date'] = pd.to_datetime(data['Delivery Date']).dt.strftime('%B %d, %Y')

    # updage ToC column to be True or False instead of 1 or 0
    data['ToC'] = data['ToC'].astype(str)
    data['ToC'] = data['ToC'].str.replace(r'1', 'True',True)
    data['ToC'] = data['ToC'].str.replace(r'0', 'False',True)

    # mapping the delivery type column with the json file
    with open('json/Delivery_Type.json') as json_file:
        DeliveryTypeJson = json.load(json_file)

    # update the delivery type column
    data['Delivery Type'] = data['Delivery Type'].replace(DeliveryTypeJson)
    del DeliveryTypeJson

    # mapping the MW Attending - primary and MW Attending - secondary
    with open('json/midwives.json') as json_file:
        midwivesJson = json.load(json_file)

    # update the MW Attending - primary and MW Attending - secondary
    data['MW Attending - primary'] = data['MW Attending - primary'].replace(midwivesJson)
    data['MW Attending - secondary'] = data['MW Attending - secondary'].replace(midwivesJson)

    del midwivesJson

    data.to_csv('cleaned_data/Blue Heron Babies and Birth Log.csv',index=False)

# data clean up for Courses of Care

def clean_up_multiple_wives(midwivesJson,data):
    whole_list = []
    for index, row in data.iterrows():
        temp = []
        if row['MW-2nd fee'] is not None:
            for i in row['MW-2nd fee']:
                try:
                    temp.append(midwivesJson[i])
                except:
                    pass
                    
            #convert the list to string
            temp = ', '.join(temp)
            whole_list.append(temp)
            
        else:
            whole_list.append(None)
    
    data['MW-2nd fee'] = whole_list


def clean_up_Courses_of_Care():
    data = pd.read_csv('raw_data/Courses of Care.csv',encoding='cp1252')
# clean up the data by removing the 0x92 byte
    data = data.replace('’', "'", regex=True)
    data = data.replace(np.nan,None)
    # update the speical population column with True or False instead of 1 or 0
    data['Special Population'] = data['Special Population'].astype(str)
    data['Special Population'] = data['Special Population'].str.replace(r'1', 'True',True)
    data['Special Population'] = data['Special Population'].str.replace(r'0', 'False',True)

    # update EDD,Initial Date, D/C,	Billing Date to be in the format of month day, year
    for item in ['EDD','Initial Date','D/C','Billing Date']:
        data[item] = pd.to_datetime(data[item]).dt.strftime('%B %d, %Y')
    del item

    with open('json/midwives.json') as json_file:
        midwivesJson = json.load(json_file)
    
    # use pandas update MW-billing	MW-other columns
    data['MW-billing'] = data['MW-billing'].replace(midwivesJson)
    data['MW-other'] = data['MW-other'].replace(midwivesJson)
    data['MW-other2']=data['MW-other2'].replace(midwivesJson)
    data['MW-coordinating'] = data['MW-coordinating'].replace(midwivesJson)

    # there are some mutiple values in the MW-2nd fee column, so we need to split the string and then update the value
    data['MW-2nd fee'] = data['MW-2nd fee'].str.split('/')
    # some of the values are null in the column, some has 1 value, some has more.

    # this is for blue_heron course of care only
    clean_up_multiple_wives(midwivesJson,data)
    
    

    del midwivesJson

    # update the IPCA and Billable column with True or False instead of 1 or 0
    data['IPCA'] = data['IPCA'].astype(str)
    data['Billable'] = data['Billable'].astype(str)
    data['Billable'] = data['Billable'].str.replace(r'1', 'True',True)
    data['Billable'] = data['Billable'].str.replace(r'0', 'False',True)
    data['IPCA'] = data['IPCA'].str.replace(r'1', 'True',True)
    data['IPCA'] = data['IPCA'].str.replace(r'0', 'False',True)

    data

    
    # cannot do speical population description mapping because there are multiple values in each row

    data.to_csv('cleaned_data/Courses of Care.csv',index=False)
    
    del data




if __name__ == "__main__":
    clean_up_client_list()
    clean_up_Blue_Heron_Babies_and_Birth_Log()
    clean_up_Courses_of_Care()
    pass