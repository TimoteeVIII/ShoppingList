# Generated by Django 5.1.1 on 2024-10-01 16:21

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='household_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('household_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.household')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='', max_length=50)),
                ('quantity', models.FloatField()),
                ('completed', models.BooleanField(default=False)),
                ('shopping_list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.shoppinglist')),
            ],
        ),
        migrations.CreateModel(
            name='UserHousehold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('household_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.household')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
