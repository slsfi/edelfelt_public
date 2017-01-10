from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView

from haystack.views import SearchView
from EdelfeltApp.forms import CustomSearchForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Edelfelt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^brev/(?P<fm_id>\d+)/(?P<slug>.+)/$', 'EdelfeltApp.views.letter_fm_id'),
    url(r'^brev/(?P<fm_id>\d+)/$', 'EdelfeltApp.views.letter_fm_id_no_slug'),

    url(r'^brev/bild/(\d+)/$', 'EdelfeltApp.views.letter_image'),
    url(r'^brev/bild/(\d+).jpg$', 'EdelfeltApp.views.letter_image'),

    url(r'^brev/$', 'EdelfeltApp.views.letter_list'),
    url(r'^plats/(\d+)/$', 'EdelfeltApp.views.letter_list_by_location'),
    url(r'^plats/(?P<fm_id>\d+)/(?P<slug>.+)/$', 'EdelfeltApp.views.letter_list_by_location_fm_id'),

    url(r'^konstverk/galleri/$', 'EdelfeltApp.views.artwork_gallery'),
    url(r'^konstverk/lista/$', 'EdelfeltApp.views.artwork_list'),

    url(r'^konstverk/(\d+)/$', 'EdelfeltApp.views.artwork'),
    url(r'^konstverk/(?P<fm_id>\d+)/(?P<slug>.+)/$', 'EdelfeltApp.views.artwork_fm_id'),
    url(r'^konstverk/bild/(\d+)/$', 'EdelfeltApp.views.artwork_image'),
    url(r'^konstverk/bild/(\d+).jpg$', 'EdelfeltApp.views.artwork_image'),

    url(r'^personer/(\d+)/$', 'EdelfeltApp.views.person'),
    url(r'^personer/(?P<fm_id>\d+)/(?P<slug>.+)/$', 'EdelfeltApp.views.person_fm_id'),

    url(r'^personer/lista/(\w+)/$', 'EdelfeltApp.views.person_list'),


    url(r'^platser/$', 'EdelfeltApp.views.location_list'),


    url(r'^amnesord/$', 'EdelfeltApp.views.subject_list'),

    url(r'^event/(\d+)/$', 'EdelfeltApp.views.event'),

    url(r'^$', 'EdelfeltApp.views.home'),
    url(r'^timeline/$', 'EdelfeltApp.views.timeline'),

    url(r'^radial/$', 'EdelfeltApp.views.radial'),
    url(r'^radial/json/(\d+)/$', 'EdelfeltApp.views.radial_json'),
    url(r'^tree/$', 'EdelfeltApp.views.tree'),

    url(r'^edge/(\d+)/$', 'EdelfeltApp.views.edge'),
    url(r'^edge/json/(\d+)/$', 'EdelfeltApp.views.edge_json_person'),
    url(r'^connections/json/(\d+)/$', 'EdelfeltApp.views.person_connections_json'),

    url(r'^sok/$', 'EdelfeltApp.views.search'),
    url(r'^amnesord/(?P<id>\d+)/(?P<slug>.+)/$', 'EdelfeltApp.views.subject_letters'),

    url(r'^databasen/$', TemplateView.as_view(template_name="EdelfeltApp/brevsamlingen.html"), name='databasen'),
    url(r'^webbutgavan/$', TemplateView.as_view(template_name="EdelfeltApp/webbutgavan.html"), name='webbutgavan'),
    url(r'^redaktion/$', TemplateView.as_view(template_name="EdelfeltApp/redaktion.html"), name='redaktion'),
    url(r'^hanvisacopyright/$', TemplateView.as_view(template_name="EdelfeltApp/hanvisacopyright.html"), name='copyright'),
    url(r'^hintze/$', TemplateView.as_view(template_name="EdelfeltApp/bertel_hintze.html"), name='hintze'),
    url(r'^albertedelfelt/$', TemplateView.as_view(template_name="EdelfeltApp/albertedelfelt.html"), name='albertedelfelt'),
    url(r'^tidigareutgavar/$', TemplateView.as_view(template_name="EdelfeltApp/tidigareutgavar.html"), name='tidigareutgavar'),
    url(r'^breviarkiven/$', TemplateView.as_view(template_name="EdelfeltApp/breviarkiven.html"), name='breviarkiven'),
    url(r'^apiinfo/$', TemplateView.as_view(template_name="EdelfeltApp/api_info.html"), name='api_info'),

    #'haystack.views',
    url(r'^search/', SearchView(form_class=CustomSearchForm, results_per_page=20), name='haystack_search'),

    url(r'^api/', include("api.urls"))
)