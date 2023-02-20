from django.db import models

# Create your models here.

class Place(models.Model):
    stanowisko = models.CharField(max_length = 100)
    placa_podstawowa = models.FloatField(max_length = 100)
    def __str__(self):
        return self.stanowisko + " " + str(self.placa_podstawowa)

class Pracownicy(models.Model):
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=20)
    stanowisko = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='pracownicy')
    haslo = models.CharField(max_length=100)
    def __str__(self):
        return str(self.stanowisko.stanowisko)+" "+ self.imie + " " + self.nazwisko
class Rodzaje_kont(models.Model):
    rodzaj_konta = models.CharField(max_length=20)
    def __str__(self):
        return self.rodzaj_konta
class Klienci(models.Model):
    imie = models.CharField(max_length=20)
    nazwisko = models.CharField(max_length=20)
    id_pracownika = models.ForeignKey(Pracownicy, on_delete=models.CASCADE, related_name='klienci')
    ocena = models.IntegerField(max_length=100)
    haslo = models.CharField(max_length=100)
    def __str__(self):
        return str(self.id_pracownika.id) + " " +self.imie + " " + self.nazwisko

class Konta(models.Model):
    rodzaj_konta = models.ForeignKey(Rodzaje_kont, on_delete=models.CASCADE, related_name='konta')
    id_klienta = models.ForeignKey(Klienci, on_delete=models.CASCADE, related_name='konta')
    id_pracownika = models.ForeignKey(Pracownicy, on_delete=models.CASCADE, related_name='konta')
    data_utworzenia = models.DateField()
    def __str__(self):
        return str(self.id_klienta.imie )+ " " + str(self.rodzaj_konta.rodzaj_konta)
class Konto_kredytowe(models.Model):
    id_konta = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='konta_kredytowe')
    oprocentowanie = models.CharField(max_length = 100)
    saldo = models.FloatField(max_length=100)
    def __str__(self):
        return str(self.id_konta.id) + " " + str(self.id_konta.id_klienta.imie)

class Konto_debetowe(models.Model):
    id_konta = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='konta_debetowe')
    saldo = models.FloatField(max_length=100)
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
    saldo = models.FloatField(max_length=100)
    def __str__(self):
        return str(self.id_konta.id) + " " + str(self.id_konta.id_klienta.imie)

class Transakcje(models.Model):
    data_transakcji = models.DateField()
    kwota = models.FloatField(max_length=100)
    id_konta_platnika = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='obciazenia')
    id_konta_odbiorcy = models.ForeignKey(Konta, on_delete=models.CASCADE, related_name='uznania')
    def __str__(self):
        return str(self.id) + " " + str(self.id_konta_platnika.id_klienta.imie) + " " + str(self.id_konta_odbiorcy.id_klienta.imie) + " " + str(self.kwota)

class Oceny_pracownikow(models.Model):
    id_pracownika = models.OneToOneField(Pracownicy, on_delete=models.CASCADE, related_name='oceny')
    ocena = models.FloatField(max_length=100)
    def __str__(self):
        return self.id_pracownika + " " + self.ocena