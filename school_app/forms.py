from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import CustomUser, Student, LibraryHistory, FeesHistory

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            'role',
            Submit('submit', 'Register', css_class='btn btn-success')
        )
        # Add placeholders and CSS classes
        for field in self.fields:
            if field == 'role':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            else:
                self.fields[field].widget.attrs.update({'placeholder': f'Enter {field.capitalize()}', 'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )

# Student Form with Crispy Forms Layout
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'class_name', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'class_name',
            'age',
            Submit('submit', 'Save Student', css_class='btn btn-primary')
        )
        # Add placeholders and CSS classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'placeholder': f'Enter {field.replace("_", " ").capitalize()}', 'class': 'form-control'})

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 5 or age > 100):
            raise forms.ValidationError("Age must be between 5 and 100.")
        return age

# Fees History Form
class FeesHistoryForm(forms.ModelForm):
    class Meta:
        model = FeesHistory
        fields = ['student', 'amount', 'payment_date', 'remarks', 'payment_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'student',
            'amount',
            'payment_date',
            'remarks',
            'payment_status',
            Submit('submit', 'Save Record', css_class='btn btn-primary')
        )
        # Add placeholders and CSS classes
        for field in self.fields:
            if field == 'student':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            else:
                self.fields[field].widget.attrs.update({'placeholder': f'Enter {field.replace("_", " ").capitalize()}', 'class': 'form-control'})

# Library Record Form
class LibraryRecordForm(forms.ModelForm):
    class Meta:
        model = LibraryHistory
        fields = ['student', 'book', 'borrow_date', 'return_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'student',
            'book',
            'borrow_date',
            'return_date',
            Submit('submit', 'Save Record', css_class='btn btn-primary')
        )
        # Add placeholders and CSS classes
        for field in self.fields:
            if field in ['student', 'book']:
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            else:
                self.fields[field].widget.attrs.update({'placeholder': f'Enter {field.replace("_", " ").capitalize()}', 'class': 'form-control'})


