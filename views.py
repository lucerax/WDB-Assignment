from flask import render_template, request

from models import *
from app import app

import requests
import re

stanfurd_deletes = set()

stanfurd_fruit = requests.get('http://fry-kea-api.herokuapp.com/api/fry').text.strip('][').split(',')
stanfurd_fruit = [fr.replace('"', '') for fr in stanfurd_fruit]
stanfurd_furniture = requests.get('http://fry-kea-api.herokuapp.com/api/kea').text.strip('][').split(',')
stanfurd_furniture = [fu.replace('"', '') for fu in stanfurd_furniture]


@app.route('/')
def index():
    """
    This method handles getting data from the Stanfurd API and local DB and joining objects to output Fruitniture.
    E.g we assume that a mango and Mirror will give mangoMirror.
    """
    local_fruit = [d.name for d in Fruit.query.all()]
    local_furniture = [d.name for d in Furniture.query.all()]
    fruit, furniture = [], []
    fruit.extend(stanfurd_fruit)
    furniture.extend(stanfurd_furniture)
    fruit.extend(local_fruit)
    furniture.extend(local_furniture)
    fruitniture = []

    for f in furniture:
        print(f)
    for fu in furniture:
        for fr in fruit:
            if fu and fr:
                if fu[0].lower() == fr[0].lower() and fu not in stanfurd_deletes and fr not in stanfurd_deletes:
                    fruitniture.append(fr+fu)
    for f in fruitniture:
        print(f)

    return render_template('index.html', fruitniture=fruitniture)


@app.route('/addFruit', methods=['GET', 'POST'])
def addFruit():
    """
    Enables addition of fruit data to the Fruit class
    """
    if request.method == 'GET':
        return render_template('addFruit.html')

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    fruit_name = request.form.get('name_field')
    fruit_added = False

    #Handle both data store options due to hybrid model
    if fruit_name in stanfurd_deletes:
        stanfurd_deletes.remove(fruit_name)
        fruit_added = True
    else:
        fruit = add_fruit(fruit_name)
        if fruit:
            fruit_added = True

    return render_template('addFruit.html', fruit_added=fruit_added, name=fruit_name)


@app.route('/addFurniture', methods=['GET', 'POST'])
def addFurniture():
    """
    Enables addition of furniture data to the Furniture class.
    """
    if request.method == 'GET':
        return render_template('addFurniture.html')

    furniture_name = request.form.get('name_field')
    furniture_added = False

    #Handle both data store options due to hybrid model
    if furniture_name in stanfurd_deletes:
        stanfurd_deletes.remove(furniture_name)
        furniture_added = True
    else:
        furniture = add_furniture(furniture_name)
        if furniture:
            furniture_added = True

    return render_template('addFurniture.html', furniture_added=furniture_added, name=furniture_name)

@app.route('/addFruitniture', methods=['GET', 'POST'])
def addFruitniture():
    """
    Enables addition of fruitniture data by breaking it up into constituent fruits and furniture.
    """
    if request.method == 'GET':
        return render_template('addFruitniture.html')

    fruitniture_name = request.form.get('name_field')
    query_str = re.sub( r"([A-Z])", r" \1", fruitniture_name).split()

    #Input has not been entered correctly
    if len(query_str) != 2:
        return render_template('addFruitniture.html', error=True)

    fruit_name = query_str[0]
    furniture_name = query_str[1]

    #We have found consituent objects
    if fruit_name and furniture_name:
        fruitniture_added = False
        fruit_added, furniture_added = False, False
        #Handle fruit first
        if fruit_name in stanfurd_deletes:
            stanfurd_deletes.remove(fruit_name)
            fruit_added = True
        else:
            fruit = add_fruit(fruit_name)
            if fruit:
                fruit_added = True
        #Handle furniture addition
        if furniture_name in stanfurd_deletes:
            stanfurd_deletes.remove(furniture_name)
            furniture_added = True
        else:
            furniture = add_furniture(furniture_name)
            if furniture:
                furniture_added = True

        fruitniture_added = fruit_added and furniture_added
        return render_template('addFruitniture.html', fruitniture_added=fruitniture_added, name=fruitniture_name)
    else:
        return render_template('addFruitniture.html', error=True)


@app.route('/deleteObject', methods=['GET', 'POST'])
def deleteObject():
    if request.method == 'GET':
        return render_template('deleteObject.html')

    object_name = request.form.get('name_field')
    deleted = None

    if object_name in stanfurd_fruit or object_name in stanfurd_furniture and object_name not in stanfurd_deletes:
        stanfurd_deletes.add(object_name)
        deleted = True
    else:
        deleted = delete_object(object_name)

    return render_template('deleteObject.html', deleted = deleted, name=object_name)
