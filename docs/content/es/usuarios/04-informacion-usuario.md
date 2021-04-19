---
title: Información de usuario
description: 'Documentación de la creación de usuarios'
category: 'Usuarios'
position: 4
userTypes:
  - Cliente - 1
  - Negocio - 2
---

<alert type="warning">

El usuario debe estar logueado.

</alert>

<code-block label="Bash" active>

### Petición

```
GET /api/v1/users/me
```

### Respuesta

> Status: `200`
```
{
  "username": "pablo",
  "email": "pablo@mail.com",
  "first_name": "Pablo",
  "last_name": "Moreno",
  "profile": {
    "type": 1
  }
}
```

</code-block>
