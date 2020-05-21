from config import db

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
    created = db.Column(db.DateTime)
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
    created = db.Column(db.DateTime)
    website = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='artist',
                            lazy=True,  cascade='all, delete')
    busy_times = db.relationship('BusyTime', backref='artist',
                            lazy=True,  cascade='all, delete')

class BusyTime(db.Model):
    __tablename__ = 'busy_times'

    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False, primary_key=True)
    start_date = db.Column(db.Date, primary_key=True)
    end_date = db.Column(db.Date, primary_key=True)