# DEISI 237 - Plataforma de gestão financeira e controlo de custos empresariais

## Vídeo de apresentação

O vídeo pode ser visto em: https://youtu.be/es9JGxIyAcM

## Guia de Instalação
* Instalar python3
* Instalar python3-pip
* Instalar pipenv (ou criar virtual environment usando IDE)

* Se tiver problemas com a falta do módulo pkg_resources: usar o comando "pip install --upgrade setuptools"

Em seguida na pasta do projeto corra os comandos abaixo
```
python -m venv /C:/.../new_env_dir
& /C:/.../new_env_dir/Scripts/Activate.ps1
python -m pip install --upgrade pip
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
