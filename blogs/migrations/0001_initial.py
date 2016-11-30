# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 10:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0431\u043b\u043e\u0433\u0430')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0411\u043b\u043e\u0433',
                'verbose_name_plural': '\u0411\u043b\u043e\u0433\u0438',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u0441\u0442\u0430\u0442\u044c\u0438')),
                ('body', models.TextField(verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0442\u044c\u0438')),
                ('pub_date', models.DateField()),
                ('mod_date', models.DateField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043f\u0438\u0441\u044c \u0431\u043b\u043e\u0433\u0430',
                'verbose_name_plural': '\u0417\u0430\u043f\u0438\u0441\u0438 \u0431\u043b\u043e\u0433\u0430',
            },
        ),
    ]