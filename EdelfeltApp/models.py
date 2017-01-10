# coding=utf8
from django.db import models
import calendar, locale, datetime
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

# Create your models here.
class Letter(models.Model):
    fm_id = models.CharField(max_length=10)
    title = models.TextField()
    subjects = models.ManyToManyField('Subject', related_name='letters')
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100)
    date_interval = models.CharField(max_length = 30)
    start_day_no = models.PositiveSmallIntegerField(null=True, blank=True)
    start_month_no = models.PositiveSmallIntegerField(null=True, blank=True)
    start_year_no = models.PositiveSmallIntegerField(null=True, blank=True)
    end_day_no = models.PositiveSmallIntegerField(null=True, blank=True)
    end_month_no = models.PositiveSmallIntegerField(null=True, blank=True)
    end_year_no = models.PositiveSmallIntegerField(null=True, blank=True)
    urn = models.CharField(max_length=50, null=True, blank=True)
    def date(self):
        if self.start_year_no and self.start_day_no and self.start_month_no:
            return datetime.date(self.start_year_no, self.start_month_no, self.start_day_no)
        elif self.start_year_no and self.start_month_no:
            return datetime.date(self.start_year_no, self.start_month_no, 1)
        elif self.start_year_no:
            return datetime.date(self.start_year_no, 1, 1)
        else:
            return None

    def year_month(self):
        year = str(self.start_year_no)
        if self.start_month_no is None:
            month = 'Okänd'
        else:
            #month = calendar.month_name[self.start_month_no]
            month = self.start_month_no
            #month = locale.nl_langinfo('MON_1')

        return str(year) + ' - ' + str(month)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

    def slug(self):
        if len(self.title) > 0:
            return slugify(self.title)
        else:
            return 'namnlös'

    def get_absolute_url(self):
        return reverse('EdelfeltApp.views.letter_fm_id', kwargs={'fm_id':self.fm_id, 'slug':self.slug()})

    class Meta:
        verbose_name = "Brev"
        verbose_name_plural = "Brev"
        ordering = ['start_year_no', 'start_month_no', 'start_day_no']


class Subject(models.Model):
    name = models.CharField(max_length = 100)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


    def slug(self):
        if len(self.name) > 0:
            return slugify(self)
        else:
            return '-'

    def get_absolute_url(self):
        return reverse('EdelfeltApp.views.subject_letters', kwargs={'id':self.id, 'slug':self.slug()})


class Event(models.Model):
    fm_id = models.IntegerField(null=True, blank=True)
    title = models.TextField()
    letter = models.ForeignKey('Letter', related_name='events')
    order = models.IntegerField(null=True, blank=True)


    class Meta:
        verbose_name = "Brevreferat"
        verbose_name_plural = "Brevreferat"
        ordering = ['order', 'fm_id',]

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('EdelfeltApp.views.letter_fm_id', kwargs={'fm_id':self.letter.fm_id, 'slug':self.letter.slug()})
        url = url + '#' + self.fm_id
        return url


