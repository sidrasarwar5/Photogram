from django import forms
from .models import Tweet
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields =['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border border-cyan-900/10 bg-white/70 px-4 py-2.5 text-sm text-[#0e2d35] focus:outline-none focus:ring-2 focus:ring-cyan-400/40 resize-none',
                'rows': 3,
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm  text-[#0e2d35] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-cyan-500/10 file:text-[#0a4a58] hover:file:bg-cyan-500/20 truncate overflow-hidden file:m-5',
            }),
        }
        help_texts = {
            'text': 'Share what you are thinking.',
            'photo': 'Upload a JPG or PNG',
        }

input_class = (
    'w-full rounded-xl border border-cyan-900/15 bg-cyan-50/50 px-4 py-2.5 '
    'text-sm text-[#0e2d35] placeholder:text-[#9ac9d2] '
    'focus:outline-none focus:ring-2 focus:ring-[#3dbccc]/40 focus:border-[#3dbccc]/50 '
    'transition-all'
)

class UserRegistrationForm(UserCreationForm):
    email= forms.EmailField()
    class Meta:
        model = User
        fields =(
            'username' ,
            'email',
            'password1', 
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': input_class}) 

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': input_class})

