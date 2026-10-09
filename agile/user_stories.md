# Blood Donor Finder: User Stories

**Problem:** In a medical emergency, families search for blood donors by forwarding WhatsApp messages and calling people at random. Many of those people have the wrong blood group, or donated recently and are not allowed to donate again yet. Precious time is lost.

**Solution:** A web app where donors register once. In an emergency, you enter the patient's blood group and city. The app lists only donors who are **medically compatible** and **allowed to donate today** (90 days since their last donation), with donors from the same city first. A dashboard warns which blood groups are running short.

**Sprint:** 1 sprint, 10 working days
**Total story points:** 30
**Story point scale:** 1, 2, 3, 5, 8 (Fibonacci). Bigger number = more work.

---

## Sprint Backlog (completed in Sprint 1)

### US-01: Register as a donor (3 points)
**As a** willing blood donor,
**I want to** register my name, blood group, city, phone, age and last donation date,
**so that** patients can find me when they need blood.

Acceptance criteria:
- The form has Name, Blood group (dropdown), City, Phone, Age and Last donation date fields.
- The last donation date is optional (blank = never donated).
- Refreshing the page after registering does not register the donor twice.

### US-02: View all donors (2 points)
**As a** blood bank volunteer,
**I want to** see a list of all registered donors with their status,
**so that** I know who is ready to donate and who is resting.

Acceptance criteria:
- The table shows Name, Blood group, City, Phone, Age and Status.
- Status is **Ready**, or **Resting until <date>** for donors who donated in the last 90 days.

### US-03: Input validation (3 points)
**As a** volunteer,
**I want** wrong data to be rejected with a clear message,
**so that** the donor list only has correct, reachable contacts.

Acceptance criteria:
- Empty name or city, an invalid blood group, a phone number that is not 10 digits, an age outside 18 to 65, or a future donation date is rejected.
- The error is shown in red at the top of the page.
- The values already typed stay in the form.

### US-04: Save donors permanently (5 points)
**As a** volunteer,
**I want** donors saved in a database,
**so that** the list is still there after the server restarts.

Acceptance criteria:
- Donors are stored in a MongoDB collection called `donors`.
- If the database cannot be reached, the app shows an error message instead of crashing.

### US-05: Emergency donor search (5 points)
**As a** patient's family member,
**I want to** enter the patient's blood group and city and get a list of donors I can call right now,
**so that** I don't waste time calling people who cannot donate.

Acceptance criteria:
- Only blood groups that can safely give to the patient's group are shown (for example, an A+ patient can receive from A+, A-, O+ and O-).
- Donors who donated in the last 90 days are not shown, but their count is mentioned.
- Donors in the same city come first, then exact blood group matches.
- The phone number is a clickable call link.

### US-06: Record a donation (2 points)
**As a** volunteer,
**I want to** mark that a donor gave blood today,
**so that** the app stops showing them in searches for the next 90 days.

Acceptance criteria:
- Ready donors have a **Donated today** button.
- Clicking it sets the last donation date to today and changes the status to Resting.

### US-07: Remove a donor (2 points)
**As a** volunteer,
**I want to** remove a donor who no longer wants to be listed,
**so that** we respect their choice and keep the list up to date.

Acceptance criteria:
- Each row has a **Remove** button, which deletes the donor from the database.
- An invalid or old link does not crash the app.

### US-08: Donor dashboard (5 points)
**As a** blood bank organiser,
**I want to** see the number of donors per blood group and per city, with charts,
**so that** I understand the donor base at a glance.

Acceptance criteria:
- The dashboard shows total donors, ready donors, resting donors, cities covered and age statistics.
- A table shows registered and ready donors for **all 8** blood groups, including groups with 0 donors.
- A bar chart shows ready donors per blood group, and a pie chart shows donors per city.

### US-09: Shortage alert (3 points)
**As a** blood bank organiser,
**I want to** be warned which blood groups have too few ready donors,
**so that** I can run a donation drive before an emergency happens.

Acceptance criteria:
- A blood group with fewer than 2 ready donors is marked as a shortage.
- The dashboard lists shortage groups in a red alert box, and their bars in the chart are red.

---

## Product Backlog (future sprints)

| ID | Story | Points |
|----|-------|--------|
| US-10 | As a patient's family member, I want matching donors to get an SMS/WhatsApp alert, so that they respond faster. | 8 |
| US-11 | As a donor, I want to log in and update my own details, so that my information stays correct. | 8 |
| US-12 | As a patient's family member, I want to see donors on a map, so that I can find the nearest one. | 5 |
| US-13 | As a hospital, I want to post a blood request, so that donors can see who needs blood right now. | 5 |

---

## Sprint 1 Progress (data used for the burndown chart)

| Day | Work done | Story completed | Points left |
|-----|-----------|-----------------|-------------|
| 0 | Sprint planning | - | 30 |
| 1 | Django project setup, MongoDB install | - | 30 |
| 2 | Donor registration form | US-01 (3) | 27 |
| 3 | Donor list table | US-02 (2) | 25 |
| 4 | MongoDB storage + error handling | US-04 (5) | 20 |
| 5 | Validation with exceptions | US-03 (3) | 17 |
| 6 | Researching blood compatibility and 90-day rule (no story finished) | - | 17 |
| 7 | Emergency search page | US-05 (5) | 12 |
| 8 | Donated today + Remove buttons | US-06 (2), US-07 (2) | 8 |
| 9 | Dashboard with Pandas + charts | US-08 (5) | 3 |
| 10 | Shortage alert, final testing | US-09 (3) | 0 |