class Person(models.Model):
    fm_id = models.CharField(max_length=10)
    def name(self):
        first_name = self.first_name
        if first_name is None:
            first_name = ""
        name = first_name + ' ' + self.von_van_af + ' ' + self.last_name
        name = ' '.join(name.split()) #removes extra spaces
        if name == '':
            name = 'N.N.'
        return name

    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    von_van_af = models.TextField(null=True, blank=True)
    name_info = models.TextField(null=True, blank=True)

    first_name2 = models.TextField(null=True, blank=True)
    last_name2 = models.TextField(null=True, blank=True)
    von_van_af2 = models.TextField(null=True, blank=True)
    name_info2 = models.TextField(null=True, blank=True)
    name_2_display = models.TextField(null=True, blank=True) #concatenated version

    first_name3 = models.TextField(null=True, blank=True)
    last_name3 = models.TextField(null=True, blank=True)
    von_van_af3 = models.TextField(null=True, blank=True)
    name_info3 = models.TextField(null=True, blank=True)
    name_3_display = models.TextField(null=True, blank=True)

    name_info4 = models.TextField(null=True, blank=True)
    name_4_display = models.TextField(null=True, blank=True)

    nickname = models.TextField(null=True, blank=True)
    alternative_name = models.TextField(null=True, blank=True)

    birth_year = models.TextField(null=True, blank=True)
    death_year = models.TextField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    source_url_1 = models.TextField(null=True, blank=True)
    source_url_1_text = models.TextField(null=True, blank=True)
    source_url_2 = models.TextField(null=True, blank=True)
    source_url_2_text = models.TextField(null=True, blank=True)
    source_url_3 = models.TextField(null=True, blank=True)
    source_url_3_text = models.TextField(null=True, blank=True)

    events = models.ManyToManyField('Event', related_name='persons', through='PersonEvent')
    #unsure_events = models.ManyToManyField('Event', related_name='unsure_persons')

    hide_image = models.BooleanField(default=False)

    TYPE_CHOICES = (
        ('1', 'samtida'),
        ('2', 'mytologisk'),
        ('3', 'historisk')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)

    def living_years(self):
        if self.birth_year and self.death_year:
            return '(' + str(self.birth_year) + '-' + str(self.death_year) + ')'
        else:
            return None
        
    def __unicode__(self):  # Python 3: def __str__(self):
        if self.first_name or self.last_name:
            if self.von_van_af:
                return self.first_name + ' ' + self.von_van_af + ' ' + self.last_name + ': ' + self.description
            else:
                return self.first_name + ' ' + self.last_name + ': ' + self.description
        else:
            return 'N.N' + ': ' + self.description

    def full_name(self):
        if not self.first_name and not self.last_name:
            return u'N.N'
        elif self.last_name and self.first_name:
            if self.von_van_af:
                name = u'%s, %s, %s' % (self.last_name, self.von_van_af, self.first_name)
            else:
                name = u'%s, %s' % (self.last_name, self.first_name)
            return name
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return self.description

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personer"
        ordering = ['last_name', 'first_name']

    def slug(self):
        return slugify(self.full_name())

    def get_absolute_url(self):
        return reverse('EdelfeltApp.views.person_fm_id', kwargs={'fm_id':self.fm_id, 'slug':self.slug()})

    #def get_absolute_url(self):
    #    return reverse('EdelfeltApp.views.person', args={self.id})


class PersonEvent(models.Model):
    person = models.ForeignKey('Person', related_name='personevents')
    event = models.ForeignKey('Event', related_name='personevents')
    unsure = models.BooleanField(default=False)

    def date(self):
        return self.event.letter.date()

class Artwork(models.Model):
    fm_id = models.CharField(max_length=10)
    title = models.TextField(null=True, blank=True)
    title2 = models.TextField(null=True, blank=True)
    title3 = models.TextField(null=True, blank=True)
    title4 = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    events = models.ManyToManyField('Event', related_name='artworks', through='ArtworkEvent')
    #unsure_events = models.ManyToManyField('Event', related_name='unsure_artworks')
    exhibition_history = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['title', 'title2']
        verbose_name = 'Konstverk',
        verbose_name_plural = 'Konstverk'

    #kind of slow...
    def description_anchors(self):
        description = self.description
        #for event in Event.objects.:
        persons = []
        for event in self.events.all():
            for person in event.persons.all():
                if person.first_name and person.last_name:
                    if person not in persons:
                        persons.append(person)
                        #print person.name()

        for person in persons:
            url = reverse('EdelfeltApp.views.person', args=(person.id,))
            description = description.replace(person.name(), '<a href="'+ url + '">' + person.name() + '</a>')

        return description

    def slug(self):
        return slugify(self)

    def get_absolute_url(self):
        return reverse('EdelfeltApp.views.artwork_fm_id', kwargs={'fm_id':self.fm_id, 'slug':self.slug()})

    #def get_absolute_url(self):
    #    return reverse('EdelfeltApp.views.artwork', args={self.id})

    #kind of slow...
    def comments_anchors(self):
        comments = self.comments
        persons = []
        #for event in Event.objects.:
        for event in self.events.all():
            for person in event.persons.all():
                if person.first_name and person.last_name:
                    if person not in persons:
                        persons.append(person)
        for person in persons:
            url = reverse('EdelfeltApp.views.person', args=(person.id,))
            comments = comments.replace(person.name(), '<a href="'+ url + '">' + person.name() + '</a>')

        return comments



    ##sorted list, may be implemented in a convoluted way?
    def get_files(self):
        return self.files.order_by('artworkfile')

    #file_order = models.
    #path = models.FilePathField(null=True, blank=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        if self.title2:
            return self.title2
        elif self.title4:
            return self.title4
        else:
            return self.title3

