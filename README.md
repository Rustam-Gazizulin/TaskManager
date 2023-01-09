# TaskManager

## Stack

* ![version](https://img.shields.io/badge/Python-v3.10.6-informational/?style=for-the-badge&logo=Python)
* ![version](https://img.shields.io/badge/Django-v4.1.3-informational/?style=for-the-badge&logo=Django)
* ![version](https://img.shields.io/badge/Postgresql-v15.0-informational/?style=for-the-badge&logo=Postgresql)

## Install

### Clone the repo

```sh
git clone https://github.com/Rustam-Gazizulin/TaskManager.git
```

### Install dependencies


pip install -r requirements.txt
```



### Start DB

```sh
docker-compose up --build -d
```

### Roll up migrations



```sh
python manage.py migrate
```

### Create superuser


```sh
python manage.py createsuperuser
```


### Run app


```sh
python manage.py runserver
```



