# notis

## A few scripts that work together to provide the following functionality:

* Email me in the morning if traffic is bad on my usual route to work
* Email me in the morning if the weather might get wild today

## Requirements:

### secrets.py
```
noti_from = 'from-email-address'
noti_pass = 'from-email-password'
noti_to = 'to-email-address'

dark_key = 'dark-sky-api-key'

maps_key = 'google-directions-api-key'
point_a = 'origin=123+Main+Street+Chicago+IL'
point_a = 'destination=Empire+State+Building'

logfile = '/var/log/app'
```
