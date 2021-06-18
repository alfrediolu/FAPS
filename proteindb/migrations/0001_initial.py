# Generated by Django 3.2.3 on 2021-06-18 16:17

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='csvAccession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='masterProtein',
            fields=[
                ('accession', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
            ],
            managers=[
                ('masterManage', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='uniProtein',
            fields=[
                ('accession', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('alpha', models.FloatField(default=0)),
                ('beta', models.FloatField(default=0)),
                ('turn', models.FloatField(default=0)),
                ('unknown', models.FloatField(default=1)),
                ('known', models.FloatField(default=0)),
                ('length', models.IntegerField()),
                ('master', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='uni', to='proteindb.masterprotein', unique=True)),
            ],
            managers=[
                ('uniManage', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='simProtein',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=20)),
                ('simType', models.CharField(default='', max_length=4)),
                ('alpha', models.FloatField(default=0)),
                ('beta', models.FloatField(default=0)),
                ('turn', models.FloatField(default=0)),
                ('length', models.IntegerField()),
                ('master', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sim', to='proteindb.masterprotein')),
            ],
            managers=[
                ('simManage', django.db.models.manager.Manager()),
            ],
        ),
    ]
