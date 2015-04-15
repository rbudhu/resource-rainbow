from django import forms

from web.models import User

class UserUpdateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {'password_mismatch':
                      'The two password fields did not  match.'}
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                required=False)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput,
                                required=False,
                                help_text='Enter the same password as above, for verification.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone_number', 'location', 'skills')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.save_m2m()
    

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {'password_mismatch':
                      'The two password fields did not  match.'}
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput,
                                help_text='Enter the same password as above, for verification.')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()


class SkillForm(forms.Form):
    skill = forms.CharField()

