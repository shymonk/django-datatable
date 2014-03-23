from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'app.views.base', name='base'),
    url(r'^edit/(\d+)/$', 'app.views.edit', name='edit'),
    url(r'^calendar-column/$', 'app.views.calendar_column', name='calendar_column'),
    url(r'^sequence-column/$', 'app.views.sequence_column', name='sequence_column'),
    url(r'^data/ajax/$', 'app.views.ajax_data', name='ajax_data'),

    url(r'^table/', include('table.urls')),
)
