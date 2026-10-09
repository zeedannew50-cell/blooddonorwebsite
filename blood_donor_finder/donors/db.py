"""MongoDB access layer (Unit III - Python and Databases).

All CREATE / READ / UPDATE / DELETE operations on the 'donors' collection live here.
"""

from datetime import date

from bson import ObjectId
from django.conf import settings
from pymongo import MongoClient

# One client for the whole app. Times out after 5s if MongoDB is unreachable.
client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
collection = client[settings.MONGO_DB_NAME]['donors']


def add_donor(donor):
    """CREATE: insert one donor document."""
    collection.insert_one(donor)


def all_donors():
    """READ: all donors sorted by name.

    Templates cannot read '_id' (leading underscore), so it is copied to 'id'.
    """
    donors = []
    for doc in collection.find().sort('name', 1):
        doc['id'] = str(doc.pop('_id'))
        donors.append(doc)
    return donors


def mark_donated(donor_id):
    """UPDATE: set the donor's last donation date to today."""
    collection.update_one({'_id': ObjectId(donor_id)},
                          {'$set': {'last_donation': date.today().isoformat()}})


def delete_donor(donor_id):
    """DELETE: remove one donor. Raises bson.errors.InvalidId for a bad id."""
    collection.delete_one({'_id': ObjectId(donor_id)})
