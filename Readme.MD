# Arify web-server

This repository contains the backend code that powers [Arify android app project](https://github.com/shiva-reddy-uic/arify-android-client).  The web server uses django framework to serve and process requests from the app. It uses a sqlite db, and depends on Amazon S3 web service for file storage. 

The app provides:-

 - UI functionality to be able to upload AR objects into the service.
 - APIs used by the android app to update and pull AR objects


## Setup

The app is a django project. It will have to be deployed on a web server before Arify app to communicate with it. The backend server also requires an AWS S3 bucket to be setup.

The following 3 environment variables need to be set up for the app to work:-
 1. env -> The environment in which the server is operating.
 2. S3_KEY -> The Aws S3 key.
 3. S3_SECRET -> The AWS S3 secret key
 
[Web site link] (
https://lh3.googleusercontent.com/-1QU-X8HsdqJf1eB9Aefz8lLRzIryKrbiJhJKV5gqdEaY4-LjtNNLqDJoFX-wEb_NSqhjKwyXDuFMF2v6v9EiAJG-Ow6qp0WX1w2I4K3dIrA9k8O1ekNb4THtFK9BlWQeKlMY-z4A4WriGZxa9OetGMDa-uoFxehSabnNLSVn2vGW_IzTi1BH-UgQyOs1q-9YmDV23T_s1SynR-1UrIFr8lVWv3QVxIN3ZbyR97M1Hp-5aP0PGXH2OU5EEFt97ABo-rtY3jZ-GbrWAPN2DowbSJGFpicJvTH07oqJwNsNSWD1ybJtMVjMj3lCaLlgBWwIuhWNb3cMMwCM8A5IXe2DbtFnOZVpGA-BBpv-fBlchiJsSoRvZ5IV7RDfrEoznjEuPSOE5Z3VH8aH4kekL7VQ1-u3_baPdMuVK3hrLOvxsecYLgKg1dpDsRYCvhSE-T0gnR7raBFXpWp3KN6IhlheITYKQvL-yfmt_mAq1mlmKRJZY0j2eQkK_0fTpOlb4wINRXN5iXSYALMLZsKSO3Kj4tcRsayDs20klICYcODIXHZTfFn_DwqeU0r7ehOrGurb-1DCEnBUnnS2Z3TQTr1EbG6ZB1VpLNj_MTjDOE6eqabSZmYtGx_2-m7OpsYf_2WNOdEbmdz9LnEiEwYJNIYuRa35CHhMZXXmQUU294R4UZFITq9eSqn1Xs=w769-h867-no)
