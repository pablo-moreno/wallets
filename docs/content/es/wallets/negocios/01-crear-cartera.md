---
title: Creación de carteras virtuales
description: 'Documentación de la creación de la cartera de un negocio'
category: 'Negocios'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `negocio (1)`.

</alert>

<code-block label="Bash" active>

### Petición

```
POST /api/v1/wallets/business/wallet
```

### Respuesta

> Status: `201`

```
{
  "uuid": "bd67d9ee-3340-4cc0-9945-f92ec8b3878b",
  "balance": "0.00",
  "created_date": "2021-04-20T10:37:18.069060Z"
}
```


</code-block>
