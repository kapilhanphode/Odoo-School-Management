from odoo import api,fields,models,_
from datetime import date, timedelta
import datetime
from odoo.exceptions import ValidationError
from dateutil import relativedelta



class Patient(models.Model):
    _name = 'student.registration'
    _description = 'Hospital Patient Details'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'student_name'

    student_name = fields.Char('Name')
    student_email = fields.Char('Email')
    student_address = fields.Char('Address')
    student_phone_no = fields.Char('Phone No.')
    student_dob = fields.Date('Date of Birth')
    student_reg_date = fields.Date('Student Reg. Date', default=fields.Date.context_today)
    student_age = fields.Integer('Age', store=True,  compute='_compute_age')
    student_gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],'Gender', defualt='male')
    marital_status = fields.Selection([('single','Single'),('married','Married'),('other','Other')],'Marital Status')
    student_admission_type = fields.Selection([('school', 'School'), ('jr_college', 'Jr College'), ('graduation', 'Graduation'), ('post_graduation','Post Graduation')],
                                           'Admission Type')
    stud_class = fields.Selection(
        [('cls1_4', 'Class 1-4'), ('cls5_7', 'Class 5-7'), ('cls8_9', 'Class 8-9'), ('cls10', 'Class 10')],
        'Student Class')
    teaching_jr_class = fields.Selection([('cls11', 'Class 11'), ('cls12', 'Class 12')],'Student Class')
    clg_stream = fields.Selection([('science','Science'),('commerce','Commerce'),('arts','Arts')])
    graduation_clg_stream = fields.Selection([('b_com', 'B.Com'), ('b_a', 'B.A'), ('bsc', 'BSC (Bachelor of Science)'),
                                              ('bca', "BCA (Bachelor of Computer Application)"),
                                              ('bcs', 'BCS (Bachelor of Computer Science)')], 'Graduation')
    post_graduation_clg_stream = fields.Selection(
        [('m_com', 'M.Com'), ('m_a', 'M.A'), ('msc', "MSC (Master's of Science)"),
         ('mca', "MCA (Master's of Computer Application)"), ('mcs', "MCS (Master's of Computer Science)")],
        'Post Graduation')
    class_teacher = fields.Many2one('teacher.registration', 'Class Teacher')
    is_birthday = fields.Boolean('Birthday',compute='_is_birthday',store=True)
    fav_sport = fields.Many2one('sport.registration', 'Favourite Sports')

    # @api.model_create_multi
    # def create(self, values_list):
    #     res = super(Patient, self).create(values_list)
    #     user_obj = self.env['res.users'].search([])
    #     print('self _uid', self._uid)
    #     print('self.env.user',self.env.user)
    #     a=self.env.user
    #     print(a.name)
    #     return res

    @api.model
    def _name_search(self, student_name, args=None, operator='ilike', limit=100,name_get_uid=None):
        args = args or []
        domain = []
        if student_name:
            domain = ['|',('student_name',operator,student_name),('student_phone_no',operator,student_name)]
        return self._search(domain+args,limit=limit,access_rights_uid=name_get_uid)

    @api.depends('student_dob')
    def _is_birthday(self):
        for rec in self:
            today = date.today()
            if rec.student_dob:
                print('today date', today)
                if today.day == rec.student_dob.day and today.month == rec.student_dob.month:
                    rec.is_birthday = True
                    print('today date inside if', today)
                    print('today today Birthday')
                else:
                    rec.is_birthday = False
            else:
                pass

    @api.onchange('marital_status')
    def onchange_marital_status(self):
        if self.marital_status == 'married':
            if self.student_gender == 'female' and self.student_age < 18:
                raise ValidationError("Age of {} is below 18 year's please check Marital Status".format(self.student_name))
            if self.student_gender == 'male' and self.student_age < 21:
                raise ValidationError("Age of {} is below 21 year's please check Marital Status".format(self.student_name))

    @api.depends('student_dob')
    def _compute_age(self):
        for record in self:
            if record.student_dob:
                today = datetime.date.today()
                # Check if the date has passed this year
                if today.strftime("%m%d") >= record.student_dob.strftime("%m%d"):
                    record['student_age'] = today.year - record.student_dob.year
                else:
                    record['student_age'] = today.year - record.student_dob.year - 1
            else:
                record['student_age'] = 0
    @api.onchange('student_admission_type','stud_class','teaching_jr_class','clg_stream','graduation_clg_stream','post_graduation_clg_stream')
    def onchange_student_admission_type(self):
        print('student_admission_type',self.student_admission_type)
        if self.student_admission_type == 'school':
            obj = self.env['class.registration'].search(['&',('class_type','=',self.student_admission_type), ('teaching_class','=',self.stud_class)])
            print('+++++++++++++++++++++++obj',obj)
            self.class_teacher = obj.class_teacher.id
        elif self.student_admission_type == 'jr_college':
            obj1 = self.env['class.registration'].search(['&','&',('class_type','=',self.student_admission_type), ('teaching_jr_class','=',self.teaching_jr_class), ('clg_stream','=',self.clg_stream)])
            print('++++++++++++++++++++++++obj1',obj1)
            self.class_teacher = obj1.class_teacher.id
        elif self.student_admission_type == 'graduation' and self.clg_stream in ['science','commerce','arts'] and self.graduation_clg_stream in ['b_com', 'b_a', 'bsc', 'bca', 'bcs']:
            obj2 = self.env['class.registration'].search(['&','&',('class_type','=',self.student_admission_type), ('clg_stream','=',self.clg_stream), ('graduation_clg_stream','=',self.graduation_clg_stream)])
            print('++++++++++++++++++++++++obj2',obj2)
            self.class_teacher = obj2.class_teacher.id
        elif self.student_admission_type == 'post_graduation' and self.clg_stream in ['science','commerce','arts'] and self.post_graduation_clg_stream in ['m_com', 'm_a', 'msc', 'mca', 'mcs']:
            obj3 = self.env['class.registration'].search(['&','&',('class_type','=',self.student_admission_type), ('clg_stream','=',self.clg_stream), ('post_graduation_clg_stream','=',self.post_graduation_clg_stream)])
            print('++++++++++++++++++++++++obj3',obj3)
            self.class_teacher = obj3.class_teacher.id




    #parent_details
    parent_name = fields.Char('Name')
    parent_phone_no = fields.Char('Phone No.')



    #partner_details
    partner_name = fields.Char('Name')
    partner_phone_no = fields.Char('Phone No.')


