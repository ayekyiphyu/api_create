### API作成するために　
Django を使って API を作成するためのプロジェクトを立ち上げます。
※私は Windows 環境なので、手順も Windows に合わせて記載しています。



```bash
mkdir project_name
cd project_name
pip install django djangorestframework uvicorn
python manage.py runserver
```

```bash

uvicorn config.asgi:application --reload

```

### settings.py
```bash
'rest_framework',
'myapi',
```


```bash
python manage.py migrate
```



```bash
config > urls.py

path('api/', include('myapi.urls'))
```

※ from django.urls.import path, include


``` 
migration
python manage.py makemigrations myapi
python manage.py migrate

```

## create sqlite 3
```
sudo apt install sqlite3
sqlite3 db.sqlite3
.tables (check myapi_table)
```



