TORTOISE_ORM = {
    "connections": {"default": "sqlite://watch.sqlite"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
