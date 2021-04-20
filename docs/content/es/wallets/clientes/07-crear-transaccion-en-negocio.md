---
title: Crear transacción en negocio
description: 'Documentación de la creación de una transacción en un negocio. '
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>

### Petición

<code-block label="Bash" active>

```
POST /api/v1/wallets/business/<business_id>/customers/transactions/
```
</code-block>

### Contenido

```
{
	"amount": "15.00",
	"description": "Compra auriculares",
	"wallet": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565"
}
```

### Respuesta

> Status: `201`

<alert type="info">

Las transacciones en con `status=1` están pendientes de pago. Las que tienen `status=2` están pagadas. 
Si tienen `status=3`, han sido rechazadas

</alert>

<alert type="info">

Las transacciones con `type=1` son depósitos. Las que tienen `type=2` son cobros.

</alert>


<code-block label="Bash" active>

```
{
  "uuid": "b8a21a3d-fdce-4719-80df-7be61332fdd8",
  "amount": "15.00",
  "description": "Compra auriculares",
  "status": 1,
  "type": 2,
  "business": "4",
  "wallet": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565"
}
```
</code-block>
