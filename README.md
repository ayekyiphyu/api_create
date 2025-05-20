
### プロジェクト概要
このプロジェクトはMemoのために使うapiです。
初めてdjangoを勉強しがなら開発しているプロジェクトです。
勉強のために参照したら幸いです。

# User API Project

This repository is for building a **User API** using **Python**, **Django**, and **Django REST Framework**.  
This project will be used as the backend for a user NoteMemo application built with **React** and **Next.js**.

---

## 🧭 Project Overview

- The project provides an API for user registration and login.
- If a user does not exist, a new user can register through the API.
- After login, users will be redirected to their Dashboard (in the frontend app).
- This repository is **only for the backend API** development.

---

## 🛠 Technologies Used

- Python
- Django
- Django REST Framework
- Uvicorn (ASGI server for local testing)
- SQLite3 (default development DB)

---

## 🚀 Getting Started (Windows Environment)

### 1. Set up your project

```bash
mkdir project_name
cd project_name
pip install django djangorestframework uvicorn
django-admin startproject config .


※：FEについは【my-project-structure】を参照してお願いします。
※：later I will be change my project name.

