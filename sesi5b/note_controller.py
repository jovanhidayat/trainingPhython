from flask import abort
from config import db
from note_model import Note, NoteSchema
from person_model import Person, PersonSchema
# GET /notes
# POST /people/{person_id}/notes
# GET /people/{person_id}/notes/{note_id}
# PUT /people/{person_id}/notes/{note_id}
# DELETE /people/{person_id}/notes/{note_id}

def read_all():
    notes = Note.query.outerjoin(Person).all()

    note_schema = NoteSchema(many=True)
    results = note_schema.dump(notes)

    return results


def create(person_id, note):
    person = {
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_more()
    }
    
    if person is None:
        abort (404, f"Person with id {person_id} is not found")

    content = note.get("content")
    new_note = Note(content = content, person_id = Person.id)

    person.notes.append(new_note)

    db.session.commit()

    note_schema = NoteSchema()

    result = note_schema(new_note)

    return result

def read_one(person_id, note_id):
    note = (Note.query.filter(Note.note_id == note_id)
            .filter(Person.person_id == person_id)
            .one_or_none()
            )
    
    print(note)

    if note is None:
        abort(404, 'Note with id {note_id} own by person {person_id} is not found')

    note_schema = NoteSchema()
    result = note_schema.dump(note)

    return result

def update(person_id, note_id, note):
    found_note = {
        Note.query.join(Person, Person.person_id == Note.person_id)
                .filter(Note.note_id == note_id)
                .one_or_none()
    }

    if found_note is None:
        abort(404, 'Note with id {note_id} own by person {person_id} is not found')

    found_note.content = note.get("content")

    db.merge(found_note)
    db.session.commit()

    note_schema = NoteSchema()
    result = note_schema.dump(found_note)

    return result