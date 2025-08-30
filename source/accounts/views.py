from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login

from accounts.forms import UserRegistrationForm
from webapp.models import Photo, Album

User = get_user_model()


class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('webapp:photo_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        current_user = self.request.user
        is_own_profile = current_user.is_authenticated and current_user == profile_user
        if is_own_profile:
            user_albums = Album.objects.filter(author=profile_user)
            user_photos_without_album = Photo.objects.filter(
                author=profile_user,
                album__isnull=True
            )
            favorite_photos = current_user.favorite_photos.filter(is_public=True)
            favorite_albums = current_user.favorite_albums.filter(is_public=True)
            context.update({
                'favorite_photos': favorite_photos,
                'favorite_albums': favorite_albums,
                'show_favorites': True
            })
        else:
            user_albums = Album.objects.filter(author=profile_user, is_public=True)
            user_photos_without_album = Photo.objects.filter(
                author=profile_user,
                album__isnull=True,
                is_public=True
            )
        context.update({
            'user_albums': user_albums,
            'user_photos_without_album': user_photos_without_album,
            'is_own_profile': is_own_profile
        })
        return context
