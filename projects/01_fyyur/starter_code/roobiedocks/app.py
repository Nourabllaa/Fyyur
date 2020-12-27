#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate 
import sys 
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrat= Migrate(app, db )


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



   # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    genres = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String())
    seeking_venue= db.Column(db.Boolean, nullable=False , default=False)
    shows = db.relationship('Show', backref='artist_shows', lazy=True, cascade='all, delete')


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String())
    state = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String())
    seeking_talent= db.Column(db.Boolean,nullable=False, default=False)
    seeking_description = db.Column(db.String())
    genres = db.Column(db.String())
    website = db.Column(db.String())
    shows = db.relationship('Show', backref='venue_shows', lazy=True, cascade='all, delete')




   


    # TODO: implement any missing fields, as a database migration using Flask-Migrate



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__= 'show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
    city_state = Venue.query.distinct('city','state').all()
    result = []
    for c_s in city_state:
      venues = Venue.query.filter(Venue.city == c_s.city, Venue.state == c_s.state).all()
      record = {
        'city': c_s.city,
        'state': c_s.state,
        'venues': venues,
       #'num_upcoming_shows': len(list(filter(lambda x: x.start_time > datetime.today(), venues.Show)))
      }
      result.append(record)

    return render_template('pages/venues.html', areas=result)
 # return render_template('pages/venues.html', areas=Venue.query.order_by('city').all());


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  result = Venue.query.filter(Venue.name.ilike('%'+ search_term +'%')).all()
  data = []
  for venue in result:
    tmp = {}
    tmp['id'] = venue.id
    tmp['name'] = venue.name
    #tmp['num_upcoming_shows'] = len(venue.shows)
    data.append(tmp)

  response = {}
  response['count'] = len(data)
  response['data'] = data
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

 my_venue = Venue.query.get(venue_id)
 my_shows = Show.query.filter_by(venue_id = venue_id).all()
 upcoming_shows = []
 past_shows = []
 upcoming_count = 0
 past_count = 0
 current_time = datetime.now()   
 for show in my_shows:
  my_artest =show.artist_id
  if show.start_time < current_time:
    past_count += 1
    past_record = {
      "artist_id": show.artist_id,
      "artist_name": Artist.query.get(my_artest).name,
      "artist_image_link": Artist.query.get(my_artest).image_link,
      "start_time": show.start_time,
    }
    past_shows.append(past_record)
  else:
      upcoming_count += 1
      record = {
        "artist_id": show.artist_id,
        "artist_name": Artist.query.get(my_artest).name,
        "artist_image_link": Artist.query.get(my_artest).image_link,
        "start_time": str(show.start_time),
      }
      upcoming_shows.append(record)





 data= {
   "id": my_venue.id,
    "name": my_venue.name ,
    "genres":my_venue.genres,
    "address":my_venue.address ,
    "city":my_venue.city ,
    "state": my_venue.state,
    "phone": my_venue.phone ,
    "website": my_venue.website,
    "facebook_link": my_venue.facebook_link,
    "seeking_talent": my_venue.seeking_talent,
    "seeking_description": my_venue.seeking_description,
    "image_link": my_venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_count,
    "upcoming_shows_count": upcoming_count,
  } 
     #data = list(filter(lambda d: d['id'] == venue_id, [data, data2, data3]))[0]
 return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)




