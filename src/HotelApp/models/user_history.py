from __future__ import annotations
from typing import List
from .exceptions import InvalidUserDataError



class User_History:
    """
    The User_History component is designed to represent and manage the relationship between users and the rooms in which they stay.
    Its primary purpose is to provide a structured and traceable record of room occupancy over time, 
    enabling efficient tracking, querying, and analysis of user-room interactions.
    
    Attributes:
        _name (str): Name of the hotel.
        _stars (int | None): Star rating of the hotel.
        _rooms (List[Room]): List of rooms available in the hotel.
        _clients (List[User]): List of registered clients.
    """