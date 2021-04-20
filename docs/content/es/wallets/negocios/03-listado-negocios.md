---
title: Listado de negocios
description: 'Documentación del listado de negocios'
category: 'Negocios'
---
<alert type="warning">

El usuario debe estar logueado.

</alert>


### Petición

<code-block label="Bash" active>

```
GET /api/v1/wallets/business/
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
      "id": 1,
      "name": "Aplazame"
    }
  ]
}
```

</code-block>
