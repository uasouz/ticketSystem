# Generated by Django 2.2.5 on 2019-09-11 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190911_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.CharField(default='', max_length=400),
        ),
    ]
