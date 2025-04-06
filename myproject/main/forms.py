from django import forms
from django.contrib.auth.forms import User, UserCreationForm, AuthenticationForm, UserChangeForm

class RegisterForm(UserCreationForm):
    lastname = forms.CharField(label='Фамилия', max_length=100)
    firstname = forms.CharField(label='Имя', max_length=100)
    middlename = forms.CharField(label='Отчество', max_length=100, required=False)
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'firstname', 'lastname', 'middlename']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'password'].help_text = "Пароли хранятся в зашифрованном виде. Вы не можете увидеть пароль, но можете изменить его <a href=\"../password/\">здесь</a>."