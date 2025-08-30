from django.urls import path

from webapp.views import PhotoListView, PhotoCreateView, PhotoDetailView, PhotoUpdateView, PhotoDeleteView, \
    AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView, GenerateTokenView, PhotoByTokenView

app_name = 'webapp'

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo_list'),
    path('photos/', PhotoListView.as_view(), name='photo_list'),
    path('photos/create/', PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),

    path('photos/<int:pk>/generate-token/', GenerateTokenView.as_view(), name='generate_token'),
    path('photo/token/<str:token>/', PhotoByTokenView.as_view(), name='photo_by_token'),

    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('albums/create/', AlbumCreateView.as_view(), name='album_create'),
    path('albums/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete')
]
