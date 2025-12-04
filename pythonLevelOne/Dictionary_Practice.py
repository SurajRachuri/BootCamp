def phone_book():
    contacts = {}

    while True:
        print("\n--- Phone Book Menu ---")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Delete Contact")
        print("4. List All Contacts")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            contacts[name] = phone
            print(f"{name} added successfully!")

        elif choice == "2":
            name = input("Enter the name to search: ")
            if name in contacts:
                print(f"{name}: {contacts[name]}")
            else:
                print("Contact not found!")

        elif choice == "3":
            name = input("Enter name to delete: ")
            if name in contacts:
                del contacts[name]
                print(f"{name} removed successfully!")
            else:
                print("Contact does not exist!")

        elif choice == "4":
            if len(contacts) == 0:
                print("No contacts saved!")
            else:
                print("\nAll Contacts:")
                for index, (name, phone) in enumerate(contacts.items(), start=1):
                   print(f"{index}. {name}: {phone}")

        elif choice == "5":
            print("Exiting Phone Book. Goodbye!")
            break

        else:
            print("Invalid choice! Enter 1 - 5.")

phone_book()