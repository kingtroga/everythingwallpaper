# Generated by Django 4.2.17 on 2025-01-01 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category_productitem_slug_alter_productitem_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name_plural': 'categories'},
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='colors',
        ),
    ]
