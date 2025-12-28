<p align="center">
  <img src="/planing/logo.png" alt="Clinic-Z Logo" width="280"/>
</p>

# Clinic-Z (aka SmartHospital)

Minimal, API-first hospital management backend built with **Django + Django REST Framework**. Designed for modular growth, clear separation of concerns, and predictable production scaling.

---

## Database design

<img src="/planing/clinic-z.png" alt="Database diagram" style="display:block; margin:12px 0; max-width:100%;"/>

* Key tables: `users` (UUID PK), `patients`, `doctors`, `appointments`, `available_times`, `reviews`, `qualifications`.
* Relationships: normalized one-to-many and many-to-many where appropriate (doctor ↔ specializations, doctor ↔ qualifications, patient ↔ appointments).
* Scalability choices: UUID primary keys for horizontal safety, targeted indexes on `email`, `user_id`, and `appointment_time`, and normalized schema to avoid redundancy.
* Media & files: media stored via configured `MEDIA_ROOT` with adapters for S3/R2 in production; media references kept in a dedicated table/field to simplify migration.

---

## API structure

<img src="/planing/api-structure.png" alt="API structure" style="display:block; margin:12px 0; max-width:100%;"/>

Routing follows `/v1/api/` base path and modular Django apps (users, patient, doctor, appointment, public_portal, operations). Each app exposes viewsets/serializers and dedicated routers; versioning is applied at the URL level for safe evolution.

---

## Features & Scalability

**Implemented features**

* Authentication: registration, OTP activation, JWT (access/refresh), token verify/refresh, password reset (OTP).
* Patient management: profile, list, self profile (`patients/me/`).
* Doctor management: public listing, profile management, qualifications, available times.
* Scheduling: appointment creation and status workflow (patient & doctor views).
* Reviews & feedback: doctor reviews, public contact / bug reports.
* Public portal: public doctor list, services, public reviews.
* API docs: OpenAPI schema + Swagger UI.

**Scalability / separation of concerns**

* Containerized: `docker compose` development, discrete `backend` service.
* Modular apps: swap DB, add caching, and resume background workers independently (Postgres / Redis / Celery path ready).

---

## Authentication API

<img src="/planing/authentication-api.png" alt="Authentication flow" style="display:block; margin:12px 0; max-width:100%;"/>

* Flow (minimal): `Register → OTP activation → JWT login (access/refresh) → token refresh / verify → password reset (OTP)`.
* Typical endpoints: `/v1/api/user/register/`, `/v1/api/user/account/activate/`, `/v1/api/user/login/`, `/v1/api/user/token/refresh/`, `/v1/api/user/token/verify/`, `/v1/api/user/forget-password/` (OTP flows follow same pattern).

**Examples (curl)**

Register + activate OTP (example):

```bash
# 1) Register (returns pending verification)
curl -s -X POST /v1/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass1234"}'

# 2) Activate (OTP delivered via email/SMS)
curl -s -X POST /v1/api/user/account/activate/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","otp":"123456"}'
```

Login + token refresh:

