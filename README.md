# Parachute Ending API

[Parachute Ending](https://www.youtube.com/watch?v=3JJsq0GbpPg) es una API creada en Python utilizando el framework Flask con el modulo Flask RESTful. Todas las peticioens son del tipo GET y por default corre en el puerto 5000.

### Requisitos

Parachute Ending toma sus datos desde una base de datos MariaDB/MySQL que debe contener las cotizaciones. 

## Endpoints
### Obtener Panel Líder

/api/arg/bluechips/{settelment}

### Obtener Bonos

/api/arg/bonds/{settelment}

### Obtener CEDEAR

/api/arg/cedear/{settelment}

### Obtener Opciones

/api/arg/options



### Obtener CCL

/api/arg/ccl

### Obtener Dolar MEP

/api/arg/mep

### Obtener Variables de BCRA

/api/arg/bcra

### Obtener valores de Lanzamiento Cubierto

/api/arg/options/lanzamiento/{ticker}
