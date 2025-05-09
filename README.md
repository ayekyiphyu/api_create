### API作成するために　
Django を使って API を作成するためのプロジェクトを立ち上げます。
※私は Windows 環境なので、手順も Windows に合わせて記載しています。

```bash
django-admin startproject myproject_name
cd myproject_name
python manage.py startapp api
```

- api/view.pyを作成委

- api/urls.pyを作成委

- myproject_name/url.py

Install REST Framework and cors Header

```bash
pip install djangorestframework django-cors-headers
```

- setting.py を作成委


Run API Django

```bash
python manage.py runserver
```



