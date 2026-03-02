from .exceptions import InvalidUserDataError


class User:
    def __init__(self, user_id:int, name:str, email:str):
        self._validate_id(user_id)
        self._validate_email(email)

        self._id=user_id
        self._name=name
        self._email=email
        self.history:list[Room]= []

    @property
    def get_id(self):
        return  self._id
    
    @property
    def get_name(self):
        return self._name

    @property
    def get_email(self):
        return self._email

    def set_email(self, new_email):
        self.validate_email(new_email)
        self._email=new_email

    def _validate_id(self, user_id):
        if user_id <=0:
            raise InvalidUserDataError("User id must be positive")
        
    def _validate_email(self, user_email):
        if "@" not in user_email:
            raise InvalidUserDataError("Invalid Email: there is not '@'")
        
class Room:
    def __init__(self, room_number:int, room_type:str):
        self._room_number=room_number
        self._room_type=room_type
        self._status:bool="available"

        def get_room_number(self):
            return self._room_number

        def get_room_type(self):
            return self._room_type
        
        def get_status(self):
            return self._status
        
        
        def set_status(self):
            if self._status == 'occupied':
                self._status='available'
            else:
                self._status='occupied'

        
class Hotel:
    def __init__(self, name:str):
        self._name=name
        self._rooms:list[Room]=[]
        self._clients:list[User]=[]
        

    @property
    def get_name(self):
        return self._name
    
    @property
    def get_stars(self):
        return self._stars
    
    def get_cliets_by_id(self, client_id):
        for client in self._clients:
            if client.get_id == client_id:
                return client
        return None
    
    def get_room_by_number(self, room_number):
        for room in self._rooms:
            if room.get_room_number() == room_number:
                return room
        return None
    
    def get_room_by_type(self, room_type):
        for room in self._rooms:
            if room.get_room_type() == room_type:
                return room