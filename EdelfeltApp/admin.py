from django.contrib import admin
from models import *
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    search_fields = ['fm_id']

admin.site.register(Event, EventAdmin)

class ArtworkAdmin(admin.ModelAdmin):
    search_fields = ['fm_id']

admin.site.register(Artwork, ArtworkAdmin)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ['fm_id']

admin.site.register(Person, PersonAdmin)


admin.site.register(ArtworkFile)
admin.site.register(Subject)
admin.site.register(Location)

class FileAdmin(admin.ModelAdmin):
    search_fields = ['fm_id']

admin.site.register(File, FileAdmin)

class LetterAdmin(admin.ModelAdmin):
    search_fields = ['fm_id']

admin.site.register(Letter, LetterAdmin)
