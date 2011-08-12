"""

### Testing simple posts ...


# Create us a test user ..
>>> from django.contrib.auth.models import User
>>> testuser = User.objects.create_user( 'sometestuser', 'testuser@sphene.net', 'testpassword' )
>>> testuser.save()

>>> testuser2 = User.objects.create_user( 'sometestuser2', 'testuser2@sphene.net', 'testpassword2' )
>>> testuser2.save()

>>> from django import http
>>> from sphene.community.testutils import setup_threadlocals
>>> from sphene.community.middleware import get_current_user

>>> req = setup_threadlocals(testuser, set_group=False)
>>> get_current_user().username
'sometestuser'

>>> from sphene.sphboard.models import Post, Category
>>> c = Category.objects.get( name = 'Example Category' )

>>> c.has_new_posts()
False

# Touch the category, ignore output
>>> c.touch(req.session, req.user) == None
False

>>> p = Post( category = c, subject = 'Test Subject', 
...           body = "Some body", markup = 'bbcode', author = testuser )
>>> p.save()
>>> p.author.username == u'sometestuser'
True

# Install monitor
>>> p.toggle_monitor() == None
False

# Check flag options
>>> p.is_sticky()
0
>>> p.is_poll()
0
>>> p.is_closed()
0

######
# Verify display of new posts for category
>>> c.has_new_posts()
True

# Touch the category, ignore output
>>> c = Category.objects.get( pk = c.id )
>>> c.touch(req.session, req.user) == None
False

>>> p.has_new_posts()
True

>>> p.touch(req.session, req.user) == None
True


>>> c = Category.objects.get( pk = c.id )
>>> c.has_new_posts()
False

#
######


>>> p.get_threadinformation().post_count
1
>>> p2 = Post( category = c, subject = 'Re: Test Subject', body = "some reply", markup = 'bbcode', thread = p, author = testuser2 )
>>> p2.save()

#######
# Again check new post display
>>> c.has_new_posts()
True

>>> p.touch(req.session, req.user) == None
True

>>> p.has_new_posts()
False

>>> c = Category.objects.get( pk = c.id )
>>> c.has_new_posts()
False

# Check catchup

>>> p3 = Post( category = c, subject = 'Re: Test Subject', body = "some reply", markup = 'bbcode', thread = p, author = testuser2 )
>>> p3.save()

>>> c = Category.objects.get( pk = c.id )
>>> c.has_new_posts()
True

>>> c.catchup(req.session, req.user)
>>> c = Category.objects.get( pk = c.id )
>>> c.has_new_posts()
False

>>> p = Post.objects.get( pk = p.id )
>>> p.has_new_posts()
False


#
#########

# Validate outgoing email ..
>>> from django.core import mail
>>> mail.outbox[0].subject
u'New Forum Post in "Example Category": Re: Test Subject'
>>> len(mail.outbox)
2

# Validate thread information ..
>>> p = Post.objects.get( pk = p.id )
>>> p.get_threadinformation().post_count
3
>>> p.get_threadinformation().latest_post == p3
True
>>> p.get_threadinformation().view_count
0
>>> p.viewed(req.session, req.user)
>>> p.get_threadinformation().view_count
1

# Check that the category returns the correct information ..
>>> c.postCount()
3
>>> c.threadCount()
1



#####################################
#
# testing flag permission system ...
#

>>> from sphene.community import testutils
>>> from sphene.community.models import Role, RoleMember, PermissionFlag, RoleMemberLimitation
>>> from django.contrib.contenttypes.models import ContentType
>>> group = testutils.get_testgroup()
>>> req = testutils.setup_threadlocals(testuser, group)

# Verify that we don't have permission ...
>>> c.allowview = 3
>>> c.allowreplies = 3
>>> c.allowthreads = 3
>>> c.save()

>>> c.has_view_permission()
False

# First create a moderator role ...
>>> moderators = Role( name = 'Moderators', group = group )
>>> moderators.save()
>>> moderators.permission_flags.add( PermissionFlag.objects.get( name = 'sphboard_view' ) )
>>> role_member = RoleMember( role = moderators, user = testuser, has_limitations = True )
>>> role_member.save()
>>> RoleMemberLimitation( role_member = role_member, content_object = c ).save()

# Check for a second category that the user as still no right to view it.
>>> c2 = Category( name = "Second example" )
>>> c2.allowview = 3
>>> c2.save()

>>> c2.has_view_permission()
False

# Check if we have view permission in the original category ..
>>> c.has_view_permission()
True

"""

