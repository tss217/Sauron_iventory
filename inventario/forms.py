from django import forms

from .models import Equipamento, Usuario


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ["hhid", "nome", "status"]

        widgets = {
            "hhid": forms.TextInput(
                attrs={
                    "placeholder": "H100",
                    "maxlength": 10,
                    "pattern": "[A-Za-z0-9-]{3,10}",
                    "autocomplete": "off",
                    "spellcheck": "false",
                    "aria-describedby": "eq-hhid-hint",
                }
            ),
            "nome": forms.TextInput(
                attrs={
                    "placeholder": "Hand Helt",
                    "maxlength": 60,
                    "autocomplete": "off",
                }
            ),
        }

        error_messages = {
            "hhid": {
                "unique": "Já existe um equipamento com este HHID.",
                "required": "Informe o HHID.",
            },
            "nome": {
                "required": "Informe o nome do equipamento.",
            },
        }

    def clean_hhid(self):
        # Normaliza antes da validação de duplicidade.
        return self.cleaned_data["hhid"].strip().upper()

    def clean_nome(self):
        return self.cleaned_data["nome"].strip()


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["id_usuario", "username", "turma", "diretrix"]

        widgets = {
            "id_usuario": forms.TextInput(
                attrs={
                    "placeholder": "2024001",
                    "maxlength": 20,
                    "autocomplete": "off",
                    "spellcheck": "false",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "placeholder": "thiago",
                    "maxlength": 40,
                    "pattern": "[A-Za-z0-9._-]{3,40}",
                    "autocomplete": "off",
                    "spellcheck": "false",
                }
            ),
            "turma": forms.TextInput(
                attrs={
                    "placeholder": "C",
                    "maxlength": 1,
                    "autocomplete": "off",
                }
            ),
            "diretrix": forms.TextInput(
                attrs={
                    "placeholder": "Rep1",
                    "maxlength": 40,
                    "autocomplete": "off",
                }
            ),
        }

        error_messages = {
            "id_usuario": {
                "unique": "Já existe um usuário com este ID.",
                "required": "Informe o ID.",
            },
            "username": {
                "unique": "Este username já está em uso.",
                "required": "Informe o username.",
            },
            "turma": {
                "required": "Informe a turma.",
            },
            "diretrix": {
                "required": "Informe a diretrix.",
            },
        }

    def clean_id_usuario(self):
        return self.cleaned_data["id_usuario"].strip()

    def clean_username(self):
        # Normaliza antes da validação de duplicidade.
        return self.cleaned_data["username"].strip().lower()

    def clean_turma(self):
        return self.cleaned_data["turma"].strip().upper()

    def clean_diretrix(self):
        return self.cleaned_data["diretrix"].strip()