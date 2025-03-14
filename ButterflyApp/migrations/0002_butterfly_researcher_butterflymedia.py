# Generated by Django 5.1.6 on 2025-03-13 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ButterflyApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='butterfly',
            name='researcher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='butterflies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ButterflyMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to='butterflies/media/')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('butterfly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='ButterflyApp.butterfly')),
                ('researcher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='butterfly_media', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
