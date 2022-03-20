# Generated by Django 3.2.10 on 2022-03-09 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220308_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='choose_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
    ]
