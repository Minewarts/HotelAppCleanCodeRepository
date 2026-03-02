import json
from pathlib import Path
from typing import List
from .models import User 
from typing import Protocol


class Storage(Protocol):
    def load(self, filepath: Path) -> List[User]: 
        self.filepath  = filepath

        if not filepath.exists():
            return []

        users = []

        with open(filepath, "r") as archivo:
            for line in archivo:
                get_id, get_name  = line.strip().split(",")
                user = User(int(get_id), get_name)
                users.append(user)


            return users
                
            
        
       
    def save(self, users: List[User]) -> None :
        data = []

        for user in users:
            data.append(user.to_dict())

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=2)
