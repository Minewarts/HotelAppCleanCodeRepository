from pathlib import Path

from ..core.config import settings
from .storage_protocol import Storage
from .json_storage import JSONStorage


def get_default_storage() -> Storage:
    """Returns the default storage implementation for the current environment."""
    use_supabase = (
        settings.use_supabase
        or (
            settings.supabase_url
            and settings.supabase_key
            and settings.supabase_url != "https://placeholder.supabase.co"
            and settings.supabase_key != "placeholder-key"
        )
    )

    if use_supabase:
        from .supabase_storage import SupabaseStorage

        return SupabaseStorage()

    return JSONStorage(Path("data/database.json"))


__all__ = [
    "Storage",
    "JSONStorage",
    "get_default_storage",
]
