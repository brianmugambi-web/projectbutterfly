# Generated by Django 5.1.6 on 2025-03-08 09:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Butterfly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('species', models.CharField(blank=True, max_length=255, null=True)),
                ('characteristics', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='butterflies/images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='butterflies/videos/')),
                ('date_taken', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('location_name', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('validated', 'Validated'), ('rejected', 'Rejected')], default='pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_researcher', models.BooleanField(default=True)),
                ('is_expert', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ExpertReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('species_identification', models.CharField(blank=True, max_length=255, null=True)),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('decision', models.CharField(choices=[('accept', 'Accept'), ('reject', 'Reject')], default='reject', max_length=10)),
                ('butterfly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ButterflyApp.butterfly')),
                ('expert', models.ForeignKey(limit_choices_to={'is_expert': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