@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    venue = Venue()
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone =request.form.get('phone')
    genres = request.form.getlist('genres')
    result = ''
    for gen in genres:
      result+','+gen
    venue.genres=genres
    venue.facebook_link = request.form.get('facebook_link')
    db.session.add(venue)
    db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
    # TODO: on unsuccessful db insert, flash an error instead.
      db.session.close()
      if error:
          flash('An error occured. Venue ' + request.form['name'] + ' Could not be listed!')
      else:
          # on successful db insert, flash success
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
          # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

  
 

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
      Venue.query.filter_by(id=venue_id).delete()
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the databas
  artists =Artist.query.all()
  data=[]
  record={}
  for a in artists:
    record= {
    "id": a.id,
    "name":a.name,
  } 
    data.append(record)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  result = Artist.query.filter(Artist.name.ilike('%'+ search_term +'%')).all()
  data = []
  for artest in result:
    tmp = {}
    tmp['id'] = artest.id
    tmp['name'] = artest.name
    #tmp['num_upcoming_shows'] = len(artest.show)
    data.append(tmp)

  response = {}
  response['count'] = len(data)
  response['data'] = data
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

   my_artist = Artist.query.get(artist_id)
   my_shows = Show.query.filter_by(id=artist_id).all()
   upcoming_shows = []
   past_shows = []
   upcoming_count = 0
   past_count = 0
   current_time = datetime.now()   
   for show in my_shows:
     my_venue =show.venue_id
     if show.start_time < current_time:
       past_count += 1
       past_record = {
      "venue_id": my_venue,
      "venue_name": Venue.query.get(my_venue).name,
      "venue_image_link": Venue.query.get(my_venue).image_link,
      "start_time": show.start_time,
    }
       past_shows.append(past_record)
     else:
       upcoming_count += 1
       record = {
       "venue_id": my_venue,
       "venue_name": Venue.query.get(my_venue).name,
       "venue_image_link": Venue.query.get(my_venue).image_link,
       "start_time": str(show.start_time),
        }
       upcoming_shows.append(record)

   data={
    "id": my_artist.id,
    "name": my_artist.name,
    "genres": my_artist.genres,
    "city": my_artist.city,
    "state": my_artist.state,
    "phone": my_artist.phone,
    "seeking_venue": my_artist.seeking_venue,
    "image_link":  my_artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
   
    "past_shows_count": past_count,
    "upcoming_shows_count": upcoming_count,
  }
 
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
   return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  my_artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=my_artist)
  
  artist={
    "id": my_artist.id,
    "name": my_artist.name,
    "genres": my_artist.genres,
    "city": my_artist.city,
    "state": my_artist.state,
    "phone": my_artist.phone,
    "seeking_venue": my_artist.seeking_venue,
    "image_link":  my_artist.image_link,
    "facebook_link": my_artist.facebook_link,
    
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  my_artists = Artist.query.get(artist_id) 
  form = ArtistForm(request.form)
  error = False
  if form.validate_on_submit():
    try:
      my_artists.name = form.name.data
      my_artists.city = form.city.data
      my_artists.state = form.state.data
      my_artists.website=form.website.data
      my_artists.seeking_venue= form.seeking_talent.data
      my_artists.seeking_description= form.seeking_description.data
      my_artists.image_link= form.image_link.data
      my_artists.genres =  form.genres.data
      my_artists.facebook_link =form.facebook_link.data
      my_artists.update()
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
      if error:
        flash('An error occurred. Artist ' +form.name.data+ ' could not be updated.')
      else:
        flash('Artist ' + form.name.data +' was successfully updated!')
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
   # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)

 

 

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  my_venue = Venue.query.get(venue_id) 
  form = VenueForm(request.form)
  error = False
  if form.validate_on_submit():
    try:
      my_venue.name = request.form.get('name')
      my_venue.city =request.form.get('city')
      my_venue.state =request.form.get('state')
      my_venue.address = request.form.get('address')
      my_venue.phone =request.form.get('phone')
      my_venue.website=request.form.get('website')
      my_venue.seeking_talent= request.form.get('seeking_talent')
      my_venue.seeking_description= request.form.get('seeking_description')
      my_venue.image_link= request.form.get('image_link')
      my_venue.genres =  request.form.get('genres')
      my_venue.facebook_link =request.form.get('facebook_link')
      my_venue.update()
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
      if error:
        flash('An error occurred. Venue ' +my_venue.name+ ' could not be updated.')
      else:
        flash('Venue ' + my_venue.name +' was successfully updated!')
   # TODO: populate form with values from venue with ID <venue_id 
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    artist = Artist()
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone =request.form.get('phone')
    genres = request.form.getlist('genres')
    result = ''
    for gen in genres:
      result+','+gen
    artist.genres=result
    artist.facebook_link = request.form.get('facebook_link')
    db.session.add(artist)
    db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
    # TODO: on unsuccessful db insert, flash an error instead.
      db.session.close()
      if error:
          flash('An error occured. Artist ' + request.form['name'] + ' Could not be listed!')
      else:
          # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows =Show.query.all()
  data=[]
  record={}
  for show in shows:
    record= {
    "venue_id": show.venue_id,
    "venue_name":Venue.query.get(show.venue_id).name, 
    "artist_id": show.artist_id,
    "artist_name": Artist.query.get(show.artist_id).name,
    "artist_image_link":Artist.query.get(show.artist_id).image_link,
    "start_time":str(show.start_time )
    }
    data.append(record)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    show = Show()
    show.artist_id = request.form.get('artist_id')
    show.venue_id = request.form.get('venue_id')
    show.start_time = request.form.get('start_time')
    db.session.add(show)
    db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
    # TODO: on unsuccessful db insert, flash an error instead.
      db.session.close()
      if error:
          flash('An error occurred. Show could not be listed.')
      else:
          # on successful db insert, flash success
          flash('Show was successfully listed!')
          # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