from django.test import TestCase
from sphene.community import testutils
from sphene.community.models import Role, PermissionFlag, RoleMember, RoleMemberLimitation
from sphene.sphboard.models import Category, Post, ThreadInformation
from sphene.community.sphutils import sph_reverse


class PermissionRoleTester(TestCase):
    
    def setUp(self):
        self.testuser = testutils.get_testuser()
        self.testgroup = testutils.get_testgroup()
        testutils.setup_threadlocals(self.testuser, self.testgroup)

        # Setup test role ..
        self.testrole = testutils.get_testrole()

        # Test category
        # Since we are testing permissions .. revoke all permissions
        self.c = Category(name = 'Simple Test Category',
                          allowview = 3,
                          allowreplies = 3,
                          allowthreads = 3,)
        self.c.save()

    def __assign_flag(self, flag, role = None ):
        if not role:
            role = self.testrole

        role.permission_flags.add( PermissionFlag.objects.get( name = flag ) )

    def __add_user_to_role(self, obj = None, user = None, role = None):
        if user is None:
            user = self.testuser
        if role is None:
            role = self.testrole

        role_member = RoleMember( role = role,
                                  user = user,
                                  has_limitations = obj is not None )
        role_member.save()

        if obj is not None:
            RoleMemberLimitation( role_member = role_member,
                                  content_object = obj, ).save()

    def __create_testpost(self):
        # Create post ...
        p = Post( category = self.c, subject = 'Just a test post', body = 'hehe', author = self.testuser )
        p.save()
        return p

    def test_view_permission(self):
        self.failIf(self.c.has_view_permission(), 'Verify that we do not have view permission.')
        self.__assign_flag( 'sphboard_view' )
        self.__add_user_to_role( self.c )
        self.failUnless(self.c.has_view_permission(), "Verify we have view permission.")

    def test_post_threads_permission(self):
        self.__assign_flag( 'sphboard_post_threads' )
        self.failIf(self.c.allowPostThread(self.testuser), 'Verify that we do not have post thread permission.')
        self.__add_user_to_role( self.c )
        self.failUnless(self.c.allowPostThread(self.testuser), 'Verify that we have post thread permission.')

    def test_post_replies_permission(self):
        p = self.__create_testpost()
        self.__add_user_to_role( self.c )
        self.failIf(p.allow_posting(self.testuser), 'Verify that we do not have repy permission.')
        self.__assign_flag( 'sphboard_post_replies' )
        self.failUnless(p.allow_posting(self.testuser), 'Verify that wehave reply permission.')

    def test_allow_editing(self):
        p = self.__create_testpost()
        # I know we can edit it, since we are the original author ..
        self.failUnless(p.allow_editing())
        p.author = testutils.get_superuser()
        p.save()
        # Now we must not have edit permission
        self.failIf(p.allow_editing())
        self.__add_user_to_role( self.c )
        self.__assign_flag( 'sphboard_editallposts' )
        self.failUnless(p.allow_editing())

    def test_allow_moving_post(self):
        p = self.__create_testpost()
        self.failIf(p.allow_moving_post())
        # add permission
        self.__add_user_to_role(self.c)
        self.__assign_flag('sphboard_moveallposts')
        self.failUnless(p.allow_moving_post())


