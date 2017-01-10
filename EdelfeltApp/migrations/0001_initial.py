# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('title', models.TextField(null=True, blank=True)),
                ('title2', models.TextField(null=True, blank=True)),
                ('title3', models.TextField(null=True, blank=True)),
                ('title4', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('type', models.TextField(null=True, blank=True)),
                ('exhibition_history', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['title', 'title2'],
                'verbose_name': ('Konstverk',),
                'verbose_name_plural': 'Konstverk',
            },
        ),
        migrations.CreateModel(
            name='ArtworkEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unsure', models.BooleanField(default=False)),
                ('artwork', models.ForeignKey(related_name='artworkevents', to='EdelfeltApp.Artwork')),
            ],
        ),
        migrations.CreateModel(
            name='ArtworkFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('order', models.PositiveIntegerField()),
                ('type', models.CharField(blank=True, max_length=1, null=True, choices=[(b'0', b''), (b'1', b'Huvudverk'), (b'2', b'Skisser'), (b'3', b'Os\xc3\xa4kra skisser'), (b'4', b'Relaterade verk och skisser'), (b'5', b'Relaterat verk'), (b'6', b'Os\xc3\xa4kert')])),
                ('artwork', models.ForeignKey(related_name='artworkfiles', to='EdelfeltApp.Artwork')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('title', models.TextField()),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['order', 'fm_id'],
                'verbose_name': 'Brevreferat',
                'verbose_name_plural': 'Brevreferat',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('path', models.FilePathField()),
                ('thumb_path', models.FilePathField(null=True, blank=True)),
                ('letter_order', models.PositiveIntegerField(null=True, blank=True)),
                ('letter_description', models.TextField(null=True, blank=True)),
                ('owner', models.TextField(null=True, blank=True)),
                ('esinetunnus', models.CharField(max_length=50, null=True, blank=True)),
                ('aihe', models.TextField(null=True, blank=True)),
                ('tekniikat', models.CharField(max_length=150, null=True, blank=True)),
                ('materiaalit', models.CharField(max_length=150, null=True, blank=True)),
                ('korkeus_cm', models.PositiveIntegerField(max_length=50, null=True, blank=True)),
                ('leveys_cm', models.PositiveIntegerField(max_length=50, null=True, blank=True)),
                ('syvyys_cm', models.PositiveIntegerField(max_length=50, null=True, blank=True)),
                ('artworks', models.ManyToManyField(related_name='files', null=True, through='EdelfeltApp.ArtworkFile', to='EdelfeltApp.Artwork', blank=True)),
            ],
            options={
                'ordering': ['letter_order'],
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('title', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
                ('language', models.CharField(max_length=50)),
                ('date_interval', models.CharField(max_length=30)),
                ('start_day_no', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('start_month_no', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('start_year_no', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('end_day_no', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('end_month_no', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('end_year_no', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('urn', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'ordering': ['start_year_no', 'start_month_no', 'start_day_no'],
                'verbose_name': 'Brev',
                'verbose_name_plural': 'Brev',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('province', models.CharField(max_length=50, null=True, blank=True)),
                ('classic_municipality', models.CharField(max_length=50, null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('long', models.FloatField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Plats',
                'verbose_name_plural': 'Platser',
            },
        ),
        migrations.CreateModel(
            name='LocationEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unsure', models.BooleanField(default=False)),
                ('letter_origin', models.BooleanField(default=False)),
                ('event', models.ForeignKey(related_name='locationevents', to='EdelfeltApp.Event')),
                ('location', models.ForeignKey(related_name='locationevents', to='EdelfeltApp.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fm_id', models.CharField(max_length=10)),
                ('first_name', models.TextField(null=True, blank=True)),
                ('last_name', models.TextField(null=True, blank=True)),
                ('von_van_af', models.TextField(null=True, blank=True)),
                ('name_info', models.TextField(null=True, blank=True)),
                ('first_name2', models.TextField(null=True, blank=True)),
                ('last_name2', models.TextField(null=True, blank=True)),
                ('von_van_af2', models.TextField(null=True, blank=True)),
                ('name_info2', models.TextField(null=True, blank=True)),
                ('name_2_display', models.TextField(null=True, blank=True)),
                ('first_name3', models.TextField(null=True, blank=True)),
                ('last_name3', models.TextField(null=True, blank=True)),
                ('von_van_af3', models.TextField(null=True, blank=True)),
                ('name_info3', models.TextField(null=True, blank=True)),
                ('name_3_display', models.TextField(null=True, blank=True)),
                ('name_info4', models.TextField(null=True, blank=True)),
                ('name_4_display', models.TextField(null=True, blank=True)),
                ('nickname', models.TextField(null=True, blank=True)),
                ('alternative_name', models.TextField(null=True, blank=True)),
                ('birth_year', models.TextField(null=True, blank=True)),
                ('death_year', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('source', models.TextField(null=True, blank=True)),
                ('source_url_1', models.TextField(null=True, blank=True)),
                ('source_url_1_text', models.TextField(null=True, blank=True)),
                ('source_url_2', models.TextField(null=True, blank=True)),
                ('source_url_2_text', models.TextField(null=True, blank=True)),
                ('source_url_3', models.TextField(null=True, blank=True)),
                ('source_url_3_text', models.TextField(null=True, blank=True)),
                ('type', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'samtida'), (b'2', b'mytologisk'), (b'3', b'historisk')])),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'verbose_name': 'Person',
                'verbose_name_plural': 'Personer',
            },
        ),
        migrations.CreateModel(
            name='PersonEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unsure', models.BooleanField(default=False)),
                ('event', models.ForeignKey(related_name='personevents', to='EdelfeltApp.Event')),
                ('person', models.ForeignKey(related_name='personevents', to='EdelfeltApp.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='person',
            name='events',
            field=models.ManyToManyField(related_name='persons', through='EdelfeltApp.PersonEvent', to='EdelfeltApp.Event'),
        ),
        migrations.AddField(
            model_name='location',
            name='events',
            field=models.ManyToManyField(related_name='mentioned_locations', null=True, through='EdelfeltApp.LocationEvent', to='EdelfeltApp.Event', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='letters',
            field=models.ManyToManyField(related_name='locations', null=True, to='EdelfeltApp.Letter', blank=True),
        ),
        migrations.AddField(
            model_name='letter',
            name='subjects',
            field=models.ManyToManyField(related_name='letters', to='EdelfeltApp.Subject'),
        ),
        migrations.AddField(
            model_name='file',
            name='letter',
            field=models.ForeignKey(related_name='files', blank=True, to='EdelfeltApp.Letter', null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='main_artwork',
            field=models.ForeignKey(blank=True, to='EdelfeltApp.Artwork', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='letter',
            field=models.ForeignKey(related_name='events', to='EdelfeltApp.Letter'),
        ),
        migrations.AddField(
            model_name='artworkfile',
            name='file',
            field=models.ForeignKey(related_name='artworkfile', to='EdelfeltApp.File'),
        ),
        migrations.AddField(
            model_name='artworkevent',
            name='event',
            field=models.ForeignKey(related_name='artworkevents', to='EdelfeltApp.Event'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='events',
            field=models.ManyToManyField(related_name='artworks', through='EdelfeltApp.ArtworkEvent', to='EdelfeltApp.Event'),
        ),
    ]
