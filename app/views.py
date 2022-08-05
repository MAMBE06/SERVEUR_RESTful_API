from flask import Flask, jsonify, abort, make_response, request, url_for, g
from datetime import datetime
from app import app, db
from app.models import Client, Voiture, Location

DATE_FORMAT = '%Y-%m-%d'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

################################# clients #################################

@app.route('/api/clients', methods=['GET'])

def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_json() for client in clients])

@app.route('/api/clients/<int:id_client>', methods=['GET'])
def get_id_client(id_client):
    client = Client.query.filter_by(id=id_client).first()
    if client is None:
        abort(404)
    return jsonify({'client': client.to_json()})


@app.route('/api/clients', methods=['POST'])
def new_client():
    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    date_naissance = datetime.strptime(request.json['date_naissance'], DATE_FORMAT)
    email = request.json.get('email')
    adresse = request.json.get('adresse')
    telephone = request.json.get('telephone')

    if nom is None or prenom is None or date_naissance is None or email is None or \
            adresse is None or telephone is None :
        print("missing crucial informations")
        abort(400) # missing crucial informations

    if Client.query.filter_by(nom = nom, prenom = prenom).first() is not None:
        print("This user already exist")
        abort(400) # user already existing

    client = Client(nom=nom, prenom=prenom, date_naissance=date_naissance,
                  email=email, adresse=adresse, telephone=telephone)

    db.session.add(client)
    db.session.commit()
    return jsonify({'Noms': client.prenom + ' ' +client.nom}), 201, {'uri': url_for('get_id_client', id_client=client.id, _external=True)}


@app.route('/api/clients/<int:id_client>', methods=['PUT'])
def update_client(id_client):
    client = Client.query.filter_by(id=id_client).first()
    if client is None:
        abort(404)
    if not request.json:
        print("bad request")
        abort(400)

    client.nom = request.json.get('nom', client.nom)
    client.prenom = request.json.get('prenom', client.prenom)
    client.date_naissance = datetime.strptime(request.json['date_naissance'], DATE_FORMAT)
    client.email = request.json.get('email', client.email)
    client.adresse = request.json.get('adresse', client.adresse)
    client.telephone = request.json.get('telephone', client.telephone)

    db.session.add(client)
    db.session.commit()
    return jsonify({'client': client.to_json()})

@app.route('/api/clients/<int:id_client>', methods=['DELETE'])
def delete_client(id_client):
    client = Client.query.filter_by(id=id_client).first()
    if client is None:
        abort(404)

    db.session.delete(client)
    db.session.commit()
    return jsonify({'result': True})

################## end clients ############################################


############################ voitures ######################

@app.route('/api/voitures', methods=['GET'])
def get_voitures():
    voitures = Voiture.query.all()
    return jsonify({'voitures': [voiture.to_json() for voiture in voitures]})

@app.route('/api/voitures/<int:id_voiture>', methods=['GET'])
def get_id_voiture(id_voiture):
    voiture = Voiture.query.filter_by(id=id_voiture).first()
    if voiture is None:
        abort(404)
    return jsonify({'voiture': voiture.to_json()})

@app.route('/api/voitures', methods=['POST'])
def create_voiture():
    if not request.json or 'immatriculation' not in request.json:
        abort(400) # bad request

    voiture = Voiture(
        marque=request.json['marque'],
        modele=request.json['modele'],
        immatriculation=request.json['immatriculation'],
        disponible=True,
        couleur=request.json['couleur']
    )
    db.session.add(voiture)
    db.session.commit()
    return jsonify({'voiture': voiture.to_json()}), 201 # Created

@app.route('/api/voitures/<int:id_voiture>', methods=['PUT'])
def update_voiture(id_voiture):
    voiture = Voiture.query.filter_by(id=id_voiture).first()
    if voiture is None:
        abort(404)
    if not request.json:
        abort(400)

    voiture.modele = request.json.get('modele', voiture.modele)
    voiture.marque = request.json.get('marque', voiture.marque)
    voiture.immatriculation = request.json.get('immatriculation', voiture.immatriculation)

    if request.json.get('disponible'):
        voiture.disponible = True

    voiture.couleur = request.json.get('couleur', voiture.couleur)

    db.session.add(voiture)
    db.session.commit()
    return jsonify({'voiture': voiture.to_json()})

@app.route('/api/voitures/<int:id_voiture>', methods=['DELETE'])
def delete_voiture(id_voiture):
    voiture = Voiture.query.filter_by(id=id_voiture).first()
    if voiture is None:
        abort(404)
    db.session.delete(voiture)
    db.session.commit()
    return jsonify({'result': True})

################################# end voitures ########################

##################################### location #########################

@app.route('/api/voitures/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    if locations is None:
        abort(404)
    return jsonify({'locations': [res.to_json() for res in locations]})

@app.route('/api/voitures/locations/<int:location_id>', methods=['GET'])
def get_location_id(location_id):
    res = Location.query.filter_by(id=location_id).first()
    if res is None:
        abort(404)
    return jsonify({'locations': res.to_json()})

@app.route('/api/voitures/locations', methods=['POST'])
def create_location():
    r_date = datetime.strptime(request.json['date_location'], DATE_FORMAT)
    c_id = request.json['id_voiture']
    u_id = Client.query.filter_by(id=request.json['id_client']).first().id

    voiture = Voiture.query.filter_by(id=c_id).first()
    if not voiture.disponible:
        abort(400)
    res = Location(
        date_location = r_date,
        id_voiture = c_id,
        id_client = u_id
    )

    voiture.disponible = False

    db.session.add(res)
    db.session.commit()
    return jsonify({'location': res.to_json()}), 201 # Created

@app.route('/api/voitures/locations/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    res = Location.query.filter_by(id=location_id).first()
    if res is None:
        abort(404)
    if not request.json:
        abort(400)

    res.location_date = request.json.get('date_location', res.location_date)
    res.id_client = request.json.get('id_client', res.id_client)
    res.id_voiture = request.json.get('id_voiture', res.id_voiture)
    
    db.session.save(res)
    db.session.commit()
    return jsonify({'locations': res.to_json()})

@app.route('/api/voitures/locations/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    res = Location.query.filter_by(id=location_id).first()
    if res is None:
        abort(404)
    car = Voiture.query.filter_by(id=res.id_voiture).first();
    if car is None:
        abort(404)
    car.disponible = True
    db.session.add(car)
    db.session.delete(res)
    db.session.commit()
    return jsonify({'result': True})

####################### end location ##################""
