from socket import create_connection
from tkinter.font import names
from pymongo import MongoClient
from bson import ObjectId
import re
from datetime import datetime
from pymongo.common import validate_string
import bson.regex
#pip install phonenumbers

database_name = 'testdb'
collection_name = 'testcollection'


def create_connection():
    client = MongoClient("mongodb://localhost:27017")
    database = client[database_name]

    if collection_name not in database.list_collection_names():
        database.create_collection(collection_name)

    return database[collection_name]


def validate_name(name):
    pattern = r'^[a-zA-Z0-9 ]+$'
    return bool(re.fullmatch(pattern, name))

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.fullmatch(pattern, email))

def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 10

def validate_address(address):
    return bool(address.strip())

#Input validation function
def valid_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print("Your input does not meet the requirements, please try again.")

#Create document function
def create_document(collection):
    while True:
        name = valid_input("Enter name: ", validate_name)

        if collection.find_one({"name": name}):
            print("A document with that name already exists, please enter a different name.")
            continue

        phone = valid_input("Enter phone number: ", validate_phone)
        email = valid_input("Enter email address: ", validate_email)
        address = valid_input("Enter address: ", validate_address)

        document = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "created_at": datetime.now()
        }
        result = collection.insert_one(document)
        print("Document created. ID: ", result.inserted_id)
        break

#Read document function
def read_document(collection):
    documents = list(collection.find())
    if not documents:
        print("No documents found.")
        return

    print(f"{'Name':<20} {'Email':<30} {'Phone':<15} {'Address':<30} {'Created At':<20}")
    print("-" * 120)

    for doc in documents:
        name = doc.get('name', 'N/A')
        email = doc.get('email', 'N/A')
        phone = doc.get('phone', 'N/A')
        address = doc.get('address', 'N/A')
        created_at = doc.get('created_at', 'N/A')

        print(f"{name:<20} {email:<30} {phone:<15} {address:<30} {created_at}")



#Update document function
def update_document(collection):
    name = input("Enter the name of the document to update: ")
    document = collection.find_one({"name": name})

    if not document:
        print("No document found with that name.")
        return

    print("Current values:")
    print(
        f"Name: {document['name']}, Email: {document['email']}, Phone: {document['phone']}, Address: {document['address']}")

    new_email = input("Enter new email: ")
    new_phone = input("Enter new phone number: ")
    new_address = input("Enter new address: ")

    updates = {}
    if new_email and validate_email(new_email):
        updates["email"] = new_email
    if new_phone and validate_phone(new_phone):
        updates["phone"] = new_phone
    if new_address and validate_address(new_address):
        updates["address"] = new_address

    if updates:
        collection.update_one({"name": name}, {"$set": updates})
        print("Document updated.")
    else:
        print("No changes made.")

def delete_document(collection):
    name = input("Enter the name of the document to delete: ")
    result = collection.delete_one({"name": name})

    if result.deleted_count > 0:
        print("Document deleted successfully.")
    else:
        print("No document found with that name.")

def main():
    collection = create_connection()

    while True:
        print("\nSelect a function:")
        print("1. Create a new document.")
        print("2. Read a document.")
        print("3. Update a document.")
        print("4. Delete a document.")
        print("5. Exit.")
        choice = input("Select input: ")

        if choice == "1":
            create_document(collection)
        elif choice == "2":
            read_document(collection)
        elif choice == "3":
            update_document(collection)
        elif choice == "4":
            delete_document(collection)
        elif choice == "5":
            break
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__" :main()
