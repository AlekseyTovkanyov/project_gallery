from django import forms

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'album', 'is_public']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите подпись к фотографии'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['album'].queryset = Album.objects.filter(author=self.user)
        else:
            self.fields['album'].queryset = Album.objects.none()
        self.fields['album'].widget.attrs.update({'class': 'form-select'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['album'].empty_label = "Без альбома"

    def clean(self):
        cleaned_data = super().clean()
        album = cleaned_data.get('album')
        is_public = cleaned_data.get('is_public')
        if album and not album.is_public and is_public:
            raise forms.ValidationError(
                'Фотография не может быть публичной в приватном альбоме. '
                'Сделайте альбом публичным или фотографию приватной.'
            )
        return cleaned_data
