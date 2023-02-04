import pandas as pd
import json
import numpy as np
from baysil_lib.Patient import *


def main():
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
                        row['Email'],row['OHIP Number'],row['DoB'],row['May Contact'],row['May Contact Method'])
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
                    coc_id=row['CoC ID'],birth_place = row['Birthplace'],baby_ohc=row['Baby OHC'])
        baby_list.append(baby)

    # check memory usage
    del data


    # read the data from Courses of Care.csv
    data = pd.read_csv('cleaned_data/Courses of Care.csv')
    data = data.replace(np.nan,None)



    # use baby coc_id to match the row in data 

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
        
# at this moment, baby instance has all information 
# from the birth log, blue heron baby and the course of care list
# mother instance has all information from the client list

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
            # make the check list as df
            df = pd.DataFrame({'coc_id':check_list_cocid,'baby_first_name':baby_first_name,'baby_last_name':baby_last_name,'mother_name':mother_name})
            df.to_csv('check_list/baby without mother.csv')
            del df

    # open json file
    with open('json/special_population_mapping.json') as f:
        special_population_map = json.load(f)
    
    # open preferredcontactmethod json file
    with open('json/preferredcontactmethod.json') as f:
        preferredcontactmethod = json.load(f)

    # family dictionary is created
    count = 0
    
    temp_list_1 = []
    temp_list_2 = []
    temp_list_3 = []

    for mother in mother_list:
        family_list = []
        count += 1
        print(count)
        # create baby record
        
        if count == 5:
            break

        for child in mother.children:
            baby_record = child.build_baby_record(mother,special_population_map)
            family_list.append(baby_record)
            # mother can have many coc-id
            mother.coc_id.append(child.coc_id)

        # create mother record
        mother_record = mother.build_mother_record(preferredcontactmethod)

        family_list.insert(0,mother_record)

        name_of_mother = str(mother.first_name or '') + ' ' + str(mother.last_name or '')    
        
        no_of_children = len(mother.episode)
        
        temp_list_1.append(name_of_mother)
        temp_list_2.append(no_of_children)
        temp_list_3.append(mother.coc_id)
    
    # make a df with mother name and number of children


        # make this family list into a json file

        # make this family list into a json file

        with open(f'sample/{mother.first_name}_{mother.last_name}_family.json', 'w') as outfile:
            json.dump(family_list, outfile)

    df = pd.DataFrame({'mother_name':temp_list_1,'mother_cod_id':temp_list_3,'number_of_children':temp_list_2})
    df.to_csv('check_list/number of baby for each mother.csv',index=False)
        

if __name__ == '__main__':
    main()