from django import forms

from webapp.models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название альбома'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание альбома (необязательно)'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        title = title.strip()
        if not title:
            raise forms.ValidationError('Название альбома не может быть пустым.')
        if len(title) < 2:
            raise forms.ValidationError('Название альбома должно содержать минимум 2 символа.')
        return title
