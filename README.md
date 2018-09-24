# notis

## A few scripts that work together with cron jobs to provide the following functionality:

* Email me in the morning if traffic is bad on my usual route to work
* Email me in the morning if the weather might get wild today
* Email me Friday afternoon with any new beers my friends really enjoy

## Requirements:

### secrets.py
```
noti_from = 'from-email-address'
noti_pass = 'from-email-password'
noti_to = 'to-email-address'

dark_key = 'dark-sky-api-key'

maps_key = 'google-directions-api-key'
point_a = 'origin=Joliet+Correctional+Center'
point_b = 'destination=1060+W+Addison+St+Chicago+IL'

untappd_ID = 'untappd-client-ID'
untappd_secret = 'untappd-client-secret'
untappd_token = 'untappd-access-token'

logfile = ''
```
