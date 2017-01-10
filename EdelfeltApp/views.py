# coding=utf8
from collections import defaultdict, OrderedDict
import colorsys
from itertools import groupby
import json
import os
import random
import urllib2

from django.shortcuts import render, HttpResponse, get_object_or_404
from EdelfeltApp.models import *
from django.db.models import Count, Max, Min

from annoying.decorators import ajax_request

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.templatetags.static import static
from django.views.decorators.cache import cache_page

# Cache only for 15 s, we want the artwork to vary.
@cache_page(15)
def home(request):
    artwork = Artwork.objects. \
        annotate(event_count=Count('events')).filter(event_count__gt=0). \
        annotate(file_count=Count('files')).filter(file_count__gt=0). \
        order_by('?').first()

    letter = None
    event_connection = None
    for event in artwork.events.all():
        if event.letter:
            event_connection = event
            letter = event.letter
            break

    person = None
    for event in artwork.events.all():
        if event.persons.first():
            person = event.persons.first()
            break
    if person is None:
        person = Person.objects.annotate(event_count=Count('events')).filter(event_count__gt=0).order_by('?').first()


    letters = Letter.objects.all()
    max_year = letters.aggregate(Max('start_year_no'))['start_year_no__max']
    min_year = letters.aggregate(Min('start_year_no'))['start_year_no__min']


    host = request.get_host()
    data = {'letter': letter, 'person': person, 'artwork': artwork, 'event':event_connection, 'letters':letters, 'max_year':max_year, 'min_year':min_year, 'host':host}

    return render(request, 'EdelfeltApp/home.html', data)

def letter(request, id):
    letter = get_object_or_404(Letter, id = id)

    letters = list(Letter.objects.order_by('start_year_no', 'start_month_no', 'start_day_no').all())

    index = letters.index(letter)

    if index != len(letters) - 1:
        next = letters[index+1]# Letter.objects.filter(fm_id__gt = letter.fm_id).order_by('start_year_no', 'start_month_no', 'start_day_no').first()
    else:
        next = None
    if index != 0:
        previous = letters[index-1] #Letter.objects.filter(fm_id__lt = letter.fm_id).order_by('start_year_no', 'start_month_no', 'start_day_no').last()
    else:
        previous = None

    event_files = OrderedDict()#{}
    for event in letter.events.all():
        files = []
        for artwork in event.artworks.all():
            if artwork.files.all():
                files.append(artwork.artworkfiles.first().file)
            #for file in artwork.files.all():


        event_files[event] = files



    return render(request, 'EdelfeltApp/letter.html', {'letter': letter, 'next': next, 'previous': previous, 'letters':letters, 'event_files':event_files})

def letter_fm_id(request, fm_id, slug):
    l = get_object_or_404(Letter, fm_id=fm_id)
    return letter(request, l.id)

def letter_fm_id_no_slug(request, fm_id):
    l = get_object_or_404(Letter, fm_id=fm_id)
    return letter(request, l.id)

def letter_list(request):
    letters = Letter.objects.order_by('start_year_no', 'start_month_no', 'start_day_no')
    subjects = Subject.objects.all()

    return render(request, 'EdelfeltApp/letter_list.html', {'letters': letters, 'subjects':subjects})


def letter_list_by_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    letters = []
    for event in location.events.all():
        if event.letter not in letters:
            letters.append(event.letter)

    for letter in location.letters.all():
        if letter not in letters:
            letters.append(letter)

    letters.sort(key=lambda x: (x.start_year_no, x.start_month_no, x.start_day_no))

    return render(request, 'EdelfeltApp/letter_list.html', {'letters': letters, 'location':location})

def letter_list_by_location_fm_id(request, fm_id, slug):
    l = get_object_or_404(Location, fm_id=fm_id)
    return letter_list_by_location(request, l.id)

def location_list(request):
    locations = Location.objects\
        .annotate(event_count=Count('events'))\
        .annotate(letter_count=Count('letters')).filter(Q(letter_count__gt=0) | Q(event_count__gt=0)).order_by('name')



    return render(request, 'EdelfeltApp/location_list.html', {'locations':locations})

def artwork_gallery(request):
    artworks = Artwork.objects.annotate(file_count=Count('files')).filter(file_count__gt=0)
    return render(request, 'EdelfeltApp/artwork_gallery.html', {'artworks': artworks})

