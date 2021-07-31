# Every Stop

This is a Twitter bot which tweets a Google Street View image of [every single bus stop for Hong Kong](https://twitter.com/everystophk).  But it could tweet any Open Street Map node that you provide it.

## Data

You'll need to know where the bus stops are in order to populate the database.  Examples include Open Street Map or GTFS data feeds.

### Open Street Map

For areas where Open Street Map has good coverage, [Overpass Turbo](http://overpass-turbo.eu/) will let you extract data as geojson.

For Hong Kong the query looks like:

```
[out:json][timeout:25];
// gather results
(
  // query part for: “highway=bus_stop and "ref:hkbus"=*”
  node["highway"="bus_stop"]["ref:hkbus"]({{bbox}});
  way["highway"="bus_stop"]["ref:hkbus"]({{bbox}});
  relation["highway"="bus_stop"]["ref:hkbus"]({{bbox}});
);
// print results
out body;
>;
out skel qt;
```

Place the resulting export.json file in this directory.

If you are bringing a geojson file from elsewhere then know that we expect each geojson element to include a name, id, latitude and longitude.

Run import_geojson.py to create an sqlite database containing this data.  You can now delete the export.json file.

### GTFS

[Transitland](https://www.transit.land/feeds) aggregates thousands of GTFS feeds across the world.  Individual transit operators are liable for the quality of this data.  Whilst all the data listed is ostensibly open data, there's no clear licensing for some feeds.

If you know the name of the operator then you can search by that, otherwise you can browse the world map.

Once you have found a GTFS zip file, extract stops.txt into this directory and then run `python import_gtfs.py` to load the data into the sqlite database `stops.db`.

## Environment Variables

The application reads credential data from environment variables.  You can export these however you like, but the simplest option when testing locally is to copy `env_template` to `.env` in this directory and then edit it.

Visit the [Google Street View Image API page](https://developers.google.com/maps/documentation/streetview/) and click get a key. Make sure that your account and key has street view enabled.  Once you have the key, place it in the `.env` file.

## Usage

Both Twitter and Mastodon versions update the stops.db file, so you can only run one.  You should use a cross-posting service if you want the same posts to appear in both, and it is easier to do this in the Mastodon to Twitter direction.

### Twitter

Visit the [Twitter Developers page](https://developer.twitter.com/en/apps) and create an app.  Fill in the credentials in the `.env` file.

`python3 everystop.py`

### Mastodon

You'll need to first edit `mastodon_register.py` to specify your instance base url along with your email and password.

Then you can run `python mastodon_register.py` to create some secret files, and then `python mastodon_poster.py` to actually post.

## Dependencies

* Python 3.6+
* `pip3 install -r requirements.txt` for everything else

## Thanks

* Heavily inspired by [Everylot Bot](https://github.com/fitnr/everylotbot) but written from scratch for modern Python
