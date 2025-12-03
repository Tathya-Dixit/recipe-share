from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class Recipe(models.Model):
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'recipe_images')
    small_description = models.TextField(max_length = 500)

    estimated_prep_time = models.CharField(max_length = 30, help_text = 'e.g. 30 Minutes or 1 Hour 30 Minutes')
    ingredients_list = models.TextField(help_text = 'Ingredients List : one item in one line, e.g. Rice - 150gm')
    process = models.TextField(help_text = 'Write one step in one line, e.g. First take Rice and rinse it in a bowl.')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'recipes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round((sum(r.rating for r in reviews) / reviews.count()), 1)
        return 0
    
    def total_reviews(self):
        return self.reviews.count()

    def __str__(self):
        return f"{self.title} - {self.author.username}" 
    
    class Meta:
        ordering = ['-created_at']



class Review(models.Model):
    review = models.TextField(max_length=500)
    rating = models.IntegerField(default=0, validators = [MinValueValidator(1), MaxValueValidator(5)], help_text="rate from 1 - 5 stars")
    
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE, related_name = 'reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'reviews')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.reviewer.username} - {self.recipe.title} : {self.rating}"
    
    class Meta:
        unique_together = ['recipe', 'reviewer']
        ordering = ['-created_at']



