# Generated by Django 5.1.1 on 2025-04-07 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_author_alter_post_category_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(help_text='Дата и время публикации комментария', verbose_name='Дата и время публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_comments', to='blog.post', verbose_name='пост')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
