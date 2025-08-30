from django.contrib.auth import get_user_model
from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Описание")
    author = models.ForeignKey(
        get_user_model(),
        related_name='author_albums',
        on_delete=models.CASCADE,
        verbose_name="Автор альбома"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_public = models.BooleanField(default=True, verbose_name="Публичный")
    favorite = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='favorite_albums',
        verbose_name="Избранное"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'albums'
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ['-created_at']
