# Generated by Django 2.1.3 on 2018-11-28 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assumption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('value', models.CharField(max_length=64)),
                ('value_type', models.CharField(max_length=32)),
                ('app_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('description', models.TextField()),
                ('year', models.IntegerField()),
                ('license', models.CharField(max_length=255)),
                ('app_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SourceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='source',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='meta.SourceCategory'),
        ),
        migrations.AddField(
            model_name='assumption',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='meta.Source'),
        ),
    ]
