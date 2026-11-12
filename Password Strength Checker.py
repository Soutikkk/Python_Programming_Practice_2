
import re
import math
import string
import secrets
import getpass


def check_password(password):
    score = 0
    suggestions = []

    checks = {
        "At least 12 characters": len(password) >= 12,
        "Contains uppercase letters": bool(re.search(r"[A-Z]", password)),
        "Contains lowercase letters": bool(re.search(r"[a-z]", password)),
        "Contains numbers": bool(re.search(r"\d", password)),
        "Contains special characters": bool(
            re.search(r"[^A-Za-z0-9]", password)
        )
    }

    for requirement, passed in checks.items():
        if passed:
            score += 20
        else:
            suggestions.append(requirement)

    if len(password) >= 16:
        score = min(score + 10, 100)

    if score >= 90:
        strength = "VERY STRONG"
    elif score >= 70:
        strength = "STRONG"
    elif score >= 50:
        strength = "MODERATE"
    else:
        strength = "WEAK"

    return score, strength, suggestions


def generate_password(length=16):
    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def main():
    while True:
        print("\n" + "=" * 45)
        print("       PASSWORD SECURITY TOOL")
        print("=" * 45)

        print("1. Check Password Strength")
        print("2. Generate Secure Password")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            password = getpass.getpass(
                "\nEnter your password: "
            )

            if not password:
                print("Password cannot be empty!")
                continue

            score, strength, suggestions = check_password(
                password
            )

            print("\n--- PASSWORD ANALYSIS ---")
            print(f"Strength: {strength}")
            print(f"Security Score: {score}/100")

            filled = score // 10
            bar = "#" * filled + "-" * (10 - filled)
            print(f"Strength Meter: [{bar}]")

            if suggestions:
                print("\nSuggestions:")
                for suggestion in suggestions:
                    print(f"- {suggestion}")
            else:
                print("\nAll basic requirements satisfied!")

            print(
                "\nNote: This is a basic rule-based score,"
                " not a guarantee of password security."
            )

        elif choice == "2":
            try:
                length = int(
                    input("Enter password length (12-128): ")
                )

                if not 12 <= length <= 128:
                    print("Choose a length between 12 and 128.")
                    continue

                password = generate_password(length)
                print(f"\nGenerated Password: {password}")
                print("Store it securely in a password manager.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            print("\nThank you for using Password Security Tool!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
