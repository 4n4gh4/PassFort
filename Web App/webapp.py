from flask import Flask, render_template, request, jsonify
import random
import re
import hashlib
import requests
from markovify import Text
import getpass

app = Flask(__name__)

try:
    response = requests.get("https://www.gutenberg.org/cache/epub/2554/pg2554.txt")
    response.raise_for_status()
    text = response.text
    text_model = Text(text)
except Exception as e:
    text_model = None

class OWASPPasswordStrengthTest:
    def __init__(self):
        self.configs = {
            "allow_passphrases": True,
            "max_length": 128,
            "min_length": 10,
            "min_phrase_length": 20,
            "min_optional_tests_to_pass": 4,
        }

        self.required_tests = [
            lambda pwd: len(pwd) >= self.configs["min_length"]
            or f"Password must be at least {self.configs['min_length']} characters long.",
            lambda pwd: len(pwd) <= self.configs["max_length"]
            or f"Password must be fewer than {self.configs['max_length']} characters.",
            lambda pwd: not any(pwd[i] == pwd[i + 1] == pwd[i + 2] for i in range(len(pwd) - 2))
            or "Password may not contain sequences of three or more repeated characters.",
        ]

        self.optional_tests = [
            lambda pwd: any(c.islower() for c in pwd) or "Password must contain at least one lowercase letter.",
            lambda pwd: any(c.isupper() for c in pwd) or "Password must contain at least one uppercase letter.",
            lambda pwd: any(c.isdigit() for c in pwd) or "Password must contain at least one number.",
            lambda pwd: any(not c.isalnum() for c in pwd) or "Password must contain at least one special character.",
        ]

    def test(self, password):
        result = {
            "errors": [],
            "is_passphrase": False,
            "strong": True,
            "optional_tests_passed": 0,
        }

        for test in self.required_tests:
            test_result = test(password)
            if isinstance(test_result, str):
                result["errors"].append(test_result)
                result["strong"] = False

        if self.configs["allow_passphrases"] and len(password) >= self.configs["min_phrase_length"]:
            result["is_passphrase"] = True

        if not result["is_passphrase"]:
            for test in self.optional_tests:
                test_result = test(password)
                if isinstance(test_result, str):
                    result["errors"].append(test_result)
                else:
                    result["optional_tests_passed"] += 1

            if result["optional_tests_passed"] < self.configs["min_optional_tests_to_pass"]:
                result["strong"] = False

        return result

def check_breached_password(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code != 200:
            return "Error checking breached status."

        hashes = (line.split(":") for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"❌ Breached {count} times!"

        return "✅ Not found in breaches."
    except Exception as e:
        return f"Error: {e}"

def generate_passphrase(keywords, num_passphrases=3):
    passphrases = []
    for _ in range(num_passphrases):
        random.shuffle(keywords)
        phrase = "".join([word.capitalize() for word in keywords])

        if text_model:
            generated_part = text_model.make_short_sentence(20, tries=20)
            if generated_part is None:
                generated_part = "BucketFishCar"
        else:
            generated_part = "BucketFishCar"

        generated_part = generated_part.replace(" ", "")
        number = str(random.randint(10, 99))
        special_char = random.choice("!@#$%^&*()").strip()

        passphrase = f"{phrase}{generated_part}{number}{special_char}"
        passphrases.append(passphrase)

    return passphrases

def camouflage_input(prompt="Enter your password: "):
    print(prompt, end="", flush=True)
    full_input = getpass.getpass("").strip()
    real_password = re.sub(r"\\\\\*.*?\\", "", full_input)
    print("\nYour real password is:", real_password, "(This code can be removed for Screen logging protection)")
    return real_password

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = camouflage_input("Enter your disguised password: ")
    tester = OWASPPasswordStrengthTest()
    result = tester.test(password)
    breach_status = check_breached_password(password)
    suggested_passphrases = generate_passphrase(password.split(), 3)

    return jsonify({
        'strength': '✅ Strong' if result['strong'] else '❌ Weak',
        'errors': result['errors'],
        'breach_status': breach_status,
        'suggested_passphrases': suggested_passphrases
    })

if __name__ == '__main__':
    app.run(debug=True)
