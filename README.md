Latipics
========
What's this thing
-----------------
You can use latipics to gather pictures from Foursquare and Instagram taken in a particular place during a specified period of time.

Usage
-----
Specify a Foursquare venue id, a date and hour, a timerange: latipics will ask foursquare for all pictures taken in that place, then it will ask that place's geocoords and will use them to query Instagram. Both queries are filtered so that only pictures published in the requested period of time are returned.
If you run the script from shell, it will print a webpage with the results.
The start-date is pecified as YYYYMMDDHH, the duration is expressed in hours.

You can quickly use it by navigating to the script's folder and typing:
```
python latipics.py -v VENUE_ID -dr 6 -inst INSTAGRAM_CLIENT_ID -fsid FOURSQUARE_CLIENT_ID -fssec FOURSQUARE_CLIENT_SECRET
```
Then go take a look to the resulting latipics_results.html page. You should see there the pictures from that venue taken during the last week. (Instagram limits this, but you can enter bigger timeranges and that will work with foursquare up to 200 pics)

If you need some more options, ask for help and see what's available:
```
python latipics.py -h
```

Troubleshooting
---------------
It's something really quickly put together, if it raises some keyError double check the venue_id and your API credentials.
If the results are empty, that is very likely to happen with short periods of time (e.g. a 5 hours small event). Try to specify a date from 2 months ago and enter a 2000 hours duration and see what happens.

License
-------
(C) Copyright 2013 Carlo Andrea Conte <carloandreaconte@icloud.com> 
MIT license

Greetings
---------
Have fun and send me a message to let me know how you use this work!
