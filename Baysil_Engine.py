import pandas as pd
import json
import numpy as np
from baysil_lib.Patient import *
import collections

def main(volumn,create_json=False):
    # data read and clean up for client list
    data = pd.read_csv('cleaned_data/Client List.csv')
    # fill nan with None
    data = data.replace(np.nan,None)


    mother_list = []
    for index, row in data.iterrows():
        # instantiate a mother from client list
        mother = Mother(row['Client Name'],row['First Name'],row['Middle Initials'],row['Last Name'],
                        row['Partner Name'],row['Home Phone'],row['Work Phone and Extension'],
                        row['Mobile Phone'],row['Address'],row['City'],row['Province'],row['Postal Code'],
                        row['Email'],row['OHIP Number'],row['DoB'],row['May Contact'],
                        row['May Contact Method'],longdistance =row['IsLongDistance'],
                        secondary_address=row['Secondary Address'])
        mother_list.append(mother)

    del data



    data = pd.read_csv('cleaned_data/Blue Heron Babies and Birth Log.csv')
    data = data.replace(np.nan,None)

    # check memory usage
    # process = psutil.Process()
    # print(process.memory_info().rss / 1024 ** 2,'MB')


    baby_list = []
    for index, row in data.iterrows():
        # instantiate a baby from Blue Heron Babies and Birth Log
        baby = Baby(first_name =row['Baby First Name'],last_name=row['Baby Last Name'],
                    date_of_birth=row['Delivery Date'],
                    gender =row['Baby Gender'],feeding_at_birth=row['Feeding at Birth'],
                    feeding_at_D_C=row['Feeding at D/C'],
                    delivery_type=row['Delivery Type'],toc=row['ToC'],
                    mw_primary=row['MW Attending - primary'],
                    mw_secondary=row['MW Attending - secondary'],
                    coc_id=row['CoC ID'],birth_place = row['Birthplace'],baby_ohc=row['Baby OHC'],
                    birth_place_comment = row['Birthplace comment'])
        baby_list.append(baby)

    # check memory usage
    del data


    # read the data from Courses of Care.csv
    data = pd.read_csv('cleaned_data/Courses of Care.csv')
    data = data.replace(np.nan,None)


    # use baby coc_id to match the row in data 
    match_list = []
    for baby in baby_list:
        # find the row in data that has the same coc_id as the baby
        row = data.loc[data['CoC ID'] == baby.coc_id]

        # get the value of the row 
        row = row.to_dict('records')[0]


        # row is the dictionary of the row
        # mother's name 
        baby.mother_name = row['Client Name']
        # baby carry all the information from the row of this Course of Care
        baby.special_population = row['Special Population']
        baby.special_population_description = row['Special Population Description']
        baby.gravida = row['Gravida']
        baby.para = row['Para']
        baby.edd = row['EDD']
        baby.initial_date = row['Initial Date']
        baby.d_c = row['D/C']
        baby.billing_date =  row['Billing Date']
        baby.billable = row['Billable']
        baby.mw_billing = row['MW-billing']
        baby.mw_other = row['MW-other']
        baby.mw_other2 = row['MW-other2']
        baby.mw_coordinating = row['MW-coordinating']
        baby.mw_2nd_fee = row['MW-2nd fee']
        baby.ipca = row['IPCA']
        baby.ipca_comment = row['IPCA Comment']
        baby.notes = row['Notes']
        baby.special_instructions = row['Special Instructions']
        baby.chart_scan_date = row['Chart Scan Date']
        baby.chart_shred_date = row['Chart Shred Date']

        # add coc id to the match list
        match_list.append(baby.coc_id)
    
    # remove the matched coc_id from the data
    data = data[~data['CoC ID'].isin(match_list)]
    
    #build dummy baby instance from data and add them to baby_list
    for index, row in data.iterrows():
        baby = Baby()

        baby.coc_id = row['CoC ID']
        baby.mother_name = row['Client Name']
        # baby carry all the information from the row of this Course of Care
        baby.special_population = row['Special Population']
        baby.special_population_description = row['Special Population Description']
        baby.gravida = row['Gravida']
        baby.para = row['Para']
        baby.edd = row['EDD']
        baby.initial_date = row['Initial Date']
        baby.d_c = row['D/C']
        baby.billing_date =  row['Billing Date']
        baby.billable = row['Billable']
        baby.mw_billing = row['MW-billing']
        baby.mw_other = row['MW-other']
        baby.mw_other2 = row['MW-other2']
        baby.mw_coordinating = row['MW-coordinating']
        baby.mw_2nd_fee = row['MW-2nd fee']
        baby.ipca = row['IPCA']
        baby.ipca_comment = row['IPCA Comment']
        baby.notes = row['Notes']
        baby.special_instructions = row['Special Instructions']
        baby.chart_scan_date = row['Chart Scan Date']
        baby.chart_shred_date = row['Chart Shred Date']


        baby_list.append(baby)

    tmp_data = pd.read_csv('cleaned_data/Blue Heron Babies and Birth Log.csv')
    tmp_data = tmp_data.replace(np.nan,None)
    tmp_data = tmp_data[~tmp_data['CoC ID'].isin(match_list)]

    # remaining data is the data that has no coc_id match
    data.to_csv('check_list/remaining data.csv',index=False)
    tmp_data.to_csv('check_list/remaining baby data.csv',index=False)
    
    del data, tmp_data

    # create a family dictionary with mother

    # once the baby find mother, add them into the family list, if the family has more than 1 baby, add them into the same family

    mother_dict = {}
    for mother in mother_list:
        # create a dictionary with mother name as key and mother instance as value
        mother_dict[mother.client_name] = mother

    n = 0
    m = 0
    check_list_cocid = []
    baby_first_name = []
    baby_last_name = []
    mother_name = []

    for baby in baby_list:
        # add baby into the mother instance to make a family
        try:
            
            mother_dict[str(baby.mother_name)].add_baby(baby)

            m += 1
        except:
            # print(baby.first_name,' has no mother')
            # adding this baby to checklist
            check_list_cocid.append(baby.coc_id)
            baby_first_name.append(baby.first_name)
            baby_last_name.append(baby.last_name)
            mother_name.append(baby.mother_name)

            n += 1
            # someone only exist in course of care, not in client list nor birth log
            
        
    # make the check list as df
    df = pd.DataFrame({'coc_id':check_list_cocid,'baby_first_name':baby_first_name,'baby_last_name':baby_last_name,'mother_name':mother_name})
    df.to_csv('check_list/baby without mother.csv',index=False)
    del df

    # print('number of baby without mother:',n)
    # print('number of baby with mother:',m)

    # open json file
    with open('json/special_population_mapping.json') as f:
        special_population_map = json.load(f)
    
    # open preferredcontactmethod json file
    with open('json/preferredcontactmethod.json') as f:
        preferredcontactmethod = json.load(f)

    with open('json/client_insurance_type.json') as f:
        client_insurance_type = json.load(f)

    with open('json/feeding_method.json') as f:
        feeding_json = json.load(f)

    # family dictionary is created
    count = 0
    
    temp_list_1 = []
    temp_list_2 = []
    temp_list_3 = []

    multiple_baby_list = []
    
    for mother in mother_list:
        family_list = []
        count += 1

        if count == volumn:
            break

        for child in mother.children:

            baby_record = child.build_baby_record(mother,special_population_map,feeding_json)
            
            # add baby record to the family list only for real baby with toc
            if child.toc != None:
                family_list.append(baby_record)

            mother.coc_id.append(child.coc_id)

        # create mother record
        mother_record = mother.build_mother_record(preferredcontactmethod,client_insurance_type)

        family_list.insert(0,mother_record)

        name_of_mother = str(mother.first_name or '') + ' ' + str(mother.last_name or '')    
        
        no_of_children = len(mother.episode)
        
        temp_list_1.append(name_of_mother)
        temp_list_2.append(no_of_children)
        temp_list_3.append(mother.coc_id)

        # update the baby coc_id if this is a twin in multiple_baby_list
        if no_of_children > 1 and len(mother.coc_id) != len(set(mother.coc_id)):
            twin_coc_id = [item for item, count in collections.Counter(mother.coc_id).items() if count > 1]
            n = 0
            for child in mother.children:

                # update twin babies's coc_id with a sequence number of A and B ...
                # cannot handle one mother has more than 2 twins now

                if child.coc_id in twin_coc_id:

                    sequence_number = chr(twin_coc_id.index(child.coc_id) + 65 + n)
                    final_identifier = child.record['episode']['identifications']['identifier'] + sequence_number
                    child.record['episode']['identifications']['identifier'] = final_identifier
                    # question: assume there is only 1 file in the documents
                    child.record['episode']['documents'][0]['fileName']=f'path/{final_identifier}.pdf'
                    n += 1

            # mother episode can be combined into one episode when the episode is from a twin
            episode_list = []
            for episode in mother.episode:
                # if the identifier already exist, remove this episode from mother.episode 
                if episode['identifications']['identifier'] in episode_list:
                    mother.episode.remove(episode)
                    # remove the last item in episode_list
                else:
                    episode_list.append(episode['identifications']['identifier'])
                      

            
           

        # make this family list into a json file
        if create_json:
            with open(f'sample/{mother.coc_id}_{mother.first_name}_{mother.last_name}_family.json', 'w') as outfile:
                json.dump(family_list, outfile)


    df = pd.DataFrame({'mother_name':temp_list_1,'mother_cod_id':temp_list_3,'number_of_episode':temp_list_2})
    df.to_csv('check_list/number of baby for each mother.csv',index=False)
        

if __name__ == '__main__':
    main(10,False)