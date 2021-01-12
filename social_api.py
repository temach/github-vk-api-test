from typing import TypedDict, Any, Generator
from datetime import datetime


class Profile(TypedDict):
    visible_name: str
    unique_id: str


class Content(TypedDict):
    text: str
    date: datetime


class BaseSocialNetworkConnector():
    """Base class that serves to descibe the interface"""

    def get_user_profile(self, username: str = "") -> Profile:
        """Retrieve a user profile object for the specified user name.

        If name is not given returns the user profile of currently authenticated user.

        :param str username:
            name of the user
        """
        pass

    def get_personal_followers(self) -> Generator[Profile, None, None]:
        """Retrieve user profiles of followers/friends for the authenticated user."""
        pass

    def get_personal_content(self) -> Generator[Content, None, None]:
        """Retrieve content generate by the currently authenticated user in the social network."""
        pass


class SocialNetworkConnector(BaseSocialNetworkConnector):
    """Selects bewteen multiple specific connectors.

    To switch the current connector call the "current_connector" function.
    """

    def __init__(self, connectors):
        self.connectors = connectors
        self.current = None

    def current_connector(self, social_network_root_domain):
        self.current = self.connectors[social_network_root_domain]

    def get_user_profile(self, username):
        return self.current.get_user_profile(username)

    def get_personal_followers(self):
        return self.current.get_personal_followers()

    def get_personal_content(self):
        return self.current.get_personal_content()
