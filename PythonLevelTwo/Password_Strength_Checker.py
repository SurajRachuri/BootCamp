import re
import getpass

def check_password_strength(password: str) -> dict:
    score = 0
    suggestions = []

    # 1. Check Length (Weighted heavily)
    # Give 2 points for every character, up to a max of 40 points
    length_score = min(len(password) * 2, 40)
    score += length_score
    
    if len(password) < 8:
        suggestions.append(f"Password is too short ({len(password)}/8 chars)")
    elif len(password) < 12:
        suggestions.append("Consider making password longer (12+ chars)")

    # 2. Check Uppercase
    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letters")

    # 3. Check Lowercase
    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letters")

    # 4. Check Numbers
    if re.search(r"[0-9]", password):
        score += 15
    else:
        suggestions.append("Add numbers")

    # 5. Check Special Characters (Improved Regex)
    # This regex [^a-zA-Z0-9\s] looks for anything NOT a letter, number, or space
    if re.search(r"[^a-zA-Z0-9\s]", password):
        score += 15
    else:
        suggestions.append("Add special characters (@, #, $, etc.)")

    # Determine Label
    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Medium"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "strength": strength,
        "score": score,
        "suggestions": suggestions
    }

# Main Execution
if __name__ == "__main__":
    print("--- Password Strength Checker ---")
    # getpass hides the input text for security
    try:
        user_pass = getpass.getpass("Enter the Password (input will be hidden): ")
    except Exception:
        # Fallback if running in an environment that doesn't support getpass (like some IDEs)
        user_pass = input("Enter the Password: ")

    result = check_password_strength(user_pass)
    
    print(f"\nResults:")
    print(f"Strength: {result['strength']}")
    print(f"Score:    {result['score']}/100")
    if result['suggestions']:
        print("Suggestions:")
        for item in result['suggestions']:
            print(f"- {item}")
