![COLEGIO SAN MIGUEL](/static/img/logo.png)




SISTEMA DE ASISTENCIAS - COLEGIO SAN MIGUEL 

Este proyecto se basa en un sistema de Escolar el cual permite el control de asistencia de los estudiantes. 
El programa cuenta con funcionalidades tanto para el ambito administrativo del Estabecimiento (preceptores) y 
para los tutores de los Estudiantes. 


.Instalación/Ejecución 
Para ejecutar este sistema desde una terminal basta con acceder a la la direccion de proyecto y ejecutar el comando 
python app.py. 

Para windows Presionar las combinaciones: Tecla Windows + R  y digite la palabra " cmd " con este modo ya se tiene acceso a la aplicación. 

Para Linux: Ctrl+Alt+T y digite la palabra sudo su previamente antes de ejecutar el comando para abrir la app. 

.Uso 

El programa esta diseñado con una interfaz para familiarizar al usuario. En primera instancia el usuario se encontrará con la 
pestaña login la cual solicita correo,clave y rol que efectua en la institución. Cabe destacar que los roles en cuanto a permisos son los siguientes: 
-Preceptor: Rol de editor, permite registrar las asistencias y agregar datos la base de datos. 
-Padre: Rol lector, permite solo la búsqueda por dni para obtener las asistencias de su hijo. (No implementado hasta el momento)

.Caracteristicas 
1. Lenguaje de programación empleado: Python versión 3.11.3 
2. Tencnologias Usadas: Flask y Bootstrap 
3. Base de datos : SQLAlchemy
4. Funcionalidades Clave: Interfaz comoda y Sencilla con un diseño moderno empleando Bootstrap 
5. Objetivo: Control y Gestión de asistencias en un establecimiento educativo 
6. Ventajas: Interfaz comoda a la vista en su lado de cliente y lenguaje multiparadigma, sencillo y de tipado dinamico para su 
lado en el servidor. 

.A mejorar: 
a_ Agregar la función date.today().strftime(%d/%m/%Y)