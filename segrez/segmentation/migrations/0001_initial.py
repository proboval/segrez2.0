# Generated by Django 5.0.1 on 2024-01-03 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=25)),
                ('Red', models.IntegerField()),
                ('Green', models.IntegerField()),
                ('Blue', models.IntegerField()),
            ],
        ),
    ]
