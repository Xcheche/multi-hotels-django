from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser




class RegistrationForm(UserCreationForm):
    """Form for registering a new user.
    Usercreation forms comes with username, password1 and password2 fields by default.
    """
    full_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )



    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_styles = {
            'full_name': {'class': 'form-control', 'placeholder': 'Full Name', 'id': 'signupFullnameInput'},
            'username': {'class': 'form-control', 'placeholder': 'Username', 'id': 'signupUsernameInput'},
            'email': {'class': 'form-control', 'placeholder': 'Email', 'id': 'signupEmailInput'},
            'phone_number': {'class': 'form-control', 'placeholder': 'Phone Number', 'id': 'signupPhoneInput'},
            
            'password1': {'class': 'form-control fakePassword', 'placeholder': 'Password', 'id': 'formSignUpPassword'},
            'password2': {'class': 'form-control fakePassword', 'placeholder': 'Confirm Password', 'id': 'formSignUpConfirmPassword'},
        }

        for field_name, attrs in field_styles.items():
            self.fields[field_name].widget.attrs.update(attrs)

        self.fields['full_name'].label = 'Full Name'
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        self.fields['phone_number'].label = 'Phone Number'
      
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
       