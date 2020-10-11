# notis

## A few modules called by cron jobs to notify me via email:

* in the morning if the weather might get wild today
* in the morning if traffic is bad enough to take a different route to work
* in the evening if traffic is bad enough to take a different route home
* Friday afternoon with any new beers my friends really enjoyed in the last week
* any time Al adds a new recipe to his site

## Requirements:

### secrets.py
```
logpath = '/path/to/logs/'

noti_from = 'from-email-address'
noti_pass = 'from-email-password'
noti_default_to = 'to-email-address'

clima_key = 'climacell-api-key'

maps_key = 'google-directions-api-key'
point_a = 'Joliet+Correctional+Center'
point_b = '1060+W+Addison+St+Chicago+IL'

untappd_ID = 'untappd-client-ID'
untappd_secret = 'untappd-client-secret'
untappd_token = 'untappd-access-token'
bad_taste = ['Array of names', 'of friends to exclude', 'from beer updates']

```
