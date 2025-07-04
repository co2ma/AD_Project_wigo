# Generated by Django 4.2 on 2025-06-14 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pybo", "0010_alter_blockeduser_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blockeduser",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterField(
            model_name="blockeduser",
            name="blocked_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blocked_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="blockeduser",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="blockeduser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blocked_users",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
