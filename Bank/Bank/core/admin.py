from django.contrib import admin

from core.models import Place, Pracownicy, Rodzaje_kont, Klienci, Konta, Konto_kredytowe, Konto_debetowe, Kursy_walutowe, Konto_walutowe, Transakcje, Oceny_pracownikow

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("stanowisko", "placa_podstawowa")
    pass

@admin.register(Pracownicy)
class PracownicyAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "stanowisko")
    pass

@admin.register(Rodzaje_kont)
class Rodzaje_kontAdmin(admin.ModelAdmin):
    pass

@admin.register(Klienci)
class KlienciAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "id_pracownika")
    pass

@admin.register(Konta)
class KontaAdmin(admin.ModelAdmin):
    list_display = ("rodzaj_konta", "id_klienta", "id_pracownika", "data_utworzenia")
    pass

@admin.register(Konto_kredytowe)
class Konto_kredytoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "oprocentowanie", "saldo")
    pass

@admin.register(Konto_debetowe)
class Konto_debetoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "saldo")
    pass

@admin.register(Kursy_walutowe)
class Kursy_walutoweAdmin(admin.ModelAdmin):
    list_display = ("waluta", "kurs_kupna", "kurs_sprzedazy")
    pass

@admin.register(Konto_walutowe)
class Konto_walutoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "waluta", "saldo")
    pass

@admin.register(Oceny_pracownikow)
class Oceny_pracownikowAdmin(admin.ModelAdmin):
    list_display = ("id_pracownika", "ocena")
    pass
