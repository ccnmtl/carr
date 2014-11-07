# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json', models.TextField(blank=True)),
                ('user', models.ForeignKey(related_name='bruise_recon_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_name', models.CharField(max_length=25)),
                ('show_correct', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to=b'media/img//%Y/%m/%d/', null=True, verbose_name=b'image', blank=True)),
                ('case_history', models.TextField()),
                ('correct_answer', models.CharField(max_length=25)),
                ('explanation', models.TextField()),
                ('factors_for_decision', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
