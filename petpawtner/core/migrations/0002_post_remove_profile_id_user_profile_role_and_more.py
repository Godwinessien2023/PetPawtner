# Generated by Django 4.2.15 on 2024-09-23 11:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('caption', models.TextField()),
                ('no_of_likes', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='post_images')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('owner', 'Pet Owner'), ('vet', 'Vet')], default='owner', max_length=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Vet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(max_length=100)),
                ('specialty', models.CharField(max_length=100)),
                ('years_of_experience', models.IntegerField()),
                ('contact_info', models.CharField(blank=True, max_length=100)),
                ('profileimg', models.ImageField(default='vet-icon.png', upload_to='vet_images')),
                ('location', models.CharField(max_length=50)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vet', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=20)),
                ('sex', models.CharField(default='Unknown', max_length=10)),
                ('bio', models.TextField(blank=True)),
                ('profileimg', models.ImageField(default='dog_paw-pp.png', upload_to='pet_images')),
                ('location', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='core.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='core.profile')),
            ],
        ),
    ]