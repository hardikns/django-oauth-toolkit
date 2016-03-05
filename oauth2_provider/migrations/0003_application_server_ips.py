# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2_provider.validators


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_provider', '0002_08_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='server_ips',
            field=models.TextField(help_text='Allowed list of Server IP address on separate lines', blank=True, validators=[oauth2_provider.validators.validate_ips]),
            preserve_default=True,
        ),
    ]
