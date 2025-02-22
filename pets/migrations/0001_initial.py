# Generated by Django 4.2.5 on 2023-10-04 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('weight', models.FloatField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Not Informed', 'Not Informed')], default='Not Informed', max_length=20)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='groups.group')),
            ],
        ),
    ]
