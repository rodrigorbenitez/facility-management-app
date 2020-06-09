# facility-management-app
A maintenance app tracker in flask

Application for monitoring maintenance or service work orders. Features: User login, Mail to users, Download PDF reports, Modification and creation of data in SQL database. URL:
URL: https://mantenimientoapp.herokuapp.com/
# facility-management-app
Note: I made this project for the Facility deparment of CBN Group SA.<br>

## Live preview link <a href = 'https://mantenimientoapp.herokuapp.com/' > https://mantenimientoapp.herokuapp.com/ </a>


# `App name:` Facility App'

``Breif description:`` Application for monitoring maintenance or service work orders. Features: User login, Mail to users, Download PDF reports, Modification and creation of data in SQL database.

* For a demo use the following login details:
USER: "user1"
PASSWORD: "33790316"

## Built With

* [Javascript] (https://www.javascript.com/) - High-level, interpreted programming language
* [Jquery] (https://jquery.com/) -JavaScript library
* [Bootstrap] (https://getbootstrap.com/) - Front-end framework
* [HTML] (https://www.html.com/) - Standard markup language
* [CSS] (https://css.com) - Style sheet language
* [Python] (https://www.python.org/) - Interpreted, high-level, general-purpose programming language.
* [Flask] (https://flask.palletsprojects.com/) - Flask is a micro web framework written in Python.
* [PostgreSQL] (https://www.postgresql.org/) - PostgreSQL, also known as Postgres, is a free and open-source relational database management system emphasizing extensibility and SQL compliance.


Server used:
heroku.com (Thank you for free web service)

### Running:

1. Clone this repositiory  or Download Source files
2. Run ```pip install -r requirements.txt``` in your terminal/CMD window to make sure that all of the necessary Python packages are installed.
3. Run ```python app.py``` to run the app
4. Done

## Features:

**Login:**  Users, once registered, are able to log in to the website with their username, email and password.

**Registration:** For security only the administrator can create users and change passwords.

**Logout:** Users can log out from the website by clicking on the logout button.

**Dashboard:**  Once a user has logged in, they are taken to a page where they can see the work orders counting and charts.

**work orders generation:**  Users can create work orders clicking in "generar os" button, oppened in a new tab.

**work orders list:**  Clicking on "Buscador OS" users can search by any attribute of the work order, and get access to a list of the total of work orders in the database.

**work orders ID:**  Clicking on the ID in the work order list, users can acces to a form to edit the work order. If the work order is not assigned to that user, It isn't allowed to edit the work order.'

**Work Order Detail:** Clicking on the "eye" icon in the work orders list, users can get a work order sheet and if they want, download a pdf file.

**Work Order notes:** When a user is editing a work order, in the work order form, they can add notes. Any user that has acces to the work order can add notes.

**your work orders list:**  Clicking on "mis ordenes" users can search by any attribute of the work order, and get access to a list of work orders that are required or assigned by the user.

**assets tracker:**  Clicking on "Equipos" users can  get access to a list of the total of assets that are in the database. Clicking on the detail icon users can get acces to a list of work orders assigned to that asset.

**Email sending:**  When a user creates a work order, an email is sent to the user to whom the created work order belongs.


## Acknowledgments

* HARVARDX Web Programming with Python and JavaScript