def artwork_list(request):
    artworks = Artwork.objects\
        .extra(select={'has_title': 'LENGTH(EdelfeltApp_artwork.title) > 0', 'sort_name': 'COALESCE(NULLIF(EdelfeltApp_artwork.title, "''"), NULLIF(EdelfeltApp_artwork.title2, "''"), NULLIF(EdelfeltApp_artwork.title4, "''"), NULLIF(EdelfeltApp_artwork.title3, "''"))'})\
        .extra(select={'hinze': 'CAST(EdelfeltApp_artwork.title AS UNSIGNED)'})\
        .order_by('-has_title', 'hinze', 'sort_name')\
        .all()
    return render(request, 'EdelfeltApp/artwork_list.html', {'artworks': artworks})

def person_list(request, type):
    type_key = 0
    for choice in Person.TYPE_CHOICES:
        if choice[1] == type:
            type_key = choice[0]

    persons = list(Person.objects.filter(type=type_key).extra(select={'sort_name': 'COALESCE(NULLIF(EdelfeltApp_person.last_name, "''"), NULLIF(EdelfeltApp_person.first_name, "''"), "N.N")'})) #.order_by('sort_name').all()
    persons = sorted(persons, key=lambda p:p.sort_name.lower())
    #print persons.query
    return render(request, 'EdelfeltApp/person_list.html', {'persons':persons})

def subject_list(request):
    subjects = sorted(Subject.objects.all(), key=lambda s: s.name.upper())

    return render(request, 'EdelfeltApp/subject_list.html', {'subjects':subjects})

def letter_image(request, id):
    file = File.objects.get(id=id)
    base_path = '//'
    path = base_path + file.path
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, mimetype="image/png")

def artwork(request, id):
    artwork = get_object_or_404(Artwork, id=id)
    next = Artwork.objects.filter(fm_id__gt = artwork.fm_id).order_by('fm_id').first()
    previous = Artwork.objects.filter(fm_id__lt = artwork.fm_id).order_by('fm_id').last()

    host = request.get_host()

    return render(request, 'EdelfeltApp/artwork.html', {'artwork': artwork, 'next': next, 'previous': previous, 'host':host})


def artwork_fm_id(request, fm_id, slug):
    a = get_object_or_404(Artwork, fm_id=fm_id)
    return  artwork(request, a.id)




def artwork_image(request, id):
    base_path = '//adilla/data/edelfelt/thumbnails/'
    path = random.choice(os.listdir(base_path)) #random for now...
    path = base_path + path #artwork.path
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, mimetype="image/png")

def person(request, id):
    person = get_object_or_404(Person, id=id)
    next = Person.objects.filter(last_name__gt = person.last_name).order_by('last_name').first()
    previous = Person.objects.filter(last_name__lt = person.last_name).order_by('last_name').last()
    letters = Letter.objects.all()
    related_letters = list()
    for event in person.events.all():
        related_letters.append(event.letter)

    opener = urllib2.build_opener()
    try:
        if not person.hide_image:
            name = person.name().replace(' ', '%20')

            url = "http://en.wikipedia.org/w/api.php?action=query&titles=" + name + "&prop=pageimages&format=json&pithumbsize=100"

            #print url
            f = opener.open(url)

            data = json.loads(f.read())
            person_url = data['query']['pages'].itervalues().next()['thumbnail']['source']
        else:
            person_url = None
    except:
       person_url = None
    return render(request, 'EdelfeltApp/person.html', {'person': person, 'next': next, 'previous': previous, 'person_url':person_url, 'letters':letters, 'related_letters':related_letters})

def person_fm_id(request, fm_id, slug):
    p = get_object_or_404(Person, fm_id=fm_id)
    return person(request, p.id)

def event(request, id):
    event = get_object_or_404(Event, id=id)
    next = Event.objects.filter(fm_id__gt = event.fm_id).order_by('fm_id').first()
    previous = Event.objects.filter(fm_id__lt = event.fm_id).order_by('fm_id').last()
    return render(request, 'EdelfeltApp/event.html', {'event': event, 'next': next, 'previous': previous})

