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
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Konta)
class KontaAdmin(admin.ModelAdmin):
    list_display = ("id",'rodzaj_konta', "id_klienta", "id_pracownika", "data_utworzenia")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_klienta":
            kwargs["queryset"] = Klienci.objects.filter(author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def formfield_form(self, db_field, request, **kwargs):
        if db_field.name == "data_utworzenia":
            kwargs["initial"] = datetime.now()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id_klienta__author=request.user)

@admin.register(Konto_kredytowe)
class Konto_kredytoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "oprocentowanie", "saldo")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_konta":
            kwargs["queryset"] = Konta.objects.filter(rodzaj_konta__rodzaj_konta="Kredytowe")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id_konta__id_klienta__author= request.user, id_konta__rodzaj_konta__rodzaj_konta = "Kredytowe")

@admin.register(Konto_debetowe)
class Konto_debetoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "saldo")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_konta":
            kwargs["queryset"] = Konta.objects.filter(rodzaj_konta__rodzaj_konta="Debetowe")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter( id_konta__id_klienta__author= request.user)


@admin.register(Kursy_walutowe)
class Kursy_walutoweAdmin(admin.ModelAdmin):
    list_display = ("waluta", "kurs_kupna", "kurs_sprzedazy")


@admin.register(Konto_walutowe)
class Konto_walutoweAdmin(admin.ModelAdmin):
    list_display = ("id","id_konta", "waluta", "saldo")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_konta":
            kwargs["queryset"] = Konta.objects.filter(rodzaj_konta__rodzaj_konta="Walutowe")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
            qs = super().get_queryset(request)
            if request.user.is_superuser:
                return qs
            return qs.filter(id_konta__id_klienta__author= request.user)


@admin.register(Oceny_pracownikow)
class Oceny_pracownikowAdmin(admin.ModelAdmin):
    list_display = ("id_pracownika", "ocena")
