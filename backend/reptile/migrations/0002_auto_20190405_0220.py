# Generated by Django 2.2 on 2019-04-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reptile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='keyword',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
