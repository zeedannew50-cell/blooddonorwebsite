"""Fill MongoDB with sample donors for a demo.

Run:  python seed.py
WARNING: this deletes all existing donors first.
"""

import os
from datetime import date, timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donor_finder.settings')
django.setup()

from donors import db  # noqa: E402  (needs Django settings loaded first)


def days_ago(n):
    return (date.today() - timedelta(days=n)).isoformat() if n else ''


# (name, blood group, city, age, days since last donation; 0 = never donated)
SAMPLE = [
    ('Aarav Sharma', 'O+', 'Pune', 24, 0),
    ('Priya Patil', 'A+', 'Pune', 29, 120),
    ('Rohan Deshmukh', 'B+', 'Pune', 33, 30),
    ('Sneha Kulkarni', 'O-', 'Pune', 27, 200),
    ('Imran Shaikh', 'AB+', 'Pune', 41, 0),
    ('Kavya Nair', 'A-', 'Mumbai', 22, 95),
    ('Vikram Singh', 'B+', 'Mumbai', 36, 0),
    ('Fatima Khan', 'O+', 'Mumbai', 31, 45),
    ('Rahul Joshi', 'A+', 'Mumbai', 45, 150),
    ('Ananya Iyer', 'B-', 'Mumbai', 26, 0),
    ('Arjun Reddy', 'O+', 'Nashik', 38, 10),
    ('Meera Pawar', 'A+', 'Nashik', 34, 0),
    ('Siddharth Rao', 'AB-', 'Nashik', 50, 300),
    ('Pooja Gupta', 'B+', 'Nagpur', 23, 0),
    ('Karan Mehta', 'O+', 'Nagpur', 28, 365),
    ('Zoya Ansari', 'A+', 'Nagpur', 30, 60),
]

db.collection.delete_many({})
for i, (name, group, city, age, ago) in enumerate(SAMPLE):
    db.add_donor({
        'name': name,
        'blood_group': group,
        'city': city,
        'phone': f'98765432{i:02d}',  # fake numbers for the demo
        'age': age,
        'last_donation': days_ago(ago),
    })
print(f'Added {len(SAMPLE)} sample donors.')
