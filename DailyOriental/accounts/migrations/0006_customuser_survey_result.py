# Generated by Django 5.0.6 on 2024-08-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_alter_customuser_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="survey_result",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="설문 결과"
            ),
        ),
    ]