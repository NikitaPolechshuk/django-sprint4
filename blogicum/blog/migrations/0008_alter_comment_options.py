# Generated by Django 5.1.1 on 2025-04-07 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date'], 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
