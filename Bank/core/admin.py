from django.contrib import admin

from core.models import Place, Pracownicy, Rodzaje_kont, Klienci, Konta, Konto_kredytowe, Konto_debetowe, Kursy_walutowe, Konto_walutowe, Transakcje, Oceny_pracownikow

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(Pracownicy)
class PracownicyAdmin(admin.ModelAdmin):
    pass

@admin.register(Rodzaje_kont)
class Rodzaje_kontAdmin(admin.ModelAdmin):
    pass

@admin.register(Klienci)
class KlienciAdmin(admin.ModelAdmin):
    pass

@admin.register(Konta)
class KontaAdmin(admin.ModelAdmin):
    pass

@admin.register(Konto_kredytowe)
class Konto_kredytoweAdmin(admin.ModelAdmin):
    pass

@admin.register(Konto_debetowe)
class Konto_debetoweAdmin(admin.ModelAdmin):
    pass

@admin.register(Kursy_walutowe)
class Kursy_walutoweAdmin(admin.ModelAdmin):
    pass

@admin.register(Konto_walutowe)
class Konto_walutoweAdmin(admin.ModelAdmin):
    pass

@admin.register(Oceny_pracownikow)
class Oceny_pracownikowAdmin(admin.ModelAdmin):
    pass
