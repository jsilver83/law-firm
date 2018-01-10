from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField

User = settings.AUTH_USER_MODEL


class Nationality(models.Model):
    nationality_ar = models.CharField(_('Nationality (Arabic)'), null=True, blank=False, max_length=100)
    nationality_en = models.CharField(_('Nationality (English)'), null=True, blank=True, max_length=100)
    country_ar = models.CharField(_('Nationality (Arabic)'), null=True, blank=True, max_length=100)
    country_en = models.CharField(_('Nationality (Arabic)'), null=True, blank=True, max_length=100)
    show = models.BooleanField(_('Show'), default=True)
    display_order = models.PositiveSmallIntegerField(_('Display Order'), null=True)

    @staticmethod
    def get_nationality_choices(add_dashes=True):
        try:
            choices = Nationality.objects.filter(show=True)

            ch = [(o.id, str(o)) for o in choices]
            if add_dashes:
                ch.insert(0, ('', '---------'))

            return ch
        except:  # was OperationalError and happened when db doesn't exist yet but later changed it to general except to catch any weird exceptions like ProgrammingError
            return [('--', '--')]

    @property
    def nationality(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.nationality_ar
        else:
            return self.nationality_en

    def __str__(self):
        return self.nationality

    class Meta:
        ordering = ['display_order', 'nationality_en']
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationalities')


class Lookup(models.Model):
    class LookupTypes:
        ORGANIZATION_TYPE = 'ORGANIZATION_TYPE'
        CASE_TYPE = 'CASE_TYPE'
        CONSULTATION_TYPE = 'CONSULTATION_TYPE'
        PAPERWORK_TYPE = 'PAPERWORK_TYPE'
        DOCUMENT_TYPE = 'DOCUMENT_TYPE'
        COURT_ROLE = 'COURT_ROLE'

        @classmethod
        def choices(cls):
            return (
                (cls.ORGANIZATION_TYPE, _('Organization Type')),
                (cls.CASE_TYPE, _('Case Type')),
                (cls.CONSULTATION_TYPE, _('Consultation Type')),
                (cls.PAPERWORK_TYPE, _('Paperwork Type')),
                (cls.DOCUMENT_TYPE, _('Document Type')),
                (cls.COURT_ROLE, _('Court Role')),
            )

    lookup_type = models.CharField(max_length=30, null=True, blank=False, db_index=True,
                                   choices=LookupTypes.choices())
    lookup_value_ar = models.CharField(max_length=100, null=True, blank=False)
    lookup_value_en = models.CharField(max_length=100, null=True, blank=False)
    show = models.BooleanField(_('Show'), default=True)
    display_order = models.PositiveSmallIntegerField(_('Display Order'), null=True)

    class Meta:
        verbose_name = _('Look up')
        verbose_name_plural = _('Look ups')
        ordering = ['lookup_type', '-display_order']

    @property
    def lookup_value(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.lookup_value_ar
        else:
            return self.lookup_value_en

    def __str__(self):
        return self.lookup_value

    @staticmethod
    def get_lookup_choices(lookup_type, add_dashes=True):
        try:
            choices = Lookup.objects.filter(
                show=True,
                lookup_type=lookup_type)

            ch = [(o.lookup_value_ar, str(o)) for o in choices]
            if add_dashes:
                ch.insert(0, ('', '---------'))

            return ch
        except:  # was OperationalError and happened when db doesn't exist yet but later changed it to general except to catch any weird exceptions like ProgrammingError
            return [('--', '--')]


class Person(models.Model):
    class Genders:
        MALE = 'M'
        FEMALE = 'F'

        @classmethod
        def choices(cls):
            return (
                (cls.MALE, _('Male')),
                (cls.FEMALE, _('Female')),
            )

    class Meta:
        #     abstract = True
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    name_ar = models.CharField(_('Full Name'), max_length=255, null=True, blank=False)
    name_en = models.CharField(_('Full Name (English)'), max_length=255, null=True, blank=False)
    mobile = models.CharField(_('Mobile'), max_length=20, null=True, blank=False)
    home_phone = models.CharField(_('Home Phone'), max_length=20, null=True, blank=True)
    work_phone = models.CharField(_('Work Phone'), max_length=20, null=True, blank=True)
    personal_email = models.EmailField(_('Personal Email'), null=True, blank=True)
    government_id = models.CharField(_('Government ID'), max_length=20, null=True, blank=True)
    gender = models.CharField(_('Gender'), max_length=1, null=True, blank=True, default='M',
                              choices=Genders.choices())
    nationality = models.ForeignKey('Nationality', null=True, blank=True, on_delete=models.SET_NULL,
                                    limit_choices_to={'show': True})
    date_of_birth = models.DateField(_('Date Of Birth'), null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=False)
    active = models.BooleanField(_('Is Active'), blank=False, default=False)
    personal_picture = models.FileField(_('Personal Picture'), null=True, blank=True)
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Created By'),
                                   related_name="%(app_label)s_created_%(class)s", )
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Updated By'))

    @property
    def name(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.name_ar
        else:
            return self.name_en

    # TODO: FIX STR ERROR
    def __str__(self):
        return self.name if self.name else ''

    @property
    def picture(self):
        if self.personal_picture:
            return self.personal_picture
        else:
            return 'images/avatar.png'


class Employee(Person):
    job_description_ar = models.CharField(_('Job Description'), max_length=255, null=True, blank=False)
    job_description_en = models.CharField(_('Job Description (English)'), max_length=255, null=True, blank=True)
    joining_date = models.DateTimeField(_('Joining Date'), null=True, blank=False)
    qualifications = models.TextField(_('Qualifications'), null=True, blank=True)
    monthly_salary = MoneyField(_('Monthly Salary'), null=True, blank=True,
                                decimal_places=2, default=0, default_currency='SAR', max_digits=11,)
    user = models.OneToOneField(User, related_name='employee', null=True, blank=True)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


class Client(Person):
    organization = models.ForeignKey('Organization', related_name='contact_persons',
                                     on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        name = super(Client, self).__str__()
        if self.organization:
            return '%s (%s)' % (name, self.organization)
        else:
            return name

    def get_absolute_url(self):
        return reverse_lazy('update_client', args=(self.pk,))

    def get_update_url(self):
        return self.get_absolute_url()


class Organization(models.Model):
    name_ar = models.CharField(_('Organization Name'), max_length=100, null=True, blank=False)
    name_en = models.CharField(_('Organization Name (English)'), max_length=100, null=True, blank=False)
    type = models.CharField(_('Type'), max_length=100, null=True, blank=False,
                            choices=Lookup.get_lookup_choices(Lookup.LookupTypes.ORGANIZATION_TYPE))
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    fax = models.CharField(_('Fax'), max_length=20, null=True, blank=True)
    website = models.URLField(_('Website'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=100, null=True, blank=False)
    address = models.TextField(_('Address'), null=True, blank=False)
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Created By'),
                                   related_name="created_organizations", )
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Updated By'))

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    @property
    def name(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.name_ar
        else:
            return self.name_en

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('update_organization', args=(self.pk,))

    def get_update_url(self):
        return self.get_absolute_url()


class Court(Organization):
    class Meta:
        verbose_name = _('Court')
        verbose_name_plural = _('Courts')


class Project(models.Model):
    # TODO: implement state machine for status
    class Statuses:
        NEW = 'NEW'
        IN_PROGRESS = 'IN_PROGRESS'
        FINISHED = 'FINISHED'
        DELAYED = 'DELAYED'
        CANCELLED = 'CANCELLED'

        @classmethod
        def choices(cls):
            return (
                (cls.NEW, _('New')),
                (cls.IN_PROGRESS, _('In Progress')),
                (cls.FINISHED, _('Finished')),
                (cls.DELAYED, _('Delayed')),
                (cls.CANCELLED, _('Cancelled')),
            )

    class Meta:
        #     abstract = True
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('-updated_on', 'created_on', )

    title_ar = models.CharField(_('Title'), max_length=100, blank=False, null=True)
    title_en = models.CharField(_('Title (English)'), max_length=100, blank=False, null=True)
    description_ar = models.TextField(_('Description'), blank=False, null=True)
    description_en = models.TextField(_('Description (English)'), blank=False, null=True)
    status = models.CharField(_('Status'), max_length=20, null=True, blank=False,
                              choices=Statuses.choices(), default=Statuses.NEW)
    status_comments = models.CharField(_('Status Comments'), max_length=500, null=True, blank=True)
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=False,
                               related_name='%(app_label)s_%(class)s', verbose_name=_('Client'))
    fees = models.CharField(max_length=200, blank=False, null=True)
    main_assignee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                      related_name='assigned_%(app_label)s_%(class)s',
                                      verbose_name=_('Main Assignee'))
    created_on = models.DateTimeField(_('Created On'), auto_now_add=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Created By'),
                                   related_name="%(app_label)s_%(class)s_created_projects", )
    updated_on = models.DateTimeField(_('Updated On'), auto_now=True)
    updated_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=False,
                                   verbose_name=_('Updated By'))

    @property
    def title(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.title_ar
        else:
            return self.title_en

    @property
    def description(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.description_ar
        else:
            return self.description_en

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('update_project', args=(self.pk,))

    def get_update_url(self):
        return self.get_absolute_url()


class Case(Project):
    case_reference = models.CharField(_('Case Reference'), max_length=100, null=True, blank=False)
    type = models.CharField(_('Type'), max_length=100, null=True, blank=False,
                            choices=Lookup.get_lookup_choices(Lookup.LookupTypes.CASE_TYPE))
    client_role = models.CharField(_('Client Role'), max_length=100, null=True, blank=False,
                                   choices=Lookup.get_lookup_choices(Lookup.LookupTypes.COURT_ROLE))
    opponent = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=False,
                                 related_name='opposing_cases', verbose_name=_('Opponent'))
    opponent_role = models.CharField(_('Opponent Role'), max_length=100, null=True, blank=False,
                                     choices=Lookup.get_lookup_choices(Lookup.LookupTypes.COURT_ROLE))
    court = models.ForeignKey('Court', on_delete=models.SET_NULL, null=True, blank=False,
                              related_name='opposing_cases', verbose_name=_('Court'))
    court_office = models.CharField(_('Court Office'), max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Case')
        verbose_name_plural = _('Cases')


class Consultation(Project):
    type = models.CharField(_('Type'), max_length=100, null=True, blank=False,
                            choices=Lookup.get_lookup_choices(Lookup.LookupTypes.CONSULTATION_TYPE))

    class Meta:
        verbose_name = _('Consultation')
        verbose_name_plural = _('Consultations')


class Paperwork(Project):
    type = models.CharField(_('Type'), max_length=100, null=True, blank=False,
                            choices=Lookup.get_lookup_choices(Lookup.LookupTypes.PAPERWORK_TYPE))

    class Meta:
        verbose_name = _('Paperwork')
        verbose_name_plural = _('Paperwork Projects')


class Reminder(models.Model):
    class Types:
        SMS = 'SMS'
        EMAIL = 'EMAIL'
        BOTH = 'BOTH'

        @classmethod
        def choices(cls):
            return (
                (cls.SMS, _('SMS')),
                (cls.EMAIL, _('Email')),
                (cls.BOTH, _('Both')),
            )

    class Meta:
        verbose_name = _('Reminder')
        verbose_name_plural = _('Reminders')
        ordering = ('-date', )

    title_ar = models.CharField(_('Title'), max_length=100, blank=False, null=True)
    title_en = models.CharField(_('Title (English)'), max_length=100, blank=False, null=True)
    description_ar = models.TextField(_('Description'), blank=False, null=True)
    description_en = models.TextField(_('Description (English)'), blank=False, null=True)
    whom_to_remind = models.ForeignKey('Employee', on_delete=models.SET_NULL,
                                       null=True, blank=False,
                                       verbose_name=_('Whom To Remind'),
                                       related_name='reminders')
    date = models.DateTimeField(_('Reminder Date'), null=True, blank=False)
    type = models.CharField(_('Type'), max_length=10, null=True, blank=True,
                            choices=Types.choices())
    project = models.ForeignKey('Project', related_name='reminders',
                                on_delete=models.SET_NULL, null=True, blank=True)
    last_seen_on = models.DateTimeField(_('Last Seen On'), null=True, blank=False)

    @property
    def title(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.title_ar
        else:
            return self.title_en

    def __str__(self):
        return self.title


class Update(models.Model):
    class Meta:
        verbose_name = _('Update')
        verbose_name_plural = _('Updates')
        ordering = ('-date', )

    project = models.ForeignKey('Project', related_name='updates',
                                on_delete=models.SET_NULL, null=True, blank=True)
    summary_ar = models.CharField(_('Title'), max_length=100, blank=False, null=True)
    summary_en = models.CharField(_('Title (English)'), max_length=100, blank=False, null=True)
    details_ar = models.TextField(_('Description'), blank=False, null=True)
    details_en = models.TextField(_('Description (English)'), blank=False, null=True)
    date = models.DateTimeField(_('Update Date'), null=True, blank=False)
    attachments = models.FileField(_('Attachments'), null=True, blank=True)
    inform_the_client = models.BooleanField(_('Inform The Client'), default=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL,
                                   null=True, blank=False,
                                   verbose_name=_('Creator'),
                                   related_name='updates')
    created_on = models.DateTimeField(_('Created On'), null=True, blank=False)

    @property
    def summary(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.summary_ar
        else:
            return self.summary_en

    @property
    def details(self):
        lang = translation.get_language()
        if lang == "ar":
            return self.details_ar
        else:
            return self.details_ar

    def __str__(self):
        return self.summary
