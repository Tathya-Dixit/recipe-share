from django import forms

from accounts.models import User

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['email', 'bio', 'profile_pic']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'placeholder': 'your@email.com',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'maxlength': '300',
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'accept': 'image/*',
            }),
        }
        
        labels = {
            'email': 'Email Address',
            'bio': 'Bio',
            'profile_pic': 'Profile Picture',
        }
        
        help_texts = {
            'bio': 'Max 300 characters',
            'profile_pic': 'JPG, PNG, or GIF (recommended size: 200x200px)',
        }

