# Generated by Django 3.1 on 2020-09-27 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0002_auto_20200919_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
