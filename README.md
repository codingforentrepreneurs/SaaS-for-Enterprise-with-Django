# SaaS for Enterprise with Django
Enterprise customers often need data isolated from other users. It's known as multi-tenant. This repo is reference code for the related course. 

## Before you start

I recommend you know some of the following:
- __Python__
  - Such as _classes_, _functions_, _variables_, _math operations_, _installing_, _setting up virtual environments_
  - If you're new to Python, watch up to day 15 of [30 Days of Python](https://www.youtube.com/playlist?list=PLEsfXFp6DpzQjDBvhNy5YbaBx9j-ZsUe6)
- __Django basics__
  - Such as _views_, _URL routing_, _models_ and _migrations_, _users_ and auth _login_
  - If new to Django, watch [Your First Django Project](https://www.codingforentrepreneurs.com/courses/your-first-django-project) or [Try Django 3.2](https://www.youtube.com/playlist?list=PLEsfXFp6DpzRMby_cSoWTFw8zaMdTEXgL)
- __SaaS fundamentals with Django__ (Optional).
  - Such as Stripe integration, groups, user permissions,
  - Consider watching [SaaS Foundations](https://www.youtube.com/watch?v=WbNNESIxJnY)

## Links
- [Code](https://github.com/codingforentrepreneurs/SaaS-for-Enterprise-with-Django)
- Course (coming soon)
- [Neon Postgres](https://kirr.co/ffogxb) (our course sponsor)

## Topics

- What, when, and why of multi-tenant apps (e.g. SaaS apps that need to keep enterprise data isolated)
- Levels of helping enterprise customers (e.g. when not to use multi-tenant)
- Implementing a multi-tenant in Django
- Per-tenant (per enterprise customer) login
- User data isoloation (via Postgres Schemas and Neon Databases)
- Custom migrations for Django models; for standard Django and Enterprise customers
- Django-hosts for subdomain routing and handling


## Tech stack

- Django 5+
- Python 3
- [django-hosts](https://django-hosts.readthedocs.io/en/latest/) - Subdomain handling in Django
- [Neon Postgres](https://kirr.co/ffogxb) - Serverless postgres + near instance database loading
- `psycopyg[binary]` and `dj-database-url` - Loading postgres
- and more

> Note: [django-tenants](https://github.com/django-tenants/django-tenants) is not used in this course. While Django Tenants is a _very good tool_ it requires you to start with Django tenants for your SaaS projects. This tutorial does not. django-tenants was instrumental in designing this course. Once you finish the course, I encourage you to play around with django-tenants!


