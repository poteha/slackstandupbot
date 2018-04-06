# Generated by Django 2.0.4 on 2018-04-05 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standupbot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='answers',
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='standupbot.User'),
            preserve_default=False,
        ),
    ]
