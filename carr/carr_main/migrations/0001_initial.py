# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pageblocks', '0001_initial'),
        ('pagetree', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlashVideoBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_url', models.CharField(max_length=512)),
                ('image_url', models.CharField(max_length=512)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PullQuoteBlock_2',
            fields=[
                ('pullquoteblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pageblocks.PullQuoteBlock')),
            ],
            options={
            },
            bases=('pageblocks.pullquoteblock',),
        ),
        migrations.CreateModel(
            name='PullQuoteBlock_3',
            fields=[
                ('pullquoteblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pageblocks.PullQuoteBlock')),
            ],
            options={
            },
            bases=('pageblocks.pullquoteblock',),
        ),
        migrations.CreateModel(
            name='SiteSection',
            fields=[
                ('section_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pagetree.Section')),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
            options={
            },
            bases=('pagetree.section',),
        ),
        migrations.CreateModel(
            name='SiteState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_location', models.CharField(max_length=255)),
                ('visited', models.TextField()),
                ('user', models.ForeignKey(related_name='application_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
