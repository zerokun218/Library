# Generated by Django 3.0.8 on 2020-07-29 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='book.Category'),
        ),
    ]