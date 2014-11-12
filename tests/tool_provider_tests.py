from test_helper import create_test_tp, create_params_tp
import unittest

class TestToolProvider(unittest.TestCase):
    def setUp(self):
        self.params = create_params_tp()
        self.tp = create_test_tp()

    def test_outcome_service(self):
        '''
        Should recognize an outcome service.
        '''
        self.assertTrue(self.tp.is_outcome_service())
        self.tp.lis_result_sourcedid = None
        self.assertFalse(self.tp.is_outcome_service())

    def test_return_url_with_messages(self):
        '''
        Should generate a return url with messages.
        '''
        self.assertEqual(self.tp.build_return_url(),
                self.params['launch_presentation_return_url'])
        self.tp.lti_errormsg = 'user error message'
        self.tp.lti_errorlog = 'lms error log'
        self.tp.lti_msg = 'user message'
        self.tp.lti_log = 'lms message'
        self.assertEqual(self.tp.build_return_url(),
                self.params['launch_presentation_return_url'] +
                '?lti_msg=user+message&lti_errormsg=user+error+message&lti_errorlog=lms+error+log&lti_log=lms+message')

    def test_roles(self):
        '''
        Should recognize the roles.
        '''
        self.assertTrue(self.tp.is_student())
        self.assertTrue(self.tp.is_instructor())
        self.assertTrue(self.tp.has_role('Observer'))
        self.assertFalse(self.tp.has_role('administrator'))

    def test_username(self):
        '''
        Should find the best username.
        '''
        self.assertEqual(self.tp.username('guy'), 'guy')
        self.tp.lis_person_name_full = 'full'
        self.assertEqual(self.tp.username('guy'), 'full')
        self.tp.lis_person_name_family = 'family'
        self.assertEqual(self.tp.username('guy'), 'family')
        self.tp.lis_person_name_given = 'given'
        self.assertEqual(self.tp.username('guy'), 'given')
