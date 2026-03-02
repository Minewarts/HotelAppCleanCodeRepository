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
                
            
        
       
    def save(self, users: List[User] , get_id , get_name) -> None:

        new_users = get_id,get_name

        for user in users : 
            if :
                u
    


    
class JSONStorage:
    def __init__(self, filepath: Path):
        self.filepath = filepath

    def load(self) -> List[User]:
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r") as f:
            data = json.load(f)

        return [User(**item) for item in data]

    def save(self, users: List[User]) -> None:
        with open(self.filepath, "w") as f:
            json.dump([user.__dict__ for user in users], f, indent=2)
