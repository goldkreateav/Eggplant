# Generated by Django 3.0.8 on 2020-07-04 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eggplant', '0002_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=70)),
                ('client', models.CharField(max_length=30)),
                ('provider', models.CharField(max_length=30)),
            ],
        ),
    ]
