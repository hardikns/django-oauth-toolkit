# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_provider', '0003_application_server_ips'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='require_email_verification',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
