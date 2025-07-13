from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)


def generate_password(length=12, use_digits=True, use_special=True):
    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    while True:
        password = ''.join(random.choice(chars) for _ in range(length))

        if (
                (not use_digits or any(c in string.digits for c in password))
                and (not use_special or any(c in string.punctuation for c in password))
                and any(c in string.ascii_uppercase for c in password)
                and any(c in string.ascii_lowercase for c in password)
        ):
            return password


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        count = int(request.form.get("count", 1))
        use_digits = request.form.get("digits") == "on"
        use_special = request.form.get("special") == "on"

        passwords = [
            generate_password(length, use_digits, use_special)
            for _ in range(count)
        ]
        return render_template("index.html", passwords=passwords)

    return render_template("index.html", passwords=None)


if __name__ == "__main__":
    app.run(debug=True)
