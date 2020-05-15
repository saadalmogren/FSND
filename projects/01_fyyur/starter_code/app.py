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
from datetime import datetime
import sys
import dateutil.parser

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Show(db.Model):
    __tablename__ = 'shows'
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False, primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='venue',
                            lazy=True, cascade='all, delete')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='artist',
                            lazy=True,  cascade='all, delete')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


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

    #returns distinct city and state names
    location = Venue.query.distinct(
        Venue.city, Venue.state).with_entities(Venue.city, Venue.state)

    data = []

    # for each location return venues and append id, name and number of shows to vdata(venue data)
    # and then append city, state and vunue data to data
    for loc in location:
        venues = Venue.query.filter_by(city=loc.city , state=loc.state).all()
        vdata = []
        for venue in venues:
            vdata.append({
                'id': venue.id,
                'name': venue.name,
                'num_shows': Show.query.filter_by(venue_id=venue.id).count()
            })

        data.append({
            'city': loc.city,
            'state': loc.state,
            'venues': vdata
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    term = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(f'%{term}%')).all()
    data = []

    #for each result append the venue id, name and number of upcoming shows to data
    for res in result:
        data.append({
            'id': res.id,
            'name': res.name,
            'num_upcoming_shows': Show.query.filter_by(venue_id=res.id).count()
        })

    response = {
        "count": len(result),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    if venue is None:
        return render_template('errors/404.html')

    past_shows = Show.query.filter(venue_id == venue_id).filter(
        Show.start_time < datetime.now())

    upcoming_shows = Show.query.filter(venue_id == venue_id).filter(
        Show.start_time > datetime.now())


    pshows = []
    for show in past_shows:
        artist = Artist.query.get(show.artist_id)
        pshows.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            #stfrtime() turns datetime object to string to be used by the parser 
            #taken from https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    ushows = []
    for show in upcoming_shows:
        artist = Artist.query.get(show.artist_id)
        ushows.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    data = {
        "id": venue_id,
        "name": venue.name,
        "genres": venue.genres.split(','),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": pshows,
        "upcoming_shows": ushows,
        "past_shows_count": len(pshows),
        "upcoming_shows_count": len(ushows),
    }

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
    venue_form = VenueForm(request.form)

    try:
        name = venue_form.name.data
        #turn the city name to sentence case format eg. san francisco to San Francisco
        #taken from https://stackoverflow.com/questions/8347048/how-to-convert-string-to-title-case-in-python
        city = venue_form.city.data.title()
        state = venue_form.state.data
        address = venue_form.address.data
        phone = venue_form.phone.data
        #sperates genres with ',' to be easily sperated and stored in list with split() when needed
        genres = ','.join(venue_form.genres.data)
        image_link = venue_form.image_link.data
        facebook_link = venue_form.facebook_link.data
        website = venue_form.website.data
        seeking_talent = venue_form.seeking_talent.data
        seeking_description = venue_form.seeking_description.data
        venue = Venue(name=name, city=city, state=state, phone=phone, genres=genres,
                      address=address, image_link=image_link, facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + name + ' could not be listed.')
        print(sys.exc_info())
    finally:
        db.session.close()

        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.get(venue_id)
        venue.delete()
        db.session.commit()
        flash('Venue' + venue.name + ' was deleted successfully!')
    except:
        db.session.rollback()
        flash('An error occured. Veneue' +
              venue.name + ' could not be deleted!')

    finally:
        db.session.close()
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    term = request.form.get('search_term', '')
    result = Artist.query.filter(Artist.name.ilike(f'%{term}%')).all()
    data = []
    for res in result:
        data.append({
            'id': res.id,
            'name': res.name,
            'num_upcoming_shows': Show.query.filter_by(artist_id=res.id).count()
        })

    response = {
        "count": len(result),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.get(artist_id)

    if artist is None:
        return render_template('errors/404.html')

    past_shows = Show.query.filter(artist_id == artist_id).filter(
        Show.start_time < datetime.now())
    upcoming_shows = Show.query.filter(artist_id == artist_id).filter(
        Show.start_time > datetime.now())

    pshows = []

    for show in past_shows:
        venue = Venue.query.get(show.venue_id)
        pshows.append({

            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    ushows = []
    for show in upcoming_shows:
        venue = Venue.query.get(show.venue_id)
        ushows.append({

            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    data = {
        "id": artist_id,
        "name": artist.name,
        "genres": artist.genres.split(','),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": pshows,
        "upcoming_shows": ushows,
        "past_shows_count": len(pshows),
        "upcoming_shows_count": len(ushows),
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_info = Artist.query.get(artist_id)
    if artist_info is None:
        return render_template('errors/404.html')

    artist = {
        "id": artist_id,
        "name": artist_info.name,
        "genres": artist_info.genres,
        "city": artist_info.city,
        "state": artist_info.state,
        "phone": artist_info.phone,
        "website": artist_info.website,
        "facebook_link": artist_info.facebook_link,
        "seeking_venue": artist_info.seeking_venue,
        "seeking_description": artist_info.seeking_description,
        "image_link": artist_info.image_link
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist_form = ArtistForm(request.form)
    try:
        artist = Artist.query.get(artist_id)
        artist.name = artist_form.name.data
        artist.city = artist_form.city.data.title()
        artist.state = artist_form.state.data
        artist.phone = artist_form.phone.data
        artist.genres = ','.join(artist_form.genres.data)
        artist.image_link = artist_form.image_link.data
        artist.facebook_link = artist_form.facebook_link.data
        artist.seeking_venue = artist_form.seeking_venue.data
        artist.seeking_description = artist_form.seeking_description.data
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_info = Venue.query.get(venue_id)
    if venue_info is None:
        return render_template('errors/404.html')

    venue = {
        "id": venue_id,
        "name": venue_info.name,
        "genres": venue_info.genres,
        "address": venue_info.address,
        "city": venue_info.city,
        "state": venue_info.state,
        "phone": venue_info.phone,
        "website": venue_info.website,
        "facebook_link": venue_info.facebook_link,
        "seeking_talent": venue_info.seeking_talent,
        "seeking_description": venue_info.seeking_description,
        "image_link": venue_info.image_link
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue_form = VenueForm(request.form)
    try:
        venue = Venue.query.get(venue_id)
        venue.name = venue_form.name.data
        venue.city = venue_form.city.data.title()
        venue.state = venue_form.state.data
        venue.phone = venue_form.phone.data
        venue.address = venue_form.address.data
        venue.genres = ','.join(venue_form.genres.data)
        venue.facebook_link = venue_form.facebook_link.data
        venue.website = venue_form.website.data
        venue.image_link = venue_form.image_link.data
        venue.seeking_talent = venue_form.seeking_talent.data
        venue.seeking_description = venue_form.seeking_description.data
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
        print(sys.exc_info())
    finally:
        db.session.close()

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
    artist_form = ArtistForm(request.form)

    try:
        # TODO: modify data to be the data object returned from db insertion
        name = artist_form.name.data
        city = artist_form.city.data.title()
        state = artist_form.state.data
        phone = artist_form.phone.data
        genres = ','.join(artist_form.genres.data)
        image_link = artist_form.image_link.data
        facebook_link = artist_form.facebook_link.data
        website = artist_form.website.data
        seeking_venue = artist_form.seeking_venue.data
        seeking_description = artist_form.seeking_description.data
        artist = Artist(name=name, city=city, state=state, phone=phone,
                        genres=genres, image_link=image_link, facebook_link=facebook_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + name + ' was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + name + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    shows = Show.query.join(Artist).join(Venue)
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

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
    try:
        venue_id = request.form.get('venue_id')
        artist_id = request.form.get('artist_id')
        start_time = request.form.get('start_time')
        show = Show(venue_id=venue_id, artist_id=artist_id,
                    start_time=start_time)
        venue = Venue.query.get(venue_id)
        artist = Artist.query.get(artist_id)
        show.venue = venue
        show.artist = artist
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
