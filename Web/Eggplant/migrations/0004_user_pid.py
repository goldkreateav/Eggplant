# Generated by Django 3.0.8 on 2020-07-04 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eggplant', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pid',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
