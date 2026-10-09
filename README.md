# Blood Donor Finder (ITL-V Project)

**Problem:** In a medical emergency, families hunt for blood donors through WhatsApp forwards and random calls. Most people they reach have the wrong blood group, or donated recently and are not allowed to donate again yet.

**Solution:** A Django web app where donors register once. In an emergency, you enter the patient's blood group and city, and the app lists only donors who are **medically compatible** and **allowed to donate today** (90 days since their last donation), with donors from the same city first. A dashboard uses Pandas and Matplotlib to warn which blood groups are running short.

## Folder Structure

```
itl 5/
├── blood_donor_finder/              Django project
│   ├── manage.py                    Runs the server
│   ├── seed.py                      Loads 16 sample donors for a demo
│   ├── requirements.txt
│   ├── blood_donor_finder/          Project settings
│   │   ├── settings.py              MONGO_URI is here
│   │   └── urls.py                  Sends every URL to the donors app
│   └── donors/                      The app
│       ├── urls.py                  /  /search/  /dashboard/  /donated/<id>/  /delete/<id>/
│       ├── views.py                 Handles requests (the View in MVT)
│       ├── db.py                    MongoDB insert / find / update / delete (the Model in MVT)
│       ├── logic.py                 Validation, compatibility search, Pandas/NumPy/Matplotlib
│       └── templates/donors/        HTML pages (the Template in MVT)
└── agile/
    ├── user_stories.md              User stories, story points, sprint progress
    ├── kanban.html                  Kanban board (open in a browser)
    ├── burndown.py                  Generates the burndown chart
    └── burndown.png                 Burndown chart image
```

## How to Run

1. Install the packages:
   ```
   cd blood_donor_finder
   pip install -r requirements.txt
   ```
2. Put your MongoDB connection string in `blood_donor_finder/settings.py` (`MONGO_URI`).
   The default `mongodb://localhost:27017` works if MongoDB is installed on your PC.
3. Load the sample donors (optional, but good for a demo). This deletes all existing donors first:
   ```
   python seed.py
   ```
4. Start the server:
   ```
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000 in your browser.

Optional self-check (does not need MongoDB): `python donors/logic.py`

## Pages

| Page | URL | What it does |
|---|---|---|
| Donors | `/` | Register a donor, see all donors with Ready/Resting status, record a donation, remove a donor |
| Find Donors | `/search/` | Enter the patient's blood group and city, get compatible donors who can donate today |
| Dashboard | `/dashboard/` | Statistics, shortage alert, bar chart per blood group, pie chart per city |

## The Two Medical Rules

1. **Compatibility** is stored in a dictionary of sets, `CAN_RECEIVE_FROM` in `logic.py`. For example, `'A+': {'A+', 'A-', 'O+', 'O-'}`. O- can give to everyone (universal donor). AB+ can receive from everyone (universal receiver).
2. **90-day gap:** after donating whole blood, a person must wait 90 days. `add_status()` adds 90 days to the last donation date. If that date is today or earlier, the donor is **Ready**. Otherwise they are **Resting**.

## How It Works (Flow of Control)

Example: searching for donors for an A+ patient in Pune.

1. The browser requests `/search/?blood_group=A+&city=Pune`.
2. `blood_donor_finder/urls.py` passes the request to `donors/urls.py`, which picks the view `search`.
3. The view calls `db.all_donors()`, which reads the donor documents from MongoDB.
4. `add_status()` marks each donor as Ready or Resting (90-day rule).
5. `find_donors()` uses a **list comprehension** to keep only compatible, ready donors. Then it sorts them with a **lambda**: same city first, then exact group match, then by name.
6. The view renders `search.html`, and Django sends the HTML back to the browser.

On the dashboard, `build_dashboard()` uses:
- **Pandas**: turns the list into a DataFrame, uses `groupby` to count donors per blood group, `reindex` so all 8 groups appear (even with 0 donors), and `value_counts` per city.
- **NumPy**: mean, min and max age.
- **Matplotlib**: a bar chart (shortage groups in red) and a pie chart, saved as PNG images in memory.

When a donor registers, `parse_donor()` checks the input. Bad input raises a `ValueError`, which the view catches and shows as a red message. If MongoDB is down, the view catches `PyMongoError` and shows an error instead of crashing.

|