def timeline(request):
    dates = []
    for l in Letter.objects.all()[:50]:
        if l.start_day_no and l.start_year_no and l.start_month_no:
            startDate = datetime.date(int(l.start_year_no), int(l.start_month_no), int(l.start_day_no))
            lettermedia, lettercaption = getLetterMedia(request, l)
            url = reverse('EdelfeltApp.views.letter', args=(l.id,))
            d = {
                "startDate":dateFormat(startDate),
                #"endDate":dateFormat(startDate + datetime.timedelta(days=2)),
                "headline": '<a href="' + url + '">' + l.title + '</a>',
                "text":"<p>" + "</p>",
                "asset":
                    {
                        "media": lettermedia,#request.build_absolute_uri(reverse('EdelfeltApp.views.timelinecontentletter', args=(4615,))),
                        "thumbnail": lettermedia,
                        "caption": lettercaption
                    }
            }
            dates.append(d)

            alskade_url =  static('EdelfeltApp/alskade.jpg')
            photo = '<img src="' + static('EdelfeltApp/albert.jpg') + '" height=100px style="border:none">'
            alskade_html = photo #+ '<img src="' + alskade_url + '" style="border:none">'

    response = \
        {
            "timeline":
                {
                    "headline":alskade_html + " Edelfelts brev i tiden",
                    "type":"default",
                    "text":" ",#Bläddra bland breven i kronologisk ordning.",
                    "date":dates
                }
        }

    return HttpResponse(json.dumps(response), mimetype='application/json')

def dateFormat(d):
    return str(d.year)+","+str(d.month)+","+str(d.day)

def getLetterMedia(request, letter):
    for event in letter.events.all():
        if event.artworks.first():
            artwork = event.artworks.first()
            if artwork.files.first():
                file = artwork.files.first()
                return static(file.thumbnail_path()), artwork.title2 #request.build_absolute_uri(reverse('EdelfeltApp.views.artwork_image', args=(event.artworks.first().id,))), event.artworks.first().title2
    if letter.files:
        return static(letter.files.first().thumbnail_path()), letter.title #request.build_absolute_uri(reverse('EdelfeltApp.views.letter_image', args=(letter.files.first().id,))), letter.title
    else:
        return ''

def radial(request):
    return render(request, 'EdelfeltApp/radial_graph.html', {'person_id' : '8326'})

def tree(request):
    return render(request, 'EdelfeltApp/tree.html', {'person_id' : '8676'})

def radial_json(request, person_id):
    person = Person.objects.get(id=person_id)
    nodes = []
    for event in person.events.all():
        children = []
        for child in event.persons.all():
            if child != person:
                children.append(
                    {
                        "name":child.first_name + ' ' + child.last_name,
                        "url":reverse('EdelfeltApp.views.person', args=(child.id,))
                    })

        if children:
            node = \
                {
                    "name":event.letter.date_interval,#event.title,
                    "children":children,
                    "url":reverse('EdelfeltApp.views.event', args=(event.id,)),

                    }
            nodes.append(node)
    response = \
        {
            "name": "",#person.first_name + ' ' + person.last_name,
            "children":nodes
        }
    #response = test()
    return HttpResponse(json.dumps(response), mimetype='application/json')

#links all persons to others through letters
def edge_json(request):
    persons = Person.objects.all()
    nodes = []
    for person in persons:
        links = []
        has_links = False
        for event in person.events.all():
            for linked_person in event.persons.all():
                if linked_person != person:
                    links.append(linked_person.first_name + ' ' + linked_person.last_name)
                    has_links = True

        node = \
            {
                'name':person.first_name + ' ' + person.last_name,
                'imports':links
            }
        if has_links:
            nodes.append(node)
    return HttpResponse(json.dumps(nodes), content_type='application/json')


#links a person to others x levels
def edge_json_person(request, person_id):
    #person_id = '11845'
    nodes = []
    root_person = get_object_or_404(Person, id=person_id)
    linked_persons = [root_person]
    #make a list of all people to include (those one degree from the root)
    handled_events = []
    for event in root_person.events.all():
        if event not in handled_events:
            handled_events.append(event)
            for person in event.persons.all():
                if person not in linked_persons:
                    linked_persons.append(person)
                    for event_lvl2 in person.events.all():
                        if event_lvl2 not in handled_events:
                            for person_lvl2 in event_lvl2.persons.all():
                                if person_lvl2 not in linked_persons:
                                    linked_persons.append(person_lvl2)



    #create nodes for each person
    for person in linked_persons:
        links = []
        has_links = False
        for event in person.events.all():
            for linked_person in event.persons.all():
                if linked_person != person and linked_person in linked_persons: #only add those links that are one degree from the root
                    links.append(linked_person.first_name + ' ' + linked_person.last_name)
                    has_links = True

        node = \
            {
                'name':person.first_name + ' ' + person.last_name,
                'imports':links,
                'root':person is root_person
            }
        if has_links:
            nodes.append(node)
    return HttpResponse(json.dumps(nodes), content_type='application/json')



