# Generated by Django 3.2.4 on 2023-02-16 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('timeStamp', models.DateTimeField()),
                ('slug', models.CharField(max_length=350)),
                ('tags', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('gender', models.CharField(max_length=7)),
                ('concern', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('appointmentdate', models.CharField(max_length=25)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.consultant')),
            ],
        ),
    ]
