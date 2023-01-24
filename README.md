# Film and staff database
A simple film-staff relational database made for a university Python course.

## Requirements
This program requires the sqlalchemy package (```pip install SQLAlchemy==1.4.46```) (will add automatic installation later).

## Usage
Run the OfflineClient.py file with the -h flag to know the available options for managing the database. (Soon will add OnlineClient that will communicate with flask webapp)

## Running a the web app version

Whilst you can modify the database offline via the OfflineClient, you can also run a web app running the command `flask run` with a standard environment (app.py being the main app in the environment). Hosting it will allow you to access an API with all the features of the OfflineClient:

### Staff API

| Link                              | HTTP method | Description                                             |
|-----------------------------------|-------------|---------------------------------------------------------|
| /Staff/add                        | POST        | Add staff with data passed in a form via the request    |
| /Staff/remove                     | DELETE      | Remove staff with data passed in a form via the request |
| /Staff/removeid                   | DELETE      | Remove staff with given id in a form via the request    |
| /Staff/clear                      | DELETE      | Remove all staff                                        |
| /Staff?first_name=X&last_name=Y   | GET         | Get list of staff with given name                       |
| /Staff/film/\<id\>                | GET         | Get all films staff with given id has worked on         |

#### Forms in add and remove requests for staff

The required data for these requests are:

| Request             | Required data                               |
|---------------------|---------------------------------------------|
| Add                 | - first_name<br>- last_name<br>- speciality |
| Remove              | - first_name<br>- last_name                 |
| RemoveID            | - id                                        |

### Film API

| Link               | HTTP method | Description                                            |
|--------------------|-------------|--------------------------------------------------------|
| /Film/add          | POST        | Add film with data passed in a form via the request    |
| /Film/remove       | DELETE      | Remove film with data passed in a form via the request |
| /Film/removeid     | DELETE      | Remove film with given id in a form via the request    |
| /Film/clear        | DELETE      | Remove all films                                       |
| /Film/\<name\>     | GET         | Get list of films with given name                      |
| /Film/staff/\<id\> | GET         | Get all staff that worked on film with given id        |

#### Forms in add and remove requests for films

The required data for these requests are:

| Request             | Required data                                     |
|---------------------|---------------------------------------------------|
| Add                 | - name<br>- description<br>- release_date(*)      |
| Remove              | - name                                            |
| RemoveID            | - id                                              |

> (*) - release_date is only the year, not the whole date. E.g. release_date=2005

### Both API

| Link                                       | HTTP method | Description                                                           |
|--------------------------------------------|-------------|-----------------------------------------------------------------------|
| /Both/addstaff?staffid=X&filmid=Y          | POST        | Add staff to a film with their IDs given in a form via the request    |
| /Both/removestaff?staffid=X&filmid=Y       | DELETE      | Remove staff to a film with their IDs given in a form via the request |
