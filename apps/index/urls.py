from django.conf.urls import url
from . import views

urlpatterns = [
  url('^$', views.index),
  url('^books/view/$', views.view_books),
  url('^book/add/$', views.add_book),
  url('^book/add_review/$', views.add_book_review),
  url('^book/details/(?P<id>\d+)/$', views.book_details),
  url('^user/details/(?P<id>\d+)/$', views.user_details),
  url('^register/$', views.register),
  url('^login/$', views.login),
  url('^logout/$', views.logout),
  url('^book/add/process/$', views.add_book_process),
  url('^book/review/delete/(?P<id>\d+)/$', views.delete_book_review),
]