# Generated by Django 5.1.2 on 2024-11-02 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appp', '0005_carritoitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carritoitem',
            name='agregado_el',
        ),
    ]
