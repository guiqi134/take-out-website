# Generated by Django 2.2.1 on 2019-05-26 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20190526_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='count',
            field=models.PositiveIntegerField(),
        ),
    ]
