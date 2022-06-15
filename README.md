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
