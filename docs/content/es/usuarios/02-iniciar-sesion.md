---
title: Inicio de sesión
description: 'Documentación del inicio de sesión de usuarios'
category: 'Usuarios'
---

<code-block label="Bash" active>

### Petición

```
POST /api/v1/users/login
```
### Contenido
```
{
  "username": "pablo",
  "password": "my-password"
}
```

### Respuesta

> Status: `200`
```
{
  "token": "<jwt-token>",
  "user": {
    "email": "pablo@mail.com",
    "first_name": "",
    "last_name": "",
    "profile": {
      "type": 1
    }
  }
}
```

</code-block>
