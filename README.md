
## Notion Restaurant Map

## Design

## Places Detail Query
The Google Maps "detailed" query has to be done per page load rather than stored in the Notion db. The returned values return things like if the place is open, which needs to be dynamic.

### Database
I originally wanted to have a postgres db that hold the returned google search data. This basically meant that I would have 2 dbs: a Notion one with clean 'pretty' data, and a postgres one with the response data from the Google Places API (messy and long). I thought it'd be bad design to trash my beautiful Notion db with messy data. But Pezz told me that it's probably even worse design to have 2 dbs with almost identical data. So Pezz wins.

This means your Notion db must have the following properties:
- Name
- Lat
- Lng
- Icon
- Photos
- Address
- Place_id

I wanted to write a function that would initialize the database for you with these properties, but it doesn't seem like the `notion-py` library can do that right now. Will revisit.

## Technicals
I wrote this with the notion-py library, Flask, JS. Deployed with gunicorn on Heroku.