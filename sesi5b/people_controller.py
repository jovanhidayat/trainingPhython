from flask import make_response, abort, request
from note_model import Note
from person_model import Person, PersonSchema
from config import db

# /api/people
def read_all():
    people = Person.query.outerjoin(Note).all()
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)
    # print(data)
    return data

def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")

def update(person_id,person_data):
    # Ambil 1 data dari database yang mempunyai id person_id
    updated_person = Person.query.get(person_id)

    if updated_person is None:
        abort(
            404,
            "Person with id {person_id} is not found!"
        )
    else:
        # person_data
        # lname = person_data.get('lname')
        # fname = person_data.get('fname')

        # updated_person.lname = lname
        # updated_person.fname = fname

        person_schema = PersonSchema()
        updated_person.fname = person_data['fname']
        updated_person.lname = person_data['lname']

        # update = schema.load(person_data, instance=updated_person, session=db.session)

        # person_instance = Person(
        #     person_id = person_id,
        #     fname = fname,
        #     lname = lname,
        #     timestamp = updated_person.timestamp
        # )

        # db.session.merge(updated_person)
        # db.session.commit()

        updated_person.update()
        return person_schema.dump(updated_person)

        # return schema.dump(update)

def delete(person_id):
    deleted_person = Person.query.get(person_id)

    if deleted_person is None:
        abort(
            404,
            "Person with id {person_id} is not found!"
        )
    else:
        nama = deleted_person.fname
        deleted_person.delete()
        return f"{nama} has been slained"

def add():

    person_data = request.get_json()

    new_person = Person(
        lname=person_data['lname'], 
        fname=person_data['fname']
    )
    
    person_schema = PersonSchema()
    new_person.add()
    return person_schema.dump(new_person)

    # return f"successfully update a person {fname} {lname}"