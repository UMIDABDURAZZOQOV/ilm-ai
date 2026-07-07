import os
import time
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from services.db import SessionLocal
from services.models import LLMLog
from typing import Optional, Dict, Any, Callable

def init_monitoring():
    """Initialize Sentry monitoring with comprehensive error tracking and performance monitoring."""
    sentry_dsn = os.environ.get("SENTRY_DSN")
    environment = os.environ.get("ENVIRONMENT", "development")
    release = os.environ.get("RELEASE_VERSION", "0.3.0")
    
    # Only initialize Sentry if DSN is provided and not empty
    if sentry_dsn and sentry_dsn.strip():
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=0.1 if environment == "production" else 1.0,
            profiles_sample_rate=0.1 if environment == "production" else 1.0,
            environment=environment,
            release=release,
            # Custom error filters
            before_send=before_send_event,
            before_send_transaction=before_send_transaction,
            # Performance monitoring
            enable_tracing=True,
            # User context
            send_default_pii=False,
            # Additional settings
            max_breadcrumbs=50,
            attach_stacktrace=True,
        )
        print(f"Sentry monitoring initialized in {environment} environment (release: {release})")
    else:
        print("Sentry DSN not configured - monitoring disabled")


def before_send_transaction(transaction, hint):
    """Filter and modify transactions before sending to Sentry."""
    # Filter out health check transactions
    if transaction.get("transaction", "").startswith("/health"):
        return None
    
    # Filter out static asset transactions
    request = transaction.get("request", {})
    if request.get("path", "").startswith("/static"):
        return None
    
    return transaction


def before_send_event(event, hint):
    """Filter and modify events before sending to Sentry."""
    # Filter out health check errors
    if event.get("transaction", "").startswith("/health"):
        return None
    
    # Filter out static asset errors
    request = event.get("request", {})
    if request.get("path", "").startswith("/static"):
        return None
    
    # Add custom tags
    environment = os.environ.get("ENVIRONMENT", "development")
    event["tags"] = event.get("tags", {})
    event["tags"]["environment"] = environment
    
    # Sanitize sensitive data
    if "request" in event and "data" in event["request"]:
        if "headers" in event["request"]["data"]:
            headers = event["request"]["data"]["headers"]
            # Remove authorization headers
            if "authorization" in headers:
                headers["authorization"] = "REDACTED"
            if "cookie" in headers:
                headers["cookie"] = "REDACTED"
        # Sanitize request body
        if "body" in event["request"]["data"]:
            body = event["request"]["data"]["body"]
            if isinstance(body, dict):
                # Remove sensitive fields
                sensitive_fields = ["password", "token", "secret", "key", "credit_card"]
                for field in sensitive_fields:
                    if field in body:
                        body[field] = "REDACTED"
    
    # Add fingerprint for better error grouping
    if "exception" in event:
        exception_type = event["exception"]["values"][0].get("type")
        exception_message = event["exception"]["values"][0].get("value")
        event["fingerprint"] = [exception_type, exception_message]
    
    return event


def set_user_context(user_id: Optional[int] = None, email: Optional[str] = None, **kwargs):
    """Set user context for Sentry events."""
    context = {}
    if user_id:
        context["id"] = user_id
    if email:
        context["email"] = email
    context.update(kwargs)
    
    sentry_sdk.set_user(context) if context else sentry_sdk.configure_scope(lambda scope: scope.set_user(None))


def track_custom_event(event_name: str, data: Dict[str, Any], level: str = "info"):
    """Track custom business logic events in Sentry."""
    if not os.environ.get("SENTRY_DSN", "").strip():
        return
    with sentry_sdk.new_scope() as scope:
        scope.set_extra("event_name", event_name)
        scope.set_extra("event_data", data)
        sentry_sdk.capture_message(f"Custom Event: {event_name}", level=level)


def track_error(error: Exception, context: Dict[str, Any] = None):
    """Track an error with additional context."""
    sentry_sdk.capture_exception(error)
    if context:
        sentry_sdk.set_extra("error_context", context)


