from tkinter import filedialog, Tk

root = Tk()
root.withdraw()  # Hide extra window

# Select only .txt files
file_path = filedialog.askopenfilename(
    title="Select Text File",
    filetypes=[("Text Files", "*.txt")]
)

if file_path:
    print("Selected file:", file_path)

    # Read the file content
    try:
        STOP_WORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
              'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
              'would', 'could', 'should', 'may', 'might', 'must', 'shall',
              'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
              'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where',
              'that', 'this', 'it', 'its', 'as', 'so'}

        word_count = {}

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                words = line.lower().replace(",", "").replace(".", "").split()
                for word in words:
                    if word not in STOP_WORDS:
                        word_count[word] = word_count.get(word, 0) + 1
        
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        total_words = len(sorted_words)   
        
        try:
            N = int(input(f"Enter how many top words you want? (Available: {total_words}) : "))
            if 1 <= N <= total_words:
                for word, count in sorted_words[:N]:
                    print(f"{word}: {count}")
            else:
                print(f"Please enter a number between 1 and {total_words}")
        except:
            print("Invalid input, please enter a number.")

    except Exception as e:
        print("Error reading file:", e)

else:
    print("No file selected")

