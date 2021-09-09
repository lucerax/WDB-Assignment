from app import db


class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name



class Furniture(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


def add_fruit(new_name):
    fruit = Fruit(new_name)
    db.session.add(fruit)
    db.session.commit()

    return fruit

def add_furniture(new_name):
    furniture = Furniture(new_name)
    db.session.add(furniture)
    db.session.commit()

    return furniture

def delete_object(name):
    deleted = False
    fruits = db.session.query(Fruit).filter(Fruit.name==name).delete()
    if fruits:
        deleted = True
    furniture = db.session.query(Furniture).filter(Furniture.name==name).delete()
    if furniture:
        deleted = True
    db.session.commit()
    return deleted


if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")
