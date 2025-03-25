<h1>Instrucciones Para levantar servidor de laravel</h1>

<p>
Laravel se utilizó en este proyecto debido a su robustez y facilidad para manejar la lógica del backend, la autenticación de usuario y la interacción con la base de datos MySQL.  
Además, Laravel permite estructurar la API de manera clara y segura, facilitando la comunicación con el frontend en React y con el microservicio en FastAPI.  
Gracias a su sistema de rutas, controladores y Eloquent ORM, se optimizó el manejo de conversaciones y almacenamiento de mensajes, garantizando un desarrollo eficiente y escalable.  
</p>


<h2>Instalación de Laravel</h2>

Carga de la base de datos, esencial para el funcionamiento de la aplicación.

<h4> Opcion 1</h4>
El nombre de la base de datos debe ser <strong> HipertensoBot </strong>

El archivo se encuentra en:
> hipertensobot.sql

<h4> Opcion 2</h4>

Ejecutar el comando <strong> php artisan migrate </strong>

> [!NOTE]  
> Para ejecutar el paso 2 debes haber creado la base de datos antes

Luego ejecutar:
> php artisan server


> [!IMPORTANT]  
> Realizo lo anterior laravel esta listo para recibir, enviar y mostrar mensajes


>instrucciones adicionales
> php artisan storage:link
