# Generated by Django 5.1 on 2024-08-18 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favlinks', '0002_remove_link_unique_user_url_link_unique_user_id_url'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='category',
            name='unique_link_category',
        ),
        migrations.RemoveConstraint(
            model_name='tag',
            name='unique_link_tag',
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('link_id', 'category'), name='unique_link_id_category'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('link_id', 'tag'), name='unique_link_id_tag'),
        ),
    ]
