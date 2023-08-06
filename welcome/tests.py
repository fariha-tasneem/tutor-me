from django.test import TestCase, Client
from .models import User, UserManager, Schedule
from django.urls import reverse

#Create your tests here.
class BasicTestingTests(TestCase):
    '''
    These are simple tests that should always pass since they have nothing to do with the project itself. 
    If one of these were to fail then something is probably broken with our testing system.
    '''
    def test_False_is_False(self):
        self.assertFalse(False)

    def test_True_is_True(self):
        self.assertTrue(True)

    def test_one_plus_one_is_two(self):
        self.assertEqual(1 + 1, 2)
    
    def test_one_plus_one_is_not_three(self):
        self.assertNotEqual(1 + 1, 3)


class UserTests(TestCase):
    '''
    These are tests for the User model. Eventually once large enough they should be moved to their own test file.
    '''
    # @classmethod
    # def setUpTestData(cls):
    #     model = User
    #     cls.user = model.objects.create_superuser(email="foobar@user.com", password="123abc", type="tut")
        
    # def test_new_test(self):
        
    #     self.assertEqual(self.user.email, )
    None


# class WebpageResponseTests(TestCase):
#     '''
#     These are tests to check that there are responses for each webpage.
#     '''

#     def test_welcome_index(self):
#         response = self.client.get(reverse('welcome:index'))
#         self.assertEqual(response.status_code, 200)

#     def test_welcome_selectType(self):
#         response = self.client.get(reverse('welcome:selectType'))
#         self.assertEqual(response.status_code, 200)

#     # def test_welcome_tutor(self):
#     #     model = User
#     #     model.objects.create_superuser(email="foobar@user.com", password="123abc", type="tut")
#     #     self.client.login(username="foobar@user.com", password="123abc")

#     #     response = self.client.get(reverse('welcome:tutor'))
#     #     self.assertEqual(response.status_code, 200)



#     # def test_welcome_student(self):
#     #     response = self.client.get(reverse('welcome:student'))
#     #     self.assertEqual(response.status_code, 200)

#     def test_welcome_finishSingup(self):
#         response = self.client.get(reverse('welcome:finishSignup'))
#         self.assertEqual(response.status_code, 200)

#     def test_welcome_selectClass(self):
#         response = self.client.get(reverse('welcome:selectClass'))
#         self.assertEqual(response.status_code, 200)

#     def test_welcome_findClass(self):
#         response = self.client.get(reverse('welcome:findClass'))
#         self.assertEqual(response.status_code, 200)

#     # def test_welcome_addToSchedule(self):
#     #     response = self.client.get(reverse('welcome:addToSchedule'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_welcome_viewTutorTime(self):
#     #     response = self.client.get(reverse('welcome:viewTutorTime'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_welcome_requestTutorTime(self):
#     #     response = self.client.get(reverse('welcome:requestTutorTime'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_welcome_findClassByTime(self):
#     #     response = self.client.get(reverse('welcome:findClassByTime'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_welcome_selectTimings(self):
#     #     response = self.client.get(reverse('welcome:selectTimings'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_welcome_confirmTimings(self):
#     #     response = self.client.get(reverse('welcome:confirmTimings'))
#     #     self.assertEqual(response.status_code, 200)

#     # def test_welcome_requestChoice(self):
#     #     response = self.client.get(reverse('welcome:requestChoice'))
#     #     self.assertEqual(response.status_code, 200)


# class UserManagerTests(TestCase):
#     '''
#     These are tests for the UserManager model. Eventually once large enough they should be moved to their own test file.
#     '''
#     def test_create_superuser_instance(self):
#         model = User
#         admin_user = model.objects.create_superuser(email="foobar@user.com", password="123abc", type="tut")
#         self.assertTrue(isinstance(admin_user, User))

#     def test_create_user_instance(self):
#         model = User
#         user = model.objects._create_user(email="foobar@user.com", password="123abc", type="tut", is_staff=False, is_superuser=False)
#         self.assertTrue(isinstance(user, User))

#     # def test_create_user_instance_2(self):
#     #     model = User
#     #     user = model.objects.create_user(email="foo2@user.com", password="123")
#     #     self.assertTrue(isinstance(user, User))

    

class ScheduleTests(TestCase):
    '''
    These are tests for the Schedule model. Eventually once large enough they should be moved to their own test file.
    '''
    None