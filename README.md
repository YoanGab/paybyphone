# Pay By Phone

## Automate your parking payments


### Why ? 
Today, people with a disability card needs to update their parking situation every 24 hours. <br>
For example, if you start your parking on Monday at 4 PM, you'll need to wait until Tuesday at 4 PM to be able to extend the parking time. The issue is that if you have a meeting at 4 PM, you'll take the risk to be fined because of it.


### Solution
Automate the parking situation everyday with a Cloud Function.


## App

### Cloud Provider: GCP

For this project, I've decided to use Google Cloud Platform infrastructures. <br>
I've used these products:
- Cloud Functions
- Cloud Scheduler
- Cloud PubSub
- Cloud Storage
- Secret Manager
- Cloud Source Repositories
- Sendgrid


### Installation

You need to enable all the API of products listed above.
- Cloud Source Repositories is where the code of the app is stored.
- Cloud Functions is the application, this is where we deploy the application, set environment variables… <br>
The environment variables needed are: 
  - SECRET_MANAGER_PROJECT_ID: The ID of the GCP Project
  - BUCKET_NAME: The name of Cloud Storage Bucket
  - LICENCE_PLATES_FILE: The name of the CSV file containing licence plates
- Cloud Scheduler with Cloud PubSub allows us to determine when to run the application. It has been chosen to execute the app from Monday to Saturday at 11 PM.
- Cloud Storage is used to store a CSV file containing licence plates of the disabled person.
- Secret Manager is used to store secret variables. <br>
The secret variables needed are:
  - paybyphone_parking_account: The id of the account where the cars will be stored.
  - paybyphone_phone_number: The phone number to login to the Paybyphone app.
  - paybyphone_password: The password to login to Paybyphone app.
  - sendgrid_apikey: The API KEY of Sendgrid to be able to send mail to know if the cars were parked successfully or not.
  - email_recipient: The email address to receive emails.
  - email_sender: The email address to send emails.
  - email_sender_name: The name displayed instead of the email address.
  - sentry_dsn: The DSN of the Sentry App to track errors.


### Usage

The application runs from Monday to Saturday at 11 PM. <br>
It will loop through each licence plate saved in csv file stored Cloud Storage and park it for 24 hours with zipcode 75100. This zipcode represents the disabled people in Paris, it allows them to park for free in Paris, and it lasts 24 hours. <br>
Once the application has tried to park every licence plate, it'll send a mail with the licence plates it succeeded to park and the ones he didn't.
If the licence plate isn't already stored in the application, it'll store it first and then park the licence plate. The user then only needs to add the licence plate to the CSV file.


