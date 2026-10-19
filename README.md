# SAURON · Sistema de Inventário

Sistema web para controlar a **entrada e saída de equipamentos** por usuário, com registro de horário em cada etapa do processo. As etapas são sequenciais e validadas no servidor — a próxima só é liberada depois que a anterior for concluída.

Projeto desenvolvido em Django como estudo de modelagem de dados, regras de negócio e interface.

## Funcionalidades

- **Cadastro de equipamentos** com `HHID` único, nome e status (disponível, em uso, manutenção).
- **Cadastro de usuários** com ID, username, turma e diretrix.
- **Consulta com busca instantânea** nas tabelas de equipamentos e usuários (ignora acentos e maiúsculas).
- **Controle diário** com as quatro etapas do processo:

  | Etapa | Descrição |
  | --- | --- |
  | `ENTRY-OP` | Entrada do equipamento no expediente |
  | `IN-LAUCH` | Início do uso (lançamento) |
  | `OUT-LAUCH` | Fim do uso |
  | `OUT-OP` | Saída do equipamento, que volta ao status *disponível* |

- **Ordem obrigatória das etapas** validada no backend (`Controle.pode_registrar`), não apenas na interface.
- **Timestamp automático** em cada etapa concluída.
- **Um registro por equipamento por dia**, garantido por `UniqueConstraint` no banco.
- **Preenchimento automático** do equipamento a partir do HHID, via endpoint JSON.
- **Django Admin** para edição e exclusão de registros.

## Stack

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.14 |
| Framework | Django 6.1 (ORM, templates, admin, messages) |
| Banco | SQLite |
| Front-end | HTML, CSS autoral e JavaScript puro |

Sem frameworks de front-end: abas acessíveis, filtro de tabelas e busca de HHID são feitos com JavaScript nativo.

## Como rodar

Pré-requisitos: Python 3.10+ e Git.

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd "Project H2.0"

# 2. Criar e ativar o ambiente virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar as tabelas no banco
python manage.py migrate

# 5. Criar um usuário para acessar o admin (opcional)
python manage.py createsuperuser

# 6. Subir o servidor
python manage.py runserver
```

Acesse em <http://127.0.0.1:8000/>.

> O arquivo `db.sqlite3` não é versionado: cada ambiente cria o próprio banco com `migrate`.

## Rotas

| Rota | Descrição |
| --- | --- |
| `/` | Redireciona para o cadastro |
| `/cadastro/` | Cadastro de equipamentos e usuários + consulta |
| `/controle/` | Controle do expediente do dia |
| `/controle/equipamento/<hhid>/` | Endpoint JSON com os dados do equipamento |
| `/controle/<id>/etapa/` | Registra a conclusão de uma etapa (POST) |
| `/admin/` | Administração do Django |

## Modelo de dados

```
Equipamento (hhid, nome, status, criado_em)
      │
      │ 1:N  (PROTECT)
      ▼
Controle (data, entry_op, in_lauch, out_lauch, out_op, criado_em)
      ▲
      │ N:1  (PROTECT)
      │
Usuario (id_usuario, username, turma, diretrix, criado_em)
```

- `Equipamento.hhid` é único e normalizado para maiúsculas.
- `Usuario.username` é único e normalizado para minúsculas.
- A combinação `(equipamento, data)` é única: um equipamento entra no máximo uma vez por dia.
- `on_delete=PROTECT` preserva o histórico: não é possível apagar um equipamento ou usuário que já tenha controle.

## Estrutura

```
Project H2.0/
├── config/                  # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── inventario/              # Aplicação principal
│   ├── migrations/
│   ├── static/inventario/   # CSS e JavaScript
│   ├── templates/inventario/  # base, cadastro e controle
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── requirements.txt
```

## Próximos passos

- [ ] Autenticação de usuários e permissões por perfil.
- [ ] Edição e exclusão de registros na própria interface (hoje via Django Admin).
- [ ] Relatórios e exportação do controle diário (CSV/Excel).
- [ ] Integração com o SAP como fonte dos dados de inventário.
- [ ] Testes automatizados das regras de negócio.
- [ ] Migrar para PostgreSQL em produção e adicionar deploy.
