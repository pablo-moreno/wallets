---
title: Cierre de sesión
description: 'Documentación del cierre de sesión de usuarios'
category: 'Usuarios'
---

<code-block label="Bash" active>

### Petición

```
POST /api/v1/users/logout
```
### Contenido
```
{
  "username": "pablo",
  "password": "my-password"
}
```

### Respuesta

> Status: `204`

</code-block>
