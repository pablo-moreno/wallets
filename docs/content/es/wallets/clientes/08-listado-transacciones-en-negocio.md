---
title: Listado de transacciones en negocio
description: 'Documentación del listado de transacciones en un negocio. '
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>

### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/business/<business_id>/customers/transactions/
```
</code-block>

### Respuesta

> Status: `200`

<code-block label="Bash" active>

```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "7d47cd18-92c0-4c13-a068-6d380c79683c",
      "amount": "15.00",
      "description": "Compra auriculares",
      "status": 2,
      "type": 2,
      "business": 4,
      "wallet": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565"
    }
  ]
}
```
</code-block>
