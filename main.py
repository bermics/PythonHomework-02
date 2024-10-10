from pymongo import MongoClient
from bson import ObjectId


def create_document(collection):
    while True:
        name = input("Enter name: ")
        if name:
            break
        else:
            print("Name cannot be empty.")

    while True:
        try:
            age = int(input("Enter age: "))
            if age > 0:
                break
            else:
                print("Age must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid age.")

    while True:
        email = input("Enter email: ")
        if email:
            break
        else:
            print("Email cannot be empty.")

    document = {"name": name, "age": age, "email": email}
    collection.insert_one(document)
    print("Document created successfully.")


def read_documents(collection):
    documents = list(collection.find())
    if not documents:
        print("No documents found.")
        return

    # Print headers
    print(f"{'Name':<20} {'Age':<5} {'Email':<30}")
    print("-" * 60)

    # Print rows
    for doc in documents:
        name = doc.get('name', "N/A")
        age = str(doc.get('age', "N/A"))
        email = doc.get('email', "N/A")
        print(f"{name:<20} {age:<5} {email:<30}")


def delete_document(collection):
    name = input("Enter which name to delete: ")
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print("Deletion Successful!")
    else:
        print("No document found with that name.")

#Update definition
def update_document(collection):
    name = input("Enter name you want to update: ")

    document = collection.find_one({"name": name})
    if document is None:
        print("No document matching that name has been found.")
        return

    print("Current values:")
    print(f"Name: {document['name']}, Age: {document['age']}, Email: {document['email']}")

    new_age = input("Enter new age: ")
    new_email = input("Enter new email: ")

    updates = {}

    if new_age:
        try:
            updates["age"] = int(new_age)
        except ValueError:
            print("Invalid input for age. Update failed.")
            return

    if new_email:
        updates["email"] = new_email

        if updates:
            result = collection.update_one({"name": name}, {"$set": updates})
            if result.modified_count > 0:
                print("Updated successfully.")
            else:
                print("No changes made to the document.")
        else:
            print("No new values provided. Update aborted.")



def main():
    # Create a MongoClient instance
    client = MongoClient("mongodb://localhost:27017")
    # Access the database and collection
    database = client['testdb']
    collection = database['testcollection']

    while True:
        print("\nChoose an operation:")
        print("1. Create a document")
        print("2. Read documents")
        print("3. Update a document")
        print("4. Delete a document")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_document(collection)
        elif choice == "2":
            read_documents(collection)
        elif choice == "3":
            update_document(collection)
        elif choice == "4":
            delete_document(collection)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

    client.close()

if __name__ == "__main__":main()