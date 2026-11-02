
from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='home'),

    path(
        'book/<str:book_id>/',
        views.book_detail,
        name='book_detail'
    ),

    path(
        'book/<str:book_id>/favorite/',
        views.add_favorite,
        name='add_favorite'
    ),

    path('favorites/', views.favorites, name='favorites'),

    path('book/<str:book_id>/remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('book/<str:book_id>/update-reading/', views.update_reading_list, name='update_reading_list'),
    path('book/<str:book_id>/add-review/', views.add_review, name='add_review'),
    path('reading-list/', views.reading_list_view, name='reading_list'),
    path('book/<str:book_id>/reviews/', views.book_reviews, name='book_reviews'),
]
