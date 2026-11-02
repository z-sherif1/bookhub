from django.urls import path
from . import api_views

urlpatterns = [
    # favorites paths
    path('favorites/', api_views.api_favorites_list, name='api_favorites_list'),
    path('favorites/add/', api_views.api_add_favorite, name='api_add_favorite'),
    path('favorites/remove/<str:book_id>/', api_views.api_remove_favorite, name='api_remove_favorite'),

    # reading pathes
    path('reading-list/', api_views.api_reading_list, name='api_reading_list'),
    path('reading-list/update/', api_views.api_update_reading_list, name='api_update_reading_list'),

    # reviews pathes
    path('book/<str:book_id>/reviews/', api_views.api_book_reviews, name='api_book_reviews'),
    path('book/<str:book_id>/reviews/add/', api_views.api_add_review, name='api_add_review'),
]