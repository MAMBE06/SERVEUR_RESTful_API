from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import g, url_for

from app import db
from config import Config

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64))
    prenom = db.Column(db.String(64))
    date_naissance = db.Column(db.Date)
    email = db.Column(db.String(64))
    adresse = db.Column(db.String(128))
    telephone = db.Column(db.String(64))

    locations = db.relationship('Location', backref='clt')

    def to_json(self):
        return {
            'id': self.id,
            'uri': url_for('get_id_client', id_client=self.id, _external=True),
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance,
            'email': self.email,
            'adresse': self.adresse,
            'telephone': self.telephone
        }


class Voiture(db.Model):
    __tablename__ = 'voitures'
    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(32))
    immatriculation = db.Column(db.String(32), index=True, unique=True)
    modele = db.Column(db.String(32))
    disponible = db.Column(db.Boolean)
    couleur = db.Column(db.String(32))
    locations = db.relationship('Location', backref='voiture')

    def to_json(self):
        return {
            'id': self.id,
            'uri': url_for('get_id_voiture', id_voiture=self.id, _external=True),
            'marque': self.marque,
            'immatriculation': self.immatriculation,
            'modele': self.modele,
            'disponible': self.disponible,
            'couleur': self.couleur,
        }



class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    date_location = db.Column(db.Date)
    id_voiture = db.Column(db.Integer, db.ForeignKey('voitures.id'))
    id_client = db.Column(db.Integer, db.ForeignKey('clients.id'))

    def to_json(self):
        nom  = prenom = ""
        if self.clt is not None:
            nom = self.clt.nom
            prenom = self.clt.prenom

        return {
            'id': self.id,
            'uri': url_for('get_location_id', location_id=self.id, _external=True),
            'date_location': self.date_location,
            'voiture_prop': self.voiture.marque + ' ' + self.voiture.modele + ' : ' + self.voiture.immatriculation,
            'nom': nom,
            'prenom': prenom,
            'id_voiture': self.id_voiture,
            'id_client': self.id_client
        }
    
