---
title: Creación de carteras virtuales
description: 'Documentación de la creación de carteras de clientes'
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>

### Petición

<code-block label="Bash" active>

```
POST /api/v1/wallets/customers/wallets
```
</code-block>

### Respuesta

> Status: `201`

<code-block label="Bash" active>

```
{
  "uuid": "e58bc9dc-6b08-4a95-bdf3-c76ea24c8565",
  "balance": "0.00",
  "created_date": "2021-04-20T09:56:34.583945Z"
}
```
</code-block>
