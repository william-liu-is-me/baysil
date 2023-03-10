import pandas as pd
import re

class Person:
    def __init__(self,first_name=None,middle_name=None,last_name=None,partner_name=None,home_phone=None,work_phone_with_extension=None,mobile_phone=None,address=None,city=None,province=None,postal_code=None,email=None,
                ohip_number=None,date_of_birth=None,may_contact=None,contact_method=None,coc_id=None):

        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.partner_name = partner_name
        self.home_phone = home_phone
        self.work_phone_with_extension = work_phone_with_extension
        self.mobile_phone = mobile_phone
        self.address = address
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.email = email
        self.ohip_number = ohip_number
        self.date_of_birth = date_of_birth
        self.may_contact = may_contact
        self.contact_method = contact_method
        self.coc_id = coc_id

    def create_dict_for_all_information(self):
        # need data mapping support 
        return {'Imported date':'date','key_value_pair':'All original data. Pending for future development'}


class Mother(Person):

    def __init__(self,client_name=None,first_name=None,middle_name=None,last_name=None,partner_name=None,home_phone=None,work_phone_with_extension=None,mobile_phone=None,address=None,city=None,province=None,postal_code=None,email=None,
                ohip_number=None,date_of_birth=None,may_contact=None,contact_method=None,coc_id=None,children=None,episode=None,longdistance=None,secondary_address = None):
        super().__init__(first_name,middle_name,last_name,partner_name,home_phone,work_phone_with_extension,mobile_phone,address,city,province,postal_code,email,
                ohip_number,date_of_birth,may_contact,contact_method,coc_id)
        self.children = []
        self.episode = []
        self.population_groups = []
        self.gender = 'Female'
        self.client_name = client_name
        self.middle_name = middle_name
        self.coc_id = []
        self.longdistance = longdistance
        self.secondary_address = secondary_address

    
    def add_baby(self,baby):
        
        self.children.append(baby)

        # more than 1 episode, notes show which episode?
        
    def create_mother_dict_for_all_information(self):
        mother_original_data_dictionary = {}
        mother_original_data_dictionary['client_name'] = self.client_name
        mother_original_data_dictionary['first_name'] = self.first_name
        mother_original_data_dictionary['middle_name'] = self.middle_name
        mother_original_data_dictionary['last_name'] = self.last_name
        mother_original_data_dictionary['partner_name'] = self.partner_name
        mother_original_data_dictionary['home_phone'] = self.home_phone
        mother_original_data_dictionary['work_phone_with_extension'] = self.work_phone_with_extension
        mother_original_data_dictionary['mobile_phone'] = self.mobile_phone
        mother_original_data_dictionary['isLongDistance'] = self.longdistance
        mother_original_data_dictionary['address'] = self.address
        mother_original_data_dictionary['city'] = self.city
        mother_original_data_dictionary['province'] = self.province
        mother_original_data_dictionary['postal_code'] = self.postal_code
        mother_original_data_dictionary['secondary address'] = self.secondary_address
        mother_original_data_dictionary['email'] = self.email
        mother_original_data_dictionary['ohip_number'] = self.ohip_number
        mother_original_data_dictionary['date_of_birth'] = self.date_of_birth
        mother_original_data_dictionary['may_contact'] = self.may_contact
        mother_original_data_dictionary['contact_method'] = self.contact_method

        # handle multiple episode: add one more key value pair
        temp = []
        for child in self.children:
                if child.coc_id not in temp:
                        temp.append(child.coc_id)
                        temp_cocid = str(child.coc_id).zfill(5)
                        key = f'notes for episode {temp_cocid}'
                        # make a dictionary for each episode
                        mother_original_data_dictionary[key] = {}
                        mother_original_data_dictionary[key]['Special population'] = child.special_population
                        mother_original_data_dictionary[key]['Special population description'] = child.special_population_description
                        mother_original_data_dictionary[key]['Gravida'] = child.gravida
                        mother_original_data_dictionary[key]['Para'] = child.para
                        mother_original_data_dictionary[key]['EDD'] = child.edd
                        mother_original_data_dictionary[key]['Initial date'] = child.initial_date
                        mother_original_data_dictionary[key]['D/C'] = child.d_c
                        mother_original_data_dictionary[key]['Billing date'] = child.billing_date
                        mother_original_data_dictionary[key]['Billable'] = child.billable
                        mother_original_data_dictionary[key]['MW-billing'] = child.mw_billing
                        mother_original_data_dictionary[key]['MW-other'] = child.mw_other
                        mother_original_data_dictionary[key]['MW-other2'] = child.mw_other2
                        mother_original_data_dictionary[key]['MW-coordinating'] = child.mw_coordinating
                        mother_original_data_dictionary[key]['MW-2nd fee'] = child.mw_2nd_fee
                        mother_original_data_dictionary[key]['IPCA'] = child.ipca
                        mother_original_data_dictionary[key]['IPCA comment'] = child.ipca_comment
                        mother_original_data_dictionary[key]['Notes'] = child.notes
                        mother_original_data_dictionary[key]['Special Instructions'] = child.special_instructions
                        mother_original_data_dictionary[key]['Chart Scan Date'] = child.chart_scan_date
                        mother_original_data_dictionary[key]['Chart Shred Date'] = child.chart_shred_date

        # end of client list file data
        # convert the dictionary into a string
        temp_dict ={'original data': mother_original_data_dictionary}
        return str(temp_dict)


    def parse_mother_ohip_number(self,clientinsurancetype):

        if self.ohip_number == None:
                return None,None
                #remove space in the string
        else:
                ohip_number = self.ohip_number.replace(' ','')

                # this is ohip number 
                if ohip_number[:-2].isdigit() and len(ohip_number[:-2]) == 10:
                        number = ohip_number[:-2]
                        version = ohip_number[-2:]
                        return "baysil_idSystem_ohipOntario",str(number+" "+version)

                elif ohip_number.isdigit() and len(ohip_number) == 10:
                        return "baysil_idSystem_ohipOntario",str(ohip_number)

                else:
                # this is not ohip number, need to use the letter to determine the insurance type
                    
                    # split the string by space
                    string_list = self.ohip_number.split(' ')
                    
                
                    try:
                        insurance_type = clientinsurancetype[string_list[0].upper()]
                        insurance_number_number = string_list[1]

                        return insurance_type,insurance_number_number
                    except:
                        return None,None
                    # return the insurance type and the number in the ohip_number
                        

    def parse_contact_preference(self,preferred_contact_method_json):
        parse_result = []
        try:
                self.contact_method = self.contact_method.lower()
        except:
                        # how to handle nan value

                self.contact_method = str(self.contact_method).lower()
                


        # how to handle nan value

        parse_result.append(preferred_contact_method_json['preferredSystem'][self.contact_method])
        parse_result.append(preferred_contact_method_json['preferredSystemType'][self.contact_method])
        parse_result.append(preferred_contact_method_json['preferredUse'][self.contact_method])

        return parse_result


    def build_mother_record(self,preferredcontactmethod,clientinsurancetype):
        mother_record = {}
        mother_record['firstName'] = self.first_name
        mother_record['middleName'] = self.middle_name
        mother_record['lastName'] = self.last_name

        # assume data clean up has been done, first name and last name always exist
        if self.middle_name:
            mother_record['preferredName'] = self.first_name + ' ' + self.middle_name + ' ' + self.last_name
        else:
            mother_record['preferredName'] = str(self.first_name or '') + ' ' + str(self.last_name or '')
        
        mother_record['gender'] = 'baysil_gender_female'
        mother_record['dateOfBirth'] = self.date_of_birth

        try:
                final_description = []
                for description in self.population_groups:
                        for item in description:
                                final_description.append(item)
                mother_record['populationGroups'] = final_description
                del final_description
        except:
                mother_record['populationGroups'] = None

        # parse ohip number, if not valid, return None 
        insurance_type,identifier = self.parse_mother_ohip_number(clientinsurancetype)

        # as per 1.30 meeting, mother CoC ID is not required
        mother_record['identifications'] = [
                {'system':insurance_type,
                'identifier':identifier}
        ]

        # if the value is none, dont even show this field 
        contact_info = []
        if self.email:
                contact_info.append({'system':'baysil_contactSystem_email',
                'value':self.email})
        if self.mobile_phone:
                contact_info.append({'system':'baysil_contactSystem_phone',
                'value':self.mobile_phone,
                'systemType':'baysil_contactUse_mobile',
                'use':'baysil_contactUse_personal'})
        if self.home_phone:
                contact_info.append({'system':'baysil_contactSystem_phone',
                'value':self.home_phone,
                'systemType':'baysil_contactUse_landline',
                'use':'baysil_contactUse_home'})
        if self.work_phone_with_extension:
                contact_info.append({'system':'baysil_contactSystem_phone',
                'value':self.work_phone_with_extension,
                'systemType':'baysil_contactUse_landline',
                'use':'baysil_contactUse_business'})
        mother_record['contactInformation'] = contact_info
        
        a,b,c = self.parse_contact_preference(preferredcontactmethod)

        mother_record['contactPreference'] = {
                'mayBeContacted':self.may_contact,
                'preferredSystem':a,
                'preferredSystemType':b,
                'preferredUse':c
                }
        # if address is None, text will be None
        # manual data cleanup for address and city, province, postal code is required
        
        if self.address == None:

                text = None
                province = self.province
        else:
                # convert ON/Ont to Ontario
                if self.province == 'Ont' or self.province == 'ON':
                        province = 'Ontario'
                else:
                        province = self.province

                text = str(self.address or '') + ', ' + str(self.city or '') + ', ' + str(province or '') + ' ' + str(self.postal_code or '') + ' Canada'

        
        mother_record['locations'] = [
                {'name':'Home address',
                'address':{
                        'text': text,
                        'streetAddress':self.address,
                        'postalCode':self.postal_code,
                        'city':self.city,
                        'region':province,
                        'country':'Canada'
                }}
        ]

        try:
                split_name = self.partner_name.split(' ')
                if len(split_name) == 2:
                        firstname = split_name[0]
                        lastname = split_name[1]
                        middle_name = None
                elif len(split_name) == 3:
                        firstname = split_name[0]
                        middle_name = split_name[1]
                        lastname = split_name[2]
                else:
                        firstname = None
                        middle_name = None
                        lastname = None

        except:
                firstname = None
                middle_name = None
                lastname = None
                split_name = None
        mother_record['relatives'] = [
                {       #leave empty
                        'person':{
                                'identifiedInSystem': None,
                                'identifiedAs': None,
                                'firstName': firstname,
                                'middleName': middle_name,
                                'lastName': lastname,
                                'preferredName': self.partner_name,
                        },
                        'relationship':
                                'baysil_relationshipType_domesticPartner'
                }
        ]
        del firstname,middle_name,lastname,split_name

        # mother episode is created by each baby episode and attend to mother.episode
        if len(self.episode) > 0:
            mother_record['episodes'] = self.episode
        else:
            mother_record['episodes'] = 'pending for future update'

        # need to update account and notes for mother episode

        mother_record['notes']  = self.create_mother_dict_for_all_information()

        return mother_record


