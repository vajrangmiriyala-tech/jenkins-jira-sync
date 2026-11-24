SECRET_WORDS = ("TOKEN", "PASSWORD", "SECRET")


def is_secret_key(name):
    """Check if a setting name holds a secret."""
    name = name.upper()
    for word in SECRET_WORDS:
        if word in name:
            return True
    return False


def redact_text(text, secrets):
    """Hide every secret in a text, so it is safe to log."""
    for secret in secrets:
        if secret:
            text = text.replace(secret, "***")
    return text


def redact_config(config):
    """Copy the settings with every secret value hidden."""
    safe = {}
    for name, value in config.items():
        if is_secret_key(name):
            safe[name] = "***"
        else:
            safe[name] = value
    return safe


def log_safe(text, config):
    """Hide all secret values from a text, using the settings."""
    secrets = []
    for name, value in config.items():
        if is_secret_key(name) and value:
            secrets.append(value)
    return redact_text(text, secrets)
