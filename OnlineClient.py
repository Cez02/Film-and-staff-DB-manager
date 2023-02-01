from sqlalchemy import DateTime, Integer, String
from DBEngine import engine, Session
from model.FilmDefinitions import Film, Staff
import services.StaffController as StaffController
import services.FilmController as FilmController
import services.BothController as BothController
import requests
import urllib
import ast
from http import HTTPStatus

import argparse

ServerURL = "http://127.0.0.1:5000"

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
    "--getall",
    "-ga",
    help="Get all staff.",
    action='store_true'
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
    "--update",
    "-u",
    nargs=4,
    metavar=("[id]", "[first name]", "[last name]", "[speciality]"),
    type=str,
    help="Update staff info",
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
    "--getall",
    "-ga",
    help="Get all films.",
    action='store_true'
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
        try:
            form_data = {
                "first_name" : args.add[0],
                "last_name" : args.add[1],
                "speciality" : args.add[2]
            }
            res = requests.post(ServerURL + "/Staff/add", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to add staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.remove:
        try:
            form_data = {
                "first_name" : args.remove[0],
                "last_name" : args.remove[1]
            }
            res = requests.delete(ServerURL + "/Staff/remove", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to remove staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.removeid:
        try:
            form_data = {
                "id" : args.removeid[0],
            }
            res = requests.delete(ServerURL + "/Staff/removeid", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to remove staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.getall:
        try:
            res = requests.get(ServerURL + "/Staff/getall")
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to get all staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.clearall:
        try:
            res = requests.delete(ServerURL + "/Staff/clear")
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to remove staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.getid:
        try:
            res = requests.get(ServerURL + f"/Staff?first_name={args.getid[0]}&last_name={args.getid[1]}")
            if res.status_code == HTTPStatus.OK:
                for rec in ast.literal_eval(res.text):
                    print(f"Found {rec['first_name']} {rec['last_name']} specialized in {rec['speciality']} with id {rec['id']}")
            else:
                print(f"Failed to get id of staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    if args.update:
        try:
            form_data = {
                "id" : args.update[0],
                "first_name" : args.update[1],
                "last_name" : args.update[2],
                "speciality" : args.update[3]
            }
            res = requests.put(ServerURL + "/Staff/update", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to update staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.getfilms:
        try:
            res = requests.get(ServerURL + f"/Staff/film/{args.getfilms[0]}")
            if res.status_code == HTTPStatus.OK:
                for rec in ast.literal_eval(res.text):
                    print(f"{rec['name']} - {rec['description']} released in {rec['release_date']}")
            else:
                print(f"Failed to get films of staff with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
elif args.managing == "Film":
    if args.add:
        try:
            form_data = {
                "name" : args.add[0],
                "description" : args.add[1],
                "speciality" : args.add[2]
            }
            res = requests.post(ServerURL + "/Film/add", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to add film with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.remove:
        try:
            form_data = {
                "name" : args.remove[0],
            }
            res = requests.delete(ServerURL + "/Film/remove", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to remove film with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.removeid:
        try:
            form_data = {
                "id" : args.removeid[0],
            }
            res = requests.delete(ServerURL + "/Film/removeid", data=form_data)
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to remove film with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.getall:
        try:
            res = requests.get(ServerURL + "/Film/getall")
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to get all films with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.clearall:
        try:
            res = requests.delete(ServerURL + "/Film/clear")
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to remove films with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.getid:
        try:
            res = requests.get(ServerURL + f"/Film/" + args.getid[0])
            if res.status_code == HTTPStatus.OK:
                for rec in ast.literal_eval(res.text):
                    print(f"Found {rec['name']} - {rec['description']} released in {rec['release_date']} with id {rec['id']}")
            else:
                print(f"Failed to get id of film with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    elif args.getstaff:
        try:
            res = requests.get(ServerURL + f"/Film/staff/{args.getstaff[0]}")
            if res.status_code == HTTPStatus.OK:
                for rec in ast.literal_eval(res.text):
                    print(f"Found {rec['first_name']} {rec['last_name']} specialized in {rec['speciality']} with id {rec['id']}")
            else:
                print(f"Failed to get staff of film with response status code: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
elif args.managing == "Both":
    if args.addstaff:
        try:
            res = requests.post(ServerURL + f"/Both/addstaff?staffid={args.addstaff[0]}&filmid={args.addstaff[1]}")
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to add staff to film: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)
    if args.removestaff:
        try:
            res = requests.delete(ServerURL + f"/Both/removestaff?staffid={args.removestaff[0]}&filmid={args.removestaff[1]}")
            if res.status_code == HTTPStatus.OK:
                print(res.text)
            else:
                print(f"Failed to add staff to film: {res.status_code}")
        except Exception as e:
            print("Failed to make the request.")
            print(e)