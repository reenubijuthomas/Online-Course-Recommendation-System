from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User, auth
from course.models import Course, Rating, Chapter
import time


class TestIntegrated(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='integrated_tests/chromedriver.exe')


    def tearDown(self):
        self.browser.close()

    def dtest_home(self):
        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        time.sleep(10)
        self.assertEqual(main.find_element_by_tag_name('h2').text, "Hello!")

    def dtest_signup(self):
        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        form = self.browser.find_element_by_tag_name('form')
        first_name = form.find_element_by_name('first_name')
        last_name = form.find_element_by_name('last_name')
        username = form.find_element_by_name('username')
        email = form.find_element_by_name('email')
        password1 = form.find_element_by_name('password1')
        password2 = form.find_element_by_name('password2')
        submit_button = form.find_element_by_id("register_button")

        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        submit_button.click()

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

    def dtest_signup_invalid_existing_username(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@email.com")
        self.user.set_password('123456')
        self.user.save()

        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        form = self.browser.find_element_by_tag_name('form')
        first_name = form.find_element_by_name('first_name')
        last_name = form.find_element_by_name('last_name')
        username = form.find_element_by_name('username')
        email = form.find_element_by_name('email')
        password1 = form.find_element_by_name('password1')
        password2 = form.find_element_by_name('password2')
        submit_button = form.find_element_by_id("register_button")

        first_name.send_keys("test2")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser2@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        submit_button.click()

        self.assertFalse(User.objects.filter(first_name="test2").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))

    def dtest_signup_invalid_existing_email(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@email.com")
        self.user.set_password('123456')
        self.user.save()

        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        form = self.browser.find_element_by_tag_name('form')
        first_name = form.find_element_by_name('first_name')
        last_name = form.find_element_by_name('last_name')
        username = form.find_element_by_name('username')
        email = form.find_element_by_name('email')
        password1 = form.find_element_by_name('password1')
        password2 = form.find_element_by_name('password2')
        submit_button = form.find_element_by_id("register_button")

        first_name.send_keys("test2")
        last_name.send_keys("user")
        username.send_keys("testuser2")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        submit_button.click()

        self.assertFalse(User.objects.filter(first_name="test2").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))

    def dtest_login(self):
        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url+reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

    def dtest_login_invalid_username(self):
        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser2")
        login_form.find_element_by_name('password').send_keys("123456")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url+reverse('login'))

    def dtest_login_invalid_password(self):
        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("12345")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url+reverse('login'))

    def dtest_profile(self):
        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

        self.browser.find_element_by_link_text("Profile").click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Profile")
        self.assertEqual(self.browser.find_element_by_id('topics').text,
                         "Favourite Topics: <No Favourite Topics Added Yet>")

        self.browser.find_element_by_name("topics").send_keys("Java,Android")
        self.browser.find_element_by_id("submit_button").click()

        self.assertEqual(self.browser.find_element_by_id('topics').text, "Favourite Topics: Java,Android")

    def dtest_recommendation(self):
        course = Course()
        course.pk = 1
        course.name = "testCourse"
        course.topics = "Java,Android"
        course.save()

        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

        self.browser.find_element_by_link_text("Profile").click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Profile")
        self.assertEqual(self.browser.find_element_by_id('topics').text,
                         "Favourite Topics: <No Favourite Topics Added Yet>")

        self.browser.find_element_by_name("topics").send_keys("Java,Android")
        self.browser.find_element_by_id("submit_button").click()

        self.assertEqual(self.browser.find_element_by_id('topics').text, "Favourite Topics: Java,Android")

        self.browser.find_element_by_link_text("Learn With Us!").click()
        self.browser.find_element_by_link_text("View Recommendations").click()

        self.assertEqual(self.browser.find_element_by_id("rec2").text, "Courses based on your favourite topics:")
        c_main = self.browser.find_element_by_tag_name('main')
        course = c_main.find_element_by_tag_name('a')
        course.click()
        time.sleep(2)

        self.assertEqual(self.browser.find_element_by_id('cname').text, "testCourse")

    def dtest_rate(self):
        course = Course()
        course.pk = 1
        course.name = "testCourse"
        course.topics = "Java,Android"
        course.save()

        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        submit_button.click()

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

        self.browser.find_element_by_link_text("Profile").click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Profile")
        self.assertEqual(self.browser.find_element_by_id('topics').text,
                         "Favourite Topics: <No Favourite Topics Added Yet>")

        self.browser.find_element_by_name("topics").send_keys("Java,Android")
        self.browser.find_element_by_id("submit_button").click()

        self.assertEqual(self.browser.find_element_by_id('topics').text, "Favourite Topics: Java,Android")

        self.browser.find_element_by_link_text("Learn With Us!").click()
        self.browser.find_element_by_link_text("View Recommendations").click()

        self.assertEqual(self.browser.find_element_by_id("rec2").text, "Courses based on your favourite topics:")
        c_main = self.browser.find_element_by_tag_name('main')
        course = c_main.find_element_by_tag_name('a')
        course.click()

        self.assertEqual(self.browser.find_element_by_id('cname').text, "testCourse")
        self.assertEqual(self.browser.find_element_by_id('rating').text, "Current rating: Not yet rated")

        rating = Select(self.browser.find_element_by_name("rating"))
        rating.select_by_visible_text('Like')
        self.browser.find_element_by_id("rate_submit").click()

        time.sleep(10)
        c_main = self.browser.find_element_by_tag_name('main')
        course = c_main.find_element_by_tag_name('a')
        course.click()
        time.sleep(10)

        self.assertEqual(self.browser.find_element_by_id('rating').text, "Current rating: Liked")

    def dtest_view_course(self):
        course = Course()
        course.pk = 1
        course.name = "testCourse"
        course.topics = "Java,Android"
        course.save()

        self.browser.get(self.live_server_url)
        time.sleep(10)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        submit_button.click()

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

        self.browser.find_element_by_link_text("Profile").click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Profile")
        self.assertEqual(self.browser.find_element_by_id('topics').text,
                         "Favourite Topics: <No Favourite Topics Added Yet>")

        self.browser.find_element_by_name("topics").send_keys("Java,Android")
        self.browser.find_element_by_id("submit_button").click()

        self.assertEqual(self.browser.find_element_by_id('topics').text, "Favourite Topics: Java,Android")

        self.browser.find_element_by_link_text("Learn With Us!").click()
        self.browser.find_element_by_link_text("View Courses").click()

        self.assertEqual(self.browser.find_element_by_id("courses").text, "Available Courses")
        c_main = self.browser.find_element_by_tag_name('main')
        course = c_main.find_element_by_tag_name('a')
        course.click()

        self.assertEqual(self.browser.find_element_by_id('cname').text, "testCourse")



    def dtest_logout(self):
        self.browser.get(self.live_server_url)
        time.sleep(10)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url+reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

        self.browser.find_element_by_id("logout").click()
        time.sleep(2)
        self.assertEqual(self.browser.current_url,self.live_server_url+reverse('home'))
        self.assertEqual(self.browser.find_element_by_tag_name('h2').text, "Hello!")

    def test_video(self):
        course = Course()
        course.pk = 1
        course.name = "testCourse"
        course.topics = "Java,Android"
        course.save()

        chapter = Chapter()
        chapter.pk = 1
        chapter.name = "Chapter 1"
        chapter.course = course
        chapter.video  = "https://www.youtube.com/"
        chapter.save()

        self.browser.get(self.live_server_url)
        main = self.browser.find_element_by_tag_name('main')
        signup_button = main.find_element_by_link_text('Signup')
        time.sleep(1)
        signup_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('register'))
        signup_form = self.browser.find_element_by_tag_name('form')
        first_name = signup_form.find_element_by_name('first_name')
        last_name = signup_form.find_element_by_name('last_name')
        username = signup_form.find_element_by_name('username')
        email = signup_form.find_element_by_name('email')
        password1 = signup_form.find_element_by_name('password1')
        password2 = signup_form.find_element_by_name('password2')
        submit_button = signup_form.find_element_by_id("register_button")

        time.sleep(1)
        first_name.send_keys("test")
        last_name.send_keys("user")
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("123456")
        password2.send_keys("123456")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

        time.sleep(1)
        login_form = self.browser.find_element_by_tag_name('form')
        login_form.find_element_by_name('username').send_keys("testuser")
        login_form.find_element_by_name('password').send_keys("123456")
        time.sleep(1)
        login_form.find_element_by_id('submit_button').click()

        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('home'))
        self.assertTrue(self.browser.find_element_by_tag_name('h2').text, "Hello! Good to see you here.")

        self.browser.find_element_by_link_text("Profile").click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Profile")
        self.assertEqual(self.browser.find_element_by_id('topics').text,
                         "Favourite Topics: <No Favourite Topics Added Yet>")

        self.browser.find_element_by_name("topics").send_keys("Java,Android")
        self.browser.find_element_by_id("submit_button").click()

        self.assertEqual(self.browser.find_element_by_id('topics').text, "Favourite Topics: Java,Android")

        self.browser.find_element_by_link_text("Learn With Us!").click()
        self.browser.find_element_by_link_text("View Recommendations").click()

        self.assertEqual(self.browser.find_element_by_id("rec2").text, "Courses based on your favourite topics:")
        c_main = self.browser.find_element_by_tag_name('main')
        course = c_main.find_element_by_tag_name('a')
        course.click()
        time.sleep(2)

        self.assertEqual(self.browser.find_element_by_id('cname').text, "testCourse")

        self.browser.find_element_by_id('chapter_list').click()
        time.sleep(5)
        self.assertEqual(self.browser.find_element_by_id('cname').text, "Chapter 1")

