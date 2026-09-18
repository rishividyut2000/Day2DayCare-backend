"""RFC 9457 problem+json error responses."""
from rest_framework.views import exception_handler


def problem_detail_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    detail = response.data
    errors = None
    if isinstance(detail, dict) and "detail" not in detail:
        errors = detail
        detail = "Validation failed"
    elif isinstance(detail, dict):
        detail = detail["detail"]

    response.data = {
        "type": f"https://day2daycare.in/problems/{response.status_code}",
        "title": response.status_text,
        "status": response.status_code,
        "detail": str(detail),
    }
    if errors:
        response.data["errors"] = errors
    return response
