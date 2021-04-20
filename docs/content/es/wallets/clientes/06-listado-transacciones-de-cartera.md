---
title: Listado de transacciones de una cartera
description: 'Documentación del listado de transacciones de una cartera de un cliente. '
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>


### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/customers/wallets/<uuid>/transactions
```

</code-block>

### Respuesta

> `200 OK`

<code-block label="Bash" active>

```
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "0bda78a8-b8f6-4542-beba-6a7c4effe81f",
      "amount": "200.00",
      "description": "Ingreso 200€",
      "status": 1,
      "type": 1,
      "business": null,
      "wallet": "eb5cf9e1-5c69-48ae-8469-610f95f74141"
    },
    {
      "uuid": "bda4bd9b-1de5-4951-8a02-720dda8111e0",
      "amount": "20.00",
      "description": "Ingreso 20€",
      "status": 1,
      "type": 1,
      "business": null,
      "wallet": "eb5cf9e1-5c69-48ae-8469-610f95f74141"
    },
    {
      "uuid": "115f465d-a4d3-40cc-8357-524676a5ea01",
      "amount": "-20.00",
      "description": "Retirada 20€",
      "status": 1,
      "type": 1,
      "business": null,
      "wallet": "eb5cf9e1-5c69-48ae-8469-610f95f74141"
    }
  ]
}
```
</code-block>
