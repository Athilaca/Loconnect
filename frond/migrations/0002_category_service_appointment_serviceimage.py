# Generated by Django 5.0.3 on 2024-04-15 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frond', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.CharField(help_text='Estimated duration of the service', max_length=50)),
                ('location', models.CharField(help_text='Location where the service is provided', max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frond.category')),
                ('provider', models.ForeignKey(help_text='Service provider', on_delete=django.db.models.deletion.CASCADE, related_name='services', to='frond.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(help_text='Date and time of the appointment')),
                ('notes', models.TextField(blank=True, help_text='Any additional notes for the appointment')),
                ('user', models.ForeignKey(help_text='User who booked the service', on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='frond.userprofile')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='frond.service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Image related to the service', null=True, upload_to='services/')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='frond.service')),
            ],
        ),
    ]