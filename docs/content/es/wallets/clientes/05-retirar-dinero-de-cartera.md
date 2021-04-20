---
title: Retirar dinero de una cartera
description: 'Documentación de la retirada de dinero en una cartera de un cliente. '
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

<code-block label="Bash" active>

```
{
  "amount": "-200.00",
  "description": "Retirada 200€"
}
```
</code-block>

### Respuesta

> `200 OK`

### Errores

> `409 Conflict`: Fondos insuficientes

<code-block label="Bash" active>

```
{
  "detail": "Balance can't be negative"
}
```

</code-block>
