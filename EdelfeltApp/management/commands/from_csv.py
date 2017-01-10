# coding=utf8
__author__ = 'dennis'
import os
from django.core.management.base import BaseCommand
from django.template import Template, Context
from django.conf import settings

import csv
from EdelfeltApp.models import *

app_directory = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]
basepath = os.path.join(os.path.split(app_directory)[0], 'csv/')

class Command(BaseCommand):
    args = 'One or more of the following: all, delete, province, municipality, source, location, link_locations'
    help = 'Loads the data for the selected class. All deletes as well, delete should be run before province if data exists. Note the correct order: province, municipality, source, location, pronounciation. Location loads pronounciations, nameforms and nameelements and links locations. Link_locations can also be run solo to fix the links without reloading everything.'
    def handle(self, *args, **options):


        print 'Deleting old database entries'
        if 'all' in args or 'letter' in args:
            Letter.objects.all().delete()

        if 'all' in args or 'event' in args:
            Event.objects.all().delete()

        if 'all' in args or 'subject' in args:
            Subject.objects.all().delete()

        if 'all' in args or 'person' in args:
            Person.objects.all().delete()

        if 'all' in args or 'file' in args:
            File.objects.all().delete()

        if 'all' in args or 'artwork' in args:
            Artwork.objects.all().delete()

        if 'all' in args or 'artworkfile' in args:
            ArtworkFile.objects.all().delete()

        if 'all' in args or 'location' in args:
            LocationEvent.objects.all().delete()
            Location.objects.all().delete()

        import codecs
        #Letters
        if 'all' in args or 'letter' in args:
            print 'Letters'
            i = 0
            with codecs.open(basepath + 'edelfelt_brev.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                for row in reader:
                    i = i+1
                    #letter = Letter.objects.get(fm_id=row[0])
                    letter = Letter(
                                fm_id = row[0],
                                title = row[1],
                                description = row[2],
                                language = row[4],
                                date_interval = row[5],
                                start_day_no = checkDigit(row[6]),
                                start_month_no = checkDigit(row[7]),
                                start_year_no = checkDigit(row[8]),
                                end_day_no = checkDigit(row[9]),
                                end_month_no = checkDigit(row[10]),
                                end_year_no = checkDigit(row[11]),
                                urn = row[12])
                    letter.save()
                    setsubjects(letter, row[3])
                print str(i) + ' letters'

        #Events
        if 'all' in args or 'event' in args:
            i = 0
            print 'Events'
            with codecs.open(basepath + 'edelfelt_handelser.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                for row in reader:
                    i = i+1
                    event = Event(
                        fm_id = row[0],
                        title = row[1],
                        letter = Letter.objects.get(fm_id = row[2]),
                    )
                    if row[3]:
                        event.order = row[3]
                        #print event.fm_id, 'was sorted'
                    event.save()
                print str(i) + ' events'

        #Persons
        if 'all' in args or 'person' in args:
            i = 0
            print 'Persons'
            with codecs.open(basepath + 'edelfelt_personer.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                try:
                    for row in reader:
                        i = i+1
                        person = Person(
                            fm_id = row[0],
                            last_name = row[2],
                            von_van_af = row[3],
                            first_name = row[4],
                            name_info = row[5],

                            last_name2 = row[6],
                            first_name2 = row[7],
                            von_van_af2 = row[8],
                            name_info2 = row[9],
                            name_2_display = row[24],

                            last_name3 = row[10],
                            first_name3 = row[11],
                            von_van_af3 = row[12],
                            name_info3 = row[13],
                            name_3_display = row[25],



                            nickname = row[14],
                            alternative_name = row[15],

                            birth_year = row[16],
                            death_year = row[17],


                            description = row[18],
                            source = row[19],
                            source_url_1 = row[26],
                            source_url_1_text = row[27],
                            source_url_2 = row[28],
                            source_url_2_text = row[29],
                            source_url_3 = row[30],
                            source_url_3_text = row[31],

                            name_4_display = row[32],
                            name_info4 = row[33],
                            hide_image = bool(int(row[34]))
                        )

                        #print row

                        if row[20] == 'Med Edelfelt samtida person':
                            person.type = 1
                        elif row[20] == 'Fiktiv/biblisk person':
                            person.type = 2
                        elif row[20] == 'Historisk person':
                            person.type = 3
                        person.save()

                        person.source = row[19].replace(';', '\n')
                        setPersonEvents(person, row[21], False)
                        setPersonEvents(person, row[22], True)
                        person.save()
                except csv.Error:
                    print 'Failed loading persons at row', i
                    pass
                print str(i) + ' persons'



        #Letter files
        if 'all' in args or 'file' in args:
            print 'Letter Files'
            i = 0
            with codecs.open(basepath + 'edelfelt_brevfiler.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                file_count = 0
                for row in reader:
                    i = i+1
                    file_count += 1

                    #letter files are connected to the letter, thumbnail and kundkopia in one
                    if File.objects.filter(fm_id=row[0]).count() == 1:
                        file = File.objects.get(fm_id=row[0])
                    else:
                        file = File(fm_id = row[0])

                    file.path = row[1]
                    file.thumb_path = row[2]

                    try:
                        file.letter = Letter.objects.get(fm_id=row[3])
                    except Letter.DoesNotExist:
                        print 'Letter for', row[3], 'for file ', row[0], ' not found '
                        print row

                    file.letter_description = row[4]
                    file.letter_order = row[5]

                    file.save()
                print str(i), 'letter files'

        #Artworks
        if 'all' in args or 'artwork' in args:
            print 'Artworks'
            i = 0
            with codecs.open(basepath + 'edelfelt_konstverk.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                for row in reader:
                    i = i+1
                    # print row[0]
                    # artwork = Artwork.objects.get(fm_id=row[0])
                    # artwork.description = row[5]
                    # artwork.save()
                    artwork = Artwork(
                            fm_id = row[0],
                            title = row[1],
                            title2 = row[2],
                            title3 = row[3],
                            title4 = row[4],
                            description = row[5],
                            comments = row[6],
                            type = row[7],
                            exhibition_history = row[8]
                    )
                    artwork.save()

                    #setEvents(artwork, row[9])
                    setArtworkEvents(artwork, row[9], False)
                    setArtworkEvents(artwork, row[10], True)

                    artwork.save()
                print str(i) + ' artworks'

        #Artwork files
        if 'all' in args or 'file' in args or 'file_test' in args:
            print 'Artwork Files'
            i = 0
            with codecs.open(basepath + 'edelfelt_konstverksfiler.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                file_count = 0
                for row in reader:
                    i = i+1
                    file_count += 1

                    file = File(fm_id = row[0])

                    file.path = 'jpg/' + row[1]
                    file.thumb_path = 'thumbnails/'+row[1] #use thumb if we ever have it

                    file.esinetunnus = row[2]
                    if row[5]:
                        file.aihe = row[3]
                    if row[4]:
                        file.tekniikat = row[4]
                    if row[5]:
                        file.materiaalit = row[5]
                    if row[6]:
                        file.korkeus_cm = checkDigit(row[6])
                    if row[7]:
                        file.leveys_cm = checkDigit(row[7])
                    if row[8]:
                        file.syvyys_cm = checkDigit(row[8])
                    if row[9]:
                        file.owner = row[9]
                    if row[10]:
                        main_id = row[10]


                        if Artwork.objects.filter(fm_id=main_id).exists():
                            main = Artwork.objects.get(fm_id=main_id)
                            file.main_artwork = main

                    file.save()
                print str(i), 'artwork files'

        #ArtworkFiles
        if 'all' in args or 'artworkfile' in args:
            print 'Connecting Artworkfiles'
            i = 0
            with codecs.open(basepath + 'mt_konstverk_bilder.csv', 'rb', encoding='utf-8') as csvfile:
                reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                for row in reader:
                    i = i+1
                    artwork = Artwork.objects.get(fm_id=row[1])
                    file = File.objects.get(fm_id=row[2])

                    artworkfile = ArtworkFile(fm_id=row[0], order=row[4], file=file, artwork=artwork)

                    #print row[0] + ': ' + row[3]

                    if row[3] == u'Osäkert':
                        artworkfile.type = 6
                        #print 6
                    elif row[3] == u'Relaterat verk':
                        artworkfile.type = 5
                        #print 5
                    elif row[3] == u'Relaterade verk och skisser':
                        artworkfile.type = 4
                        #print 4
                    elif row[3] == u'Osäkra skisser':
                        artworkfile.type = 3
                        #print 3
                    elif row[3] == u'Skisser':
                        artworkfile.type = 2
                        #print 2
                    elif row[3] == u'Huvudverk':
                        artworkfile.type = 1
                        #print 1
                    else:
                        #print row[3]
                        artworkfile.type = 0
                        print 0
                    artworkfile.save()

        #Locations
        if 'all' in args or 'location' in args:
                print 'Locations'
                i = 0
                with codecs.open(basepath + 'edelfelt_platser.csv', 'rb', encoding='utf-8') as csvfile:
                    reader = unicode_csv_reader(csvfile, delimiter=',',quotechar='"') #,dialect='excel'
                    for row in reader:
                        location = Location(fm_id=row[0],
                                            name=row[1],
                                            country=row[3],
                                            province=row[4],
                                            classic_municipality=row[5])
                        if row[7]:
                            location.lat=row[7].replace(',','.')
                        if row[8]:
                            location.long=row[8].replace(',','.')

                        if row[9]:
                            location.comment=row[9]

                        location.save()
                        setLocationEvents(location, row[10], False, True)
                        setLocationEvents(location, row[11], False, False)
                        setLocationEvents(location, row[12], True, False)




def setLocationEvents(location, values, unsure, letter_origin):
    ids = values.split(';')
    for fm_id in ids:
        if fm_id:
            try:
                if letter_origin:
                    letter = Letter.objects.get(fm_id=fm_id)
                    letter.locations.add(location)
                    letter.save()
                else:
                    event = Event.objects.get(fm_id=fm_id)
                    locationevent = LocationEvent(location=location, event=event, unsure=unsure, letter_origin=letter_origin)
                    locationevent.save()
            except Event.DoesNotExist:
                pass
            except Letter.DoesNotExist:
                #print 'letter', fm_id, 'not found'
                pass

def setArtworkEvents(artwork, values, unsure):
    events = values.split(';')
    for event_fm_id in events:
        if event_fm_id:
            try:
                event = Event.objects.get(fm_id=event_fm_id)
                artworkevent = ArtworkEvent(artwork=artwork, event=event, unsure=unsure)
                artworkevent.save()
            except Event.DoesNotExist:
                pass

def setPersonEvents(person, values, unsure):
    events = values.split(';')
    for event_fm_id in events:
        if event_fm_id:
            try:
                event = Event.objects.get(fm_id=event_fm_id)
                personevent = PersonEvent(person=person, event=event, unsure=unsure)
                personevent.save()
            except Event.DoesNotExist:
                pass



def setsubjects(letter, values):
    subjects = values.split(',')
    for sub in subjects:
        sub = sub.strip()
        subject, created = Subject.objects.get_or_create(name=sub)
        letter.subjects.add(subject)




def checkDigit(value):
    if value.isdigit():
        return value
    else:
        #print value, 'is not a digit'
        return None

#There were Unicode (?) problems using the dictionary
def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(unicode(key, 'utf-8'), unicode(value, 'utf-8')) for key, value in row.iteritems()])




def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]