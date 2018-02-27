# SMSeveryHour
Web Application is made to remind John his name as he is suffering Amnesia. The Web App will send a Text SMS every hour to remind him of his name (except the night hours considered as 10:00 PM to 7:00 AM). <br>
If the John wants to use this Web App, he should have his number verified on Twilio from the admin's account. Verification is done through an OTP. Contact the Admin <br> <br>
If the status of the message is Sent or Delivered after 1min of sending the message, the status is categorised as Delivered otherwise it is categorised as Failed or Undelivered and the message is sent again (Max 5 Times). Like if John's phone is switched off when the message was sent it will categorised as Sent message as John will recieve the message as he switches on his phone
After entering the number, John will be redirected to Logs Information of Delivered, Undelivered <br><br>
To get benefit of this application, one need to have Twilio account with Account Id, Auth key and a numbered verified by Twilio for SMS services. <br><br>
This application demonstates a simple Web Application based on [Django Framework](https://www.djangoproject.com/) of Python. The application uses python2.7  

## To run this app locally 
1. Install Python2.7 : https://www.python.org/downloads/
2. Install pip for python <br>
`sudo apt-get update` <br>
`sudo apt-get install python-pip`
3. Install Virtual Environment <br>
`sudo pip install virtualenv`
4. Make directory <br>
`mkdir SMSeveryHour` <br>
`cd SMSeveryHour`<br>
`virtualenv venv` <br>
5. Activate the Virtual Environment <br>
`source venv/bin/activate` <br>
6. Clone the GitHub repo <br>
`git clone https://github.com/karantatiwala/SMSeveryHour.git` <br>
`cd SMSeveryHour` <br>
7. Install the requirements for the application <br>
`pip install django==1.11` <br>
`pip install -r requirements.txt` <br>
8. Migrate the SQLite Database for the application <br>
`python manage.py makemigrations` <br>
`python manage.py migrate` <br>
9. Running the Server <br>
`python manage.py runserver` <br>
Open localhost on your browser  `127.0.0.1:8000` <br>
To stop SMS at any point, close your terminal by `Ctrl + c`
