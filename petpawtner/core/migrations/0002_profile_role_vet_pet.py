# Generated by Django 4.2.15 on 2024-08-30 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('owner', 'Pet Owner'), ('vet', 'Vet')], default='owner', max_length=5),
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
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vet_profile', to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('bio', models.TextField(blank=True)),
                ('profileimg', models.ImageField(default='dog_paw-pp.png', upload_to='pet_images')),
                ('location', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='core.profile')),
            ],
        ),
    ]