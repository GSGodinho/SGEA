# Generated by Django 5.1 on 2024-10-23 02:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Sistema", "0002_alter_evento_descricao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cronograma",
            name="evento",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cronograma",
                to="Sistema.evento",
            ),
        ),
        migrations.AlterField(
            model_name="participante",
            name="email",
            field=models.EmailField(max_length=255),
        ),
    ]
