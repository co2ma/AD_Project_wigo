from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class ProfileUpdateForm(forms.Form):
    username = forms.CharField(
        label='닉네임',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label='새 비밀번호 확인',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    current_password = forms.CharField(
        label='현재 비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise ValidationError('이미 사용 중인 닉네임입니다.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('비밀번호가 일치하지 않습니다.')
        if password1:
            try:
                validate_password(password1, self.user)
            except ValidationError as error:
                self.add_error('password1', error)
        return password2

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError('현재 비밀번호가 일치하지 않습니다.')
        return current_password
