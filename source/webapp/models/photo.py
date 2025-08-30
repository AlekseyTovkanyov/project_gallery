import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Photo(models.Model):
    image = models.ImageField(upload_to='photos', verbose_name="Фотография")
    caption = models.CharField(max_length=200, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(
        get_user_model(),
        related_name='author_photos',
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    album = models.ForeignKey(
        "Album",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Альбом",
        related_name='photos'
    )
    is_public = models.BooleanField(default=True, verbose_name="Публичная")
    favorite = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='favorite_photos',
        verbose_name="Избранное"
    )
    access_token = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Токен доступа"
    )

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('webapp:photo_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.album and not self.album.is_public:
            self.is_public = False
        super().save(*args, **kwargs)

    def generate_access_token(self):
        if not self.access_token:
            self.access_token = str(uuid.uuid4())
            self.save()
        return self.access_token

    def get_token_url(self):
        if self.access_token:
            return reverse('webapp:photo_by_token', kwargs={'token': self.access_token})
        return None

    class Meta:
        db_table = 'photos'
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ['-created_at']
