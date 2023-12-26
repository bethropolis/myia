from flask import Response

def error_response(message, status_code):
    return Response(message, status_code)


