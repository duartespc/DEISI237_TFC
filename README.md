# DEISI 237 - Plataforma de gestão financeira e controlo de custos empresariais

## Vídeo de apresentação

O vídeo pode ser visto em: https://youtu.be/q8RCXLw5spc

## Guia de Instalação
* Instalar python3
* Instalar python3-pip
* Instalar pipenv (ou criar virtual environment usando IDE)

Em seguida na pasta do projeto corra os comandos abaixo
```
python -m venv Code\Python\Project1\venv
pipenv shell
pip install -r requirements.txt
python manage.py makemigrations
python  manage.py migrate
```
Crie uma conta de administrador
```
python manage.py createsuperuser
```
Escolha umas credenciais à sua escolha e por fim, lance o servidor:
```
python manage.py runserver
```
