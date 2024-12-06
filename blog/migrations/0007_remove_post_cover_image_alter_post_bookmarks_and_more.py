# Generated by Django 4.2.7 on 2024-11-16 13:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_post_recipe_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='cover_image',
        ),
        migrations.AlterField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='post_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='cook_time',
            field=models.PositiveIntegerField(blank=True, default=60, null=True, verbose_name='زمان پخت (دقیقه)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='difficulty',
            field=models.CharField(blank=True, choices=[('easy', 'آسان'), ('medium', 'متوسط'), ('hard', 'سخت')], default='medium', max_length=10, null=True, verbose_name='سطح سختی'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='prep_time',
            field=models.PositiveIntegerField(blank=True, default=30, null=True, verbose_name='زمان آماده\u200cسازی (دقیقه)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='servings',
            field=models.PositiveIntegerField(blank=True, default=4, null=True, verbose_name='تعداد نفرات'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=250, null=True, unique=True, verbose_name='نامک'),
        ),
    ]