class ArtworkEvent(models.Model):
    artwork = models.ForeignKey('Artwork', related_name='artworkevents')
    event = models.ForeignKey('Event', related_name='artworkevents')
    def date(self):
        return self.event.letter.date()

    unsure = models.BooleanField(default=False)

class ArtworkFile(models.Model):
    fm_id = models.CharField(max_length=10)
    artwork = models.ForeignKey('Artwork', related_name='artworkfiles')
    file = models.ForeignKey('File', related_name='artworkfile')
    order = models.PositiveIntegerField()

    def has_main_work(self):
        return self.file.main_artwork is not None

    TYPE_CHOICES = (
        ('0', ''),
        ('1', 'Huvudverk'),
        ('2', 'Skisser'),
        ('3', 'Osäkra skisser'),
        ('4', 'Relaterade verk och skisser'),
        ('5', 'Relaterat verk'),
        ('6', 'Osäkert'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['order',]

class File(models.Model):
    fm_id = models.CharField(max_length=10)

    path = models.FilePathField()
    thumb_path = models.FilePathField(null=True, blank=True)
    def thumbnail_path(self):
        if self.thumb_path:
            return self.thumb_path
        else:
            return self.path
            #return 'thumbnails/' + self.path

    letter = models.ForeignKey('Letter', related_name='files', null=True, blank=True)
    letter_order = models.PositiveIntegerField(null=True, blank=True)
    letter_description = models.TextField(null=True, blank=True)
    #note, only for letters, artworkfiles are different, convoluted shit
    class Meta:
        ordering = ['letter_order']

    artworks = models.ManyToManyField('Artwork', related_name='files', null=True, blank=True, through='ArtworkFile')
    main_artwork = models.ForeignKey('Artwork', null=True, blank=True)
    owner = models.TextField(null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.thumb_path

    def description(self):
        #descr = 'Finlands Nationalgalleri / ' + str(self.esinetunnus)
        descr = ''
        if self.owner:
            descr = self.owner + ' / '
        descr = descr + str(self.esinetunnus)
        if (self.korkeus_cm and self.leveys_cm):
            descr = descr + ' ('
        if self.korkeus_cm and self.leveys_cm:
            descr = descr + str(self.korkeus_cm) + 'x' + str(self.leveys_cm) + ' cm'

        if (self.korkeus_cm and self.leveys_cm):
            descr = descr + ')'

        return descr

    #ateneum info
    esinetunnus = models.CharField(max_length=50, null=True, blank=True)
    aihe = models.TextField(null=True, blank=True)
    tekniikat = models.CharField(max_length=150, null=True, blank=True)
    materiaalit = models.CharField(max_length=150, null=True, blank=True)
    korkeus_cm = models.PositiveIntegerField(max_length=50, null=True, blank=True)
    leveys_cm = models.PositiveIntegerField(max_length=50, null=True, blank=True)
    syvyys_cm = models.PositiveIntegerField(max_length=50, null=True, blank=True)

    def fng_url(self):
        print self.esinetunnus
        tunnus = self.esinetunnus
        if ' / ' in tunnus:
            print 'found'
            pos = tunnus.find(' / ')
            tunnus = tunnus[:pos]

        print tunnus
        return "http://kokoelmat.fng.fi/app?si=" + tunnus.replace(' ', '+') + '&lang=se'

class Location(models.Model):
    fm_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    classic_municipality = models.CharField(max_length=50, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    letters = models.ManyToManyField('Letter', related_name='locations', null=True, blank=True)
    events = models.ManyToManyField('Event', related_name='mentioned_locations', null=True, blank=True, through='LocationEvent')

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Plats"
        verbose_name_plural = "Platser"

    def slug(self):
        return slugify(self)

    def get_absolute_url(self):
        return reverse('EdelfeltApp.views.letter_list_by_location_fm_id', kwargs={'fm_id':self.fm_id, 'slug':self.slug()})

    #unsure_events = models.ManyToManyField('Event', related_name='unsure_mentioned_locations', null=True, blank=True)

class LocationEvent(models.Model):
    location = models.ForeignKey('Location', related_name='locationevents')
    event = models.ForeignKey('Event', related_name='locationevents')
    unsure = models.BooleanField(default=False)

    letter_origin = models.BooleanField(default=False)
