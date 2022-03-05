''' Hobbies App Forms '''

from django import forms


class LoginForm(forms.Form):
    '''Form for user login'''

    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )


class SignupForm(forms.Form):
    '''
        Form for user signup
        assumes each field to be required by default
    '''

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'username',
            }
        )
    )

    email = forms.EmailField(
        label='enter email',
    )

    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )
