from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date, time, timezone

db = SQLAlchemy()



class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Sites(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, nullable=False, unique=True)
      location = db.Column(db.String, nullable=False)

class Area(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, nullable=False, unique=True)
      site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)

class Assets(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, nullable=False)
      site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)

class Failure(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, nullable=False)

class Vendors(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, nullable=False, unique=True)
      field = db.Column(db.String, nullable=False)  
      location = db.Column(db.String, nullable=False)       

class Tickets(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      description = db.Column(db.String, nullable=False)
      petitioner_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
      responsible_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)  
      site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)
      area_id = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)
      asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"), nullable=False)
      vendor_id= db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)
      date_start =  db.Column(db.DateTime, default=datetime.date, nullable=False)
      priority = db.Column(db.String, nullable=False)
      failure_id = db.Column(db.Integer, db.ForeignKey("failure.id"), nullable=False)
      status = db.Column(db.String, nullable=False)
      date_end =  db.Column(db.DateTime, default=None, nullable=True)

class Tickets_notes(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      description = db.Column(db.String(600), nullable=False)
      ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"), nullable=False)
      user_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
      date = db.Column(db.DateTime, default=datetime.date, nullable=False)