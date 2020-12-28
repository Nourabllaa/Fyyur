from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    website = db.Column(db.String())
    seeking_venue= db.Column(db.Boolean, nullable=False , default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist_shows', lazy=True, cascade='all, delete')
 


class Show(db.Model):
   __tablename__= 'show'
   id = db.Column(db.Integer, primary_key=True)
   artist_id = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
   venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
   start_time = db.Column(db.DateTime, nullable=False)
 