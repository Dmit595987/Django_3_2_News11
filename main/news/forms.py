from django import forms
from django.core.exceptions import ValidationError

from .models import Category, News
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, initial='Напишите ваш ЛОГИН', label='Имя пользователя',  widget=forms.TextInput(
        attrs=({'class': 'form-control'})))
    email = forms.EmailField(label='Email', initial='Напишите ваш e-mail', widget=forms.EmailInput(
        attrs=({'class': 'form-control'})))
    password1 = forms.CharField(max_length=155,  label='Пароль', help_text='Пароль не менее 8 символов и не может быть только из цифр', widget=forms.PasswordInput(
        attrs=({'class': 'form-control'})))
    password2 = forms.CharField(max_length=155, help_text='Пароли должны совпадать', label='Повтор пароля', widget=forms.PasswordInput(
        attrs=({'class': 'form-control'})))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['email'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['password1'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['password2'].widget.attrs.update({'class': 'form-control'})








class NewsForms(forms.Form):
    title = forms.CharField(max_length=150,  label='Наименование',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Контент', required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 5, }))
    is_published = forms.BooleanField(label='Публикация', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      empty_label='Выберите категорию',
                                      widget=forms.Select(attrs={'class': 'form-control', }))


class NewsFormsModel(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 5})

        #self.fields['photo'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'is_published', 'category']


    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].isdigit():
            raise ValidationError('Наименование не может начинаться с цифры!')
        return title.title()

