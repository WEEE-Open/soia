#!/bin/env python
import requests, random, yaml, time

# Groups to fill the database with, plus the special HR and administrators groups
thematic_groups = ['Riparatori', 'Informatici', 'Elettronici', 'Riuso creativo', 'Sysadmin']
administrators_group = 'Amministratori'
human_resources_group = 'HR'

# File to be written
yaml_file = {'ldap_persons':[]}

# List of PoliTO courses, normalized as used in Crauto
courses =   [
	            'Architecture',
	            'Architecture Construction City',
	            'Architecture For The Sustainability Design',
	            'Architettura',
	            'Architettura Costruzione Città',
	            'Architettura Per Il Progetto Sostenibile',
	            'Architettura Per Il Restauro E Valorizzazione Del Patrimonio',
	            'Automotive Engineering',
	            'Civil Engineering',
	            'Communications And Computer Networks Engineering',
	            'Computer Engineering',
	            'Design E Comunicazione Visiva',
	            'Design Sistemico',
	            'Dottorato in Ambiente E Territorio',
	            'Dottorato in Architettura. Storia E Progetto',
	            'Dottorato in Beni Architettonici E Paesaggistici',
	            'Dottorato in Beni Culturali',
	            'Dottorato in Bioingegneria E Scienze Medico-chirurgiche',
	            'Dottorato in Energetica',
	            'Dottorato in Fisica',
	            'Dottorato in Gestione, Produzione E Design',
	            'Dottorato in Ingegneria Aerospaziale',
	            'Dottorato in Ingegneria Biomedica',
	            'Dottorato in Ingegneria Chimica',
	            'Dottorato in Ingegneria Civile E Ambientale',
	            'Dottorato in Ingegneria Elettrica, Elettronica E Delle Comunicazioni',
	            'Dottorato in Ingegneria Informatica E Dei Sistemi',
	            'Dottorato in Ingegneria Meccanica',
	            'Dottorato in Ingegneria Per La Gestione Delle Acque E Del Territorio',
	            'Dottorato in Matematica Pura E Applicata',
	            'Dottorato in Metrologia',
	            'Dottorato in Scienza E Tecnologia Dei Materiali',
	            'Dottorato in Storia Dell\'architettura E Dell\'urbanistica',
	            'Dottorato in Urban And Regional Development',
	            'Electronic And Communications Engineering',
	            'Electronic Engineering',
	            'Engineering And Management',
	            'ICT For Smart Societies',
	            'Ingegneria Aerospaziale',
	            'Ingegneria Biomedica',
	            'Ingegneria Chimica E Alimentare',
	            'Ingegneria Chimica E Dei Processi Sostenibili',
	            'Ingegneria Civile',
	            'Ingegneria Dei Materiali',
	            'Ingegneria Del Cinema E Dei Mezzi Di Comunicazione',
	            'Ingegneria Dell\'autoveicolo',
	            'Ingegneria Della Produzione Industriale',
	            'Ingegneria Della Produzione Industriale E Dell\'innovazione Tecnologica',
	            'Ingegneria Edile',
	            'Ingegneria Elettrica',
	            'Ingegneria Elettronica',
	            'Ingegneria Energetica',
	            'Ingegneria Energetica E Nucleare',
	            'Ingegneria Fisica',
	            'Ingegneria Gestionale',
	            'Ingegneria Gestionale L-8',
	            'Ingegneria Gestionale L-9',
	            'Ingegneria Informatica',
	            'Ingegneria Matematica',
	            'Ingegneria Meccanica',
	            'Ingegneria Per L\'ambiente E Il Territorio',
	            'Matematica Per L\'ingegneria',
	            'Mechanical Engineering',
	            'Mechatronic Engineering',
	            'Nanotechnologies For Icts',
	            'Petroleum And Mining Engineering',
	            'Physics Of Complex Systems',
	            'Pianificazione Territoriale, Urbanistica E Paesaggistico-ambientale',
	            'Progettazione Delle Aree Verdi E Del Paesaggio',
	            'Territorial, Urban, Environmental And Landscape Planning',
            ]

# How many identities to generate for each group
people_per_group = 5

uids = []

for i,group in enumerate(thematic_groups):
    for j in range(people_per_group):
        attributes = {}
        
        while True:
            identity = requests.get('https://api.namefake.com/italian-italy/random/').json()
            print(f'Gathering identity {(i * people_per_group) + j + 1}/{people_per_group * len(thematic_groups)}')

            attributes['givenName'] = identity['name'].split()[-2]  # Name
            attributes['sn'] = identity['name'].split()[-1]         # Surname

            attributes['cn'] = f'{attributes["givenName"]} {attributes["sn"]}' # Name Surname
            attributes['uid'] = '.'.join([attributes['givenName'].lower(), attributes['sn'].lower()]) # name.surname

            if attributes['uid'] in uids:
                continue
            else:
                uids.append(attributes['uid'])
                break

        attributes['schacPersonalUniqueCode'] = f's{"".join([str(random.randint(0, 9)) for i in range(6)])}'

        attributes['degreeCourse'] = random.choice(courses)

        attributes['mail'] = f'{identity["email_u"]}@{identity["email_d"]}'
        attributes['mobile'] = f'+39{"".join([str(random.randint(0, 9)) for i in range(10)])}'
        attributes['telegramID'] = ''.join([str(random.randint(0,9)) for i in range(8)])

        attributes['schacPlaceOfBirth'] = ' '.join(identity['address'].split(', ')[-1].split(' ')[1:])

        attributes['userPassword'] = "asd"  # Only top-notch security for our test users!
        attributes['weeelabNickname'] = identity['username']

        # Month and day are lowerbounded by 10 so that I don't have to handle zero-padding
        attributes['schacDateOfBirth'] = ''.join([str(random.randint(1995, 2000)), str(random.randint(10, 12)), str(random.randint(10,28))])
        attributes['safetyTestDate'] = ''.join([str(random.randint(2016, 2019)), str(random.randint(10, 12)), str(random.randint(10,28))])

        userGroups = [thematic_groups[i]]

        # If the user is the first of its tematic group, also add it to the administrative groups
        if j == 0:
            userGroups.append(administrators_group)
            userGroups.append(human_resources_group)
        
        yaml_file['ldap_persons'].append({'attributes':attributes, 'groups':userGroups})

        # Servers get *really* upset if we don't wait a bit
        time.sleep(0.25)

with open('identities.yml', 'w') as output_file:
    yaml.dump(yaml_file, output_file)