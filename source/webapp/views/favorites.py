from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from webapp.models import Photo, Album


class AddToFavorites(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        photo_id = request.data.get('photo_id')
        album_id = request.data.get('album_id')

        if photo_id:
            try:
                photo = Photo.objects.get(id=photo_id, is_public=True)
                if photo.favorite.filter(id=user.id).exists():
                    return Response({'error': 'Photo already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
                photo.favorite.add(user)
                return Response({'status': 'Photo added to favorites'}, status=status.HTTP_201_CREATED)
            except Photo.DoesNotExist:
                return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

        if album_id:
            try:
                album = Album.objects.get(id=album_id, is_public=True)
                if album.favorite.filter(id=user.id).exists():
                    return Response({'error': 'Album already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
                album.favorite.add(user)
                return Response({'status': 'Album added to favorites'}, status=status.HTTP_201_CREATED)
            except Album.DoesNotExist:
                return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromFavorites(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        photo_id = request.data.get('photo_id')
        album_id = request.data.get('album_id')

        if photo_id:
            try:
                photo = Photo.objects.get(id=photo_id)
                if not photo.favorite.filter(id=user.id).exists():
                    return Response({'error': 'Photo not in favorites'}, status=status.HTTP_400_BAD_REQUEST)
                photo.favorite.remove(user)
                return Response({'status': 'Photo removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
            except Photo.DoesNotExist:
                return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

        if album_id:
            try:
                album = Album.objects.get(id=album_id)
                if not album.favorite.filter(id=user.id).exists():
                    return Response({'error': 'Album not in favorites'}, status=status.HTTP_400_BAD_REQUEST)
                album.favorite.remove(user)
                return Response({'status': 'Album removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
            except Album.DoesNotExist:
                return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
