# Ejemplos de Mensajes Militares

## Mensaje entrante
 - Tipo: Mensaje Militar
 - Subtipo: Entrante
 - Descripción:
```
ORIGEN: Red Mat Pers
CLASIFICACION: publico
PRECEDENCIA: rutina
EVENTO: generado
MENSAJE: xxx
```

## Mensaje saliente
 - Tipo: Mensaje Militar
 - Subtipo: Saliente
 - Descripción:
 ```
DESTINO: Red Mat Pers
CLASIFICACION: publico
PRECEDENCIA: rutina
EVENTO: generado
MENSAJE: xxx
```

### Valores válidos

#### Origen / Destino:
- Red Cdo Op
- Red Mat Pers
- Red Cdo
- Red Op
- *Red Icia* (es la que tiene asignada el nodo, no usar)
#### Clasificacion
- Publico
- Reservado
- Confidencial
- Secreto
#### Precedencia
- Rutina
- Prioridad
- Inmediato
- Flash
#### Evento
- Generado
- Recibido_estafeta
- Entregado_estafeta
- Transmitido
#### Cifrado
(solo es necesario que exista la palabra dentro de la descripción).