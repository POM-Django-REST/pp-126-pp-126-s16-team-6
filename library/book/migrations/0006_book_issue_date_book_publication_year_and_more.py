# Generated by Django 4.2 on 2025-04-02 01:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_remove_author_books'),
        ('book', '0005_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='issue_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date of issue'),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.PositiveIntegerField(default=None, verbose_name='Publication year'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author', verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='count',
            field=models.IntegerField(default=10, verbose_name='Copies available'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, max_length=256, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(blank=True, max_length=128, verbose_name='Title'),
        ),
    ]
