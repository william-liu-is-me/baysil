import pandas as pd
import re
import copy

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
        return 'Pending for future development'


class Mother(Person):
    def __init__(self,client_name=None,first_name=None,middle_name=None,last_name=None,partner_name=None,home_phone=None,work_phone_with_extension=None,mobile_phone=None,address=None,city=None,province=None,postal_code=None,email=None,
                ohip_number=None,date_of_birth=None,may_contact=None,contact_method=None,coc_id=None,children=None,episode=None):
        super().__init__(first_name,middle_name,last_name,partner_name,home_phone,work_phone_with_extension,mobile_phone,address,city,province,postal_code,email,
                ohip_number,date_of_birth,may_contact,contact_method,coc_id)
        self.children = []
        self.episode = []
        self.population_groups = []
        self.gender = 'Female'
        self.client_name = client_name
        self.middle_name = middle_name
        self.coc_id = []

    
    def add_baby(self,baby):
        
        self.children.append(baby)

    # inherit from Person class
    def create_dict_for_all_information(self):
        return super().create_dict_for_all_information()

    def parse_ohip_number(self):

        if self.ohip_number == None:
                return None
                #remove space in the string
        else:
                self.ohip_number = self.ohip_number.replace(' ','')
                try:
                #check if the last two characters are letters and first 10 characters are digits
                        if self.ohip_number[:-2].isdigit() and self.ohip_number[-2:].isalpha():
                                version = self.ohip_number[-2:]
                                number = self.ohip_number[:-2]
                                return str(number)+'-'+str(version)
                                # number = number[:4] + ' ' + number[4:7] + ' ' + number[7:]
                        elif self.ohip_number[:-2].isdigit() and not self.ohip_number[-2:].isalpha():
                                version = None
                                number = self.ohip_number
                                return str(number)
                                # add one space after 4 digits and another space after 7 digits
                                # number = number[:4] + ' ' + number[4:7] + ' ' + number[7:]
                        else:
                                return None

                except:
                        return None




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


    def build_mother_record(self,preferredcontactmethod):
        mother_record = {}
        mother_record['firstName'] = self.first_name
        mother_record['middleName'] = self.middle_name
        mother_record['lastName'] = self.last_name
        try:
            mother_record['preferredName'] = str(self.first_name or '') + ' ' + str(self.middle_name or '') + ' ' + str(self.last_name or '')
        except:
            mother_record['preferredName'] = self.first_name + ' ' + self.last_name
        
        mother_record['gender'] = 'bay_gender_female'
        mother_record['dateOfBirth'] = self.date_of_birth
        # question: if many children, which speical population description should be used?
        # now let's use all
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
        identifier = self.parse_ohip_number()

        # as per 1.30 meeting, mother CoC ID is not required
        mother_record['identifications'] = [
                {'system':'bay_idSystem_ohip',
                'identifier':identifier}
                # 'identifierVersion':ohip_version}
                # {'system':'bay_idSystem_internal',
                # 'name':'CoC ID',
                # 'identifier':str(self.coc_id)}
        ]


        mother_record['contactInformation'] = [
                {'system':'bay_contactSystem_email',
                'value':self.email},
                {'system':'bay_contactSystem_phone',
                'value':self.mobile_phone,
                'systemType':'bay_contactUse_mobile',
                'use':'bay_contactUse_personal'},
                {'system':'bay_contactSystem_phone',
                'value':self.home_phone,
                'systemType':'bay_contactUse_landline',
                'use':'bay_contactUse_home'},
                {'system':'bay_contactSystem_phone',
                'value':self.work_phone_with_extension,
                'systemType':'bay_contactUse_landline',
                'use':'bay_contactUse_business'}
        ]
        a,b,c = self.parse_contact_preference(preferredcontactmethod)

        mother_record['contactPreference'] = {
                'mayBeContacted':self.may_contact,
                'preferredSystem':a,
                'preferredSystemType':b,
                'preferredUse':c
                }
                
        
        # question, if data missing, cannot perfrom string concatenation, how to handle this?
        mother_record['locations'] = [
                {'name':'Home address',
                'address':{
                        'text': str(self.address or '') + ', ' + str(self.city or '') + ', ' + str(self.province or '') + ' ' + str(self.postal_code or '') + ' Canada',
                        'streetAddress':self.address,
                        'postalCode':self.postal_code,
                        'city':self.city,
                        'region':self.province,
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
                        'identifiedInSystem': None,
                        'identifiedAs': None,
                        'firstName': firstname,
                        'middleName': middle_name,
                        'lastName': lastname,
                        'preferredName': self.partner_name,
                        'relationship':'bay_relationshipType_domesticPartner'
                }
        ]
        del firstname,middle_name,lastname,split_name

        mother_record['episode'] = self.episode

        # need to update account and notes for mother episode

        mother_record['notes']  = self.create_dict_for_all_information()

        return mother_record




class Baby(Person):


    def __init__(self,first_name=None,middle_name=None,last_name=None,partner_name=None,home_phone=None,work_phone_with_extension=None,
                mobile_phone=None,address=None,city=None,province=None,postal_code=None,email=None,
                ohip_number=None,date_of_birth=None,may_contact=None,contact_method=None,
                mother=None,episode=None,gender= None,feeding_at_birth=None,feeding_at_D_C=None,delivery_type=None,
                toc=None,mw_primary=None,mw_secondary=None,coc_id=None,birth_place = None,baby_ohc=None):
        super().__init__(first_name,middle_name,last_name,partner_name,home_phone,work_phone_with_extension,
                mobile_phone,address,city,province,postal_code,email,
                ohip_number,date_of_birth,may_contact,contact_method,coc_id)
                
        self.mother = mother
        self.gender = gender
        self.episode = episode
        self.feeding_at_birth = feeding_at_birth
        self.feeding_at_D_C = feeding_at_D_C
        self.delivery_type = delivery_type
        self.toc = toc
        self.mw_primary = mw_primary
        self.mw_secondary = mw_secondary
        self.birth_place = birth_place
        self.baby_ohc = baby_ohc

    def create_dict_for_all_information(self):
        return super().create_dict_for_all_information()


    def parse_baby_ohc(self):
        if self.baby_ohc:
                #remove space in the string
                self.baby_ohc = self.baby_ohc.replace(' ','')
                try:
                #check if the last two characters are letters and first 10 characters are digits
                        if self.baby_ohc[:-2].isdigit() and self.baby_ohc[-2:].isalpha():
                                version = self.baby_ohc[-2:]
                                number = self.baby_ohc[:-2]
                                return str(number)+'-'+str(version)
                        elif self.baby_ohc[:-2].isdigit() and not self.baby_ohc[-2:].isalpha():
                                version = None
                                number = self.baby_ohc
                                return number

                        else:
                                return None

                        # add one space after 4 digits and another space after 7 digits
                        #number = number[:4] + ' ' + number[4:7] + ' ' + number[7:]

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
    def parse_feeding_method(self,parse_value):
        try:
                parse_value.lower()
                if parse_value == 'breast':
                        return 'bay_feedingMethod_breast'
                elif parse_value == 'formula':
                        return 'bay_feedingMethod_formula'
                elif parse_value == 'breast and formula':
                        return 'bay_feedingMethod_combination'
        
                else:
                        pass
                # pending for future development

        except:
                pass
                
    def build_baby_record(self,mother_instance,PopulationGroupJson):
        self.mother = mother_instance
        record_dict = {}
        record_dict['firstName'] = self.first_name
        record_dict['middleName'] = self.middle_name if self.middle_name else None
        record_dict['lastName'] = self.last_name
        record_dict['preferredName'] = str(self.first_name or '') + ' ' + str(self.last_name or '')
        record_dict['gender'] = self.gender
        record_dict['dateOfBirth'] = self.date_of_birth
        record_dict['populationGroups'] = self.parse_special_population_description(PopulationGroupJson)
        # pass this populationgroups to mother instance
        self.mother.population_groups.append(self.parse_special_population_description(PopulationGroupJson))
        
        # parse baby ohc
        identifier = self.parse_baby_ohc()

        record_dict['identifications'] = [
                {'system':'bay_idSystem_ohip',
                'identifier':identifier},
                # 'identifierVersion':version},
                {'system':'bay_idSystem_internal',
                'name':'CoC ID',
                'identifier':str(self.coc_id or '')+'-B'}
        ]
        # add baby's coc_id to mother's coc_id
        # self.mother.coc_id = self.coc_id

        record_dict['contactInformation'] = [
                {'system':'bay_contactSystem_email',
                'value':self.mother.email},
                {'system':'bay_contactSystem_phone',
                'value':self.mother.mobile_phone,
                'systemType':'bay_contactUse_mobile',
                'use':'bay_contactUse_personal'},
                {'system':'bay_contactSystem_phone',
                'value':self.mother.home_phone,
                'systemType':'bay_contactUse_landline',
                'use':'bay_contactUse_home'},
                {'system':'bay_contactSystem_phone',
                'value':self.mother.work_phone_with_extension,
                'systemType':'bay_contactUse_landline',
                'use':'bay_contactUse_business'}
        ]
        record_dict['contactPreference'] = {
                'mayBeContacted':self.mother.may_contact,
                'preferredRelative':'bay_relationshipType_mother'
        }
        # here we need to pass the address from mother to baby
        
        self.address = self.mother.address
        self.city = self.mother.city
        self.province = self.mother.province
        self.postal_code = self.mother.postal_code

        # question, if data missing, cannot perfrom string concatenation, how to handle this?
        record_dict['locations'] = [
                {'name':'Home address',
                'address':{
                        'text': str(self.address or '') + ', ' + str(self.city or '') + ', ' + str(self.province or '') + ' ' + str(self.postal_code or '') + ' Canada',
                        'streetAddress':self.address,
                        'postalCode':self.postal_code,
                        'city':self.city,
                        'region':self.province,
                        'country':'Canada'
                }}
        ]

        record_dict['relative'] = [
                {'identifiedInSystem':'bay_idSystem_internal',
                'idSystemName':'CoC ID',
                'identifiedAs':str(self.coc_id),
                'firstName':self.mother.first_name,
                'middleName':self.mother.middle_name,
                'lastName':self.mother.last_name,
                'preferredName':str(self.mother.first_name or '') + ' ' + str(self.mother.last_name or ''),
                'relationship':'bay_relationshipType_mother'}
        ]

        # mw_billing
        
        # build the observation outside of the episode, one copy for baby and one copy for mother

        record_dict['episode'] = {
                'start': self.initial_date,
                'end': self.d_c,
                'careManager': {
                        'firstName':None,
                        'middleName':None,
                        'lastName':None,
                },
                'careTeamParticipants':[
                        {'firstName':None,
                        'middleName':None,
                        'lastName':None,
                        'role':'bay_providerRole_primaryMidwife'},
                        {
                        'firstName':None,
                        'middleName':None,
                        'lastName':None,
                        'role':'bay_providerRole_secondaryMidwife'}
                        ],
                # baby and mother has different obersevations
                'observations':[
                        {'observable':'bay_observable_feedingAtBirth',
                        'value':self.feeding_at_birth,
                        'notes':self.feeding_at_birth},
                        {'observable':'bay_observable_feedingAtDischarge',
                        'value':self.feeding_at_D_C,
                        'notes':self.feeding_at_D_C},
                        {'observable':'bay_observable_transferredCare',
                        'value':self.toc,
                        'notes':None},
                        {'observable':'bay_observable_deliveryDate',
                        'value':self.date_of_birth,
                        'notes':None},
                        {'observable':'bay_observable_deliveryPatternAtBirth',
                        'value':self.delivery_type,
                        'notes':None}, # question here.# what is this preterm?
                        {'observable':'bay_observable_birthPlace',
                        'value':self.birth_place,
                        'notes':None}],
                'account':None,
                'notes':None,
                
        }

        record_dict['notes'] = self.create_dict_for_all_information()

        # update the caremanager, primary midwife and secondary midwife
        caremanager = self.mw_billing.split(' ') if pd.isnull(self.mw_billing) == False else None
        primary_midwife = self.mw_primary.split(' ') if pd.isnull(self.mw_primary) == False else None
        secondary_midwife = self.mw_secondary.split(' ') if pd.isnull(self.mw_secondary) == False else None
        
        # update the caremanager, primary midwife and secondary midwife
        try:
       
            record_dict['episode']['careManager']['firstName'] = caremanager[0]
            record_dict['episode']['careManager']['lastName'] = caremanager[1]
        except:
                pass
        try:
            record_dict['episode']['careTeamParticipants'][0]['firstName'] = primary_midwife[0]
            record_dict['episode']['careTeamParticipants'][0]['lastName'] = primary_midwife[1]
        except:
                pass
        try:
            record_dict['episode']['careTeamParticipants'][1]['firstName'] = secondary_midwife[0]
            record_dict['episode']['careTeamParticipants'][1]['lastName'] = secondary_midwife[1]
        except:
                pass


        # send episode to the mother instance
        # update the episode observation for mother and delete the baby observation

        temp_list = [
        {'observable':'bay_observable_gravida',
                        'value':self.gravida,
                        'notes':None},
                        {'observable':'bay_observable_para',
                        'value':self.para,
                        'notes':None},
                        {'observable':'bay_observable_edd',
                        'value':self.edd,
                        'notes':None},
                        {'observable':'bay_observable_transferredCare',
                        'value':self.toc,
                        'notes':None},
                        {'observable':'bay_observable_deliveryDate',
                        'value':self.date_of_birth,
                        'notes':None},
                        {'observable':'bay_observable_deliveryPatternAll',
                        'value':self.delivery_type,
                        'notes':None}
        ] # need to understand the stillbirth and premature
        # replace the episode observations with the temp_list
        
        # make a hard copy of the record_dict
        account_dict = {'account':
                {
                        'billable':self.billable,
                        'notBillingReason':None,
                        'billingDate':self.billing_date,
                        'notes':None,
                }
                }
        note_dict = {'notes':self.parse_notes_remove_html()}
        record_dict_copy = copy.deepcopy(record_dict)
        record_dict_copy['episode']['observations'] = temp_list
        record_dict_copy['episode']['account'] = account_dict['account']
        record_dict_copy['episode']['notes'] = note_dict['notes']
        del temp_list, account_dict, note_dict

        self.mother.episode.append(record_dict_copy['episode'])
        del record_dict_copy

        return record_dict

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

 