def edge(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    return render(request, 'EdelfeltApp/edge_bundling.html', {'person': person})

@ajax_request
def person_connections_json(request, person_id):
    two_degrees = request.GET.get('two_degrees') == 'true'
    root_person = get_object_or_404(Person, id=person_id)

    connections = defaultdict(lambda: defaultdict(lambda: 0))

    # As much as possible, get query results in values,
    # querying all data and initializing model objects is slow.

    #Get all events that the root person was involved with, then all the other people
    #who took part in those events.
    root_person_events = root_person.events.all().values_list('id', flat=True)
    contacts = Person.objects.filter(events__in=root_person_events).distinct()

    # Get all the events where any of contacts were involved
    second_level_contact_events = Event.objects.filter(persons__in=[c.id for c in contacts])\
        .distinct().values_list('id', flat=True)

    if two_degrees:
        contacts = Person.objects.filter(events__in=second_level_contact_events).distinct()

    # Get people who took part in each event.
    event_people = PersonEvent.objects.filter(event__in=second_level_contact_events)\
        .order_by('event').values('event', 'person')
    event_people = dict([(event_id, list(pe_g)) for event_id, pe_g in
                         groupby(event_people, key=lambda pe: pe['event'])])

    # Calculate number of connections (events in common) between people
    for contact_event_id in second_level_contact_events:
        contact_event_people = [pe['person'] for pe in event_people[contact_event_id]]
        for person_id in contact_event_people:
            for person_connection_id in contact_event_people:
                if person_id == person_connection_id:
                    continue
                connections[person_id][person_connection_id] += 1

    # Put the root person first, others in name order.
    def cmp_people(p1, p2):
        if p1 == root_person:
            return -1
        elif p2 == root_person:
            return 1

        return cmp(p1.full_name(), p2.full_name())
    contacts = sorted(contacts, cmp_people)

    def get_hex_colors(count):
        hsv_tuples = [(x*1.0/count, 0.5, 0.5) for x in xrange(count)]
        hex_out = []
        for rgb in hsv_tuples:
            rgb = map(lambda color: int(color*255), colorsys.hsv_to_rgb(*rgb))
            hex_out.append('#' + ''.join(map(lambda x: chr(x).encode('hex'), rgb)))
        return hex_out

    contact_data = zip([c.name() for c in contacts], get_hex_colors(len(contacts)),
                       [c.fm_id for c in contacts], [c.slug() for c in contacts],
                       [c.description for c in contacts])

    matrix = []
    for c1 in contacts:
        row = []
        for c2 in contacts:
            row.append(connections[c1.id][c2.id])
        matrix.append(row)

    return {'contacts': contact_data, 'matrix': matrix}






def search(request):
    if 'search_string' in request.GET:
        search_string = request.GET['search_string']
        persons = Person.objects.filter(Q(first_name__icontains=search_string) | Q(last_name__icontains=search_string)).order_by("last_name")[:35]
        artworks = Artwork.objects.filter(Q(title__icontains=search_string) |
                                            Q(title2__icontains=search_string) |
                                            Q(title3__icontains=search_string) |
                                            Q(title4__icontains=search_string) |
                                            Q(comments__icontains=search_string) |
                                            Q(description__icontains=search_string))[:25]
        letters = list(Letter.objects.filter(Q(title__icontains=search_string) | Q(description__icontains=search_string) | Q(date_interval__icontains=search_string)).order_by("start_year_no", "start_month_no", "start_day_no")[:25])
        events = Event.objects.filter(title__icontains=search_string)[:25]

        for event in events:
            letters.append(event.letter)

    else:
        person = None
    return render(request, 'EdelfeltApp/search.html', {'persons': persons, 'artworks':artworks, 'letters':letters})

def subject_letters(request, id, slug):
    try:
        subject = Subject.objects.get(id=id)
    except Subject.DoesNotExist:
        subject = get_object_or_404(Subject, name=slug)

    letters = subject.letters.all()
    return render(request, "EdelfeltApp/subject_letters.html", {"letters": letters, 'subject':subject})
