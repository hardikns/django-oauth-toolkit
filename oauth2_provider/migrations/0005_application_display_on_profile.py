# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_provider', '0004_application_require_email_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='display_on_profile',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
