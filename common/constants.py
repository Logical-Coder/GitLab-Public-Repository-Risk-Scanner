SENSITIVE_FILES = [
    ".env",
    ".pem",
    "id_rsa",
    "config.json",
    "secrets.yml"
]

SECRET_PATTERNS = {
    "password": r"password\s*=",
    "api_key": r"api[_-]?key\s*=",
    "token": r"token\s*="
}