```bash
# 1) Login -> returns {"access":"<jwt>","refresh":"<refresh_token>"}
curl -s -X POST /v1/api/user/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass1234"}'

# 2) Refresh access token
curl -s -X POST /v1/api/user/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

---

## Project API overview

### User / Auth

| Method | Path                                      |                        Purpose |           Auth          |
| ------ | ----------------------------------------- | -----------------------------: | :---------------------: |
| POST   | /v1/api/user/register/                    |              Register new user |            No           |
| POST   | /v1/api/user/account/activate/            |         Activate account (OTP) |            No           |
| POST   | /v1/api/user/account/activate/otp/resend/ |          Resend activation OTP |            No           |
| POST   | /v1/api/user/login/                       | Login (may require OTP verify) |            No           |
| POST   | /v1/api/user/login/otp/resend/            |               Resend login OTP |            No           |
| POST   | /v1/api/user/login/otp/verify/            |               Verify login OTP |            No           |
| POST   | /v1/api/user/token/refresh/               |             Refresh JWT access | No (uses refresh token) |
| POST   | /v1/api/user/token/verify/                |          Verify token validity |            No           |
| POST   | /v1/api/user/change-password/             |         Change password (auth) |           Yes           |
| POST   | /v1/api/user/forget-password/             |   Request password reset (OTP) |            No           |
| POST   | /v1/api/user/forget-password/otp/send/    |        Send password reset OTP |            No           |
| POST   | /v1/api/user/forget-password/otp/resend/  |            Resend password OTP |            No           |
| POST   | /v1/api/user/forget-password/confirm/     |         Confirm password reset |            No           |
| GET    | /v1/api/user/list/                        |             List users (admin) |           Yes           |

### Patients

| Method           | Path                                    |                     Purpose | Auth |
| ---------------- | --------------------------------------- | --------------------------: | :--: |
| GET              | /v1/api/patient/patients/               |               List patients |  Yes |
| GET              | /v1/api/patient/patients/{user__email}/ |            Patient by email |  Yes |
| GET              | /v1/api/patient/patients/me/            |          My patient profile |  Yes |
| PUT/PATCH/DELETE | /v1/api/patient/patients/me/            | Update / delete own profile |  Yes |

### Doctors

| Method           | Path                                 |                 Purpose | Auth |
| ---------------- | ------------------------------------ | ----------------------: | :--: |
| GET              | /v1/api/doctor/list/                 |      Public doctor list |  No  |
| GET              | /v1/api/doctor/profile/{user__email} | Doctor profile by email |  No  |
| GET              | /v1/api/doctor/profile/me/           |       My doctor profile |  Yes |
| PUT/PATCH/DELETE | /v1/api/doctor/profile/me/           |      Manage own profile |  Yes |

### Appointments

| Method   | Path                                           |                               Purpose | Auth |
| -------- | ---------------------------------------------- | ------------------------------------: | :--: |
| GET/POST | /v1/api/appointment/doctor/                    |  Doctor-side appointments list/create |  Yes |
| PATCH    | /v1/api/appointment/doctor/{id}/update_status/ |             Update appointment status |  Yes |
| GET/POST | /v1/api/appointment/patient/                   | Patient-side appointments list/create |  Yes |

### Public portal (user-feedback / website)

| Method | Path                                       |               Purpose | Auth |
| ------ | ------------------------------------------ | --------------------: | :--: |
| POST   | /v1/api/public-portal/contact-us/          |   Submit contact form |  No  |
| POST   | /v1/api/public-portal/report-bug/          |     Submit bug report |  No  |
| GET    | /v1/api/public-portal/list/doctor/         |    Public doctor list |  No  |
| GET    | /v1/api/public-portal/list/doctor/reviews/ | Public doctor reviews |  No  |
| GET    | /v1/api/public-portal/services/            |  Public services list |  No  |

### Doctor metadata (available times, designation, specialization)

| Method               | Path                                    |                                      Purpose | Auth |
| -------------------- | --------------------------------------- | -------------------------------------------: | :--: |
| GET/POST             | /v1/api/doctor/available-times/         | Manage doctor available times (admin/doctor) |  Yes |
| GET/POST             | /v1/api/doctor/available-times-patient/ |       Patient view / request available times |  Yes |
| GET/PUT/PATCH/DELETE | /v1/api/doctor/available-times/{id}/    |                        Available time detail |  Yes |
| GET/POST             | /v1/api/doctor/designations/            |                   Doctor designations (CRUD) |  Yes |
| GET/POST             | /v1/api/doctor/specializations/         |                       Specializations (CRUD) |  Yes |

### Reviews

| Method               | Path                         |                Purpose |         Auth        |
| -------------------- | ---------------------------- | ---------------------: | :-----------------: |
| GET/POST             | /v1/api/doctor/reviews/      |  List / submit reviews | GET: No / POST: Yes |
| GET/PUT/PATCH/DELETE | /v1/api/doctor/reviews/{id}/ | Review detail / manage |         Yes         |

### Qualifications & Operations

| Method | Path                                       |                    Purpose | Auth |
| ------ | ------------------------------------------ | -------------------------: | :--: |
| GET    | /v1/api/doctor/{doctor_id}/qualifications/ | List doctor qualifications |  Yes |
| POST   | /v1/api/doctor/qualifications/apply/       |        Apply qualification |  Yes |
| POST   | /v1/api/operations/apply/to-be/doctor/     |     Apply to become doctor |  Yes |

---

## Getting started (developer quickstart)

1. `git clone <repo>` && `cd repo`
2. copy `.env.example` → `.env` and set vars.
3. `docker compose up --build`
4. `docker compose exec backend python manage.py migrate`
5. `docker compose exec backend python manage.py createsuperuser`
6. `docker compose exec backend python manage.py test`

`.env.example`

```env
SECRET_KEY=replace_me
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=True
MEDIA_ROOT=/data/media
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=secret
JWT_ACCESS_LIFETIME=5m
JWT_REFRESH_LIFETIME=7d
```

---

## Deployment notes

Recommended production stack: **Postgres**, **S3 / R2 for media**, **Redis** (cache + broker), **Celery** (background tasks), **Gunicorn** + **Nginx** as reverse proxy.
For cloud migration: start with Docker Compose for CI/CD, then extract services into Kubernetes manifests (Deployment + Service + Ingress). Convert volume mounts to object storage and attach Redis/Celery as managed services in K8s.

---

## Maintenance & roadmap

* Move primary DB to PostgreSQL and enable partitioning/index review.
* Add Redis caching for hot reads (doctor lists, availability).
* Introduce Celery for async email, reports, and heavy exports.
* Optional: migrate media to S3/R2 and ensure signed URLs for secure media delivery.

---

## Contributing

* File issues for feature requests or bugs; reference minimal repro steps.
* Open PRs against `develop` with tests and linting; include changelog entry.
* CI enforces tests + linters; maintainers will review and merge.

### CODE_OF_CONDUCT

(See repository `CODE_OF_CONDUCT` placeholder file.)

---

## License & authors

Licensed under an open-source license (add `LICENSE` file). Maintainer: `Maintainer Name` — contact via repo issues or maintainer email in `.env`.

---

**Icon example (for README badges):**

```js
// example using react-icons in a docs site
import { FaHospital } from 'react-icons/fa';
// <FaHospital /> used as a small badge next to headings
```

**Assumptions & confidence:** Assumed endpoint behaviors and required payloads from the provided list; where method-level auth is ambiguous, standard conventions were applied. Confidence: **medium** — verify exact auth requirements and payload shapes from the API serializers/views.
