# Google Analytics Reporting API v4 with Python

All necessary functions to perform bulk calls to the Google Analytics Reporting API. 

Most examples online only provide the code for a single call that return a raw response. These functions can be used to make bulk calls with 'exponential backoff' and return a Pandas DataFrame.

This code expects a .json keyfile in the same directory and a secrets.py file. You can make your own secrets.py file following the example below and is purely meant as a way to keep my private login credentials seperate from files that will be shared.

## Example secrets.py file
```
obj = {
    'SCOPES' : ['https://www.googleapis.com/auth/analytics.readonly',
                'https://www.googleapis.com/auth/analytics.edit',
                'https://www.googleapis.com/auth/analytics.manage.users',
                'https://www.googleapis.com/auth/analytics.manage.users.readonly',
                'https://www.googleapis.com/auth/analytics.user.deletion'],
    'DISCOVERY_URI' : ('https://analyticsreporting.googleapis.com/$discovery/rest'),
    'KEY_FILE_LOCATION' : 'yourkeyfile.json',
    'SERVICE_ACCOUNT_EMAIL' : 'your_service_account_email.iam.gserviceaccount.com'
}

def secrets ():
    return obj
```

## JSON keyfile
The .json keyfile can be retrieved from console.cloud.google.com under Service Accounts. There are plenty tutorials to be found on how to do this. :)