# Generated by Django 2.2.5 on 2019-09-11 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190911_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='board',
            field=models.IntegerField(default=0),
        ),
    ]
