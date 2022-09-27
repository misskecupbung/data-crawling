## Database config
pada .env file penyesuaian database host, password, user

untuk memigrate settingan database

```
flask db migrate
flask db upgrade
```

## Menjalankan api
```
flask run
```

## Dokumentasi API

### Admin
- POST /admin

  Registrasi user admin. Memerlukan inputan form "name", "email", dan "password".

### Link
- POST /link

  Mendaftarkan link hasil visualisasi data. Memerlukan inputan form "place", "category", dan "link".

### User
- GET /user

  Mendapatkan daftar user maupun admin.

- POST /user

  Mendaftarkan user. Memerlukan inputan form "name", "email", dan "password".

### Item

### Login