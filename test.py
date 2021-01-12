import unittest
import datetime
from dateutil.tz import tzutc
from social_api import SocialNetworkConnector, Profile, Content
from api_vk import VkontakteConnector
from api_github import GithubConnector


class TestConnector(unittest.TestCase):
    """Tests

    TODO: Right now unit tests use my personal data (which is public anyway), 
    normally a test account should be created and used for testing.
    """

    def setUp(self):
        vk_conn = VkontakteConnector(
            login="LOGIN", password="PASSWORD"
            # token=""
        )

        github_conn = GithubConnector(
            # login="LOGIN", password="PASSWORD"
            token="TOKEN"
        )

        self.connector = SocialNetworkConnector({
            "vk.com": vk_conn,
            "github.com": github_conn,
        })

    def test_vkontakte_single_profile(self):
        self.connector.current_connector("vk.com")
        data: Profile = self.connector.get_user_profile("")
        expected: Profile = {
            'unique_id': 40841957,
            'visible_name': 'Артем Абрамов'
        }
        self.assertEqual(data["unique_id"], expected["unique_id"])
        self.assertEqual(data["visible_name"], expected["visible_name"])

    def test_vkontakte_personal_content(self):
        self.connector.current_connector("vk.com")
        data: list[Content] = list(self.connector.get_personal_content())
        expected: Content = {
            'date': datetime.datetime(2020, 3, 8, 19, 34, 11),
            'text': ''
        }
        self.assertEqual(data[0]["date"], expected["date"])
        self.assertEqual(data[0]["text"], expected["text"])

    def test_vkontakte_personal_followers(self):
        self.connector.current_connector("vk.com")
        data: list[Content] = list(self.connector.get_personal_followers())
        expected: Content = {
            'unique_id': 578439580,
            'visible_name': 'Petr Šindelář'
        }
        self.assertEqual(data[0]["unique_id"], expected["unique_id"])
        self.assertEqual(data[0]["visible_name"], expected["visible_name"])

    def test_github_single_profile(self):
        self.connector.current_connector("github.com")
        data: Profile = self.connector.get_user_profile("")
        expected: Profile = {
            'unique_id': 'temach',
            'visible_name': 'tematibr@gmail.com'
        }
        self.assertEqual(data["unique_id"], expected["unique_id"])
        self.assertEqual(data["visible_name"], expected["visible_name"])

    def test_github_personal_content(self):
        self.connector.current_connector("github.com")
        data: list[Content] = list(self.connector.get_personal_content())
        expected: Content = {
            'date': datetime.datetime(2020, 12, 13, 10, 50, 39, tzinfo=tzutc()),
            'text': 'Natural Language ToolKit',
        }
        self.assertEqual(data[1]["date"], expected["date"])
        self.assertEqual(data[1]["text"], expected["text"])

    def test_github_personal_followers(self):
        self.connector.current_connector("github.com")
        data: list[Content] = list(self.connector.get_personal_followers())
        expected: Content = {
            'unique_id': 'FedorArbuzov',
            'visible_name': 'Fedor Arbuzov'
        }
        self.assertEqual(data[0]["unique_id"], expected["unique_id"])
        self.assertEqual(data[0]["visible_name"], expected["visible_name"])


if __name__ == '__main__':
    unittest.main()
