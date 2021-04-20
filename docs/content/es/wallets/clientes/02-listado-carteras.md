---
title: Listado de carteras virtuales
description: 'Documentación del listado de las carteras de clientes'
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>

### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/customers/wallets
```
</code-block>

### Respuesta

> Status: `200`

<code-block label="Bash" active>

```
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "eb5cf9e1-5c69-48ae-8469-610f95f74141",
      "balance": "0.00",
      "created_date": "2021-04-20T09:54:16.354975Z"
    },
    {
      "uuid": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565",
      "balance": "0.00",
      "created_date": "2021-04-20T09:56:34.583945Z"
    }
  ]
}
```
</code-block>

