# Generated by Django 5.0.2 on 2024-11-07 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=150)),
                ('committe_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('order_Text', models.CharField(blank=True, max_length=500, null=True)),
                ('order_Description', models.TextField(blank=True, null=True)),
                ('committe_Expiry', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Committees',
                'db_table': 'committe',
            },
        ),
        migrations.CreateModel(
            name='SubCommittee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_committee_name', models.CharField(max_length=255)),
                ('sub_committee_Text', models.CharField(blank=True, max_length=500, null=True)),
                ('committee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_committees', to='committee.committe')),
            ],
            options={
                'verbose_name_plural': 'Sub Committees',
                'db_table': 'sub_committee',
            },
        ),
        migrations.CreateModel(
            name='CommitteeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=250)),
                ('score', models.IntegerField()),
                ('is_past_member', models.BooleanField(default=False)),
                ('committee_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='committee.committe')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committees_employee', to='employee.employee')),
                ('subcommittee_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='committee.subcommittee')),
            ],
            options={
                'verbose_name_plural': 'Committee Details',
                'db_table': 'committee_details',
            },
        ),
    ]