def log_llm_call(user_id, prompt, response_text, latency_ms, token_count=None, model="gemini-2.5-flash", context: Dict[str, Any] = None):
    """Log LLM call to both database and Sentry."""
    # Set user context for this operation
    set_user_context(user_id=user_id)
    
    db = SessionLocal()
    try:
        log_entry = LLMLog(
            user_id=user_id,
            prompt=prompt,
            response=response_text,
            latency_ms=latency_ms,
            token_count=token_count,
            model=model
        )
        db.add(log_entry)
        db.commit()
        
        # Track performance metrics in Sentry
        with sentry_sdk.start_transaction(op="llm_call", name=f"LLM Call - {model}") as transaction:
            transaction.set_data("user_id", user_id)
            transaction.set_data("model", model)
            transaction.set_data("latency_ms", latency_ms)
            transaction.set_data("token_count", token_count)
            
            # Track slow responses
            if latency_ms > 5000:  # More than 5 seconds
                transaction.set_status("slow")
                track_custom_event("llm_slow_response", {
                    "user_id": user_id,
                    "model": model,
                    "latency_ms": latency_ms,
                    "token_count": token_count
                }, level="warning")
            
            if context:
                for key, value in context.items():
                    transaction.set_data(key, value)
                    
    except Exception as e:
        track_error(e, context={"user_id": user_id, "operation": "log_llm_call"})
        print(f"Error logging LLM call: {e}")
    finally:
        db.close()


def track_user_signup(user_id: int, email: str, method: str = "email"):
    """Track user signup events."""
    set_user_context(user_id=user_id, email=email)
    track_custom_event("user_signup", {
        "user_id": user_id,
        "email": email,
        "method": method
    })


def track_user_login(user_id: int, email: str, method: str = "email"):
    """Track user login events."""
    set_user_context(user_id=user_id, email=email)
    track_custom_event("user_login", {
        "user_id": user_id,
        "email": email,
        "method": method
    })


def track_payment_success(user_id: int, amount: int, gateway: str, session_id: str):
    """Track successful payment events."""
    set_user_context(user_id=user_id)
    track_custom_event("payment_success", {
        "user_id": user_id,
        "amount": amount,
        "gateway": gateway,
        "session_id": session_id
    })


def track_payment_failure(user_id: int, amount: int, gateway: str, error: str):
    """Track failed payment events."""
    set_user_context(user_id=user_id)
    track_custom_event("payment_failure", {
        "user_id": user_id,
        "amount": amount,
        "gateway": gateway,
        "error": error
    }, level="warning")


def track_file_upload(user_id: int, filename: str, file_size: int):
    """Track file upload events."""
    set_user_context(user_id=user_id)
    track_custom_event("file_upload", {
        "user_id": user_id,
        "filename": filename,
        "file_size": file_size
    })


def track_quiz_completion(user_id: int, score: int, total: int, difficulty: str):
    """Track quiz completion events."""
    set_user_context(user_id=user_id)
    track_custom_event("quiz_completion", {
        "user_id": user_id,
        "score": score,
        "total": total,
        "difficulty": difficulty,
        "percentage": (score / total * 100) if total > 0 else 0
    })


def track_api_request(method: str, path: str, status_code: int, response_time_ms: float):
    """Track API request metrics."""
    track_custom_event("api_request", {
        "method": method,
        "path": path,
        "status_code": status_code,
        "response_time_ms": response_time_ms
    }, level="info" if status_code < 400 else "warning")


def track_database_query(operation: str, table: str, duration_ms: float):
    """Track database query performance."""
    if duration_ms > 1000:  # Track slow queries
        track_custom_event("slow_database_query", {
            "operation": operation,
            "table": table,
            "duration_ms": duration_ms
        }, level="warning")


def add_breadcrumb(category: str, message: str, level: str = "info", data: Dict[str, Any] = None):
    """Add a breadcrumb for better debugging context."""
    sentry_sdk.add_breadcrumb(
        category=category,
        message=message,
        level=level,
        data=data or {}
    )


def track_error_recovery(error: Exception, recovery_method: str, context: Dict[str, Any] = None):
    """Track when an error is recovered from."""
    track_custom_event("error_recovery", {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "recovery_method": recovery_method,
        "context": context or {}
    }, level="info")


def track_external_api_call(service: str, endpoint: str, status_code: int, duration_ms: float):
    """Track external API calls (Gemini, Payme, Click, etc.)."""
    track_custom_event("external_api_call", {
        "service": service,
        "endpoint": endpoint,
        "status_code": status_code,
        "duration_ms": duration_ms
    }, level="warning" if status_code >= 400 or duration_ms > 5000 else "info")


def monitor_function(name: str):
    """Decorator to monitor function performance and errors."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                add_breadcrumb("function", f"Starting {name}", level="info")
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                if duration_ms > 5000:
                    track_custom_event("slow_function", {
                        "function_name": name,
                        "duration_ms": duration_ms
                    }, level="warning")
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                track_error(e, context={
                    "function_name": name,
                    "duration_ms": duration_ms,
                    "args": str(args)[:200],
                    "kwargs": str(kwargs)[:200]
                })
                raise
        return wrapper
    return decorator
