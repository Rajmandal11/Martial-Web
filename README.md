# Warrior Martial Arts — Website

A complete, production-quality website for a martial arts school: class styles with detail pages,
a filterable weekly schedule, trainer profiles, membership plans (INR pricing), photo gallery with
lightbox, blog, contact form, free-trial booking with member login, and a full Django admin.

**Live design reference:** the homepage mirrors the "Warrior Martial Arts" mockup (black/red theme,
hero, benefits strip, "Choose Your Style" cards, about/stats band, CTA, rich footer). The member
login page uses a soft neumorphic light theme.

---

## Stack choice

**Django 5.x + server-rendered HTML templates + one hand-written CSS file.** No React, no
Bootstrap, no extra Python packages (requirements: Django only).

Why: a marketing + booking site like this is content-first. One codebase, one `pip install`,
`python manage.py runserver` and it works — easier for Raj to host, extend and hand over than a
split Django API + React SPA. Photos are plain static files referenced by filename (no Pillow /
media uploads), so deployment needs nothing beyond Django itself.

## Quick start

```bash
cd warrior-martial-arts
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate        # create the database
python manage.py seed_demo      # load demo content (idempotent — safe to re-run)
python manage.py createsuperuser  # optional: for /admin access
python manage.py runserver
```

Open http://127.0.0.1:8000/ — the admin is at http://127.0.0.1:8000/admin/.

## Demo credentials

A demo member is created by `seed_demo`:

- username: `demo`
- password: `warrior123`

Log in at **/login/** → redirected to **/member/**, which lists that member's trial bookings.
Staff users also get an "Open Admin" shortcut there.

## What's included

| Page | URL | Notes |
|---|---|---|
| Home | `/` | Hero, benefits, style cards, about + stats, testimonials, CTA |
| About | `/about/` | Story, values, instructor highlights |
| Classes | `/classes/` | All styles; each links to `/classes/<slug>/` detail with schedule, trainers, trial CTA |
| Schedule | `/schedule/` | Mon–Sat grid, filterable by style (`?style=karate`) |
| Trainers | `/trainers/` | Profile cards with specialty + classes taught |
| Membership | `/membership/` | 3 plans: Monthly ₹2,499 / Quarterly ₹6,499 / Yearly ₹21,999 |
| Gallery | `/gallery/` | Grid with keyboard-accessible lightbox |
| Blog | `/blog/`, `/blog/<slug>/` | Seeded with 3 posts |
| Contact | `/contact/` | Saved to DB, visible in admin; success page |
| Free trial | `/free-trial/` | Saved to DB (`Booking`), visible in admin; success page |
| Login | `/login/` | Neumorphic design, Remember-me, demo hint |
| Member area | `/member/` | Login required; shows own bookings |

Admin registers every model; bookings are newest-first and statuses are editable inline.

## Pricing note

Plans are priced in **INR (₹)** since the dojo operates in India. Swap the seeded prices in
`seed_demo.py` (or edit in admin) for any other currency.

## Swapping in real photos

All imagery is AI-generated placeholder art in `dojo/static/dojo/img/` (14 files). To use real
photos: drop your JPGs into that folder with the same filenames (or update the `image` field on
the model in admin), e.g.:

- `hero-fighter.jpg`, `about-warrior.jpg`
- `class-karate.jpg`, `class-bjj.jpg`, `class-muaythai.jpg`, `class-kids.jpg`, `class-kickboxing.jpg`
- `trainer-1.jpg` … `trainer-4.jpg`
- `gallery-1.jpg`, `gallery-2.jpg`, `gallery-3.jpg`

## Running the checks

```bash
python manage.py check
python manage.py test
```

## Project layout

```
warrior-martial-arts/
├── manage.py
├── requirements.txt
├── README.md
├── warrior_site/          # project settings, root urls, wsgi
└── dojo/                  # the app
    ├── models.py          # ClassStyle, Trainer, MembershipPlan, ScheduleSlot,
    │                      # BlogPost, GalleryItem, Testimonial, Booking, ContactMessage
    ├── views.py / urls.py / forms.py / admin.py
    ├── management/commands/seed_demo.py
    ├── templates/dojo/    # 16 templates
    └── static/dojo/
        ├── css/style.css  # warrior theme (no frameworks)
        ├── css/login.css  # neumorphic login theme
        ├── js/main.js     # mobile nav + header shadow
        └── img/           # AI-generated site art (replace with real photos)
```

## Production notes

- Change `SECRET_KEY` and set `DEBUG = False`, `ALLOWED_HOSTS` before deploying.
- Bookings/contact messages currently save to the DB for admin follow-up; wire an email/SMS
  notification in `views.booking` / `views.contact` if you want instant alerts.
