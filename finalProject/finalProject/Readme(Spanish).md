

Distinctiveness and Complexity

Este trabajo realizado simula una aplicacion de homebanking web.

El proyecto se hizo tratando de cumplir todos los requisitos que pedia el proyecto final. 

Distintividad y Complejidad
El proyecto de Gestión de Banca en Línea satisface los requisitos de distinción y complejidad por varias razones:

*Interfaz de Usuario Amigable:
Hemos desarrollado una interfaz de usuario intuitiva y fácil de usar que permite a los usuarios gestionar sus cuentas,
realizar transferencias y pagar servicios de manera eficiente.
Tambien se logro una interfaz correcta para dispositivos moviles, y ademas se agrego un teclado virtual para poder ser utilizado en 
caso de ser necesario para ello usamos css, bs y js.

*Seguridad: 
Implementamos medidas de seguridad robustas, como autenticación de usuarios, password encriptadas para garantizar que 
los datos de los usuarios estén protegidos. 
Se utilizo el sistema de recuperacion de password de django y se modifico la funcion PasswordResetCompleteView en la redireccion de pagina
Para las alerta via sms se utilizo una app de Twilio 8.5.0 en conjunto con django. Cave destacar que el codigo enviado no tiene los datos de mi cuenta personal de twilio por lo que si desean usar la funcion, deben ingresar los datos de una cuenta personal. La mia era gratuita por lo que solo mandaba mensajes al numero de telefono asociado a la misma. 


*Notificaciones en Tiempo Real:
Incorporamos un sistema de notificaciones en tiempo real que informa a los usuarios sobre transacciones, vencimientos de servicios y 
otros eventos importantes. 
Esto se logro utilizando background_task de django, se creo un archivo task.py donde se definio la funcion que realiza las notificaciones, cuando enviarlas y usando una terminal separada se ejecuta process_tasks para que las mismas se ejecuten en tiempo real.
En el caso de los vencimientos de los servicio se deben modificar manualmente las fechas, ya que cuando se crean los servicios se 
le da una fecha al dia 10 del proximo mes,simulando un servicio real. La funcion que llama a task es check_services_and_transactions 
que se encuentra en el archivo urls.py

*Gestión de Cuentas y Servicios:
Los superusuarios pueden crear y administrar múltiples cuentas y servicios, lo que aumenta la versatilidad y la utilidad de la aplicación.
El usuario comun debe generar el registro a travez del lin en la pag de inicio, debe crear usuario, ingresar nombre, apellido, dni, mail,
telefono y password 2 veces. Estos datos son obligatorios ya que todos se utilizan tanto para notificaciones como alertas. 
Cada usuario agrega un servicio previamente creado para simular empresas de luz, agua y gas a modo de ejemplo. 
El monto generado es aleatorio y la fecha de vencimiento se crea para el dia 10 del mes siguiente. La misma queda en un estado 
pendiente para uqe despues el usuario pueda pagarlo. Para pagarlo se corrobora que efectivaamente el usuario tenga el dinero suficiente en la cuenta. 
Cada servicio tiene una pagina donde se ve el detalle y se puede pagar. Una vez pago se puede generar un pdf como comprobante.
El usuario tambien puede modificar su email y su numero de telefono en caso de ser necesario. Esto se realiza a travez de una llamada fetch con js 
para que los datos se puedan reflejar en el momento.

*Información en Tiempo Real: 
Proporcionamos a los usuarios información actualizada sobre sus saldos y transacciones, lo que mejora la transparencia y la visibilidad de sus actividades financieras.

*Transferencias :
La aplicación permite a los usuarios realizar transferencias de dinero a otras cuentas y pagar servicios en línea, lo que agrega una capa
adicional de funcionalidad y comodidad. El sistema de transferencias tiene como mencinamos anteriormente un plus de seguridad con la verificacion via sms
y ademas el sistema de notificacion via email. El sistema via sms consiste en ingresar el monto a transferir y la cuenta destino.
Se utiliza JS para a una ventana modal en la que se coloco el boton para generar el codigo  numerico con una funcion  en el archivo views, 
alli se guarda el codigo en una variable global para luego poder ser recuperada por otra funcion que, atravez de un pedido fetch la compara
con el numero ingresado por el usuario. Si es correcto el boton de generar codigo desaparece y aparece en su lugar el boton transferir. Cada 
trasferencia tambien tiene una pagina donde se puede ver con mas detalle la informacion de la misma. Cave destacar que aqui tambien se agrego un boton 
de comprobante que genera un pdf. 

