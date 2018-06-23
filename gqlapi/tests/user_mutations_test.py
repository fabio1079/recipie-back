from django.test import TestCase, Client
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserMutationsTestCase(TestCase):

    def test_create_a_user(self):
        user_data = ('test@user.com', 'test123')
        c = Client()
        query = """
            mutation {
                createUser(
                    email: "%s",
                    password: "%s")
                {
                    user {
                        id
                        email
                    }
                }
            }
        """ % user_data

        response = c.post('/graphql/', {'query': query})
        json = response.json()

        created_user = json['data']['createUser']['user']

        self.assertEqual(created_user['email'], user_data[0])
        self.assertEqual(True, 'id' in created_user.keys())

    def test_cant_create_two_users_with_the_same_email(self):
        """Cant create users with the same email"""
        user_data = ('test@user.com', 'test123')
        c = Client()
        query = """
            mutation {
                createUser(
                    email: "%s",
                    password: "%s")
                {
                    user {
                        id
                        email
                    }
                }
            }
        """ % user_data

        response = c.post('/graphql/', {'query': query})
        json = response.json()

        created_user = json['data']['createUser']['user']

        self.assertEqual(created_user['email'], user_data[0])
        self.assertEqual(True, 'id' in created_user.keys())

        response = c.post('/graphql/', {'query': query})
        json = response.json()

        self.assertEqual(True, 'errors' in json.keys())
        error_message = 'UNIQUE constraint failed: accounts_user.email'
        self.assertEqual(error_message, json['errors'][0]['message'])
