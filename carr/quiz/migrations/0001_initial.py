# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
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
                ('submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(related_name='quiz_user', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordinality', models.IntegerField(default=1)),
                ('value', models.CharField(max_length=256, blank=True)),
                ('label', models.TextField(blank=True)),
                ('correct', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('question', 'ordinality'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('question_type', models.CharField(max_length=256, choices=[(b'multiple choice', b'Multiple Choice: Multiple answers'), (b'single choice', b'Multiple Choice: Single answer'), (b'short text', b'Short Text'), (b'long text', b'Long Text')])),
                ('ordinality', models.IntegerField(default=1)),
                ('explanation', models.TextField(blank=True)),
                ('intro_text', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('quiz', 'ordinality'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('rhetorical', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(blank=True)),
                ('question', models.ForeignKey(to='quiz.Question', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('quiz', models.ForeignKey(to='quiz.Quiz', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='response',
            name='submission',
            field=models.ForeignKey(to='quiz.Submission', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(to='quiz.Quiz', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='quiz.Question', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
