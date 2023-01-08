## Projects and Tasks API.

### The API was built with Django REST Framework.

#### API features include:

1.  Built with docker and docker compose. The containers are for development. They are not production ready. Database used is PostgreSQL.

2.  Swagger API documentation.

3.  Token authentication system with custom user model and manager.

4.  Unit Tests with 96% code coverage.

5.  Cached using Redis and Django-Redis.

6.  CRUD Projects API:

    -   Contains a title, description, progress and finish date.
    -   personal access (only the owner can view and edit it and it’s tasks)
    -   The progress is automatically updated using the associated tasks' average progress

7.  CRUD Task API.

    -   Contains a title, description, tags, parent project, progress and finish date.

    -   The progress is the completion percentage of the task. It is updated manually
        from the project/task owner. When the task is completed, the progress is not editable.

    -   The tags are user-defined strings that are used for the logical grouping
        of tasks under a project and are passed optionally as a query parameter
        on the task read operations.

8.  Search Filtering for the Projects and Tasks.

#### Details:

With docker installed, run `docker-compose build`
Then, you can run the tests separately by runing `docker-compose run --rm app sh -c "python manage.py test"`
or you can run `docker-compose up` .

Running the `docker-compose up` makes all the migrations, runs the tests, generates a code coverage report and runs the local server.
Three containers are created. The app, the database and the cache containers.

[![image](https://www.linkpicture.com/q/test_coverage.jpg)](https://www.linkpicture.com/view.php?img=LPic63b7eca23ce991982202688)

#### Confirming the cache is working:

[![image](https://www.linkpicture.com/q/cache.jpg)](https://www.linkpicture.com/view.php?img=LPic63b7eca23ce991982202688)
