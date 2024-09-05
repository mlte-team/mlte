"""
mlte/backend/api/codes.py

Status codes for MLTE backend.
"""

OK = 200
"""HTTP 'OK'"""

BAD_REQUEST = 400
"""HTTP 'Bad Request'"""

UNAUTHORIZED = 401
"""HTTP 'Unauthorized'"""

FORBIDDEN = 403
"""HTTP 'Forbidden'"""

NOT_FOUND = 404
"""HTTP 'Not Found'"""

ALREADY_EXISTS = 409
"""HTTP 'Already Exists'"""

UNPROCESSABLE_ENTITY = 422
"""HTTP 'Unprocessable Entitiy'"""

INTERNAL_ERROR = 500
"""HTTP 'Internal Server Error'"""
