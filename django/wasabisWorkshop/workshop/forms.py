''' Hobbies App Forms '''

from django import forms


class LoginForm(forms.Form):
    '''Form for user login'''

    email = forms.CharField(
        label='email',
        max_length=50,
        widget=forms.TextInput(attrs={'autocomplete': 'email'})
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

    name = forms.CharField(
        label='name',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'name',
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
