from django import forms
from django.forms import ModelForm
from selling.models import Item_posting

class SignupForm(forms.Form):
    username=forms.CharField(max_length=100,
            error_messages = {'required': 'Please make a username'}
                             )
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_confirm = forms.CharField()
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != \
                cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class changeForm(forms.Form):
    last_name=forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()

class changePassword(forms.Form):
    username = forms.CharField()
    password = forms.CharField( error_messages = {'required': 'Please choose a password'})
    password_confirm = forms.CharField( error_messages = {'required': 'Please confirm a password'})

    def clean(self):
        cleaned_data = super(changePassword, self).clean()

        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != \
                cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        return cleaned_data


class ItemSalesForm(ModelForm):
    class Meta:
        model = Item_posting
        fields = ['descrip', 'image','image2','image3','image4','price','type','color','designer','title', 'size']
