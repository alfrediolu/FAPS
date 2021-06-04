# Generated by Django 3.2.3 on 2021-06-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteindb', '0003_remove_protein_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='simProtein',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=10)),
                ('alpha', models.FloatField(default=0)),
                ('beta', models.FloatField(default=0)),
                ('turn', models.FloatField(default=0)),
                ('unknown', models.FloatField(default=1)),
                ('length', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='uniProtein',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=10)),
                ('alpha', models.FloatField(default=0)),
                ('beta', models.FloatField(default=0)),
                ('turn', models.FloatField(default=0)),
                ('unknown', models.FloatField(default=1)),
                ('length', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='protein',
        ),
    ]
