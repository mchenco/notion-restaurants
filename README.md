
# Notion Restaurant Map
I love food and discovering new places. This app pulls data from my Notion database of restaurants and plots them on a map for you to see the physical location of restaurants.

## Why not just add restaurants on Google Maps?
Well, short answer, I'm lazy. If I see a restaurant on Instagram, it takes too many steps to open Google Maps, search for the restaurant, and add it to my collections. But with Notion, I can use the web clipper to save the restaurant to my database in a few clicks.

This app then automatically performs the Google search query for me to populate information like address, place_id, etc. Lazy :)

## User Flow
1. User clips restaurants to Notion db
2. User loads web app
3. App will call the Places API for newly added restaurants in Notion that don't already have the address/place_id info populated. Information gets populated and saved in Notion db to reduce future calls.
4. Web app will load with a form for someone to enter a city to return results for (i.e New York, Toronto, Los Angeles, etc.)
5. After submission, the database returns restaurants within that city and plots it
	a. The app will automatically replot markers when the map moves
	b. Only plotting the restaurants within a given city makes it faster, especially for large databases and well-travelled users :)
7. Users can click on the markers to show information like price and rating, as well as a link to open it in Google Maps for directions

### Technicals
I wrote this with a forked version of the [notion-py](https://github.com/jamalex/notion-py) library, the [Google Maps Place API](https://developers.google.com/places/web-service/intro), [Maps Javascript API](https://developers.google.com/maps/documentation/javascript/tutorial) and Flask. Deployed with gunicorn on Heroku. 

## Design Decisions
### Database
I originally wanted to have a postgres db that holds the returned google search data. This basically meant that I would have 2 dbs: a Notion one with clean 'pretty' data, and a postgres one with the response data from the Google Places API (messy and long). I thought it'd be bad design to trash my beautiful Notion db with messy data. But my friend Pezz told me that it's probably even worse design to have 2 dbs with almost identical data. So Pezz wins.

This means your Notion db must have the following properties:
- Name
- Lat
- Lng
- Icon
- Photos
- Address
- Place_id

I wanted to write a function that would initialize the database for users with these properties instantiated, but it doesn't seem like the notion-py library can do that right now. Will revisit.

## Places Detail Query
The Google Maps "detailed" query has to be done per page load rather than stored in the Notion db. The returned values return things like if the place is open now, which needs to be dynamic.

## Future work
- Plotting markers takes a while
- Show 'Open Now' or hours in marker info window 
- Make info window prettier