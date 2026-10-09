"""Business logic: validation, donor search and data analysis.

- parse_donor      -> exception handling (Unit II)
- find_donors      -> dict/set, list comprehension, lambda (Unit II)
- build_dashboard  -> NumPy (Unit IV), Pandas + Matplotlib (Unit V)

This file does not import Django, so it can be run on its own:
    python donors/logic.py
"""

import base64
import io
from datetime import date, datetime, timedelta

import matplotlib
matplotlib.use('Agg')  # draw charts to memory, no window needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BLOOD_GROUPS = ('O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+')

# Medical rule: a patient with blood group KEY can safely receive blood from these groups.
CAN_RECEIVE_FROM = {
    'O-':  {'O-'},
    'O+':  {'O+', 'O-'},
    'A-':  {'A-', 'O-'},
    'A+':  {'A+', 'A-', 'O+', 'O-'},
    'B-':  {'B-', 'O-'},
    'B+':  {'B+', 'B-', 'O+', 'O-'},
    'AB-': {'AB-', 'A-', 'B-', 'O-'},
    'AB+': set(BLOOD_GROUPS),  # universal receiver
}

GAP_DAYS = 90        # a donor must wait 90 days between whole-blood donations
SHORTAGE_LIMIT = 2   # fewer ready donors than this = shortage alert


