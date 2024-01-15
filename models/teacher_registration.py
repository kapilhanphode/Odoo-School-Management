from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class SchoolTeacher(models.Model):
    _name = 'teacher.registration'
    _description = 'School Teacher Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'teacher_name'

    teacher_name = fields.Char('Name')
    teacher_email = fields.Char('Email')
    teacher_qualification = fields.Char('Qualification')
    teacher_address = fields.Char('Address')
    teacher_phone_no = fields.Char('Phone No.')
    teacher_dob = fields.Date('Date of Birth')
    teacher_joining_date = fields.Date('Teacher Joining Date', default=fields.Date.context_today)
    teacher_age = fields.Integer('Age')
    teacher_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], 'Gender')
    teacher_marital_status = fields.Selection([('single', 'Single'), ('married', 'Married'), ('other', 'Other')],
                                              'Marital Status')
    teaching_type = fields.Selection([('school', 'School'), ('jr_college', 'Jr College'), ('graduation', 'Graduation'), ('post_graduation','Post Graduation')])
    teaching_subjects = fields.Selection([('english', 'English'), ('maths', 'Mathematics'), ('marathi', 'Marathi'),
                                          ('hindi', 'Hindi'), ('env_studies', 'Environmental Studies')], 'Subjects')
    teaching_class = fields.Selection(
        [('cls1_4', 'Class 1-4'), ('cls5_7', 'Class 5-7'), ('cls8_9', 'Class 8-9'), ('cls10', 'Class 10')],
        'Student Class')
    teaching_jr_class = fields.Selection([('cls11', 'Class 11'), ('cls12', 'Class 12')],'Student Class')
    clg_stream = fields.Selection([('science','Science'),('commerce','Commerce'),('arts','Arts')], 'College Stream')
    graduation_clg_stream = fields.Selection([('b_com', 'B.Com'), ('b_a', 'B.A'), ('bsc', 'BSC (Bachelor of Science)'),
                                              ('bca', "BCA (Bachelor of Computer Application)"),
                                              ('bcs', 'BCS (Bachelor of Computer Science)')], 'Graduation')
    post_graduation_clg_stream = fields.Selection(
        [('m_com', 'M.Com'), ('m_a', 'M.A'), ('msc', "MSC (Master's of Science)"),
         ('mca', "MCA (Master's of Computer Application)"), ('mcs', "MCS (Master's of Computer Science)")],
        'Post Graduation')
    sub_name = fields.Many2many('school.subject', string='Subjects')

    @api.model
    def create(self, vals):
        res = super(SchoolTeacher, self).create(vals)
        print('vals===============================',vals)
        if not vals['teaching_type']:
            raise ValidationError('Teaching Type is Mandatory')
        if vals['teaching_type'] in ['school','jr_college','college'] and not vals['teaching_class']:
            raise ValidationError('Student Class is Mandatory')
        if not vals["sub_name"][0][2]:
            raise ValidationError(_('For {} at least select 1 Subject'.format(vals['teaching_class'])))

        return res


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'School Subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sub_name'

    sub_name = fields.Char('Subject Name')
