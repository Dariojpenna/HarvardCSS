istinctiveness and Complexity

This work simulates a web homebanking application.

The project was made trying to meet all the requirements that pediatrics the final project.

Distinctiveness and Complexity The Online Banking Management project meets the requirements of distinction and complexity for several reasons:

*User Friendly Interface: We have developed an intuitive and user-friendly user interface that allows users to manage their accounts, make transfers and pay for services efficiently. It also achieved a correct interface for mobile devices, and also added a virtual keyboard to be used if necessary for this we use css, bs and js.

*Security: We implement robust security measures, such as user authentication, encrypted passwords to ensure that user data is protected. The django password recovery system was used and the PasswordResetCompleteView function was modified in the page redirection For alerts via sms an app of Twilio 8.5.0 was used in conjunction with django. Cave note that the code sent does not have the data of my personal twilio account so if you want to use the function, you must enter the data of a personal account. Mine was free so I only sent messages to the phone number associated with it.

*Real Time Notifications:
We incorporate a real-time notification system that informs users about transactions, service expirations and 
other important events. 
This was achieved using django background_task, a task.py file was created where the function that makes the notifications was defined,
when sending them and using a separate terminal, process_tasks are executed so that they run in real time.
In the case of service expirations, the dates must be manually modified, since when the services are created 
gives you a date on the 10th of the next month,simulating a real service. The function calling task is check_services_and_transactions 
which is in the urls.py file

*Management of Accounts and Services:
Superusers can create and manage multiple accounts and services, increasing the versatility and utility of the application.
The common user must generate the log through the lin in the home page, must create user, enter first name, last name, dni, mail,
phone and password 2 times. These data are mandatory as they are all used for both notifications and alerts. 
Each user adds a service previously created to simulate electricity, water and gas companies as an example. 
The amount generated is random and the due date is created for the 10th day of the following month. It remains in a state 
pending for uqe after the user can pay it. To pay it, it is confirmed that the user actually has enough money in the account. 
Each service has a page where you can see the detail and you can pay. Once paid a pdf can be generated as proof.
The user can also modify their email and phone number if necessary. This is done through a fetch call with js 
so that the data can be reflected at the time.

*Real Time Information: 
We provide users with up-to-date information about their balances and transactions, improving transparency and visibility of their financial activities.

*Transfers :
The app allows users to make money transfers to other accounts and pay online services, which adds a layer
additional functionality and comfort. The transfer system has as mentioned above a security plus with the verification via sms
and also the notification system via email. The system via sms consists of entering the amount to transfer and the destination account.
JS is used for a modal window in which the button was placed to generate the numeric code with a function in the views file, 
alli the code is saved in a global variable to then be able to be recovered by another function that, through a fetch request compares it
with the number entered by the user. If correct, the button to generate code disappears and the transfer button appears instead. Each 
transfer also has a page where you can see in more detail the information of the same. Cave highlight that here also added a boton 
of proof that generates a pdf. 

*Supporting documents:
For the creation of the proof we detail the steps 
-Creation of the PDF Template:
First, a PDF template is created using ReportLab. This template includes static elements such as headers, 
bank logos and dynamic fields for transaction details such as date, amount and 
the names of the parties involved.
-Dynamic Content Generation:
When a user requests a PDF voucher, transaction details are collected from the database.
This includes information such as transaction date, amount, accounts involved and other relevant details.
-Combination of Data and Template:
Using ReportLab, dynamic data is combined with the PDF template. Dynamic field values are set in the
template to reflect the details of the specific transaction.
-Generation of the final PDF: 
Once the data and template have been combined, the final PDF is generated using ReportLab.This creates a PDF file 
containing the transaction voucher.
-Download of the PDF: 
The newly generated PDF is offered to the user as a download. The user can click a link or button on the
web interface to download the voucher in PDF. This is to make it a little more real.

*Notifications by Email:
-Collection of data:
When an event occurs that requires email notification (for example, a successful deposit),
relevant data about that event is collected. This could include details such as the email address of the 
recipient, the type of event and any additional information related to the event.
-Generation of E-mail:
Using the django.core.mail library, an email containing the notification message is created. 
This includes email subject and message content, which is usually generated dynamically to include 
specific information about the event.
-Sending of the E-mail: 
The email is sent to the recipient using the send_mail() function provided by Django.
This function requires the subject, message content, sender email address and 
email address of the recipient.
-Receipt of the Notification:
The recipient receives the notification in their email box and can read the message to get information about the event that occurred in the application.
In addition to in-app notifications, we also send email notifications to users to keep them
informed about their transactions and accounts.

*Other Features:
-- It is worth highlighting in my particular case the use of the global variable to use the bannk account variable on all pages 
without the need to pass the account object to it. For this we create a file called global_variable.py where we define the 
function that gives the name to the variable and returns the variable already assigned to use it in any template, also changes according to the user. 
-Icons were also added with social networks using ionicons and also with a js file (index) indicating the location as of 
contact. Also an icon on the project tabs to make it a little more enjoyable.
-It should be noted that the deposit function was used as a way of entering money as a salary and to prove
-The super user has the possibility to change, add or modify any model or feature
-A digital credit card was also added which is just something decorative


-Technologies Used:
Django: Framework for building web applications.
Python: Programming language used for backend development.
HTML/CSS: Frontend technologies for designing the user interface.
JavaScript: Used for enhancing user interactions.
SQLite: The default database system provided by Django for data storage.
Twilio API: Integrated for sending real-time notifications via SMS.
ReportLab: Used to generate PDF vouchers for transactions.
Django’s authentication system: Ensures secure user account management.

Implementation
To run the application, follow these steps:
Clone this repository: git clone https://github.com/Dariojpenna/HarvardCSS.git
Navigate to the project directory: cd HarvardCSS/finalProject
Installs dependencies: pip install -r requirements.txt
Apply migrations: python manage.py migrate
Create a superuser: python manage.py createsuperuser
Start server: python manage.py runserver

-Complete documentation:
This README.md provides complete project documentation, including details on how to run the application, what files were created and more.

The intension of the project is to make it as real as possible and for this I had to do a lot of research on the issue of security, keys, notifications and alerts from Django. The truth learned a lot so I want to thank the EDX and Hardvard foundation for the opportunity

