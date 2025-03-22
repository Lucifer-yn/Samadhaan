from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'password1', 'password2']


from django import forms
from .models import ReportIssue


class ReportIssueForm(forms.ModelForm):
    class Meta:
        model = ReportIssue
        fields = ['full_name', 'contact_no', 'address', 'state', 'district', 'reported_location', 'field_of_report', 'location_image', 'latitude', 'longitude', 'description']


from .models import Admin

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['full_name', 'application_id', 'email', 'post', 'posted_area', 'password','profile_picture']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")


from django.contrib.auth.hashers import check_password
from .models import Admin

class AdminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            raise forms.ValidationError("Invalid email or password.")

        if not check_password(password, admin.password):
            raise forms.ValidationError("Invalid email or password.")

        cleaned_data["admin"] = admin  # Store the admin object for later use
        return cleaned_data

from django import forms
from .models import ProjectDetail

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }
