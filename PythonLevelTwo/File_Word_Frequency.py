# First Method
STOP_WORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
              'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
              'would', 'could', 'should', 'may', 'might', 'must', 'shall',
              'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
              'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where',
              'that', 'this', 'it', 'its', 'as', 'so'}

word_count = {}

with open("demo.txt", "r", encoding="utf-8") as file:
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
     
    

# Using the oops concepts 
class WordFrequencyAnalyzer:
    STOP_WORDS = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'to', 'of', 'in', 'for',
        'on', 'with', 'at', 'by', 'from', 'and', 'or', 'but', 'if', 'then',
        'else', 'when', 'where', 'that', 'this', 'it', 'its', 'as', 'so'
    }

    def __init__(self, filename):
        self.filename = filename
        self.word_count = {}
        self.sorted_words = []

    def process_file(self):
        """Reads file, removes stop words & counts frequency"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                for line in file:
                    words = line.lower().replace(",", "").replace(".", "").split()

                    for word in words:
                        if word and word not in self.STOP_WORDS:
                            self.word_count[word] = self.word_count.get(word, 0) + 1

            self.sorted_words = sorted(self.word_count.items(), key=lambda x: x[1], reverse=True)
            print(sorted_words)

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found!")

    def show_top_words(self, n):
        """Displays top N most frequent words"""
        if not self.sorted_words:
            print("No data processed! Run process_file() first.")
            return

        if n < 1 or n > len(self.sorted_words):
            print(f"Please enter a number between 1 and {len(self.sorted_words)}")
            return

        print(f"\nTop {n} most frequent words:\n")
        for word, count in self.sorted_words[:n]:
            print(f"{word}: {count}")


# ----------------
# Usage
# ----------------
analyzer = WordFrequencyAnalyzer("demo.txt")
analyzer.process_file()

try:
    N = int(input("Enter how many top words you want: "))
    analyzer.show_top_words(N)
except ValueError:
    print("Invalid input! Please enter a number.")
