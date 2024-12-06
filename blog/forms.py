from django import forms
from .models import Post, Comment, RecipeIngredient
from django.forms import inlineformset_factory
from django.utils.text import slugify

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'cover_image', 'category', 'tags', 'prep_time', 'cook_time', 'servings', 'difficulty', 'calories', 'recipe_ingredients']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'recipe_ingredients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        
        # ایجاد نامک از عنوان
        instance.slug = slugify(instance.title)
        
        if commit:
            instance.save()
            
            # پردازش برچسب‌ها
            tags = self.cleaned_data.get('tags', '')
            if tags:
                instance.tags.clear()
                for tag in tags:
                    instance.tags.add(tag)
                    
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'notes']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }

RecipeIngredientFormSet = inlineformset_factory(
    Post, RecipeIngredient,
    form=RecipeIngredientForm,
    fields=['ingredient', 'amount', 'notes'],
    extra=3,
    can_delete=True
)
