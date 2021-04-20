---
title: Cobro de transacciones a clientes
description: 'Documentación del cobro de una transacción a un cliente'
category: 'Negocios'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `negocio (1)`.

</alert>

<code-block label="Bash" active>

### Petición

```
(PUT | PATCH) /api/v1/wallets/business/transactions/<uuid>/debit
```

### Respuesta

> Status: `200`

```
{
  "uuid": "b8a21a3d-fdce-4719-80df-7be61332fdd8",
  "amount": "15.00",
  "description": "Compra auriculares",
  "status": 2,
  "type": 2,
  "business": 4,
  "wallet": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565"
}
```


</code-block>
