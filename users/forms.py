from django import forms


# Create your forms here.
class ChangePasswordForm(forms.Form):
    old_password = forms.PasswordInput(label='Старый пароль')
    new_password = forms.PasswordInput(label='Новый пароль')
    new_password_repeat = forms.PasswordInput(label='Новый пароль (повтор)')