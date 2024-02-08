"""MIDDLEWARE FOR AUTHORISATION"""
from functools import wraps
from cryptography.hazmat.primitives import serialization
from flask import redirect, session, url_for
import jwt
import requests

# Function to validate JWT token


def validate_token(token):
    """validates token"""
    # Fetch JWKS from Auth0
    jwks_url = 'https://dev-eym6ylpoplxr2f0n.jp.auth0.com/.well-known/jwks.json'
    jwks = requests.get(jwks_url, timeout=5000).json()

    # Extract RSA public keys from JWKS
    rsa_public_keys = {
        key['kid']: jwt.algorithms.RSAAlgorithm.from_jwk(key)
        for key in jwks['keys']
    }
    # Validate the token signature using public keys
    try:
        decoded_token = jwt.get_unverified_header(
            token
        )
        # Get the RSA public key used to sign the token
        rsa_public_key = rsa_public_keys[decoded_token['kid']]

        rsa_public_key_string = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        # Verify the token signature using the public key
        jwt.decode(
            token,
            key=rsa_public_key_string,
            algorithms=['RS256'],
            # Replace with your audience
            audience='https://dev-eym6ylpoplxr2f0n.jp.auth0.com/api/v2/',
            # Replace with your Auth0 domain
            issuer='https://dev-eym6ylpoplxr2f0n.jp.auth0.com/'
        )

        # Token is valid
        return decoded_token

    except jwt.ExpiredSignatureError:
        print("expired")
        # Token is expired
        return None
    except (jwt.InvalidTokenError, KeyError):
        # Invalid token or key
        print("invalid")
        return None


def requires_auth(f):
    """
    Use on routes that require a valid session, otherwise it aborts with a 403
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated


if __name__ == "__main__":
    access = """eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9XZjJ5MmVYVEdZejc3ZDZaVVl0SiJ9.eyJpc3MiOiJodHRwczovL2Rldi1leW02eWxwb3BseHIyZjBuLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWMxZjY0NjY5Y2VkMjM4OTM2OTk1ZjIiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtZXltNnlscG9wbHhyMmYwbi5qcC5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZGV2LWV5bTZ5bHBvcGx4cjJmMG4uanAuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcwNzM3NTgyNiwiZXhwIjoxNzA3NDYyMjI2LCJhenAiOiIxbGRCaDYwTFpYSkdUZHlURmZtcTVWTjZJWEQ3eWVpYyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.oqd6cyfFI6DvY9jlwk5OELUQ9P_eo1RHKrlmiho-9xG6fG0re1P7R1ntdgYt7JQN8Dtbq1TQEFIb-bcjm5HJQTdVgC7qHxRLP0X3TAJynuMC-IoOxZfDhT8x3vmHGKK3hYYxbwwcp6quWjRXjOcwC7XHcCAN_OI3u4GRkm1vbtFRF3ITnY5YTVhlMT-vp0Gf5b4b48xvQwcR6lsmfoN8NZj3TdAHeZq8XwU8oMg_pEYL6MgeumlVwtazdRSuSYcyGQdE3rqnYHYs4umb36D_smwDhoBK6VaUgK6VG-BBARvZ0RSeCmFW1SAr2xOMAvxLW-OZCMfV0N0818lJUPRxMw"""
    print(validate_token(access))
