from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from webapp.forms import PhotoForm
from webapp.models import Photo


class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 12

    def get_queryset(self):
        return Photo.objects.filter(is_public=True).select_related('author', 'album')


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_object()
        if not photo.is_public and photo.author != self.request.user:
            context['no_access'] = True
        else:
            context['favorited_users'] = photo.favorite.all()
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.album and not form.instance.album.is_public:
            form.instance.is_public = False
        return super().form_valid(form)


class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_form.html'
    permission_required = 'webapp.change_photo'

    def has_permission(self):
        photo = self.get_object()
        return super().has_permission() or self.request.user == photo.author

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.instance.album and not form.instance.album.is_public:
            form.instance.is_public = False
        return super().form_valid(form)


class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    success_url = reverse_lazy('webapp:photo_list')
    permission_required = 'webapp.delete_photo'

    def has_permission(self):
        photo = self.get_object()
        return super().has_permission() or self.request.user == photo.author


class PhotoByTokenView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

    def get_object(self):
        token = self.kwargs['token']
        photo = get_object_or_404(Photo, access_token=token)
        return photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_object()
        context['favorited_users'] = photo.favorite.all()
        context['token_access'] = True
        return context


class GenerateTokenView(LoginRequiredMixin, View):
    def get(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        if photo.author != request.user:
            return redirect('webapp:photo_detail', pk=pk)
        photo.generate_access_token()
        return redirect('webapp:photo_detail', pk=pk)
