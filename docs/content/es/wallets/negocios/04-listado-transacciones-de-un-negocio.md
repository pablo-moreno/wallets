---
title: Listado de transacciones de un negocio
description: 'Documentación del listado de transacciones en un negocio. '
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `negocio (2)`.

</alert>

### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/business/transactions/
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
      "uuid": "4267a27a-d97a-4444-b55a-181dcaa993ba",
      "amount": "15.00",
      "description": "Compra auriculares",
      "status": 1,
      "type": 2,
      "business": 4,
      "wallet": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565"
    }
  ]
}
```
</code-block>
