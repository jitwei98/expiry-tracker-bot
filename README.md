# Dockerizing Django with Postgres, Gunicorn, and Nginx

## API Endpoints
1. GET, POST `/api/food`

        CRUD on the list of food

1. GET `/api/notify?item={item_name}&chat_id={chat_id}`

        Call this endpoint to prompt user (identified by the chat_id) for an expiry date for food with <item_name> on Telegram

1. GET `/api/expiry`

        Get the latest expiry date (d-m-yyyy) from user (manual input), default to 3 days after today

1. GET `/api/set-expiry?date={date_string}`

        Set expiry date to <date_string> 

Note: Remember to `POST` the complete Food object (with the expiry date) to `/api/food`

## Want to learn how to build this?

Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

## Want to use this project?

### Development

Uses the default Django development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
