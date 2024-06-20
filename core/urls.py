from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_users, name='search'),
    path('friends/', views.get_friends, name='get-friends'),
    path('friend-req/send/', views.send_friend_request,
         name='send-friend-request'),
    path('friend-req/pending/', views.pending_requests, name='pending-requests'),
    path('friend-req/manage/<str:action>/',
         views.manage_friend_request, name='manage-friend-request'),

]
