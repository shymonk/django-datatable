from django.conf.urls import patterns, url
from table.views import FeedDataView

urlpatterns = patterns('',
    url(r'^ajax/$', FeedDataView.as_view(), name='feed_data'),
)
