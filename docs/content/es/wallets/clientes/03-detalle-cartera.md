---
title: Detalle de cartera virtual
description: 'Documentación del detalle de una cartera de un cliente. '
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>

### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/customers/wallets/<uuid>
```
</code-block>

### Respuesta

> Status: `200`

<code-block label="Bash" active>

```
{
  "uuid": "eb5cf9e1-5c69-48ae-8469-610f95f74141",
  "balance": "0.00",
  "created_date": "2021-04-20T09:54:16.354975Z"
}
```

</code-block>
