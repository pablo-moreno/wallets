---
title: Detalle de cartera virtual
description: 'Documentación del detalle de la cartera de un negocio'
category: 'Negocios'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `negocio (1)`.

</alert>


### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/business/wallet
```

</code-block>


### Respuesta

> Status: `200`

<code-block label="Bash" active>

```
{
  "uuid": "bd67d9ee-3340-4cc0-9945-f92ec8b3878b",
  "balance": "0.00",
  "created_date": "2021-04-20T10:37:18.069060Z"
}
```

</code-block>
