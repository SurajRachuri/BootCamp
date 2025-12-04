def todo_list():
    tasks = []

    while True:
        print("\n1. Add task")
        print("2. View tasks")
        print("3. Remove task")
        print("4. Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            task = input("Enter task: ")
            tasks.append(task)
            print("Task added!")

        elif choice == "2":
            if len(tasks) == 0:
                print("No tasks available!")
            else:
                print("\nYour Tasks:")
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task}")

        elif choice == "3":
            if len(tasks) == 0:
                print("No tasks to remove!")
            else:
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task}")
                
                remove_index = int(input("Enter task number to remove: "))
                if 1 <= remove_index <= len(tasks):
                    removed = tasks.pop(remove_index - 1)
                    print(f"Removed: {removed}")
                else:
                    print("Invalid task number!")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Enter 1-4.")

todo_list()
