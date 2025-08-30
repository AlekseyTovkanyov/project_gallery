from django.contrib import admin

from webapp.models import Photo, Album


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'author', 'album', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at', 'author', 'album']
    search_fields = ['caption']
    list_editable = ['is_public']
    readonly_fields = ['created_at']
    fields = ['image', 'caption', 'author', 'album', 'is_public', 'created_at']


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'author', 'created_at', 'is_public']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'is_public']
    list_filter = ['is_public', 'created_at', 'author']
    readonly_fields = ['author', 'created_at']


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
