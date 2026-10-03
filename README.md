# Juice Shop Login Form

A small login page modeled on the OWASP Juice Shop login screen. It checks the email and password in the browser, then checks them again on the server.

The page asks for an email and a password. The browser blocks an empty email or password, requires `@` in the email, and requires a password of at least 8 characters. `server.py` repeats those same checks for `POST /login`, so the rules still apply if someone skips the JavaScript and calls the server directly. There is no user database. A valid-looking submission is rejected as an invalid login, and the password is not stored.

## Run

Python 3 is required. From this directory:

```bash
python3 server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Checks

| Input | Result |
| --- | --- |
| Empty email or password | Rejected in the browser and on the server |
| Email without `@` | Rejected in the browser and on the server |
| Password shorter than 8 characters | Rejected in the browser and on the server |
| Email containing `@` and a password of 8 or more characters | Accepted by both checks, then rejected as an unknown account |
