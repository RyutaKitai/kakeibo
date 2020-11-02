# Generated by Django 2.1.7 on 2019-03-07 08:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kakeibo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='kakeibo',
            options={'verbose_name': 'Kakeibo', 'verbose_name_plural': 'Kakeibo'},
        ),
        migrations.AlterField(
            model_name='kakeibo',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kakeibo.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='kakeibo',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='kakeibo',
            name='memo',
            field=models.CharField(max_length=500, verbose_name='Memo'),
        ),
        migrations.AlterField(
            model_name='kakeibo',
            name='money',
            field=models.IntegerField(help_text='Australia dollars', verbose_name='Fee'),
        ),
    ]
