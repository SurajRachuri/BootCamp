def WordCounter(a):
    # Remove extra spaces at start, end, or multiple between words
    a = " ".join(a.split())
    
    # Counting characters except space
    n = 0
    for ch in a:
        if ch != " ":
            n += 1
    print("Characters without spaces:", n)
    
    # Total length including spaces
    print("Total length:", len(a))
    
    # Split into words
    words = a.split()
    print("Words:", len(words))
    
    # Initialize with first word
    largeWord = words[0]
    smallWord = words[0]
    
    # Loop through words
    for w in words:
        if len(w) > len(largeWord):
            largeWord = w
        if len(w) < len(smallWord):
            smallWord = w
    
    print("Longest Word:", largeWord)
    print("Shortest Word:", smallWord)


a ="The quick brown fox jumps over the lazy dog"
WordCounter(a)
print("---------------------------------")

# with inbulit functions 

def analyze_sentence(sentence: str) -> dict:
    words = sentence.split()
 
    total_words = len(words)
    total_chars_with_spaces = len(sentence)
    total_chars_without_spaces = len(sentence.replace(" ", ""))
    longest_word = max(words, key=len)
    shortest_word = min(words, key=len)
 
    return {
        "Total Words": total_words,
        "Total Characters with spaces": total_chars_with_spaces,
        "Total Characters without spaces": total_chars_without_spaces,
        "Longest Word": longest_word,
        "Shortest Word": shortest_word,
    }
 
result = analyze_sentence("The quick brown fox jumps over the lazy dog")
print(result)


