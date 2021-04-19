---
title: Creación de usuario
description: 'Documentación de la creación de usuarios'
category: 'Usuarios'
position: 1
userTypes:
  - Cliente - 1
  - Negocio - 2
---

<alert>

Podemos crear dos tipos de usuario `Cliente` y `Negocio`.



</alert>

> Para ello, tendremos que especificar el tipo de cliente en la petición. 
> `1` para `Cliente` y `2` para `Negocio`



<code-block label="Bash" active>

### Petición

```
POST /api/v1/users/sign-up
```
### Contenido
```
{
  "username": "pablo",
  "email": "pablo@mail.com",
  "first_name": "Pablo",
  "last_name": "Moreno",
  "password": "my-password",
  "password2": "my-password",
  "type": 1
}
```

### Respuesta

> Status: `201`
```
{
  "email": "pablo@mail.com",
  "first_name": "Pablo",
  "last_name": "Moreno",
  "profile": {
    "type": 1
  }
}
```

</code-block>