class PostMovingTester(TestCase):

    def setUp(self):
        """
            We have 2 categories cat1 and cat2 and 2 threads (total 4 posts):

              cat1/                  -- category cat1
                 cat1_p1             -- thread/post c1_p1 in category cat1
                   cat1_p2           -- post c1_p2 in thread cat1_p1
                   cat1_p3           -- post c1_p3 in thread cat1_p1
              cat2/                  -- category cat2
                 cat2_p1             -- thread/post cat2_p1 in category cat2
        """
        self.testuser = testutils.get_testuser()
        self.superuser = testutils.get_superuser()
        self.testgroup = testutils.get_testgroup()
        testutils.setup_threadlocals(self.testuser, self.testgroup)

        # Setup test role ..
        self.testrole = testutils.get_testrole()

        # Test category 1
        self.cat1 = Category(name = 'Category 1',
                          allowview = 3,
                          allowreplies = 3,
                          allowthreads = 3,
                          group = self.testgroup)
        self.cat1.save()

        self.cat2 = Category(name = 'Category 2',
                          allowview = 3,
                          allowreplies = 3,
                          allowthreads = 3,
                          group = self.testgroup)
        self.cat2.save()

        # create thread 1 in category c1
        self.cat1_p1 = Post(category = self.cat1,
                          subject = 'Post p1 in category c1',
                          body = "post 1",
                          markup = 'bbcode',
                          author = self.testuser)
        self.cat1_p1.save()

        self.cat1_p2 = Post(category = self.cat1,
                          subject = 'Post p2 in category c1',
                          body = "post 2",
                          markup = 'bbcode',
                          thread = self.cat1_p1,
                          author = self.testuser)
        self.cat1_p2.save()

        self.cat1_p3 = Post(category = self.cat1,
                          subject = 'Post p3 in category c1',
                          body = "post 3",
                          markup = 'bbcode',
                          thread = self.cat1_p1,
                          author = self.testuser)
        self.cat1_p3.save()

        # create thread 2 in category cat2
        self.cat2_p1 = Post(category = self.cat2,
                          subject = 'Post p1 in category cat2',
                          body = "post 1",
                          markup = 'bbcode',
                          author = self.testuser)
        self.cat2_p1.save()

        # log in the user
        logged_in = self.client.login(username='supertestuser', password='testpassword')



    def test_move_cat1_p2_to_cat2(self):
        """
             Test moving post p2 from category cat1 directly into category cat2.

             Expected output is to have new thread (created from post p2) in category cat2.
             Thread cat1_p1 in category c1 will have less posts now
        """
        mv1url = self.cat1_p2.get_absolute_moveposturl()
        self.assertEqual(mv1url, sph_reverse('move_post_1', kwargs={'post_id':self.cat1_p2.pk}))

        # check first step
        response = self.client.get(mv1url, {})
        self.assertEqual(response.status_code, 200)

        # check second step (category is selected)
        mv2url = sph_reverse('move_post_2', kwargs={'post_id':self.cat1_p2.pk,
                                                    'category_id':self.cat2.pk})
        response = self.client.get(mv2url, {})
        self.assertEqual(response.status_code, 200)

        # check step 3 (with GET) - annotation form for post moved into category
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat1_p2.pk,
                                                        'category_id':self.cat2.pk})
        response = self.client.get(mv3url, {})
        self.assertEqual(response.status_code, 200)

        # submit annotation form and move the post!
        self.assertEqual(self.cat2.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instance of moved post
        p2 = Post.objects.get(pk=self.cat1_p2.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if new thread exists in category cat2
        self.assertEqual(self.cat2.threadCount(), 2)
        # check if post p2 was removed form thread p1
        self.assertEqual(self.cat1_p1.postCount(), 2)
        # check if post p2 is now new thread in category cat2
        self.assertEqual(p2.get_thread(), p2)
        # check if ThreadInformation for post p1 was updated
        ti = self.cat1_p1.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        # check if number of ThreadInformation objects has been changed
        self.assertEqual(ThreadInformation.objects.all().count(), 3)
        # check ThreadInformation for new thread
        ti2 = p2.get_threadinformation()
        self.assertEqual(ti2.post_count, 1)

    def test_move_cat1_p1_to_cat2(self):
        """
             Test moving post p1 (root post of thread!) from category cat1 directly
             into category cat2.

             Expected output is to have new thread (created from post p1) in category cat2
             and new thread in category cat1 created from second post in former p1 thread.
             Old ThreadInformation object for thread p1 should be removed.
             Two new ThreadInformation objects will be crated
        """
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat1_p1.pk,
                                                    'category_id':self.cat2.pk})
        # submit annotation form and move the post!
        self.assertEqual(self.cat2.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instances of posts
        p1 = Post.objects.get(pk=self.cat1_p1.pk)
        p2 = Post.objects.get(pk=self.cat1_p2.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if new thread exists in category cat2
        self.assertEqual(self.cat2.threadCount(), 2)
        # check if post p2 is now thread
        
        self.assertEqual(p2.get_thread(), p2)
        # check if post p1 is now new thread in category cat2
        self.assertEqual(p1.get_thread(), p1)
        # check if ThreadInformation for post p2 was created properly
        ti = p2.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        # check if number of ThreadInformation objects has been changed
        self.assertEqual(ThreadInformation.objects.all().count(), 3)

    def test_move_cat1_p1_to_cat1(self):
        """
             Test moving post p1 (root post of thread!) from category c1 directly
             into category cat1.

             Expected output is to have new thread (created from post p1) in category c1
             and new thread in category c1 created from second post in former p1 thread.
             Old ThreadInformation object for thread p1 should be removed.
             Two new ThreadInformation objects will be crated
        """
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat1_p1.pk,
                                                    'category_id':self.cat1.pk})
        # submit annotation form and move the post!
        self.assertEqual(self.cat1.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instances of posts
        p1 = Post.objects.get(pk=self.cat1_p1.pk)
        p2 = Post.objects.get(pk=self.cat1_p2.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if new thread exists in category cat1
        self.assertEqual(self.cat1.threadCount(), 2)
        # check if post p2 is now thread
        self.assertEqual(p2.get_thread(), p2)
        # check if post p1 is now new thread in category cat1
        self.assertEqual(p1.get_thread(), p1)
        # check if ThreadInformation for post p2 was created properly
        ti = p2.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        self.assertEqual(ti.category, self.cat1)
        # check if ThreadInformation for post p1 was updated properly
        ti2 = p1.get_threadinformation()
        self.assertEqual(ti2.post_count, 1)
        self.assertEqual(ti2.category, self.cat1)
        # check if number of ThreadInformation objects has been changed
        self.assertEqual(ThreadInformation.objects.all().count(), 3)

    def test_move_cat1_p3_to_cat1(self):
        """
             Test moving post p3 from category cat1 directly into category cat1.

             Expected output is to have new thread (created from post p3) in category c1.
             Old ThreadInformation object for thread p1 should be updated.
        """
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat1_p3.pk,
                                                    'category_id':self.cat1.pk})
        # submit annotation form and move the post!
        self.assertEqual(self.cat1.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instances of posts
        p1 = Post.objects.get(pk=self.cat1_p1.pk)
        p3 = Post.objects.get(pk=self.cat1_p3.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if new thread exists in category cat1
        self.assertEqual(self.cat1.threadCount(), 2)
        # check if post p3 is now thread
        self.assertEqual(p3.get_thread(), p3)
        # check if ThreadInformation for post p3 was created properly
        ti = p3.get_threadinformation()
        self.assertEqual(ti.post_count, 1)
        self.assertEqual(ti.category, self.cat1)
        # check if ThreadInformation for post p1 was updated properly
        ti = p1.get_threadinformation()
        self.assertEqual(ti.post_count, 2)

    def test_move_cat2_p1_to_cat1(self):
        """
             Test moving post p1 from category cat2 directly into category cat1.

             Expected output is to have new thread (created from post cat2_p1) in category c1.
             Old ThreadInformation object from cat2 should be removed.
        """
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat2_p1.pk,
                                                    'category_id':self.cat1.pk})
        # submit annotation form and move the post!
        self.assertEqual(self.cat1.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instances of posts
        cat2_p1 = Post.objects.get(pk=self.cat2_p1.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if new thread exists in cat1
        self.assertEqual(self.cat1.threadCount(), 2)
        # check if no threads left in cat2
        self.assertEqual(self.cat2.threadCount(), 0)
        # check if post cat2_p1 is thread
        self.assertEqual(cat2_p1.get_thread(), cat2_p1)
        # check if ThreadInformation for post cat2_p1 was created properly
        ti = cat2_p1.get_threadinformation()
        self.assertEqual(ti.post_count, 1)
        self.assertEqual(ti.category, self.cat1)
        
    def test_move_cat1_p3_to_cat2_p1(self):
        """
             Test moving post p3 from thread cat1_p1 into thread cat2_p1.

             Expected output is to have thread cat2_p1 updated and containing 2 posts.
             Thread cat1_p1 should be updated too as it now contains only 2 posts
        """
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat1_p3.pk,
                                                    'category_id':self.cat1.pk,
                                                    'thread_id':self.cat2_p1.pk})
        # submit annotation form and move the post!
        self.assertEqual(self.cat1.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instances of posts
        p1 = Post.objects.get(pk=self.cat1_p1.pk)
        p3 = Post.objects.get(pk=self.cat1_p3.pk)
        cat2_p1 = Post.objects.get(pk=self.cat2_p1.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if thread cat2_p1 was updated
        ti = cat2_p1.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        # check if ThreadInformation for post p1 was updated properly
        ti = p1.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        self.assertEqual(ti.category, self.cat1)
        # check if post cat1_p3 is now in thread cat2_p1
        self.assertEqual(p3.get_thread(), cat2_p1)

    def test_move_cat1_p1_to_cat2_p1(self):
        """
             Test moving post cat1_p1 (root post of thread!) from thread cat1_p1 into thread cat2_p1.

             Expected output is to have thread cat2_p1 updated and containing 2 posts.
             Thread cat1_p1 should be updated too as it now contains only 2 posts
        """
        mv3url = sph_reverse('move_post_3', kwargs={'post_id':self.cat1_p1.pk,
                                                    'category_id':self.cat1.pk,
                                                    'thread_id':self.cat2_p1.pk})
        # submit annotation form and move the post!
        self.assertEqual(self.cat1.threadCount(), 1)
        response = self.client.post(mv3url, {'body':'test body'})
        self.assertEqual(response.status_code, 302)

        # get fresh instances of posts
        cat1_p1 = Post.objects.get(pk=self.cat1_p1.pk)
        cat1_p2 = Post.objects.get(pk=self.cat1_p2.pk)
        cat2_p1 = Post.objects.get(pk=self.cat2_p1.pk)

        # check if success message was created
        self.assertEqual(self.superuser.message_set.count(), 1)
        # check if thread cat2_p1 was updated
        ti = cat2_p1.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        # check if ThreadInformation for post p2 was created properly
        ti = cat1_p2.get_threadinformation()
        self.assertEqual(ti.post_count, 2)
        self.assertEqual(ti.category, self.cat1)
        # check if post cat1_p1 is now in thread cat2_p1
        self.assertEqual(cat1_p1.get_thread(), cat2_p1)
        # check if post cat1_p1 was added at the end of thread
        self.assertEqual(cat2_p1.get_latest_post(), cat1_p1)