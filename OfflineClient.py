from sqlalchemy import DateTime, Integer, String
from DBEngine import engine, Session
from model.FilmDefinitions import Film, Staff
import services.StaffController as StaffController
import services.FilmController as FilmController
import services.BothController as BothController

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

if args.managing == "Staff":
    if args.add:
        res = StaffController.AddStaff(args.add[0], args.add[1], args.add[2])
        if res:
            print("Added staff.")
        else:
            print("Failed to add staff.")
    elif args.remove:
        res = StaffController.RemoveStaff(args.remove[0], args.remove[1])
        if res >= 0:
            print(f"Removed {res} staff.")
        else:
            print("Failed to remove staff.")
    elif args.removeid:
        res = StaffController.RemoveStaffID(args.removeid[0])
        if res >= 0:
            print(f"Removed {res} staff.")
        else:
            print("Failed to remove staff.")
    elif args.clearall:
        res = StaffController.ClearAll()
        if res:
            print("Removed all staff")
        else:
            print("Failed to remove all staff")
    elif args.getid:
        res = StaffController.GetID(args.getid[0], args.getid[1])
        if res is int:
            print("Failed to search for staff")
        elif len(res) > 0:
            for rec in res:
                print(f"Found staff named {args.getid[0]} {args.getid[1]} with speciality {rec.speciality} and id {rec.id}")
        else:
            print("Couldn't find any staff")
    elif args.getfilms:
        res = StaffController.GetFilms(args.getfilms[0])
        if res is int:
            print("Failed to search for staff")
        elif len(res) > 0:
            print("This staff has worked on:")
            for rec in res:
                print(f"- {rec.name} released in {rec.release_date}")
        else:
            print("Couldn't find any films.")
elif args.managing == "Film":
    if args.add:
        res = FilmController.AddFilm(args.add[0], args.add[1], args.add[2])
        if res:
            print("Added film.")
        else:
            print("Failed to add film.")
    elif args.remove:
        res = FilmController.RemoveFilm(args.remove[0])
        if res >= 0:
            print(f"Removed {res} films.")
        else:
            print("Failed to remove film.")
    elif args.removeid:
        res = FilmController.RemoveStaffID(args.removeid[0])
        if res >= 0:
            print(f"Removed {res} film.")
        else:
            print("Failed to remove film.")
    elif args.clearall:
        res = FilmController.ClearAll()
        if res:
            print("Removed all films")
        else:
            print("Failed to remove all films")
    elif args.getid:
        res = FilmController.GetID(args.getid[0])
        if len(res) > 0:
            for rec in res:
                print(f"Found film named {args.getid[0]} with release year {rec.release_date} and id {rec.id}")
        else:
            print("Couldn't find any films")
    elif args.getstaff:
        res = FilmController.GetStaff(args.getstaff[0])
        if len(res) > 0:
            print(f"The following people have been credited for this film:")
            for rec in res:
                print(f"{rec.first_name} {rec.last_name} has been credited as {rec.speciality}.")
        else:
            print("Failed to find any staff.")
elif args.managing == "Both":
    if args.addstaff:
        res = BothController.AddStaff(args.addstaff[0], args.addstaff[1])
        if res:
            print("Added the staff to the film.")
        else:
            print("Failed to add the staff to the film.")
    if args.removestaff:
        res = BothController.RemoveStaff(args.addstaff[0], args.addstaff[1])
        if res:
            print("Removed the staff from the film.")
        else:
            print("Failed to remove the staff from the film.")
