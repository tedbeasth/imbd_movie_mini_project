# Generated by Django 2.2.5 on 2019-09-25 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imbdapp', '0003_auto_20190925_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_score',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
    ]