class Baby(Person):


    def __init__(self,first_name=None,middle_name=None,last_name=None,partner_name=None,home_phone=None,work_phone_with_extension=None,
                mobile_phone=None,address=None,city=None,province=None,postal_code=None,email=None,
                ohip_number=None,date_of_birth=None,may_contact=None,contact_method=None,
                mother=None,episode=None,gender= None,feeding_at_birth=None,feeding_at_D_C=None,delivery_type=None,
                toc=None,mw_primary=None,mw_secondary=None,mw_2nd_fee=None,mw_coordinating=None,
                mw_other2=None,coc_id=None,birth_place = None,baby_ohc=None,birth_place_comment=None):
        super().__init__(first_name,middle_name,last_name,partner_name,home_phone,work_phone_with_extension,
                mobile_phone,address,city,province,postal_code,email,
                ohip_number,date_of_birth,may_contact,contact_method,coc_id)
                
        self.mother = mother
        self.gender = gender
        self.episode = episode
        self.feeding_at_birth = feeding_at_birth
        self.date_of_birth = date_of_birth
        self.feeding_at_D_C = feeding_at_D_C
        self.delivery_type = delivery_type
        self.toc = toc
        self.mw_primary = mw_primary
        self.mw_secondary = mw_secondary
        self.birth_place = birth_place
        self.baby_ohc = baby_ohc
        self.birth_place_comment = birth_place_comment

    def create_baby_dict_for_all_information(self):
        # create a baby dictionary for all original information
        baby_dict = {}
        # coc id is 5 digit number, need to add 0s in front
        if self.coc_id:
                coc_id = str(self.coc_id).zfill(5) + 'B'
        else:
                coc_id = self.coc_id

        baby_dict['coc id'] = coc_id
        baby_dict['first name'] = self.first_name
        baby_dict['last name'] = self.last_name
        baby_dict['baby gender'] = self.gender 
        baby_dict['feeding at birth'] = self.feeding_at_birth
        baby_dict['feeding at D/C'] = self.feeding_at_D_C
        baby_dict['baby ohip'] = self.baby_ohc
        # question: ignore field 1,2,3 for now 
        baby_dict['delivery date'] = self.date_of_birth
        baby_dict['delivery type'] = self.delivery_type
        baby_dict['toc'] = self.toc
        baby_dict['MW attending - primary'] = self.mw_primary
        baby_dict['MW attending - secondary'] = self.mw_secondary
        baby_dict['Birthplace'] = self.birth_place
        baby_dict['Birthplace comment'] = self.birth_place_comment
        
        temp_dict = {'original data':baby_dict}
        return temp_dict

    def parse_baby_ohc(self):
        if self.baby_ohc:
                #remove space in the string
                self.baby_ohc = self.baby_ohc.replace(' ','')
                try:
                #check if the last two characters are letters and first 10 characters are digits
                        if self.baby_ohc[:-2].isdigit() and self.baby_ohc[-2:].isalpha():
                                version = self.baby_ohc[-2:]
                                number = self.baby_ohc[:-2]
                                return str(number)+' '+str(version)
                        elif self.baby_ohc[:-2].isdigit() and not self.baby_ohc[-2:].isalpha():
                                version = None
                                number = self.baby_ohc
                                return number

                        else:
                                return None

                except:
                        return None
        else:
                return None

    def parse_notes_remove_html(self):
        # remove html tags
        if self.notes:
                self.notes = re.sub('<.*?>','',self.notes)
                return self.notes
        else:
                return None

    def gender_mapping_for_baby(self):
            if self.gender == 'F':
                gender = 'baysil_gender_famale'
            elif self.gender == 'M':
                gender = 'baysil_gender_male'
            else:
                gender = self.gender
        
            return gender 

    def build_baby_record(self,mother_instance,PopulationGroupJson,feeding_json):
        self.mother = mother_instance
        record_dict = {}
        record_dict['firstName'] = self.first_name
        record_dict['middleName'] = None #self.middle_name if self.middle_name else None
        record_dict['lastName'] = self.last_name
        record_dict['preferredName'] = None #str(self.first_name or '') + ' ' + str(self.last_name or '')
        gender = self.gender_mapping_for_baby()
        record_dict['gender'] = gender
        record_dict['dateOfBirth'] = self.date_of_birth
        record_dict['populationGroups'] = self.parse_special_population_description(PopulationGroupJson)
        # pass this populationgroups to mother instance
        self.mother.population_groups.append(self.parse_special_population_description(PopulationGroupJson))
        
        # parse baby ohc
        identifier = self.parse_baby_ohc()
        self.baby_ohc = identifier

        record_dict['identifications'] = [{'system':'baysil_idSystem_ohip',
                'identifier':identifier}]
                
        contact_info = []
        if self.mother.email:
                contact_info.append({'system':'baysil_contactSystem_email',
                'value':self.mother.email}) 
        if self.mother.mobile_phone:
                contact_info.append({'system':'baysil_contactSystem_phone',
                'value':self.mother.mobile_phone,
                'systemType':'baysil_contactUse_mobile',
                'use':'baysil_contactUse_personal'})
        if self.mother.home_phone:
                contact_info.append({'system':'baysil_contactSystem_phone',
                'value':self.mother.home_phone,
                'systemType':'baysil_contactUse_landline',
                'use':'baysil_contactUse_home'})
        if self.mother.work_phone_with_extension:
                contact_info.append({'system':'baysil_contactSystem_phone',
                'value':self.mother.work_phone_with_extension,
                'systemType':'baysil_contactUse_landline',
                'use':'baysil_contactUse_business'})
        record_dict['contactInformation'] = contact_info
        
        record_dict['contactPreference'] = {
                'mayBeContacted':self.mother.may_contact,
                'preferredSystem':None,
                'preferredUse':None,
                'preferredRelative':'baysil_relationshipType_mother'
        }
        # here we need to pass the address from mother to baby
        

        self.address = self.mother.address
        self.city = self.mother.city
        self.province = self.mother.province
        self.postal_code = self.mother.postal_code
        if self.address == None:

                text = None
                province = self.province
        else:
                # convert ON/Ont to Ontario
                if self.province == 'Ont' or self.province == 'ON':
                        province = 'Ontario'
                else:
                        province = self.province

                text = str(self.address or '') + ', ' + str(self.city or '') + ', ' + str(province or '') + ' ' + str(self.postal_code or '') + ' Canada'

        # question, if data missing, cannot perfrom string concatenation, how to handle this?
        record_dict['locations'] = [
                {'name':'Home address',
                'address':{
                        'text': text,
                        'streetAddress':self.address,
                        'postalCode':self.postal_code,
                        'city':self.city,
                        'region':province,
                        'country':'Canada'
                }}
        ]
        
        # coc_id is 5 digits, if it is less than 5 digits, add 0 in front of it
        if self.coc_id:
                coc_id = str(self.coc_id).zfill(5)
        else:
                coc_id = self.coc_id
        record_dict['relatives'] = [
                {
                'person':{
                        'identifiedInSystem':'baysil_idSystem_blueHeronCocid',
                        'identifiedAs':str(coc_id),
                        # as per requirements
                        'firstName':None,#self.mother.first_name,
                        'middleName':None,#self.mother.middle_name,
                        'lastName':None,#self.mother.last_name,
                        'preferredName':None,
                },
                'relationship':'baysil_relationshipType_mother'
                }
                                        ]

        self.build_baby_episode(record_dict,feeding_json)
       
        mother_episode = self.build_mother_episode()
        self.mother.episode.append(mother_episode)

        record_dict['notes'] = self.create_baby_dict_for_all_information()

        self.record = record_dict

        return record_dict

    def parse_feeding_method(self,feeding_method,feeding_json):

        # parse the feeding method is very complicated

        # 1. check if the feeding method is empty
        if feeding_method == None:
                # assume none / unknown
                return 'baysil_feedingMethod_unknown'
        else:   
                
                # 2. lower case string, split by comma, space, and slash, & sign, + sign
                feeding_method = feeding_method.upper()
                feeding_method = feeding_method.replace(',',' ')
                feeding_method = feeding_method.replace('/',' ')
                feeding_method = feeding_method.replace('&',' ')
                feeding_method = feeding_method.replace('+',' ')
                feeding_method = feeding_method.split(' ')

                temp = []
                for i in feeding_method:
                        try:
                                temp.append(feeding_json[i])
                        except:
                                pass
                if len(temp) == 0:
                        return 'baysil_feedingMethod_unknown'
                else:
                        return temp


    def build_mother_episode(self):
        # cocid is 5 digits, if it is less than 5 digits, add 0 in front of it

        coc_id = str(self.coc_id).zfill(5)
        identifier = str(coc_id)
        mother_episode = {
        'start': self.initial_date,
        'end': self.d_c,
        'identifications':[{
                'system':'baysil_idSystem_blueHeronCocid',
                'identifier':identifier
        }],
        'careManager': {
                'firstName':None,
                'middleName':None,
                'lastName':None,
        },
        'careTeamParticipants':[],
        'observations':[
                {'observable':'baysil_observable_gravida',
                        'value':self.gravida,
                        'notes':None},
                        {'observable':'baysil_observable_para',
                        'value':self.para,
                        'notes':None},
                        {'observable':'baysil_observable_edd',
                        'value':self.edd,
                        'notes':None},
                        {'observable':'baysil_observable_ipca',
                        'value':self.ipca,
                        'notes':self.ipca_comment},
                        {'observable':'baysil_observable_transferredCare',
                        'value':self.toc,
                        'notes':None},
                        {'observable':'baysil_observable_deliveryDate',
                        'value':self.date_of_birth,
                        'notes':None},
                        {'observable':'baysil_observable_deliveryType',
                        'value':self.delivery_type,
                        'notes':None},
                ],
        'account':{
                'billable':self.billable,
                        'notBillingReason':None,
                        'billingDate':self.billing_date,
                        'notes':None
        },
        'notes':self.parse_notes_remove_html(),
        'documents':[
                {'fileName':f'{identifier}.pdf'}
        ],
        }

        # update the caremanager, primary midwife and secondary midwife, 2nd fee, mw coordinating, other2.
        final_mother_episode = self.update_mother_care_team_participants(mother_episode)
        
        return final_mother_episode


    def build_baby_episode(self,record_dict,feeding_json):
        # cocid is 5 digits, if it is less than 5 digits, add 0 in front of it
        if self.coc_id:
                coc_id = str(self.coc_id).zfill(5)
        else:
                coc_id = self.coc_id

        sequence_number = ''
        
        # if there are twins, the sequence number is A and B and etc.
        identifier = str(coc_id or '')+'B' + sequence_number
        record_dict['episodes'] = {
                'start': self.date_of_birth,
                'end': self.d_c,
                'identifications':[{
                        'system':'baysil_idSystem_blueHeronCocid',
                        'identifier':identifier
                }],
                'careManager': {
                        'firstName':None,
                        'middleName':None,
                        'lastName':None,
                },
                'careTeamParticipants':[
                        # MW-billing
                        
                        {'person':
                                {'firstName':None,
                                'middleName':None,
                                'lastName':None,
                        },
                        'role':'baysil_providerRole_primaryMidwife'
                        },
                        ],
                # baby and mother has different obersevations
                'observations':[
                        {'observable':'baysil_observable_feedingMethodAtBirth',
                        'value':self.parse_feeding_method(self.feeding_at_birth,feeding_json),
                        'notes':self.feeding_at_birth},
                        {'observable':'baysil_observable_feedingMethodAtDischarge',
                        'value':self.parse_feeding_method(self.feeding_at_D_C,feeding_json),
                        'notes':self.feeding_at_D_C},
                        {'observable':'baysil_observable_transferredCare',
                        'value':self.toc,
                        'notes':None},
                        {'observable':'baysil_observable_dateOfBirth',
                        'value':self.date_of_birth,
                        'notes':None},
                        {'observable':'baysil_observable_deliveryType',
                        'value':self.delivery_type,
                        'notes':None}, # question here.# what is this preterm?
                        {'observable':'baysil_observable_birthPlace',
                        'value':self.birth_place,
                        'notes':None}],
                'account':None,
                'notes':None,
                'documents':[
                        {'fileName':f'{identifier}.pdf',}
                ]
                }
        if self.delivery_type == 'Premature':
            record_dict['episodes']['observations'].insert(5,{'observable':'baysil_observable_pretermBirth',
                                'value':self.delivery_type,
                                'notes':None})

            record_dict['episodes']['observations'].pop(4)

        self.update_baby_care_team_participants(record_dict)#, mw_2nd_fee, mw_coordinating, mw_other2)

        record_dict['episodes'] = [record_dict['episodes']]



    def update_baby_care_team_participants(self,record_dict):# ,mw_2nd_fee,mw_coordinating,mw_other2):
                # update the caremanager, primary midwife and secondary midwife
        caremanager = self.mw_primary.split(' ') if pd.isnull(self.mw_primary) == False else None
        primary_midwife = caremanager
        secondary_midwife = self.mw_secondary #.split(' ') if pd.isnull(self.mw_secondary) == False else None

        try:
       
            record_dict['episodes']['careManager']['firstName'] = caremanager[0]
            record_dict['episodes']['careManager']['lastName'] = caremanager[1]
        except:
                pass
        try:
            record_dict['episodes']['careTeamParticipants'][0]['person']['firstName'] = primary_midwife[0]
            record_dict['episodes']['careTeamParticipants'][0]['person']['lastName'] = primary_midwife[1]
        except:
                pass


        self.handle_multiple_midwives_in_team_participants(secondary_midwife,record_dict['episodes'],'baysil_providerRole_secondaryMidwife')
    
    def handle_multiple_midwives_in_team_participants(self,midwife,episode,role):
        if midwife:
                # convert to list
                midwife = midwife.split(',')

                for item in midwife:
                        item = item.split(' ')
                        episode['careTeamParticipants'].append({'person':
                                {'firstName':item[0],
                                'middleName':None,
                                'lastName':item[1]},
                                'role':role
                                }
                                )

    def update_mother_care_team_participants(self,mother_episode):
        # update the caremanager, primary midwife and secondary midwife

        caremanager = self.mw_billing.split(' ') if pd.isnull(self.mw_billing) == False else None
        primary_midwife = caremanager
        secondary_midwife = self.mw_other
        mw_coordinating = self.mw_coordinating
        mw_2nd_fee = self.mw_2nd_fee
        mw_other2 = self.mw_other2

        try:
            mother_episode['careManager']['firstName'] = caremanager[0]
            mother_episode['careManager']['lastName'] = caremanager[1]
        except:
                pass
        
        if primary_midwife:
                mother_episode['careTeamParticipants'].append(
                      {'person':{'firstName':primary_midwife[0],
                                'middleName':None,
                                'lastName':primary_midwife[1]},
                        'role':'baysil_providerRole_primaryMidwife'
                        }
                        )
        
        self.handle_multiple_midwives_in_team_participants(secondary_midwife,mother_episode,'baysil_providerRole_secondaryMidwife')

        self.handle_multiple_midwives_in_team_participants(mw_2nd_fee,mother_episode,'baysil_providerRole_secondaryMidwife')

        self.handle_multiple_midwives_in_team_participants(mw_coordinating,mother_episode,'baysil_providerRole_coordinatingMidwife')

        self.handle_multiple_midwives_in_team_participants(mw_other2,mother_episode,'baysil_providerRole_midwife')

        del caremanager, primary_midwife, secondary_midwife, mw_coordinating, mw_other2,mw_2nd_fee

        return mother_episode


    def parse_special_population_description(self,PopulationGroupJson):

        if pd.isnull(self.special_population_description):
            return None
            # cannot return None, return value will be iterated in the for loop
        else:
        # all upper case
            process_description = self.special_population_description.upper()

            # split the string by / or , 
            string_list = re.split(r'[/,]', process_description)
            
            # remove spaces if the space is in the first or the last position
            string_list = [x.strip() for x in string_list]

            population_description_list = []

            for string in string_list:
                try:
                    population_description_list.append(PopulationGroupJson[string])
                except:
                    
                    population_description_list.append('')
            
            return population_description_list 

 


