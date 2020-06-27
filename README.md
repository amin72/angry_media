# Angry Media Project

A project which shares users feeling and mistakes during their life

Implemented in django and reactjs.


## How to run the project

- Install packages in **backend/requirements.txt**

- Create settings file in **backend/angrymind/settings.json** and add following keys with their values:
    - Secret key
    - Database

Template for settings.json:
```
{
    "SECRET_KEY": "B9-4=r1A60b+f$xt!2g@z#bc#cpg5^iopasuj2!(4h$+)8ze^fyoy(3n74#')xH",
    "DATABASE_BACKEND": "django.db.backends.postgresql",
    "NAME": "angrymind",
    "USER": "angrymind",
    "PASSWORD": "testpassword",
    "HOST": "",
    "PORT": "5432"
}
```
