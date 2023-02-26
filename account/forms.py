from .models import UserProf
from django import forms  

class EditProfile(forms.ModelForm):
    class Meta:
        model = UserProf
        fields = ('username', 'first_name', 'last_name','email', 'prof_image', 'biography', 'is_public')
        
        
        
        
class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput)

class changepassform(forms.Form):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget = forms.PasswordInput)

class createuserform(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget = forms.PasswordInput)
    
    class Meta:
        model = UserProf
        fields = ['username', 'first_name', 'last_name','email', 'prof_image', 'biography', 'is_public']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValdationError("Passwords don't match.")
        return cd['password2']
        
        
class RegistrationForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    username = forms.CharField(max_length=20)
    
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("password don't match")
        return cd['password2']
        
