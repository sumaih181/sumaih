from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('wishes', views.show_wishes),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout_user),
    path('wishes/Make_a_wish', views.Make_a_wish),
    path('wishes/create', views.create_wish),
    path('wishes/<int:wish_id>/granted', views.mark_wish_granted),
    path('wishes/<int:wish_id>/favorite', views.mark_wish_as_favorite),
    path('wishes/<int:wish_id>/unfavorite', views.mark_wish_as_unfavorite),
    path('wishes/<int:wish_id>/edit', views.wish_edit),
    path('wishes/<int:wish_id>/update', views.wish_update),
    path('wishes/<int:wish_id>/remove', views.wish_remove),
    path('wishes/view_stats', views.view_stats),

]