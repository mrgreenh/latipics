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
python latipics.py -d 2013082720 -v VENUE_ID -dr 6 -inst INSTAGRAM_CLIENT_ID -fsid FOURSQUARE_CLIENT_ID -fssec FOURSQUARE_CLIENT_SECRET
```

If you need some more options, ask for help and see what's available:
```
python latipics.py -h
```

License
-------
(C) Copyright 2013 Carlo Andrea Conte <carloandreaconte@icloud.com> 
MIT license

Greetings
---------
Have fun and send me a message to let me know how you use this work!
