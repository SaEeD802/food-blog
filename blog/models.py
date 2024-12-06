from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
# import requests
import json
# import unicodedata
import jdatetime
# import re
from .utils import persian_slugify

# Create your models here.

class BaseModel(models.Model):
    """مدل پایه برای فیلدهای مشترک"""
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def get_jalali_date(self):
        if self.created_date:
            return jdatetime.datetime.fromgregorian(datetime=self.created_date).strftime('%Y/%m/%d')
        return ''

class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, verbose_name="نامک")
    icon = models.CharField(max_length=50, verbose_name="آیکون", help_text="نام کلاس FontAwesome")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

class Tag(BaseModel):
    name = models.CharField(max_length=50, verbose_name="نام برچسب")
    slug = models.SlugField(unique=True, verbose_name="نامک")

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"

    def __str__(self):
        return self.name

class Ingredient(BaseModel):
    name = models.CharField(max_length=100, verbose_name="نام ماده")
    unit = models.CharField(max_length=50, verbose_name="واحد اندازه‌گیری")

    class Meta:
        verbose_name = "ماده اولیه"
        verbose_name_plural = "مواد اولیه"

    def __str__(self):
        return self.name

class RecipeIngredient(BaseModel):
    recipe = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="ماده")
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="مقدار")
    notes = models.CharField(max_length=200, blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "ماده دستور پخت"
        verbose_name_plural = "مواد دستور پخت"

    def __str__(self):
        return f"{self.amount} {self.ingredient.unit} {self.ingredient.name}"

class Post(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'آسان'),
        ('medium', 'متوسط'),
        ('hard', 'سخت'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان", default="عنوان پیش‌فرض")
    slug = models.SlugField(unique=True, verbose_name="نامک", null=True, blank=True, allow_unicode=True)
    content = models.TextField(verbose_name="دستور پخت", default="دستور پخت پیش‌فرض")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="دسته‌بندی")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="برچسب‌ها")
    
    image = models.ImageField(upload_to='recipe_images/%Y/%m/', verbose_name="عکس دستور پخت", blank=True, null=True,
                            help_text="عکس اصلی دستور پخت")
    cover_image = models.ImageField(upload_to='recipe_covers/%Y/%m/', verbose_name="عکس کاور", blank=True, null=True,
                                  help_text="عکس کاور برای نمایش در لیست دستورها")
    
    prep_time = models.PositiveIntegerField(verbose_name="زمان آماده‌سازی (دقیقه)", default=30)
    cook_time = models.PositiveIntegerField(verbose_name="زمان پخت (دقیقه)", default=60)
    servings = models.PositiveIntegerField(verbose_name="تعداد نفرات", default=4)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name="سطح سختی", default='medium')
    calories = models.PositiveIntegerField(verbose_name="کالری (در هر وعده)", null=True, blank=True, default=500)
    
    recipe_ingredients = models.ManyToManyField(RecipeIngredient, verbose_name="مواد لازم", blank=True)
    
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipe_likes', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipe_bookmarks', blank=True)

    class Meta:
        verbose_name = "دستور پخت"
        verbose_name_plural = "دستورهای پخت"
        ordering = ['-created_date']

    def publish(self):
        self.status = 'published'
        self.save()

    def is_published(self):
        return self.status == 'published'

    def __str__(self):
        return self.title

    def total_time(self):
        return self.prep_time + self.cook_time

    def like_count(self):
        return self.likes.count()

    def bookmark_count(self):
        return self.bookmarks.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = persian_slugify(self.title)
        super().save(*args, **kwargs)

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="پست")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="نویسنده")
    text = models.TextField(verbose_name="متن نظر")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="امتیاز",
        null=True,
        blank=True,
        help_text="امتیاز بین 1 تا 5 (اختیاری)"
    )

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_date']

    def __str__(self):
        return f'نظر {self.author} برای {self.post}'
