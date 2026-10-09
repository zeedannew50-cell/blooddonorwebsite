"""Views (the 'V' in Django's MVT): handle a request, return a page."""

from datetime import date

from bson.errors import InvalidId
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from pymongo.errors import PyMongoError

from . import db
from .logic import BLOOD_GROUPS, GAP_DAYS, add_status, build_dashboard, find_donors, parse_donor

DB_ERROR = 'Could not reach MongoDB. Check MONGO_URI in settings.py and your internet connection.'


def index(request):
    """Home page: donor registration form + list of all donors."""
    error = None

    if request.method == 'POST':
        try:
            db.add_donor(parse_donor(request.POST))
            return redirect('index')  # Post/Redirect/Get: refresh won't register twice
        except ValueError as e:
            error = str(e)
        except PyMongoError:
            error = DB_ERROR

    try:
        donors = add_status(db.all_donors())
    except PyMongoError:
        donors, error = [], DB_ERROR

    return render(request, 'donors/index.html', {
        'donors': donors,
        'blood_groups': BLOOD_GROUPS,
        'today': date.today().isoformat(),
        'error': error,
        'form': request.POST,  # keep what the user typed if there was an error
    })


def search(request):
    """Emergency search: who can give blood to this patient right now?"""
    group = request.GET.get('blood_group', '')
    city = request.GET.get('city', '')
    results, resting, error = None, 0, None

    if group in BLOOD_GROUPS:
        try:
            results, resting = find_donors(add_status(db.all_donors()), group, city)
        except PyMongoError:
            error = DB_ERROR

    return render(request, 'donors/search.html', {
        'blood_groups': BLOOD_GROUPS,
        'group': group,
        'city': city,
        'results': results,
        'resting': resting,
        'gap_days': GAP_DAYS,
        'error': error,
    })


@require_POST
def donated(request, donor_id):
    """Donor gave blood today: they become 'resting' for the next 90 days."""
    try:
        db.mark_donated(donor_id)
    except (InvalidId, PyMongoError):
        pass  # bad id or DB down: nothing changed, just go back
    return redirect('index')


@require_POST
def delete(request, donor_id):
    try:
        db.delete_donor(donor_id)
    except (InvalidId, PyMongoError):
        pass
    return redirect('index')


def dashboard(request):
    """Analysis page: totals, shortage alert and charts."""
    error = None
    try:
        data = build_dashboard(add_status(db.all_donors()))
    except PyMongoError:
        data, error = None, DB_ERROR
    return render(request, 'donors/dashboard.html', {'s': data, 'error': error})
