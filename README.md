# Team Builder
Project 12 of the Python Web Development Techdegree program

This is a site where people can sign up to find projects that need help 
or post their own projects for other people to join. Users are able to create
a profile with an avatar, a bio, and pick skills from a list or add custom
skills that can be used to help connect them with projects.

Users can post also post projects with a title, description, and positions
they need filled.

Users can find a project and ask to join it. The project owner can approve
or deny the person asking to join.

## Installation

1. Download the project and change into the project directory.
    (This is the directory containing `manage.py`.)
2. Create a new virtual environment.
    -`python -m venv env`
3. Activate the virtual environment.
    - Windows: `.\env\Scripts\activate`
    - Linux/Mac: `source env/bin/activate`
4. Install the project's Python dependencies.
    - `pip install -r requirements.txt`
5. Run migrations to initialize the database.
    - `python manage.py migrate`
6. Load the example data to test functionality.
    - `python manage.py loaddata exampledata.json`

The example data loads multiple user accounts.
Use the following to log into an administrator account with a completed
profile and multiple projects and applications:

- Username: `zorbert@example.com`
- Password: `test`

The password for all test accounts is `test`, and the username will be
the first name with `@example.com` appended.

#### Important Notes

When testing, user registration emails as well as notifications for application
status can be found in the `test_emails` folder, which is in the main project
directory.

To edit your user avatar, use the button that appears in the upper right corner
of your avatar on the Edit Profile page after you have uploaded an image and
saved your profile. This will open a basic image editor.

You can use Markdown on the profile and project pages by activating the
Markdown option on your profile page.

Select `Show only projects that need my skills` on the index/search pages
to filter open projects for your skills.