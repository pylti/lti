import attr


@attr.s
class Word(object):
    """A known definition in a vocabulary.

    Has a ``name``, ``urn``, and ``url``. The ``name``
    is the short version of the word that can be used if
    the namespace is implied by the context. The ``urn``
    is the full URN as specified in LTI 1, and deprecated
    in LTI 2. The ``url`` is the new full RDF URL that
    replaces the deprecated ``urn``.
    """
    name = attr.ib()
    urn = attr.ib()
    url = attr.ib()


@attr.s
class Vocabulary(object):
    """A collection of known words with their synonyms."""
    urn = attr.ib()
    url = attr.ib()
    words = attr.ib(default=attr.Factory(set))

    @staticmethod
    def make_urn(urn, name):
        return '{}/{}'.format(urn, name)

    @staticmethod
    def make_url(url, name):
        if '/' in name:
            front, back = name.rsplit('/', 1)
            return '{}/{}#{}'.format(url, front, back)
        return '{}#{}'.format(url, name)

    @classmethod
    def generate(cls, urn, url, names):
        return cls(urn=urn, url=url, words={
            Word(
                name=name,
                urn=cls.make_urn(urn, name),
                url=cls.make_url(url, name),
            ) for name in names
        })


VOCABULARY_CONTEXT_TYPE = Vocabulary.generate(
    urn='urn:lti:context-type:ims/lis',
    url='http://purl.imsglobal.org/vocab/lis/v2/course',
    names=[
        'CourseTemplate',
        'CourseOffering',
        'CourseSection',
        'Group',
    ],
)


VOCABULARY_SYSTEM_ROLE = Vocabulary.generate(
    urn='urn:lti:sysrole:ims/lis',
    url='http://purl.imsglobal.org/vocab/lis/v2/person',
    names=[
        'SysAdmin',
        'SysSupport',
        'Creator',
        'AccountAdmin',
        'User',
        'Administrator',
        'None',
    ],
)


VOCABULARY_INST_ROLE = Vocabulary.generate(
    urn='urn:lti:instrole:ims/lis',
    url='http://purl.imsglobal.org/vocab/lis/v2/person',
    names=[
        'Student',
        'Faculty',
        'Member',
        'Learner',
        'Instructor',
        'Mentor',
        'Staff',
        'Alumni',
        'ProspectiveStudent',
        'Guest',
        'Other',
        'Administrator',
        'Observer',
        'None',
    ],
)


VOCABULARY_CONTEXT_ROLE = Vocabulary.generate(
    urn='urn:lti:role:ims/lis',
    url='http://purl.imsglobal.org/vocab/lis/v2/membership',
    names=[
        'Learner',
        'Learner/Learner',
        'Learner/NonCreditLearner',
        'Learner/GuestLearner',
        'Learner/ExternalLearner',
        'Learner/Instructor',
        'Instructor',
        'Instructor/PrimaryInstructor',
        'Instructor/Lecturer',
        'Instructor/GuestInstructor',
        'Instructor/ExternalInstructor',
        'ContentDeveloper',
        'ContentDeveloper/ContentDeveloper',
        'ContentDeveloper/Librarian',
        'ContentDeveloper/ContentExpert',
        'ContentDeveloper/ExternalContentExpert',
        'Member',
        'Member/Member',
        'Manager',
        'Manager/AreaManager',
        'Manager/CourseCoordinator',
        'Manager/Observer',
        'Manager/ExternalObserver',
        'Mentor',
        'Mentor/Mentor',
        'Mentor/Reviewer',
        'Mentor/Advisor',
        'Mentor/Auditor',
        'Mentor/Tutor',
        'Mentor/LearningFacilitator',
        'Mentor/ExternalMentor',
        'Mentor/ExternalReviewer',
        'Mentor/ExternalAdvisor',
        'Mentor/ExternalAuditor',
        'Mentor/ExternalTutor',
        'Mentor/ExternalLearningFacilitator',
        'Administrator',
        'Administrator/Administrator',
        'Administrator/Support',
        'Administrator/Developer',
        'Administrator/SystemAdministrator',
        'Administrator/ExternalSystemAdministrator',
        'Administrator/ExternalDeveloper',
        'Administrator/ExternalSupport',
        'TeachingAssistant',
        'TeachingAssistant/TeachingAssistant',
        'TeachingAssistant/TeachingAssistantSection',
        'TeachingAssistant/TeachingAssistantSectionAssociation',
        'TeachingAssistant/TeachingAssistantOffering',
        'TeachingAssistant/TeachingAssistantTemplate',
        'TeachingAssistant/TeachingAssistantGroup',
        'TeachingAssistant/Grader',
    ],
)
