# notis

## A few modules called by cron jobs to provide the following functionality:

* Notify me in the morning if traffic is bad on my usual route to work
* Notify me in the morning if the weather might get wild today
* Notify me in the evening if traffic is bad on my usual route home
* Notify me Friday afternoon with any new beers my friends really enjoyed in the last week

## Requirements:

### secrets.py
```
noti_from = 'from-email-address'
noti_pass = 'from-email-password'
noti_to = 'to-email-address'

dark_key = 'dark-sky-api-key'

maps_key = 'google-directions-api-key'
point_a = 'Joliet+Correctional+Center'
point_b = '1060+W+Addison+St+Chicago+IL'

untappd_ID = 'untappd-client-ID'
untappd_secret = 'untappd-client-secret'
untappd_token = 'untappd-access-token'

logfile = ''
```
