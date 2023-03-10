# Generated by Django 2.2.28 on 2023-03-09 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('image', models.ImageField(upload_to='blog_images')),
                ('text', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotifyURL', models.CharField(max_length=128)),
                ('youtubeURL', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('coverArt', models.ImageField(upload_to='cover_images')),
                ('genre', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30, unique=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('artist', models.BooleanField()),
                ('review', models.BooleanField()),
                ('artsIndusry', models.BooleanField()),
                ('follows', models.ManyToManyField(related_name='_userprofile_follows_+', to='musicBlogger.UserProfile')),
                ('likedSong', models.ManyToManyField(to='musicBlogger.Songs')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('date', models.DateField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicBlogger.Blogs')),
                ('commentedBy', models.ManyToManyField(to='musicBlogger.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='blogs',
            name='postedBy',
            field=models.ManyToManyField(to='musicBlogger.UserProfile'),
        ),
    ]
