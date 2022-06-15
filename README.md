# PROYECTO DE PAGO DE SERVICIOS DE IMPUESTO


# Para instalar y dejar listo el proyecot para usar seguir estos pasos

# 1. Crear la carpeta project

# 2. ejecutar cd project

# 3. Crear el entorno virtual 
    python3 -m venv .env

# 4. Activar el entono virtual 
    source .env/bin/activate

# 5. instlar dependencias 
    pip install -r requirements.txt

# 6. Crear un adminsitrador django

    python manage.py createsuperuser

# 7. Hacer y Ejecutar migraciones

    python manage.py makemigrations 
    python manage.py migrate

# 8. Para levantar el proyecto ejecutar 
    python manage.py runserver


# Como usar la API 

### Para conocer la documentacion de la API y los endpoint 

### Debes acceder a la ruta https://127.0.0.1:8000


### Para obtener la consultas del punto número 3:

3. Debe permitir listar aquellas boletas impagas en forma total o filtradas por tipo de servicio, devolviendo la siguiente información:

Tipo de servicio (solo si se lista sin filtro)
Fecha de vencimiento
Importe del servicio
Código de barra

# Deberas pasar a la url estos dos parmetros:

# El primero es service_type -> las opciones son (water,light, gas, internet) 
# Ejemplo:
http://127.0.0.1:8000/api/tax/?service_type=gas

# El endpoint anterior te traera todos los pagos relacionado a la boleta (impuesto) que tenga ese servicio


# El segundo es payment_status -> las opciones son (paid, pending) 
# Ejemplo:
http://127.0.0.1:8000/api/tax/?payment_status=paid

# El endpoint anterior te traera todos los pagos relacionado a la boleta (impuesto) que tengas este estatus de pago


### Para obtener la consultas del punto número 4:

4. Debe permitir listar los pagos (transacciones) entre un período de fechas, acumulando por día, devolviendo la siguiente información:

Fecha de pago
Importe acumulado
Cantidad de transacciones en esa fecha

# Deberas pasar a la url estos dos parmetros:

# El primero es la fecha inicial -> el formato es dd//mm/yyyy 
# El segundo parametro es la fecha final -> el formato es dd//mm/yyyy 

# Ejemplo:
http://127.0.0.1:8000/api/tax_payment/?date_initial=10/05/2022&date_end=20/06/2022


# Esto te dara el pago diario de los impuestos indicando la cantidad acomulada ese dia y las canitdad de transacciones realizada ese mismo dia.

