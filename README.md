[![Build Status](https://travis-ci.org/Pbezerra-dev/pbezerra_blog.svg?branch=master)](https://travis-ci.org/Pbezerra-dev/pbezerra_blog)
[![Updates](https://pyup.io/repos/github/Pbezerra-dev/Mtranscoder/shield.svg)](https://pyup.io/repos/github/Pbezerra-dev/Mtranscoder/)
[![Python 3](https://pyup.io/repos/github/Pbezerra-dev/Mtranscoder/python-3-shield.svg)](https://pyup.io/repos/github/Pbezerra-dev/Mtranscoder/)


#  Pbezerra Blog - __Blog Pessoal__

>## Como contribuir:

### clonando o projeto:
```
git clone git remote add origin https://github.com/Pbezerra-dev/pbezerra_blog.git
cd pbezerra_blog
```
### criando o ambiente python e instalando as dependências:

- [Documentação Poetry](https://python-poetry.org/docs/)
```
poetry use env 3.7
poetry shell
poetry install
python contrib/env_gen.py
```
> Atenção: configurar as variaveis de ambiente em .env

### rodando as migrações e startando o projeto
```
python manage.py migrate
python manage.py loaddata data.json
python manage.py createsuperuser
python manage.py runserver
```
