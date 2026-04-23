from __future__ import annotations
from typing import List
from ..exceptions import InvalidUserDataError



class User_History:
    """
    The User_History component is designed to represent and manage the relationship between users and the rooms in which they stay.
    Its primary purpose is to provide a structured and traceable record of room occupancy over time, 
    enabling efficient tracking, querying, and analysis of user-room interactions.

    Attributes:
        _id (int): Unique identifier of the user.
        _name (str): Name of the user.
        check_in: Timestamp indicating when the user entered the room
        check_out: Timestamp indicating when the user left the room (nullable if ongoing)
    """
    