# Generated by Django 5.1.6 on 2025-03-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ButterflyApp', '0002_butterfly_video_alter_butterfly_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='butterfly',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='butterfly',
            name='location_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='butterfly',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='butterfly',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='butterflies/images/'),
        ),
        migrations.AlterField(
            model_name='butterfly',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='butterfly',
            name='species',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