def parse_donor(form):
    """Turn raw form data into a clean donor dict. Raises ValueError if invalid."""
    name = form.get('name', '').strip()
    if not name:
        raise ValueError('Name is required.')

    blood_group = form.get('blood_group')
    if blood_group not in BLOOD_GROUPS:
        raise ValueError('Please pick a valid blood group.')

    city = form.get('city', '').strip().title()
    if not city:
        raise ValueError('City is required.')

    phone = form.get('phone', '').strip()
    if not (phone.isdigit() and len(phone) == 10):
        raise ValueError('Phone number must be exactly 10 digits.')

    try:
        age = int(form.get('age', ''))
    except ValueError:
        raise ValueError('Age must be a whole number.')
    if not 18 <= age <= 65:
        raise ValueError('Donors must be between 18 and 65 years old.')

    last_donation = form.get('last_donation', '').strip()
    if last_donation:  # optional: empty means "never donated"
        try:
            donated_on = datetime.strptime(last_donation, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Last donation date must be in YYYY-MM-DD format.')
        if donated_on > date.today():
            raise ValueError('Last donation date cannot be in the future.')

    return {
        'name': name,
        'blood_group': blood_group,
        'city': city,
        'phone': phone,
        'age': age,
        'last_donation': last_donation,  # 'YYYY-MM-DD' text, or '' if never donated
    }


def add_status(donors, today=None):
    """Add 'eligible' (True/False) and 'next_date' (when they can donate again) to each donor."""
    today = today or date.today()
    for d in donors:
        if d['last_donation']:
            next_date = date.fromisoformat(d['last_donation']) + timedelta(days=GAP_DAYS)
        else:
            next_date = today  # never donated -> can donate now
        d['eligible'] = next_date <= today
        d['next_date'] = next_date.isoformat()
    return donors


def find_donors(donors, needed_group, city):
    """Donors who can give blood to a patient of `needed_group`, best matches first.

    Returns (ready, resting_count):
      ready         - compatible donors who can donate today
      resting_count - compatible donors who donated in the last 90 days
    Donors must already have a status from add_status().
    """
    city = city.strip().title()
    compatible = [d for d in donors if d['blood_group'] in CAN_RECEIVE_FROM[needed_group]]
    ready = [d for d in compatible if d['eligible']]

    # Same city first, then exact blood group match, then by name
    ready.sort(key=lambda d: (d['city'] != city, d['blood_group'] != needed_group, d['name']))
    for d in ready:
        d['same_city'] = d['city'] == city
    return ready, len(compatible) - len(ready)


def _chart_to_base64(fig):
    """Save a Matplotlib figure as PNG text so the HTML page can show it directly."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode()


def build_dashboard(donors):
    """Analyse donors (with status). Returns None when there is no data."""
    if not donors:
        return None

    # Pandas: list of dicts -> DataFrame (a table)
    df = pd.DataFrame(donors)

    # Pandas: count total and ready donors per blood group.
    # reindex() makes sure all 8 groups appear, even ones with 0 donors.
    by_group = (df.groupby('blood_group')
                  .agg(total=('name', 'count'), ready=('eligible', 'sum'))
                  .reindex(BLOOD_GROUPS, fill_value=0))
    shortage = [g for g in BLOOD_GROUPS if by_group.loc[g, 'ready'] < SHORTAGE_LIMIT]
    by_city = df['city'].value_counts()

    # NumPy: statistics on the age column
    ages = df['age'].to_numpy()
    ready_count = int(df['eligible'].sum())

    # Matplotlib: ready donors per blood group, shortage groups in red
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ['#c0392b' if g in shortage else '#2e86de' for g in BLOOD_GROUPS]
    ax.bar(BLOOD_GROUPS, by_group['ready'], color=colors)
    ax.axhline(SHORTAGE_LIMIT, color='gray', linestyle='--', label=f'Shortage limit ({SHORTAGE_LIMIT})')
    ax.set_title('Donors Ready to Donate, by Blood Group (red = shortage)')
    ax.set_ylabel('Ready donors')
    ax.yaxis.get_major_locator().set_params(integer=True)  # whole numbers only
    ax.legend()
    group_chart = _chart_to_base64(fig)

    # Matplotlib: donors per city
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(by_city.values, labels=by_city.index, autopct='%1.0f%%', startangle=90)
    ax.set_title('Donors by City')
    city_chart = _chart_to_base64(fig)

    return {
        'total': len(df),
        'ready': ready_count,
        'resting': len(df) - ready_count,
        'cities': len(by_city),
        'average_age': round(float(np.mean(ages)), 1),
        'youngest': int(np.min(ages)),
        'oldest': int(np.max(ages)),
        'by_group': [(g, int(row.total), int(row.ready)) for g, row in by_group.iterrows()],
        'shortage': shortage,
        'group_chart': group_chart,
        'city_chart': city_chart,
    }


if __name__ == '__main__':
    # Quick self-check, no database needed.
    good = parse_donor({'name': ' Asha ', 'blood_group': 'O-', 'city': ' pune ',
                        'phone': '9876543210', 'age': '25', 'last_donation': ''})
    assert good == {'name': 'Asha', 'blood_group': 'O-', 'city': 'Pune',
                    'phone': '9876543210', 'age': 25, 'last_donation': ''}

    base = {'name': 'X', 'blood_group': 'A+', 'city': 'Pune', 'phone': '9876543210', 'age': '30', 'last_donation': ''}
    for field, bad_value in [('name', ''), ('blood_group', 'C+'), ('city', ' '), ('phone', '12345'),
                             ('age', 'abc'), ('age', '17'), ('last_donation', '01-01-2026'),
                             ('last_donation', '2999-01-01')]:
        try:
            parse_donor({**base, field: bad_value})
            raise AssertionError(f'should have failed: {field}={bad_value}')
        except ValueError:
            pass

    today = date(2026, 10, 8)
    donors = add_status([
        {'name': 'Asha', 'blood_group': 'O-', 'city': 'Pune', 'age': 25, 'last_donation': ''},
        {'name': 'Ravi', 'blood_group': 'A+', 'city': 'Mumbai', 'age': 40, 'last_donation': '2026-01-10'},
        {'name': 'Neha', 'blood_group': 'A+', 'city': 'Pune', 'age': 30, 'last_donation': '2026-09-01'},
        {'name': 'Omar', 'blood_group': 'B+', 'city': 'Pune', 'age': 35, 'last_donation': ''},
    ], today)
    assert [d['eligible'] for d in donors] == [True, True, False, True]
    assert donors[2]['next_date'] == '2026-11-30'

    ready, resting = find_donors(donors, 'A+', 'pune')
    assert [d['name'] for d in ready] == ['Asha', 'Ravi']  # B+ can't give to A+, Neha is resting
    assert resting == 1
    ready, _ = find_donors(donors, 'O-', 'Mumbai')
    assert [d['name'] for d in ready] == ['Asha']  # O- can only receive O-

    s = build_dashboard(donors)
    assert s['total'] == 4 and s['ready'] == 3 and s['cities'] == 2 and s['average_age'] == 32.5
    assert ('A+', 2, 1) in s['by_group'] and ('AB+', 0, 0) in s['by_group']
    assert 'AB+' in s['shortage'] and 'O-' in s['shortage']
    assert build_dashboard([]) is None
    print('All checks passed.')
