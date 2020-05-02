# Every Stop

This is a Twitter bot which tweets a Google Street View image of every single bus stop for Hong Kong.  But it could tweet any Open Street Map node that you provide it.

## Setup

Use [Overpass Turbo](http://overpass-turbo.eu/) to extract the desired bus stops as geojson.  For Hong Kong the query looks like:

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

Run import.py to create an sqlite database containing this data.  You can now delete the export.json file.

Copy `env_template` to `.env` in this directory.

Visit the [Google Street View Image API page](https://developers.google.com/maps/documentation/streetview/) and click get a key. Make sure that your account and key has street view enabled.  Once you have the key, place it in the `.env` file.

Visit the [Twitter Developers page](https://developer.twitter.com/en/apps) and create an app.  Fill in the credentials in the `.env` file.

## Usage

`python3 everystop.py`

## Dependencies

* Python 3.6
* `pip3 install -r requirements.txt` for everything else

## Thanks

* Heavily inspired by [Everylot Bot](https://github.com/fitnr/everylotbot) but written from scratch for modern Python