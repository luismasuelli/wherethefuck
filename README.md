Installing this project
=======================

1. Create a docker image with this command:

   ```
   $ docker container create -p 5432:5432 -v $HOME/DockerVolumes/wherethefuck/db --name=postgis_world \
                        -e POSTGRES_USER=postgres -e POSTGRES_PASS=my-insecure-dev-password -e POSTGRES_DBNAME=world \
                        -e POSTGRES_MULTIPLE_EXTENSIONS=postgis kartoza/postgis
   ```

   You will perhaps need to customize some parts of this command, like:

   i. The host: perhaps you will not mount this docker image and, instead, use an external database service (e.g. Amazon).  
   ii. The port: instead of `5432:5432` you may use `whatever:5432` provided `whatever` is a valid an available port number.  
   iii. The docker container's name.  
   iv. The `POSTGRES_USER`, `POSTGRES_PASS` and `POSTGRES_DBNAME` provided you use the *same* names in the django settings.  
   v. Adding comma-separated to `POSTGRES_MULTIPLE_EXTENSIONS` provided you know what you're doing.  

2. work in a Python 3.7 / Django 2.2 virtual environment. Add these packages:

   ```
   Django==2.2.4
   django-map-widgets==0.2.2
   psycopg2==2.8.3
   ```
   
   And other you'd need.

3. Install GDAL library! This part is troublesome and depends on the operating system.

4. Run `python manage.py collectstatic` for the google maps widget to work.

5. For the google maps field, add settings according to [this documentation](https://django-map-widgets.readthedocs.io/en/latest/widgets/point_field_map_widgets.html#settings).
