# Generated by Django 4.1.7 on 2023-02-20 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Klienci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=20)),
                ('nazwisko', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Konta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_utworzenia', models.DateField()),
                ('id_klienta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta', to='core.klienci')),
            ],
        ),
        migrations.CreateModel(
            name='Kursy_walutowe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waluta', models.CharField(max_length=100)),
                ('kurs_kupna', models.FloatField(max_length=100)),
                ('kurs_sprzedazy', models.FloatField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stanowisko', models.CharField(max_length=100)),
                ('placa_podstawowa', models.FloatField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rodzaje_kont',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodzaj_konta', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transakcje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_transakcji', models.DateField()),
                ('kwota', models.FloatField(max_length=100)),
                ('id_konta_odbiorcy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uznania', to='core.konta')),
                ('id_konta_platnika', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='obciazenia', to='core.konta')),
            ],
        ),
        migrations.CreateModel(
            name='Pracownicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=20)),
                ('nazwisko', models.CharField(max_length=20)),
                ('stanowisko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pracownicy', to='core.place')),
            ],
        ),
        migrations.CreateModel(
            name='Oceny_pracownikow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocena', models.FloatField(max_length=100)),
                ('id_pracownika', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='oceny', to='core.pracownicy')),
            ],
        ),
        migrations.CreateModel(
            name='Konto_walutowe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.FloatField(max_length=100)),
                ('id_konta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta_walutowe', to='core.konta')),
                ('waluta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta_walutowe', to='core.kursy_walutowe')),
            ],
        ),
        migrations.CreateModel(
            name='Konto_kredytowe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oprocentowanie', models.CharField(max_length=100)),
                ('saldo', models.FloatField(max_length=100)),
                ('id_konta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta_kredytowe', to='core.konta')),
            ],
        ),
        migrations.CreateModel(
            name='Konto_debetowe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.FloatField(max_length=100)),
                ('id_konta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta_debetowe', to='core.konta')),
            ],
        ),
        migrations.AddField(
            model_name='konta',
            name='id_pracownika',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta', to='core.pracownicy'),
        ),
        migrations.AddField(
            model_name='konta',
            name='rodzaj_konta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konta', to='core.rodzaje_kont'),
        ),
        migrations.AddField(
            model_name='klienci',
            name='id_pracownika',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='klienci', to='core.pracownicy'),
        ),
        migrations.AddField(
            model_name='klienci',
            name='login',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
