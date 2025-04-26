import secrets

def generate_jwt_secret(length: int = 64) -> str:
    """Generate a random secret key for JWT signing."""
    return secrets.token_urlsafe(length)
