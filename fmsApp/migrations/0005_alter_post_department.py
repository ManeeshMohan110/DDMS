# Generated by Django 4.0.3 on 2024-02-15 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fmsApp', '0004_alter_post_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fmsApp.department'),
        ),
    ]
