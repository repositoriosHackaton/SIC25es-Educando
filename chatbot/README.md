<h1>Instrucciones Para levantar servidor de laravel</h1>
<h2>Instalación de Laravel</h2>

Carga de la base de datos, esencial para el funcionamiento de la aplicación.

<h4> Opcion 1</h4>
El nombre de la base de datos debe ser <strong> HipertensoBot </strong>

El archivo se encuentra en:
> hipertensobot.sql

<h4> Opcion 2</h4>

Ejecutar el comando <strong> php artisan migrate </strong>
Ejecutar el comando <strong> php artisan db:seed </strong>

> [!NOTE]  
> Para ejecutar el paso 2 debes haber creado la base de datos antes

Luego ejecutar:
> php artisan server


> [!IMPORTANT]  
> Realizo lo anterior laravel esta listo para recibir, enviar y mostrar mensajes


acceder a la siguiente direccion
> http://127.0.0.1:8000/
