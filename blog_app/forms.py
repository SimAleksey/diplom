from django import forms
from django.forms import TextInput, ModelForm, NumberInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Color, Product, Favorite


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв',
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),

    )

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email',
            'password1',
            'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            })
        }


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = [
            'color',
            'price',
            'quantity',
            'preview',
            'discount'
        ]

        widgets = {
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цвет',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество товара',
            }),
            'preview': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Превью',
            })
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'preview',
            'quantity',
            'category',
            'price',
            'color',
            'discount'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }),
            'preview': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Превью',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество товара',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Скидка',
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цвет',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            })
        }


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = [
            'product'
        ]
