# Generated by Django 2.2.28 on 2023-03-09 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicBlogger', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='artsIndusry',
            new_name='artsIndustry',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.AddField(
            model_name='songs',
            name='name',
            field=models.CharField(default='No-Name', max_length=128),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='image',
            field=models.ImageField(blank=True, upload_to='blog_images'),
        ),
        migrations.RemoveField(
            model_name='blogs',
            name='postedBy',
        ),
        migrations.AddField(
            model_name='blogs',
            name='postedBy',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='musicBlogger.UserProfile'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='comments',
            name='commentedBy',
        ),
        migrations.AddField(
            model_name='comments',
            name='commentedBy',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='musicBlogger.UserProfile'),
            preserve_default=False,
        ),
    ]
