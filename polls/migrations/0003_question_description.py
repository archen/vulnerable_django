# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_decoration'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
