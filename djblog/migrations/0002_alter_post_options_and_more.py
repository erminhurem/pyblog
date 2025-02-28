# Generated by Django 5.1.5 on 2025-01-28 20:44

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djblog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-publish'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='djblog_post_publish_bec98b_idx',
        ),
        migrations.RemoveField(
            model_name='post',
            name='published',
        ),
        migrations.AddField(
            model_name='post',
            name='create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='djblog_post_publish_2e7e62_idx'),
        ),
    ]
