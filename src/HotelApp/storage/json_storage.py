import json
from pathlib import Path
from typing import List

from ..models import User, Room


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
        reconstructs User and Room objects from the stored JSON data.

        Returns:
            List[User]: A list of reconstructed User objects.

        Raises:
            Exception: If there is an error reading or parsing the JSON file.
        """
        # Si el archivo no existe, devolvemos una lista vacía
        if not self.filepath.exists():
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            users: List[User] = []
            for item in data:
                # Reconstrucción robusta con claves esperadas
                user = User(
                    user_id=item["id"],
                    name=item["name"],
                    email=item["email"],
                )
                # Reconstruimos historial de habitaciones si existe
                for room_data in item.get("history", []):
                    room = Room(
                        room_number=room_data["room_number"],
                        room_type=room_data["room_type"],
                    )
                    # restauramos el estado (por seguridad, validar)
                    status = room_data.get("status", "available")
                    if status not in ("available", "occupied"):
                        status = "available"
                    room.set_status(status)
                    user.history.append(room)

                users.append(user)
            return users

        except (json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Error al leer la base de datos JSON: {e}")

    def save(self, users: List[User]) -> None:
        """
        Saves users to a JSON file.

        Converts User and Room objects into serializable dictionaries
        and writes them to the specified file. Ensures that the target
        directory exists before saving.

        Args:
            users (List[User]): The list of users to be saved.
        """
        data = []
        for user in users:
            # usamos los métodos getters (llamados)
            user_dict = {
                "id": user.get_id(),
                "name": user.get_name(),
                "email": user.get_email(),
                "history": [
                    {
                        "room_number": room.get_room_number(),
                        "room_type": room.get_room_type(),
                        "status": room.get_status(),
                    }
                    for room in user.history
                ],
            }
            data.append(user_dict)

        # aseguramos carpeta existe
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
