from django.conf.urls import patterns, url

urlpatterns = patterns('montage_maker.views',
    url(r'^create_montage/$', 'create_montage', name='create_montage'),
    url(r'^montagify/$', 'montagify', name='montagify'),
)
