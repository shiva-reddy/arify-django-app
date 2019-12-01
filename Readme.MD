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
 
