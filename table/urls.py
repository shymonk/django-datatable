from django.conf.urls import patterns, url
from table.views import FeedDataView

urlpatterns = patterns('',
    url(r'^ajax/(?P<token>\w{32})/$', FeedDataView.as_view(), name='feed_data'),
)
