from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from webapp.forms import AlbumForm
from webapp.models import Album


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.get_object()
        if not album.is_public and album.author != self.request.user:
            context['no_access'] = True
            return context
        if album.author == self.request.user:
            photos = album.photos.all()
        else:
            photos = album.photos.filter(is_public=True)
        paginator = Paginator(photos, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['photos'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    permission_required = 'webapp.change_album'

    def has_permission(self):
        album = self.get_object()
        return super().has_permission() or self.request.user == album.author

    def form_valid(self, form):
        old_album = Album.objects.get(pk=self.object.pk)
        response = super().form_valid(form)
        if old_album.is_public and not form.instance.is_public:
            self.object.photos.update(is_public=False)
        return response


class AlbumDeleteView(PermissionRequiredMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('webapp:photo_list')
    permission_required = 'webapp.delete_album'

    def has_permission(self):
        album = self.get_object()
        return super().has_permission() or self.request.user == album.author
