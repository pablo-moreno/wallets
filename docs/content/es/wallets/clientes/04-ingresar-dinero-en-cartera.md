---
title: Ingreso de dinero en una cartera
description: 'Documentación del ingreso de dinero en una cartera de un cliente. '
category: 'Clientes'
---
<alert type="warning">

El usuario debe estar logueado y ser de tipo `cliente (1)`.

</alert>

### Petición

<code-block label="Bash" active>

```
(PUT | PATCH) /api/v1/wallets/customers/wallets/<uuid>/deposit
```
</code-block>

### Contenido

```
{
  "amount": "200.00",
  "description": "Ingreso 200€"
}
```

### Respuesta

> Status: `200`

<code-block label="Bash" active>

```
{
  "uuid": "eb5cf9e1-5c69-48ae-8469-610f95f74141",
  "balance": "200.00",
  "created_date": "2021-04-20T09:54:16.354975Z"
}
```
</code-block>
