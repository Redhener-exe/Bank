from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Q
from core.models import Place, Pracownicy, Rodzaje_kont, Klienci, Konta, Konto_kredytowe, Konto_debetowe, Kursy_walutowe, Konto_walutowe, Transakcje, Oceny_pracownikow

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("stanowisko", "placa_podstawowa")
    pass

@admin.register(Pracownicy)
class PracownicyAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "stanowisko")
    def get_queryset(self, request):
        Kierownik_dzialu = Group.objects.get(name='Kierownik działu')
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        qs = super().get_queryset(request)
        if request.user in Kierownik_dzialu.user_set.all():
            return qs
        elif request.user in Senior.user_set.all():
            return qs.filter(Q(author__id=request.user.id) | Q(stanowisko__stanowisko="Junior") | Q(stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(Q(author__id=request.user.id) | Q(stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        return qs

@admin.register(Rodzaje_kont)
class Rodzaje_kontAdmin(admin.ModelAdmin):
    pass

@admin.register(Klienci)
class KlienciAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "id_pracownika")
    def get_queryset(self, request):
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        Klient = Group.objects.get(name='Klient')
        qs = super().get_queryset(request)
        if request.user in Senior.user_set.all():
            return qs.filter(Q(id_pracownika__author__id=request.user.id) | Q(id_pracownika__stanowisko__stanowisko="Junior") | Q(id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(Q(id_pracownika__author__id=request.user.id) | Q(id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(id_pracownika__author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        elif request.user in Klient.user_set.all():
            return qs.filter(Q(author__id=request.user.id))
        return qs


@admin.register(Konta)
class KontaAdmin(admin.ModelAdmin):
    list_display = ("id",'rodzaj_konta', "id_klienta", "id_pracownika", "data_utworzenia")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        Klient = Group.objects.get(name='Klient')
        if db_field.name == "id_klienta":
            if request.user in Klient.user_set.all():
                kwargs["queryset"] = Klienci.objects.filter(author=request.user)
            else:
                kwargs["queryset"] = Klienci.objects.filter(id_pracownika__author=request.user)
        if db_field.name == "id_pracownika":
            kwargs["queryset"] = Pracownicy.objects.filter(klienci__author = request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def formfield_form(self, db_field, request, **kwargs):
        if db_field.name == "data_utworzenia":
            kwargs["initial"] = datetime.now()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        Klient = Group.objects.get(name='Klient')
        qs = super().get_queryset(request)
        if request.user in Senior.user_set.all():
            return qs.filter(
                Q(id_klienta__id_pracownika__author__id=request.user.id) | Q(id_klienta__id_pracownika__stanowisko__stanowisko="Junior") | Q(
                    id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(
                Q(id_klienta__id_pracownika__author__id=request.user.id) | Q(id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(id_klienta__id_pracownika__author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        elif request.user in Klient.user_set.all():
            return qs.filter(id_klienta__author=request.user)
        return qs

@admin.register(Konto_kredytowe)
class Konto_kredytoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "oprocentowanie", "saldo")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_konta":
            kwargs["queryset"] = Konta.objects.filter(rodzaj_konta__rodzaj_konta="Kredytowe")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        Klient = Group.objects.get(name='Klient')
        qs = super().get_queryset(request)
        if request.user in Senior.user_set.all():
            return qs.filter(
                Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id) | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Junior") | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(
                Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id) | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        elif request.user in Klient.user_set.all():
            return qs.filter(id_konta__id_klienta__author=request.user)
        return qs

@admin.register(Konto_debetowe)
class Konto_debetoweAdmin(admin.ModelAdmin):
    list_display = ("id_konta", "saldo")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_konta":
            kwargs["queryset"] = Konta.objects.filter(rodzaj_konta__rodzaj_konta="Debetowe")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        Klient = Group.objects.get(name='Klient')
        qs = super().get_queryset(request)
        if request.user in Senior.user_set.all():
            return qs.filter(
                Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id) | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Junior") | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(
                Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id) | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        elif request.user in Klient.user_set.all():
            return qs.filter(id_konta__id_klienta__author=request.user)
        return qs


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
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        Klient = Group.objects.get(name='Klient')
        qs = super().get_queryset(request)
        if request.user in Senior.user_set.all():
            return qs.filter(
                Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id) | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Junior") | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(
                Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id) | Q(
                    id_konta__id_klienta__id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(id_konta__id_klienta__id_pracownika__author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        elif request.user in Klient.user_set.all():
            return qs.filter(id_konta__id_klienta__author=request.user)
        return qs


@admin.register(Oceny_pracownikow)
class Oceny_pracownikowAdmin(admin.ModelAdmin):
    list_display = ("id_pracownika", "ocena")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        Klient = Group.objects.get(name='Klient')
        if db_field.name == "id_pracownika":
            if request.user in Klient.user_set.all():
                kwargs["queryset"] = Pracownicy.objects.filter(klienci__author=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        Kierownik_dzialu = Group.objects.get(name='Kierownik działu')
        Senior = Group.objects.get(name='Senior')
        Junior = Group.objects.get(name='Junior')
        Praktykant = Group.objects.get(name='Praktykant')
        Szef_admin = Group.objects.get(name='Szef/admin')
        qs = super().get_queryset(request)
        if request.user in Senior.user_set.all():
            return qs.filter(
                Q(id_pracownika__author__id=request.user.id) | Q(
                    id_pracownika__stanowisko__stanowisko="Junior") | Q(
                    id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Junior.user_set.all():
            return qs.filter(
                Q(id_pracownika__author__id=request.user.id) | Q(
                    id_pracownika__stanowisko__stanowisko="Praktykant"))
        elif request.user in Praktykant.user_set.all():
            return qs.filter(Q(id_pracownika__author__id=request.user.id))
        elif request.user in Szef_admin.user_set.all():
            return qs
        elif request.user in Kierownik_dzialu.user_set.all():
            return qs
        return qs