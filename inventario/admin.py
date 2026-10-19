from django.contrib import admin

from .models import Controle, Equipamento, Usuario


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ("hhid", "nome", "status", "criado_em")
    list_filter = ("status",)
    search_fields = ("hhid", "nome")


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_usuario", "username", "turma", "diretrix", "criado_em")
    list_filter = ("turma", "diretrix")
    search_fields = ("id_usuario", "username", "turma", "diretrix")


@admin.register(Controle)
class ControleAdmin(admin.ModelAdmin):
    list_display = (
        "data",
        "equipamento",
        "usuario",
        "entry_op",
        "in_lauch",
        "out_lauch",
        "out_op",
    )
    list_filter = ("data",)
    search_fields = (
        "equipamento__hhid",
        "equipamento__nome",
        "usuario__username",
    )
