from django import forms
from .models import Tag, Handover, HandoverImage, Comment
from accounts.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Handover
        fields = [
            'handover',
            'tag',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['tag'] = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.SelectMultiple(attrs={'class': 'select2bs4'}),
        )


class ImageForm(forms.ModelForm):

    class Meta:
        model = HandoverImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField(
            required=False,
            widget=forms.ClearableFileInput(
                attrs={
                    'multiple': True
                }
            )
        )


class SearchForm(forms.Form):
    search_contributor_ID = forms.ModelChoiceField(
            required=False,
            queryset=User.objects.all(),
            widget=forms.Select(attrs={'class': 'select2bs4'}),
        )

    search_date = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control date_picker'}
        ),
        required=False,
    )

    search_tag = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control select2bs4'}
        ),
        queryset=Tag.objects.all(),
        required=False,
    )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
        }