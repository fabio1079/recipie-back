from django.test import TestCase, Client
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserQueryTestCase(TestCase):
    def setUp(self):
        if not UserModel.objects.filter(email='admin@test.com').exists():
            self.admin_user = UserModel.objects.create_superuser(
                email='admin@test.com', password='test')

        self.user1, created = UserModel.objects.get_or_create(
            email='user1', defaults={'email': 'user1@test.com',
                                     'password': 'test'})

    def test_user_can_get_its_own_data(self):
        """An user can get its own data"""
        c = Client()
        query = """
            query {
                me {
                    id
                    email
                }
            }
        """

        response = c.post('/graphql/', {'query': query})
        expected_message = 'You do not have permission to perform this action'
        self.assertEqual(response.json()['errors']
                         [0]['message'], expected_message)

        token = get_token(self.user1)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        json = response.json()
        self.assertEqual(json['data']['me']['id'], str(self.user1.id))
        self.assertEqual(json['data']['me']['email'], self.user1.email)

    def test_only_admin_can_get_users(self):
        """Only an admin can get all users"""
        c = Client()
        query = """
            query {
                users {
                    id
                    email
                }
            }
        """

        token = get_token(self.user1)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        expected_message = 'You do not have permission to perform this action'
        self.assertEqual(response.json()['errors']
                         [0]['message'], expected_message)

        token = get_token(self.admin_user)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        json = response.json()
        self.assertEqual(len(json['data']['users']), 2)

    def test_only_admin_can_get_user(self):
        """Only an admin can get a user data"""
        c = Client()
        query = """
            query {
                user(id: %d) {
                    id
                    email
                }
            }
        """ % self.user1.id

        token = get_token(self.user1)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        expected_message = 'You do not have permission to perform this action'
        self.assertEqual(response.json()['errors']
                         [0]['message'], expected_message)

        token = get_token(self.admin_user)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        json = response.json()
        self.assertEqual(json['data']['user']['id'], str(self.user1.id))

    def test_get_user_by_email(self):
        """Only get user by its email"""
        c = Client()
        query = """
            query {
                user(email: "%s") {
                    id
                    email
                }
            }
        """ % self.user1.email

        token = get_token(self.admin_user)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        json = response.json()
        self.assertEqual(json['data']['user']['id'], str(self.user1.id))

    def test_user_not_found(self):
        """UserModel not found message"""
        c = Client()
        query = """
            query {
                user {
                    id
                    email
                }
            }
        """

        token = get_token(self.admin_user)
        response = c.post('/graphql/', {'query': query},
                          **{
                              'HTTP_AUTHORIZATION': 'JWT %s' % token, })

        expected_message = 'User matching query does not exist.'
        self.assertEqual(response.json()['errors']
                         [0]['message'], expected_message)
