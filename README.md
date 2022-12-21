
# URL Shortener

URL Shortener is a simple tool used to shorten long URLs to just 3 characters. It also allows to short url to custom back-half. You can also view/update/delete your short urls after login/signup.

## Tech Stack

**Client:** HTML, CSS, JavaScript, Bootstrap

**Server:** Python, Flask, SQLite3(for database using Flask-SQLAlchemy), Flask-Session(for server-side sessions)

## Run Locally

Clone the project

```bash
  git clone https://github.com/askandola/url_shortener.git
```

Go to the project directory

```bash
  cd url_shortener
```

If you want use virtual environment

```bash
  virtualenv env
```

```bash
  env/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python ./run.py
```
