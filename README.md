# Parachute Ending API

[Parachute Ending](https://www.youtube.com/watch?v=3JJsq0GbpPg) es una API creada en Python utilizando el framework Flask con el modulo Flask RESTful. Todas las peticioens son del tipo GET y por default corre en el puerto 5000.

### Requisitos

Parachute Ending toma sus datos desde una base de datos MariaDB/MySQL que debe contener las cotizaciones. 

## Endpoints
### Obtener Panel Líder

/api/arg/bluechips/{settelment}

### Obtener Bonos

/api/arg/bonds/{settelment}

### Obtener Panel General

/api/arg/galpones/{settelment}

### Obtener CEDEAR

/api/arg/cedear/{settelment}

### Obtener Opciones

/api/arg/options

### Obtener Indices

/api/arg/indices

### Obtener CCL

/api/arg/cedear-ccl

### Obtener Stocks USA

/api/us/stocks
