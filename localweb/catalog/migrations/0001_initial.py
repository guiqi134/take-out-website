# Generated by Django 2.2.1 on 2019-05-19 03:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('AName', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=256)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('first_name', models.CharField(max_length=32)),
                ('birth', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('personal_ID', models.CharField(max_length=18, unique=True)),
                ('account_type', models.CharField(choices=[('customer', '顾客'), ('rider', '骑手'), ('restaurant', '商家')], default='customer', max_length=32)),
                ('c_time', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('food_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('FName', models.CharField(max_length=128)),
                ('price', models.FloatField(max_length=1000)),
                ('count', models.IntegerField()),
                ('FImage', models.ImageField(blank=True, upload_to='food_image')),
                ('rating', models.FloatField(max_length=100)),
            ],
            options={
                'ordering': ['FName', 'count'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('AName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.Account')),
                ('address', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['AName'],
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('AName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.Account')),
                ('RName', models.CharField(max_length=128, unique=True)),
                ('RImage', models.ImageField(blank=True, upload_to='restaurant_image')),
                ('rating', models.FloatField(max_length=100)),
                ('RType', models.CharField(choices=[('snack', '快餐'), ('japanese', '日料'), ('chinese', '中式料理'), ('western', '西餐'), ('dessert', '甜品')], max_length=32)),
            ],
            options={
                'ordering': ['rating', 'RName'],
            },
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('AName', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.Account')),
                ('rating', models.FloatField(max_length=100)),
            ],
            options={
                'ordering': ['rating', 'AName'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('start_time', models.TimeField(auto_now_add=True)),
                ('end_time', models.TimeField(max_length=100)),
                ('order_status', models.IntegerField(choices=[(-1, '未送达'), (0, '正在配送'), (1, '已送达')], default=-1)),
                ('rest_rating', models.FloatField(default=-1, max_length=100)),
                ('rider_rating', models.FloatField(default=-1, max_length=100)),
                ('foods', models.ManyToManyField(to='catalog.Food')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Customer')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Restaurant')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Rider')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
        migrations.AddField(
            model_name='food',
            name='RName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Restaurant'),
        ),
        migrations.AlterUniqueTogether(
            name='food',
            unique_together={('FName', 'RName', 'price')},
        ),
    ]
