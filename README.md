# SaaS for Enterprise with Django
Learn how to build an Enterprise SaaS project using Django, Neon Postgres, TailwindCSS, SaaS Starter Code, and more. Enterprise SaaS means we need a a way to isolate customer data by implementing multi-tenancy, subdomain-based auth, and much more. We start with an existing Django application and build on top of that.

## Need help?
Use [the discussions tab](https://saasgorillas.com/discussions).

## Before you start

I recommend you know some of the following:
- __Python__
  - Such as _classes_, _functions_, _variables_, _math operations_, _installing_, _setting up virtual environments_
  - If you're new to Python, watch up to day 15 of [30 Days of Python](saasgorillas.com/python1)(free)
- __Django basics__
  - Such as _views_, _URL routing_, _models_ and _migrations_, _users_ and auth _login_
  - If new to Django, watch [Your First Django Project](https://saasgorillas.com/django1)(paid) or [Try Django 3.2](https://saasgorillas.com/django2)(free)
- __SaaS fundamentals with Django__ (Optional).
  - Such as Stripe integration, groups, user permissions,
  - Consider watching SaaS Foundations course on [YouTube](https://www.youtube.com/watch?v=WbNNESIxJnY) or on [CFE](https://saasgorillas.com/pre)
  - Review the SaaS starter code on [GitHub](https://github.com/codingforentrepreneurs/SaaS-Foundations)(open source) or [cfe.run](https://get.cfe.run)(managed)

## Links
- [Code](https://saasgorillas.com/code)
- SaaS Starter Code on [GitHub](https://github.com/codingforentrepreneurs/SaaS-Foundations)(open source) or [cfe.run](https://get.cfe.run)(managed)
- Course (coming soon)
- [Neon Postgres](https://saasgorillas.com/db) (our course sponsor)

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
- Python 3+
- [django-hosts](https://django-hosts.readthedocs.io/en/latest/) - Subdomain handling in Django
- [Neon Postgres](https://kirr.co/ffogxb) - Serverless postgres + near instance database loading
- Django SaaS Starter code via [GitHub](https://github.com/codingforentrepreneurs/SaaS-Foundations)(open source) or [cfe.run](https://get.cfe.run)(managed)
- `psycopyg[binary]` and `dj-database-url` - Loading postgres
- and more

> Note: [django-tenants](https://github.com/django-tenants/django-tenants) is not used in this course. While Django Tenants is a _very good tool_ it requires you to start with Django tenants for your SaaS projects. This tutorial does not. django-tenants was instrumental in designing this course. Once you finish the course, I encourage you to play around with django-tenants!


## Definitions

Read the course-specific definitions [on the GitHub discussions](https://github.com/codingforentrepreneurs/SaaS-for-Enterprise-with-Django/discussions/1). This course has a number of definitions that are specific to multi-tenant, enterprise-ready, Django SaaS projects _and_ specific to this course.


