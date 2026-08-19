"""
Auth0-based authentication for the web UI.

Uses the standard OAuth2 Authorization Code flow against an
Auth0 "Regular Web Application", via authlib -- deliberately not
hand-rolled, since getting OIDC token/state validation wrong is
an easy way to introduce a real auth bypass.

The resulting identity is stored in a signed session cookie
(Starlette's SessionMiddleware, configured in app.py). Signed
means tamper-proof, not hidden -- don't put anything sensitive
beyond basic profile info in the session.

Required environment variables (see .env.example for the full
Auth0 dashboard setup steps):

    AUTH0_DOMAIN          e.g. your-tenant.us.auth0.com
    AUTH0_CLIENT_ID
    AUTH0_CLIENT_SECRET
    SESSION_SECRET_KEY    random string that signs the session
                           cookie -- generate with:
                           python -c "import secrets; print(secrets.token_hex(32))"
    APP_BASE_URL          e.g. http://localhost:8000 (no trailing slash)
"""

from __future__ import annotations

import os

from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from starlette.requests import Request


#
# Called here, not just in app.py, so these module-level reads
# below see .env values regardless of import order -- Python
# executes this module's top level (including these os.environ
# reads) the moment anything imports it, before any code in the
# importer runs.
#
load_dotenv()


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "")
APP_BASE_URL = os.environ.get(
    "APP_BASE_URL",
    "http://localhost:8000",
)

#
# Local dev runs over plain http, so the session cookie can't be
# marked Secure (browsers won't send Secure cookies over http).
# Set SESSION_COOKIE_HTTPS_ONLY=true once this is ever run behind
# real TLS.
#
SESSION_COOKIE_HTTPS_ONLY = (
    os.environ.get(
        "SESSION_COOKIE_HTTPS_ONLY",
        "false",
    ).lower()
    == "true"
)


def require_auth_config() -> None:
    """
    Fail loudly and early if required config is missing, rather
    than starting the server in a half-configured state that
    fails confusingly on the first login attempt.
    """

    missing = [
        name
        for name, value in (
            ("AUTH0_DOMAIN", AUTH0_DOMAIN),
            ("AUTH0_CLIENT_ID", AUTH0_CLIENT_ID),
            ("AUTH0_CLIENT_SECRET", AUTH0_CLIENT_SECRET),
            ("SESSION_SECRET_KEY", SESSION_SECRET_KEY),
        )
        if not value
    ]

    if missing:

        raise RuntimeError(
            "Missing required Auth0/session configuration: "
            f"{', '.join(missing)}. "
            "Copy .env.example to .env and fill these in."
        )


oauth = OAuth()


def configure_oauth() -> None:
    """
    Register the Auth0 OAuth client. Called once at import time,
    after require_auth_config() has already confirmed the
    environment is set up.
    """

    oauth.register(
        name="auth0",
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=(
            f"https://{AUTH0_DOMAIN}"
            "/.well-known/openid-configuration"
        ),
    )


def get_session_user(
    request: Request,
) -> dict | None:
    """
    Return the logged-in user's session record, or None.
    """

    return request.session.get("user")
