from django.db import models
from django.contrib.auth.models import User # new
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, F, Value
# Create your models here.

class Place(models.Model):
    stanowisko = models.CharField(max_length = 100)
    placa_podstawowa = models.FloatField(max_length = 100)
    def __str__(self):
        return self.stanowisko + " " + str(self.placa_podstawowa)

class Pracownicy(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=20)
    stanowisko = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='pracownicy')
    nr_ocen = models.IntegerField(default=0)
    def __str__(self):
        return str(self.stanowisko.stanowisko)+" "+ self.imie + " " + self.nazwisko
class Rodzaje_kont(models.Model):
    rodzaj_konta = models.CharField(max_length=20)
    def __str__(self):
        return self.rodzaj_konta
class Klienci(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=20)
    id_pracownika = models.ForeignKey(Pracownicy, on_delete=models.CASCADE, related_name='klienci')
    def __str__(self):
        return str(self.id_pracownika.id) + " " +self.imie + " " + self.nazwisko

class Konta(models.Model):
    rodzaj_konta = models.ForeignKey(Rodzaje_kont, on_delete=models.CASCADE, related_name='rodzaje_kont')
    id_klienta = models.ForeignKey(Klienci, on_delete=models.CASCADE, related_name='konta_klienta')
    id_pracownika = models.ForeignKey(Pracownicy, on_delete=models.CASCADE, related_name='konta_pracownika')
    data_utworzenia = models.DateField()
    def __str__(self):
        return str(self.id_klienta.imie )+ " " + str(self.rodzaj_konta.rodzaj_konta)
class Konto_kredytowe(models.Model):
    id_konta = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='konta_kredytowe')
    oprocentowanie = models.CharField(max_length = 100)
    saldo = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.id_konta.id) + " " + str(self.id_konta.id_klienta.imie) + " " + str(self.saldo)

class Konto_debetowe(models.Model):
    id_konta = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='konta_debetowe')
    saldo = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.id_konta.id)+" "+str(self.id_konta.id_klienta.imie)
class Kursy_walutowe(models.Model):
    waluta = models.CharField(max_length = 100)
    kurs_kupna = models.FloatField(max_length=100)
    kurs_sprzedazy = models.FloatField(max_length=100)
    def __str__(self):
        return self.waluta
class Konto_walutowe(models.Model):
    id_konta = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='konta_walutowe')
    waluta = models.ForeignKey(Kursy_walutowe, on_delete=models.CASCADE, related_name='konta_walutowe')
    saldo = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.id_konta.id) + " " + str(self.id_konta.id_klienta.imie) + " " + str(self.saldo)

class Transakcje(models.Model):
    data_transakcji = models.DateField()
    kwota = models.FloatField()
    id_konta_platnika = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='obciazenia')
    id_konta_odbiorcy = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='uznania')

    def __str__(self):
        return str(self.id) + " " + str(self.id_konta_platnika.id_klienta.imie) + " " + str(self.id_konta_odbiorcy.id_klienta.imie) + " " + str(self.kwota)


class Oceny_pracownikow(models.Model):
    id_pracownika = models.OneToOneField(Pracownicy, on_delete=models.CASCADE, related_name='oceny')
    ocena = models.FloatField(max_length=100, validators=[MinValueValidator(0), MaxValueValidator(5)])
    ilosc_ocen_pracownika = models.OneToOneField(Pracownicy, on_delete=models.CASCADE, related_name='ilosc_ocen')
    def __str__(self):
        return self.id_pracownika + " " + self.ocena

@receiver(post_save, sender=Oceny_pracownikow, dispatch_uid="update_ocen")
def update_ocen(sender, instance, created, **kwargs):
        instance.id_pracownika.ilosc_ocen = instance.id_pracownika.ilosc_ocen + 1
        instance.id_pracownika.save()
        instance.id_pracownika.oceny.all().values('ocena').update(ocena=(instance.id_pracownika.oceny.all().aggregate(Sum('ocena'))['ocena__sum'])/instance.id_pracownika.ilosc_ocen)
#nie dotykać tegoS
@receiver(post_save, sender=Transakcje, dispatch_uid="update_konta")
def update_konta(sender, instance, created, **kwargs):
    if instance.id_konta_platnika.rodzaj_konta.rodzaj_konta == "Debetowe":
        if instance.id_konta_platnika.konta_debetowe.all().aggregate(Sum('saldo'))['saldo__sum'] < instance.kwota:
            raise ValidationError("Brak środków na koncie")
        else:
            instance.id_konta_platnika.konta_debetowe.all().values('saldo').update(saldo=F('saldo') - instance.kwota)
    if instance.id_konta_platnika.rodzaj_konta.rodzaj_konta == "Kredytowe":
        if instance.id_konta_platnika.konta_kredytowe.all().aggregate(Sum('saldo'))['saldo__sum'] < instance.kwota:
            raise ValidationError("Brak środków na koncie")
        else:
            instance.id_konta_platnika.konta_kredytowe.all().values('saldo').update(saldo=F('saldo') - instance.kwota)
    if instance.id_konta_platnika.rodzaj_konta.rodzaj_konta == "Walutowe":
        if instance.id_konta_platnika.konta_walutowe.all().aggregate(Sum('saldo'))['saldo__sum'] < instance.kwota:
            raise ValidationError("Brak środków na koncie")
        if instance.id_konta_platnika.konta_walutowe.waluta.waluta == instance.id_konta_odbiorcy.konta_walutowe.waluta.waluta:
            instance.id_konta_platnika.konta_walutowe.all().Konto_kredytowe.objects.filter(id=instance.id_konta_platnika.konta_kredytowe.all().values_list('id', flat=True)).update(saldo=F('saldo') - instance.kwota)
        else:
            instance.id_konta_platnika.konta_walutowe.all().values('saldo').update(saldo=F('saldo') - instance.kwota * instance.id_konta_odbiorcy.konta_walutowe.waluta.kurs_sprzedazy)
    if instance.id_konta_odbiorcy.rodzaj_konta.rodzaj_konta == "Debetowe":
        instance.id_konta_odbiorcy.konta_debetowe.all().values('saldo').update(saldo=F('saldo') + instance.kwota)
    if instance.id_konta_odbiorcy.rodzaj_konta.rodzaj_konta == "Kredytowe":
        instance.id_konta_odbiorcy.konta_kredytowe.all().values('saldo').update(saldo=F('saldo') + instance.kwota)
    if instance.id_konta_odbiorcy.rodzaj_konta.rodzaj_konta == "Walutowe":
        if instance.id_konta_platnika.konta_walutowe.waluta.waluta == instance.id_konta_odbiorcy.konta_walutowe.waluta.waluta:
            instance.id_konta_odbiorcy.konta_walutowe.all().values('saldo').update(saldo=F('saldo') + instance.kwota)
        else:
            instance.id_konta_odbiorcy.konta_walutowe.all().values('saldo').update(saldo=F('saldo') + instance.kwota * instance.id_konta_odbiorcy.konta_walutowe.waluta.kurs_sprzedazy)
