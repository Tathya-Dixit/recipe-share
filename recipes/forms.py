from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'small_description', 'estimated_prep_time', 'ingredients_list', 'process']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'placeholder': 'e.g., Matar Paneer, Chocolate Cake',
                'maxlength': '100',
            }),
            'small_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'rows': 3,
                'placeholder': 'A brief description of your recipe...',
                'maxlength': '500',
            }),
            'estimated_prep_time': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'placeholder': 'e.g., 30 Minutes, 1 Hour 15 Minutes',
                'maxlength': '30',
            }),
            'ingredients_list': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500 font-mono text-sm',
                'rows': 8,
                'placeholder': 'List each ingredient on a new line:\nRice - 2 cups\nPaneer - 500g\nOnions - 2 medium',
            }),
            'process': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'rows': 10,
                'placeholder': 'Write each step on a new line:\nWash and soak the rice\nHeat oil in a pan\nShallow fry paneer',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-yellow-500',
                'accept': 'image/*',
            }),
        }
        
    labels = {
        'small_description': 'Description',
        'ingredients_list': 'Ingredients',
    }
