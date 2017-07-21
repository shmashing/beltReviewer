from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.user_page, name='home'),
  url(r'^add$', views.add_book, name='add'),
  url(r'^add_book$', views.make_book, name='addBook'),
  url(r'^(?P<id>\d+)$', views.book_page, name='bookPage'),
  url(r'^(?P<id>\d+)/add_review', views.add_review, name='addReview'),
  url(r'^(?P<book_id>\d+)/(?P<rev_id>\d+)/add_like', views.add_like, name='addLike'),
  url(r'^(?P<book_id>\d+)/(?P<rev_id>\d+)/remove_review', views.remove_review, name='removeReview'),
]
