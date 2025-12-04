questions = [
    {
        "question": "What is the capital of France?",
        "options": ["a) London", "b) Paris", "c) Berlin", "d) Madrid"],
        "answer": "b"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["a) Earth", "b) Jupiter", "c) Mars", "d) Venus"],
        "answer": "c"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["a) Charles Dickens", "b) William Shakespeare", "c) Mark Twain", "d) Leo Tolstoy"],
        "answer": "b"
    },
    {
        "question": "What is the largest mammal?",
        "options": ["a) Elephant", "b) Blue Whale", "c) Giraffe", "d) Hippopotamus"],
        "answer": "b"
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["a) 5", "b) 6", "c) 7", "d) 8"],
        "answer": "c"
    }
]

def run_quiz(questions: list) -> None:
    score = 0
    total = len(questions)

    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        for opt in q['options']:
            print(opt)

        user_ans = input("Enter your answer (a/b/c/d): ").lower()

        if user_ans == q['answer']:
            score += 1
            print("Correct!")
        else:
            print(f"Wrong! Correct answer is: {q['answer']}")

    percentage = (score / total) * 100
    print("\n--- Quiz Complete! ---")
    print(f"Your Score: {score}/{total}")
    print(f"Percentage: {percentage:.2f}%")

# Start the quiz
run_quiz(questions)
