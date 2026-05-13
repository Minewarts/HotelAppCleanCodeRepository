import json
from pathlib import Path
from typing import List

from ..models import User


class JSONStorage:
    """
    Storage implementation that persists user data in a JSON file.
    """

    def __init__(self, filepath: Path):
        """
        Initializes the JSON storage with a file path.

        Args:
            filepath (Path): Path to the JSON file used for storage.
        """
        self.filepath = filepath

    def load(self) -> List[User]:
        """
        Loads users from a JSON file.

        If the file does not exist, an empty list is returned. The method
        reconstructs User objects from the stored JSON data.

        Returns:
            List[User]: A list of reconstructed User objects.

        Raises:
            Exception: If there is an error reading or parsing the JSON file.
        """
        if not self.filepath.exists():
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            users: List[User] = []
            for item in data:
                user = User(
                    user_id=item["id"],
                    first_name=item["first_name"],
                    last_name=item["last_name"],
                    email=item["email"],
                )
                users.append(user)
            return users

        except (json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Error reading the JSON database: {e}")

    def save(self, users: List[User]) -> None:
        """
        Saves users to a JSON file.

        Converts User objects into serializable dictionaries
        and writes them to the specified file. Ensures that the target
        directory exists before saving.

        Args:
            users (List[User]): The list of users to be saved.
        """
        data = []
        for user in users:
            user_dict = {
                "id": user.get_id(),
                "first_name": user.get_first_name(),
                "last_name": user.get_last_name(),
                "email": user.get_email(),
                "history": [
                    {
                        "user_id": h.get_user_id(),
                        "action": h.get_action(),
                        "description": h.get_description(),
                        "timestamp": h.get_timestamp().isoformat(),
                    }
                    for h in user.history
                ],
            }
            data.append(user_dict)

        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