*Comprobantes:
Para la creacion edel comprobante  detallamos los pasos 
--Creación de la Plantilla PDF:
En primer lugar, se crea una plantilla PDF utilizando ReportLab. Esta plantilla incluye elementos estáticos como encabezados, 
logotipos de la entidad bancaria y campos dinámicos para los detalles de la transacción, como la fecha, el monto y 
los nombres de las partes involucradas.
--Generación de Contenido Dinámico:
Cuando un usuario solicita un voucher en PDF, se recopilan los detalles de la transacción desde la base de datos.
Esto incluye información como la fecha de la transacción, el monto, las cuentas involucradas y otros detalles relevantes.
--Combinación de Datos y Plantilla:
Utilizando ReportLab, los datos dinámicos se combinan con la plantilla PDF. Se establecen los valores de los campos dinámicos en la
plantilla para reflejar los detalles de la transacción específica.
--Generación del PDF Final: 
Una vez que se han combinado los datos y la plantilla, se genera el PDF final utilizando ReportLab.Esto crea un archivo PDF 
que contiene el voucher de la transacción.
--Descarga del PDF: 
El PDF recién generado se ofrece al usuario como una descarga. El usuario puede hacer clic en un enlace o un botón en la
interfaz web para descargar el voucher en PDF. Esto es para hacerlo un poco mas real.

*Notificaciones por Correo Electrónico:
--Recopilación de Datos:
Cuando ocurre un evento que requiere una notificación por correo electrónico (por ejemplo, un depósito exitoso),
se recopilan los datos relevantes sobre ese evento. Esto podría incluir detalles como la dirección de correo electrónico del 
destinatario, el tipo de evento y cualquier información adicional relacionada con el evento.
--Generación del Correo Electrónico:
Utilizando la biblioteca django.core.mail, se crea un correo electrónico que contiene el mensaje de notificación. 
Esto incluye el asunto del correo electrónico y el contenido del mensaje, que generalmente se genera dinámicamente para incluir 
información específica sobre el evento.
--Envío del Correo Electrónico: 
El correo electrónico se envía al destinatario utilizando la función send_mail() proporcionada por Django.
Esta función requiere el asunto, el contenido del mensaje, la dirección de correo electrónico del remitente y la 
dirección de correo electrónico del destinatario.
--Recepción de la Notificación:
El destinatario recibe la notificación en su buzón de correo electrónico y puede leer el mensaje para obtener información sobre el evento que ocurrió en la aplicación.
Además de las notificaciones en la aplicación, también enviamos notificaciones por correo electrónico a los usuarios para mantenerlos
informados sobre sus transacciones y cuentas.

*Otras Caracteristicas:
-- Cabe destacar en mi caso particular el uso de la variable global para utilizar la variable account bannk en todas las paginas 
sin la necesidad de pasar  el objeto account a la misma. Para ello creamos un archivo llamado global_variable.py donde definimos la 
funcion que da el nombre a la variable y nos devuelve la variable ya asignada para usarla en cualquier plantilla, ademas cambia segun el usuario. 
--Tambien se agregaron iconos con las redes sociales usando ionicons y tambien con un archivo js (index) que indica la ubicacion como de 
contacto. Tambien un icono en las pestañas del proyecto para hacerlo un poco mas agradable.
--Cabe destacar que se utilizo la funcion deposito como manera de ingresar dinero a modo sueldo y para probar
--El super Usuario tiene posibilidad de cambiar, agregar o modificar cualquier modelo o caracteristica
--Se agrego tambien una tarjeta de credito digital que es solo algo decorativo

-Technologies Used:
Django: Framework for building web applications.
Python: Programming language used for backend development.
HTML/CSS: Frontend technologies for designing the user interface.
JavaScript: Used for enhancing user interactions.
SQLite: The default database system provided by Django for data storage.
Twilio API: Integrated for sending real-time notifications via SMS.
ReportLab: Used to generate PDF vouchers for transactions.
Django's authentication system: Ensures secure user account management.

Ejecución de la Aplicación
Para ejecutar la aplicación, sigue estos pasos:
Clone este repositorio: git clone https://github.com/Dariojpenna/HarvardCSS.git
Navega al directorio del proyecto: cd HarvardCSS/finalProject
Instala las dependencias: pip install -r requirements.txt
Aplica las migraciones: python manage.py migrate
Crea un superusuario: python manage.py createsuperuser
Inicia el servidor: python manage.py runserver

-Documentación Completa:
Este README.md proporciona una documentación completa del proyecto, incluyendo detalles sobre cómo ejecutar la aplicación, qué archivos se crearon y más.

La intension del proyecto es hacerlo lo mas real posible y para ello tuve que indagar bastante en el tema de seguridad, claves,contraseñas, 
notificaciones y alertas de Django. La verdad aprendi mucho por lo cual quiero agradecerle a la fundacion EDX y Hardvard por la oportunidad
