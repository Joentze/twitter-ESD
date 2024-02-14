"""MIDDLEWARE FOR AUTHORISATION"""
from functools import wraps
from flask import request
from cryptography.hazmat.primitives import serialization
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
        decoded_token_header = jwt.get_unverified_header(
            token
        )
        # Get the RSA public key used to sign the token
        rsa_public_key = rsa_public_keys[decoded_token_header['kid']]

        rsa_public_key_string = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        # Verify the token signature using the public key
        data = jwt.decode(
            token,
            key=rsa_public_key_string,
            algorithms=['RS256'],
            # Replace with your audience
            audience='https://dev-eym6ylpoplxr2f0n.jp.auth0.com/api/v2/',
            # Replace with your Auth0 domain
            issuer='https://dev-eym6ylpoplxr2f0n.jp.auth0.com/'
        )

        # Token is valid
        return {**decoded_token_header, "uid": data["sub"]}

    except jwt.ExpiredSignatureError:
        print("expired")
        # Token is expired
        return None
    except (jwt.InvalidTokenError, KeyError):
        # Invalid token or key
        print("invalid")
        return None


# def requires_auth(f):
#     """
#     Use on routes that require a valid session, otherwise it aborts with a 403
#     """

#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if session.get('user') is None:
#             return redirect(url_for('auth.login'))

#         return f(*args, **kwargs)

#     return decorated


def validate_access_token(func):
    """authorisation middleware"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the access token from the Authorization header
        access_token = request.headers.get('Authorization')

        if access_token:
            # Assuming your validate_token function validates the access token
            decoded_token = validate_token(access_token)
            if decoded_token:
                # If the token is valid, execute the original function
                return func(decoded_token, *args, **kwargs)
        # If the token is not valid or not provided, return unauthorized
        return {"message": "Unauthorized Access: Invalid Access Token"}, 401

    return wrapper


if __name__ == "__main__":
    access = """eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9XZjJ5MmVYVEdZejc3ZDZaVVl0SiJ9.eyJpc3MiOiJodHRwczovL2Rldi1leW02eWxwb3BseHIyZjBuLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWMxZjY0NjY5Y2VkMjM4OTM2OTk1ZjIiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtZXltNnlscG9wbHhyMmYwbi5qcC5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZGV2LWV5bTZ5bHBvcGx4cjJmMG4uanAuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcwNzkxMzkwMywiZXhwIjoxNzA4MDAwMzAzLCJhenAiOiIxbGRCaDYwTFpYSkdUZHlURmZtcTVWTjZJWEQ3eWVpYyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.MGHsy915amkey8qMEQRUKyquSeRgm9nIdgsMEOsNtylTFirj_WvuJTiCpKRauUdJjBxB1zqTaVrGgt_X2fsqWPPBXOYU6lalY3Up2_MYmIyT42oQmPOOafesmUWAEuqiCGx3RlSOewM56-Mi8hKpGohF6WZBFLk8xNKJxo9t3zXkIHp1xmARTlNc_c6fuwbnnHr8kwdD5G6cSGPe_XTuArpLWZbYAmFWA_-zH_ylJxJ1KwvAU_F0f1M_n2qdSFnZdQWTLlOwBknKt09QVWwrhiogaEwW-F1RP0u3wm4-SCwYoiYXUEdB7iPJCcQUOe_foWhyWJOw6p70I2rMxusN0A"""
    print(validate_token(access))
