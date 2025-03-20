from flask import Flask, render_template, request, jsonify
import random
import re
import hashlib
import requests
from markovify import Text

app = Flask(__name__)

try:
    response = requests.get("https://www.gutenberg.org/cache/epub/2554/pg2554.txt")
    response.raise_for_status()
    text = response.text
    text_model = Text(text)
except Exception as e:
    print(f"Error loading online corpus: {e}")
    text_model = None

class OWASPPasswordStrengthTest:
    def __init__(self):
        self.configs = {
            "allow_passphrases": True,
            "max_length": 128,
            "min_length": 8,
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

# Function to check if the password has been breached
def check_breached_password(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    # Check Have I Been Pwned API first
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        response.raise_for_status()

        hashes = (line.split(":") for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"❌ Breached {count} times (HIBP)!"

    except Exception as e:
        return f"Error checking HIBP API: {e}"

    # If not found in HIBP, check local rockyou.txt
    try:
        # Download rockyou.txt from a reliable source
        response = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou.txt.tar.gz")
        response.raise_for_status()

        # Handle compressed file
        import tarfile
        import io
        tar = tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
        rockyou_file = tar.extractfile("rockyou.txt")

        if rockyou_file:
            common_passwords = rockyou_file.read().decode("latin-1").splitlines()
            if password in common_passwords:
                return "❌ Found in rockyou.txt (Common Password)!"
    
    except Exception as e:
        return f"Error fetching rockyou.txt: {e}"


# Generate suggested passphrases
def generate_passphrase(keywords, num_passphrases=3):
    passphrases = []
    for _ in range(num_passphrases):
        random.shuffle(keywords)
        phrase = "".join([word.capitalize() for word in keywords])

        # Now relying on the online corpus directly
        if text_model:
            generated_part = text_model.make_short_sentence(20, tries=20)
            if generated_part is None:
                generated_part = "BucketFishCar"
        else:
            generated_part = "BucketFishCar"

        # Ensure no spaces sneak in
        generated_part = re.sub(r"\s+", "", generated_part)
        number = str(random.randint(10, 99))
        special_char = random.choice("!@#$%^&*()")

        passphrase = f"{phrase}{generated_part}{number}{special_char}"
        passphrases.append(passphrase)

    return passphrases

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    try:
        data = request.get_json()
        password = data.get('password', '')

        if not password:
            return jsonify({'error': 'Password is required!'}), 400

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

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
