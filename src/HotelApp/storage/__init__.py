from .storage_protocol import Storage
from .supabase_storage import SupabaseStorage


def get_default_storage() -> Storage:
    """Returns the default storage implementation."""
    return SupabaseStorage()


__all__ = [
    "Storage",
    "SupabaseStorage",
    "get_default_storage",
]