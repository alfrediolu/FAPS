# Generated by Django 3.2.3 on 2021-06-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proteindb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simprotein',
            name='simType',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='uniprotein',
            name='accession',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
