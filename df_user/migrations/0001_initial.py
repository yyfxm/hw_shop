# Generated by Django 2.0.4 on 2018-04-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=50)),
                ('urelname', models.CharField(default='', max_length=20)),
                ('uadr', models.CharField(default='', max_length=100)),
                ('uphone', models.CharField(default='', max_length=11)),
            ],
        ),
    ]
