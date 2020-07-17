import os
from time import sleep
from django.test import override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import encode_multipart
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Post, Image, Category


User = get_user_model()

static_dir = settings.STATIC_ROOT

def create_image():
    """Create image object for post by given image path"""

    image_path = os.path.join(static_dir, 'img/test_image.png')

    image = SimpleUploadedFile(name='test_image.png',
        content=open(image_path, 'rb').read(),
        content_type='image/png')

    return image



def remove_file(path):
    """Remove a file if exists"""
    
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as ex:
        print(ex)



class ImageAPITests(APITestCase):
    user_info = {
        'username': 'user',
        'email': 'user@example.com',
        'password': 'user123456'
    }

    user_info2 = {
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'user123456'
    }

    def setUp(self):
        self.user = User.objects.create_user(**self.user_info)
        self.user2 = User.objects.create_user(**self.user_info2)
        
        # category slug: دسته-بندی-اول
        self.cat1 = Category.objects.create(title='دسته بندی اول')
        
        # category slug: دسته-بندی-دوم
        self.cat2 = Category.objects.create(title='دسته بندی دوم')

        # create two Image objects for `user`
        Image.objects.create(category=self.cat1, image=create_image(),
            owner=self.user)
        Image.objects.create(category=self.cat2, image=create_image(),
            owner=self.user)

        # create one Image object for `user2`
        Image.objects.create(category=self.cat1, image=create_image(),
            owner=self.user2)
        
        self.total_objects = Image.objects.count()


    def test_list_images(self):
        """List Image objects for authenticated user"""

        url = reverse('post:image_user-list')
        response = self.client.get(url)

        # 401 - unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate user
        self.client.login(**self.user_info)
 
        response = self.client.get(url)
        # 200 - OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.json()['results']
        # `user` has two Image objects
        self.assertEqual(len(results), 2)

        # check total images
        self.assertEqual(Image.objects.count(), self.total_objects)


    def test_get_single_image(self):
        """Get Image object"""

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        
        image2 = Image.objects.filter(
            owner__username=self.user2.username).first()

        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})
        response = self.client.get(url)

        # 401 - unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate user
        self.client.login(**self.user_info)
 
        response = self.client.get(url)
        # 200 - OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try to get Image object not belongs to `user`
        url = reverse('post:image_user-detail', kwargs={'pk': image2.pk})
        response = self.client.get(url)
        # 404 - Not found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_image(self):
        """Create Image object with all required fields set"""

        url = reverse('post:image_user-list')

        image = {
            'title': 'Test Image',
            'category': 'دسته-بندی-اول',
            'image': create_image()
        }
        response = self.client.post(url, image)

        # 401 - unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate user
        self.client.login(**self.user_info)

        image = {
            'title': 'Test Image',
            'category': 'دسته-بندی-اول',
            'image': create_image()
        }
        response = self.client.post(url, image)

        # 201 - CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # we added one object
        self.assertEqual(Image.objects.count(), self.total_objects + 1)


    def test_create_image_with_no_category_and_image_field(self):
        """Create Image object with category and image fields left empty"""

        url = reverse('post:image_user-list')

        # authenticate user
        self.client.login(**self.user_info)

        image = {}
        response = self.client.post(url, image)
        
        # 400 - Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # no object got added
        self.assertEqual(Image.objects.count(), self.total_objects)


    def test_create_image_with_no_category_field(self):
        """Create Image object with category field left empty"""

        url = reverse('post:image_user-list')

        # authenticate user
        self.client.login(**self.user_info)

        image = {
            'title': 'Test Image',
            'image': create_image()
        }
        response = self.client.post(url, image)
        
        # 400 - Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # no object got added
        self.assertEqual(Image.objects.count(), self.total_objects)


    def test_create_image_with_no_image_field(self):
        """Create Image object with image field left empty"""

        url = reverse('post:image_user-list')

        # authenticate user
        self.client.login(**self.user_info)

        image = {
            'category': 'دسته-بندی-اول'
        }
        response = self.client.post(url, image)
        
        # 400 - Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # no object got added
        self.assertEqual(Image.objects.count(), self.total_objects)


    def test_create_image_with_throttling(self):
        """Create images and test throttling"""

        url = reverse('post:image_user-list')

        # authenticate user
        self.client.login(**self.user_info)

        # create Image objects
        for i in range(10):
            image = {
                'title': 'Test Image',
                'category': 'دسته-بندی-اول',
                'image': create_image()
            }
            response = self.client.post(url, image)
            # 201 - CREATED
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        image = {
            'title': 'Test Image',
            'category': 'دسته-بندی-اول',
            'image': create_image()
        }
        response = self.client.post(url, image)
        
        # 429 - too many requests
        self.assertEqual(response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS)

        # ten more objects got added
        self.assertEqual(Image.objects.count(), self.total_objects + 10)


    def test_update_category_field_via_patch_method(self):
        """
        Test updating category field of Image objects.
        Test throttling.
        """

        # update image (patch)
        data = {
            'category': 'دسته-بندی-دوم'
        }

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        response = self.client.patch(url, data)
        # 401 - unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


        # authenticate user
        self.client.login(**self.user_info)

        for i in range(10):
            response = self.client.patch(url, data)
            # 200 - OK
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(url, data)
        # 429 - too many requests
        self.assertEqual(response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS)


    def test_update_image_field_via_patch_method(self):
        """
        Test updating image field of Image objects.
        Test throttling.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        # update image (patch)
        for i in range(10):
            data = {
                'image': create_image()
            }
            response = self.client.patch(url, data)
            # 200 - OK
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'image': create_image()
        }
        response = self.client.patch(url, data)

        # 429 - too many requests
        self.assertEqual(response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS)


    def test_update_category_field_via_patch_method_leave_field_empty(self):
        """
        Test updating category field of Image objects.
        Leave category field empty.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {
            'category': ''
        }
        response = self.client.patch(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_image_field_via_patch_method_leave_field_empty(self):
        """
        Test updating category field of Image objects.
        Leave category field empty.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {
            'image': ''
        }
        response = self.client.patch(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_via_patch_method_leave_required_fields_empty(self):
        """
        Test updating Image objects.
        Leave all required fields empty.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {
            'category': '',
            'image': ''
        }
        response = self.client.patch(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_via_put_method_leave_required_fields_empty(self):
        """
        Test updating Image objects.
        Leave all required fields empty.
        """

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {
            'category': '',
            'image': ''
        }

        response = self.client.put(url, data)
        # 401 - unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate user
        self.client.login(**self.user_info)

        response = self.client.put(url, data)
        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_via_put_method_no_field_set(self):
        """
        Test updating Image objects.
        Not settings any of the fields.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {}
        response = self.client.put(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_via_put_method_set_all_required_fields(self):
        """
        Test updating Image objects.
        Set all required fields.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        for i in range(10):
            # remove old image file
            remove_file(image.image.path)
            data = {
                'category': 'دسته-بندی-دوم',
                'image': image
            }
            response = self.client.put(url, data)

        data = {
            'category': 'دسته-بندی-دوم',
            'image': image
        }
        response = self.client.put(url, data)

        # 429 - too many requests
        self.assertEqual(response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS)


    def test_update_via_put_method_leave_one_field_empty(self):
        """
        Test updating Image objects.
        Leave one required field empty.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {
            'category': 'دسته-بندی-دوم',
            'image': ''
        }
        response = self.client.put(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'category': '',
            'image': create_image()
        }
        response = self.client.put(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_update_via_put_method_one_field_not_set(self):
        """
        Test updating Image objects.
        Not settings one of the reqiured fields.
        """

        # authenticate user
        self.client.login(**self.user_info)

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})

        data = {
            'category': 'دسته-بندی-دوم',
        }
        response = self.client.put(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'image': create_image()
        }
        response = self.client.put(url, data)

        # 400 - Bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_image(self):
        """
        Test deleting Image objects.
        """

        image = Image.objects.filter(
            owner__username=self.user.username).first()
        url = reverse('post:image_user-detail', kwargs={'pk': image.pk})
        response = self.client.delete(url)

        # 401 - unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate user
        self.client.login(**self.user_info)

        response = self.client.delete(url)
        # 204 - No content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # we must have zero Image object in database
        self.assertEqual(Image.objects.count(), 2)



    def tearDown(self):
        """Remove image files"""
        
        images = Image.objects.all()
        for image in images:
            remove_file(image.image.path)
