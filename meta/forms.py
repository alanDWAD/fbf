from django import forms
from models import Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from meta.models import Profile
from django.contrib.admin.widgets import AdminDateWidget


class BootstrapForm(forms.Form):
    '''Convenient base class for applying Bootstrap CSS classes to fields in
       Forms.'''
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if type(field.widget) == forms.CheckboxInput:
                    field.widget.attrs['class'] = 'checkbox'
                elif type(field.widget) == forms.RadioSelect:
                    field.widget.attrs['class'] = 'radio'
                else:
                    field.widget.attrs['class'] = 'form-control'


class BootstrapModelForm(forms.ModelForm):
    '''Convenient base class for applying Bootstrap CSS classes to fields in
       ModelForms.'''
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if type(field.widget) == forms.CheckboxInput:
                    field.widget.attrs['class'] = 'checkbox'
                elif type(field.widget) == forms.RadioSelect:
                    field.widget.attrs['class'] = 'radio'
                else:
                    field.widget.attrs['class'] = 'form-control'


class RegistrationForm(BootstrapModelForm, UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # The default Django user model doesn't require these fields to be set
        # but we do.
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True
        # self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('There is already an account registered with this e-mail address.')
        return email

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class ProfileForm(BootstrapModelForm):
    class Meta:
        model = Profile
        fields = ('contact_number','referral_code',)
        labels = {
            'contact_number': ('Contact No.'), 'referral_code': ('Referral Code'),
        }

class ProfileFormAddress(BootstrapModelForm):
    class Meta:
        model = Profile
        exclude = ('user','contact_number','referral_code',)
        labels = {
            'add1housenumberorname': ('House Number / Name:'),
            'add1street1': ('Street Name:'),
            'add1street2': ('Street Name 2:'),
            'add1townorcity': ('Town / City:'),
            'add1county': ('County:'),
            'add1country': ('Country (If not England)'),
            'add1postcode': ('Postcode:'),
            'add2housenumberorname': ('House Number / Name:'),
            'add2street1': ('Street Name:'),
            'add2street2': ('Street Name 2:'),
            'add2townorcity': ('Town / City:'),
            'add2county': ('County:'),
            'add2country': ('Country (If not England)'),
            'add2postcode': ('Postcode:'),
        
        }


class DocumentForm(BootstrapModelForm):
    class Meta:
        model = Document
        fields = ('document', )


class ChangeEmailForm(BootstrapForm):
    new_email = forms.EmailField(label='New e-mail address')

    def clean_email(self):
        email = self.cleaned_data['new_email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('There is already an account registered with this e-mail address.')
        return email

