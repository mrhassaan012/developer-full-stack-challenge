# Run Project Locally

### Prerequisites
1. **Visual Studio Code:** Make sure you have [Visual Studio Code (VS Code)](https://code.visualstudio.com/) installed on your system.
2. **Docker:** Ensure that [Docker](https://www.docker.com/get-started) is installed and running on your machine.

### Install Visual Studio Code Extensions
Install the `Remote - Containers` extension for VS Code. This extension allows you to open a project folder inside a container.

### Open the Project Folders
1. Launch Visual Studio Code in 2 different windows.
2. Open the `src/api` folder of your project in one window that contains the `.devcontainer` folders and the `.devcontainer/docker-compose.yaml`.
4. Open the `src/dashboard` folders of your project in 2nd window that contains the `.devcontainer` folders and the `.devcontainer/docker-compose.yaml`.
5. VS Code should automatically detect it and prompt you to reopen the folder in a container. You can also manually select this option by clicking on the green icon in the bottom left corner of VS Code (it looks like a green rectangle with a white arrow).
6. On opening dev container window, it should prompt `starting dev containers (show logs)`, you can click to show logs about building docker image (will take some time).
7. `Port forwarding [some port] > [some port] > [some port] stderr: Connection established` is the indication that container is running. Run Frontend at [http://localhost:3000](http://localhost:3000)

### Run Project
Visit [http://localhost:3000](http://localhost:3000) (if not accessible go to ports tab in integrated terminal and add port 8000 for api and 3000 for dashboard)
If you are not authenticated, you will be redirected to `/login`.
Login credentials:
- Username: `testuser`
- Password: `testuser123`

To view the API documentation for FastAPI, visit [http://localhost:8000/docs](http://localhost:8000/docs).


## Building and Starting Containers
Visual Studio Code will automatically build and start the containers defined in your `docker-compose.yaml` file, including any necessary dependencies.

## Development Environment Inside the Container
Once the containers are up and running, your development environment will be inside the container. You can open terminal windows, install packages, run commands, and use VS Code's integrated development features just as you would on your local machine.

## Exit the Container
To exit the container and return to your local environment, you can use the "Remote-Containers: Reopen Locally" command from the command palette.

## Save and Commit Changes
Any changes you make to the project folder will be reflected inside the container, and you can commit your changes to version control.

# DataCose Full Stack Challenge

The goal of this challenge if to create a Nuxt frontend with a FastAPI backend matching the objectives down below.

To bootstrap this project, we've used a basic [Nuxt 2](https://nuxtjs.org/) and [FastAPI](https://fastapi.tiangolo.com/lo/) template. There is a Dockerfile available in case you want to work with Docker during development, but this is not a requirement.

The usage of the following packages is mandatory:
- Nuxt
    - BootstrapVue
    - [VueTreeselect](https://vue-treeselect.js.org/) (you need to install this yourself)
- FastAPI
    - Pydantic
    - SQLAlchemy (you need to install this yourself)

To store your data you can either use a sqllite database file, or use a local Postgres database (preferred).

If you choose to use a Postgres database, please provide a seed-file with some dummy data and a migration file to setup the database schema.

In case you use sqllite, provide the database file.

## Objectives

Create a username/password protected app that authenticates API requests using Bearer tokens (not session tokens). Store the user credentials in your database and allow us to sign in using the frontend (please provide the credentials for one user, no need to create functionality to create users). All pages, except for the login page, should be inaccessible when not signed in.

### Data schema

The portal will be used to manage data about authors and their books. An author can have zero or more books, a book always has an author. An author just has a required name field. Books have a required name field, and a required page numbers field.


### Pages
In the portal, there should be two pages (+ a login page). Make sure a user can navigate to both pages using a nav-bar layout.

#### Authors
On this page, render a paginated table of authors with the following columns:
- Name
- Number of books (this is calculated based on the books)

On top of this page, add an input field that is used to search for authors. Next to it, create a button that opens a modal to add a new author. When clicked on a table row, show a modal to edit the author. Make sure any changes can be saved to the database.

The modal to add/edit an author should a name field (of the author) + a table with the books of the authors (name + number of pages). A user should be able to add, edit or delete a book.

#### Books
On this page, render a paginated table of books with the following columns:
- Name
- Author name
- Number of pages

On top of this page, add an input field that is used to search for books. Next to it, create a button that opens a modal to add a new book. When clicked on a table row, show a modal to edit the book. Make sure any changes can be saved to the database.

The modal to add/edit a book should have three fields:
- Name
- Number of pages
- Author (should be a searchable treeselect with authors)

## Notes
The usage of the provided template is mandatory. Submissions not written in this template, will not be reviewed. Writing tests is not mandatory, but doing so will give you bonus points.
