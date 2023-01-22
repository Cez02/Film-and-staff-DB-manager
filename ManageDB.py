from sqlalchemy import DateTime, Integer, String
from DBEngine import engine, Session
from FilmDefinitions import Film, Staff

import argparse

parser = argparse.ArgumentParser(description="Manage your film and staff database", conflict_handler="resolve")
subparsers = parser.add_subparsers(help="Pick whether to manage staff or films.", dest='managing')

# Prepare parser

staff_parser = subparsers.add_parser("Staff")
film_parser = subparsers.add_parser("Film")
both_parser = subparsers.add_parser("Both")

# ============= Prepare staff parser =============

staff_options = staff_parser.add_mutually_exclusive_group()

staff_options.add_argument(
    "--add",
    "-a",
    nargs=3,
    metavar=("[first name]", "[last name]", "[speciality]"),
    type=str,
    help="Add a new staff person.",
)

staff_options.add_argument(
    "--remove",
    "-r",
    nargs=2,
    metavar=("[first name]", "[last name]"),
    type=str,
    help="Remove every person with given name.",
)

staff_options.add_argument(
    "--removeid",
    "-ri",
    nargs=1,
    metavar="[staff id]",
    type=int,
    help="Remove every person with given id.",
)

staff_options.add_argument(
    "--clearall",
    "-c",
    help="Delete all staff.",
    action='store_true'
)

staff_options.add_argument(
    "--getid",
    "-i",
    nargs=2,
    metavar=("[first name]", "[last name]"),
    type=str,
    help="Get staff id.",
)

staff_options.add_argument(
    "--getfilms",
    "-f",
    nargs=1,
    metavar="[staff id]",
    type=int,
    help="Get all the films this staff has worked on.",
)

# ============= Prepare film parser =============

film_options = film_parser.add_mutually_exclusive_group()

film_options.add_argument(
    "--add",
    "-a",
    nargs=3,
    metavar=("[film name]", "[description]", "[release date]"),
    type=str,
    help="Add a new film.",
)

film_options.add_argument(
    "--remove",
    "-r",
    nargs=1,
    metavar="[film name]",
    type=str,
    help="Remove film with given name.",
)

film_options.add_argument(
    "--removeid",
    "-ri",
    nargs=1,
    metavar="[film id]",
    type=int,
    help="Remove film with given id.",
)

film_options.add_argument(
    "--clearall",
    "-c",
    help="Delete all films.",
    action='store_true'
)

film_options.add_argument(
    "--getid",
    "-i",
    nargs=1,
    metavar="[film name]",
    type=str,
    help="Get film id.",
)

film_options.add_argument(
    "--getstaff",
    "-s",
    nargs=1,
    metavar="[film id]",
    type=int,
    help="Get film staff.",
)

# ============= Prepare both parser =============

both_options = both_parser.add_mutually_exclusive_group()

both_options.add_argument(
    "--addstaff",
    "-a",
    nargs=2,
    metavar=("[staff id]", "[film id]"),
    type=str,
    help="Add staff to film's credits.",
)

both_options.add_argument(
    "--removestaff",
    "-r",
    nargs=2,
    metavar=("[staff id]", "[film id]"),
    type=str,
    help="Remove staff from film's credits.",
)

# ============= Execute commands =============

args = parser.parse_args()

local_session = Session(bind=engine)

if args.managing == "Staff":
    if args.add:
        newStaff = Staff(args.add[0], args.add[1], args.add[2])
        local_session.add(newStaff)
        print(f"Added staff.")
    elif args.remove:
        query = local_session.query(Staff).filter(Staff.first_name == args.remove[0] and Staff.last_name == args.remove[1])
        print(f"Removed {query.count()} staff.")
        query.delete()
    elif args.removeid:
        query = local_session.query(Staff).filter(Staff.id == args.removeid[0])
        print(f"Removed {query.count()} staff.")
        query.delete()
    elif args.clearall:
        query = local_session.query(Staff)
        print(f"Removed {query.count()} staff.")
        query.delete()
    elif args.getid:
        staff = local_session.query(Staff).filter(Staff.first_name == args.getid[0] and Staff.first_name == args.getid[1])
        if not(staff):
            print(f"Staff named {args.getid[0]} {args.getid[1]} not found.")
        else:
            for record in staff.all():
                print(f"Found staff named {args.getid[0]} {args.getid[1]} with speciality {record.speciality} and id {record.id}")
    elif args.getfilms:
        staff = local_session.query(Staff).get(args.getfilms[0])
        allfilms = local_session.query(Film).filter(Film.staff_credited.any(id=staff.id))
        if allfilms.count() == 0:
            print("This staff has worked on 0 movies.")
        else:
            print(f"This staff has worked on the following movies:")
            for record in allfilms:
                print(f"- {record.name} released in {record.release_date}")
elif args.managing == "Film":
    if args.add:
        newMovie = Film(args.add[0], args.add[1], int(args.add[2]))
        local_session.add(newMovie)
        print(f"Added film.")
    elif args.remove:
        query = local_session.query(Film).filter(Film.name == args.remove[0])
        print(f"Removed {query.count()} films.")
        query.delete()
    elif args.removeid:
        query = local_session.query(Film).filter(Film.id == args.removeid[0])
        print(f"Removed {query.count()} films.")
        query.delete()
    elif args.clearall:
        query = local_session.query(Film)
        print(f"Removed {query.count()} films.")
        query.delete()
    elif args.getid:
        film = local_session.query(Film).filter(Film.name == args.getid[0])
        if not(film):
            print(f"Film named {args.getid[0]} not found.")
        else:
            for record in film.all():
                print(f"Found film named {args.getid[0]} with release year {record.release_date} and id {record.id}")
    elif args.getstaff:
        film = local_session.query(Film).get(args.getstaff[0])
        allstaff = local_session.query(Staff).filter(Staff.films_credited.any(id=film.id))
        if allstaff.count() == 0:
            print("No staff has been credited for the movie.")
        else:
            print(f"The following people have been credited for {film.name}")
            for record in allstaff:
                print(f"{record.first_name} {record.last_name} has been credited as {record.speciality}.")
elif args.managing == "Both":
    if args.addstaff:
        movie = local_session.query(Film).get(args.addstaff[1])
        staff = local_session.query(Staff).get(args.addstaff[0])
        if not(movie):
            print(f"Movie with id {args.addstaff[1]} not found")
        elif not(staff):
            print(f"Staff with id {args.addstaff[0]} not found")
        else:
            movie.staff_credited.append(staff)
            print(f"Added {staff.first_name} {staff.last_name} to {movie.name} credits.")
    if args.removestaff:
        movie = local_session.query(Film).get(args.removestaff[1])
        staff = local_session.query(Staff).get(args.removestaff[0])
        if not(movie):
            print(f"Movie with id {args.removestaff[1]} not found")
        elif not(staff):
            print(f"Staff with id {args.removestaff[0]} not found")
        else:
            movie.staff_credited.remove(staff)
            print(f"Removed {staff.first_name} {staff.last_name} from {movie.name} credits.")

local_session.commit()
