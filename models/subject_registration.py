from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'School Subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sub_name'

    sub_name = fields.Char('Subject Name')
    class_type = fields.Selection([('school', 'School'), ('jr_college', 'Jr College'), ('graduation', 'Graduation'), ('post_graduation','Post Graduation')],'Class Type')
    clg_stream = fields.Selection([('science','Science'),('commerce','Commerce'),('arts','Arts')], 'College Stream')
    stud_class = fields.Selection(
        [('cls1_4', 'Class 1-4'), ('cls5_7', 'Class 5-7'), ('cls8_9', 'Class 8-9'), ('cls10', 'Class 10')],
        'Student Class')
    teaching_jr_class = fields.Selection([('cls11', 'Class 11'), ('cls12', 'Class 12')],'Student Class')
    graduation_clg_stream = fields.Selection([('b_com','B.Com'),('b_a','B.A'),('bsc','BSC (Bachelor of Science)'),('bca',"BCA (Bachelor of Computer Application)"),('bcs','BCS (Bachelor of Computer Science)')], 'Graduation')
    post_graduation_clg_stream = fields.Selection([('m_com','M.Com'),('m_a','M.A'),('msc',"MSC (Master's of Science)"),('mca',"MCA (Master's of Computer Application)"),('mcs',"MCS (Master's of Computer Science)")], 'Post Graduation')




class SchoolSubject(models.Model):
    _name = 'class.registration'
    _description = 'Class Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'class_type'

    class_type = fields.Selection([('school', 'School'), ('jr_college', 'Jr College'), ('graduation', 'Graduation'), ('post_graduation','Post Graduation')],'Class Type')
    teaching_class = fields.Selection([('cls1_4', 'Class 1-4'), ('cls5_7', 'Class 5-7'), ('cls8_9', 'Class 8-9'), ('cls10', 'Class 10')],'Student Class')
    teaching_jr_class = fields.Selection([('cls11', 'Class 11'), ('cls12', 'Class 12')],'Student Class')
    clg_stream = fields.Selection([('science','Science'),('commerce','Commerce'),('arts','Arts')], 'College Stream')
    graduation_clg_stream = fields.Selection([('b_com', 'B.Com'), ('b_a', 'B.A'), ('bsc', 'BSC (Bachelor of Science)'),
                                              ('bca', "BCA (Bachelor of Computer Application)"),
                                              ('bcs', 'BCS (Bachelor of Computer Science)')], 'Graduation')
    post_graduation_clg_stream = fields.Selection(
        [('m_com', 'M.Com'), ('m_a', 'M.A'), ('msc', "MSC (Master's of Science)"),
         ('mca', "MCA (Master's of Computer Application)"), ('mcs', "MCS (Master's of Computer Science)")],
        'Post Graduation')
    subject = fields.Many2many('school.subject', string='Class Subjects')
    class_teacher = fields.Many2one('teacher.registration','Class teacher')

    @api.onchange("class_teacher")
    def onchange_stud_name(self):
        self.subject = self.class_teacher.sub_name

    @api.onchange('class_type','teaching_class','teaching_jr_class','clg_stream','graduation_clg_stream','post_graduation_clg_stream')
    def onchange_class_teaching(self):
        # res = super(SchoolSubject, self).create(vals)
        print('+++++++self.class_type',self.class_type)
        obj = self.env['class.registration'].search([])
        print('obj',obj)

        for rec in obj:
            print('rec',rec.id,rec.class_type,rec.teaching_class)
            print('self',rec.id,self.class_type,self.teaching_class)
            if self.class_type == 'school':
                if rec.class_type == self.class_type and rec.teaching_class == self.teaching_class:
                    raise ValidationError('record exists1')
            if self.class_type == 'jr_college':
                self.teaching_class == False
                if self.class_type == rec.class_type and rec.teaching_jr_class == self.teaching_jr_class and rec.clg_stream == self.clg_stream:
                    raise ValidationError('record exists2')
            if self.class_type == 'graduation':
                self.teaching_class == False
                if self.class_type == rec.class_type and rec.graduation_clg_stream == self.graduation_clg_stream and rec.clg_stream == self.clg_stream:
                    raise ValidationError('record exists3')
            if self.class_type == 'post_graduation':
                self.teaching_class == False
                if self.class_type == rec.class_type and rec.post_graduation_clg_stream == self.post_graduation_clg_stream and rec.clg_stream == self.clg_stream:
                    raise ValidationError('record exists4')


        # return res





    # @api.constrains('class_type','clg_stream')
    # def _check_name(self):
    #     partner_rec = self.env['class.registration'].search(
    #         [('class_type', '=', self.class_type), ('clg_stream', '=', self.clg_stream)])
    #     print('++++++++++++++++',partner_rec)
    #     if partner_rec:
    #         raise ValidationError(_('Exists ! Already a record exists in this name'))

    # @api.onchange("class_type")
    # def onchange_class_type(self):
    #     print('Class Type--------------------',self.class_type)
    #
    #     obj = self.env['class.registration'].search([('class_type','=',self.class_type), ('teaching_class','=',self.teaching_class)])
    #     obj1 = self.env['class.registration'].search([])
    #     print('obj-------------------------obj',obj)
    #     print('obj1-------------------------obj1',obj1)
    #     # if obj:
    #     #     raise ValidationError('Class Type already exist')
    #     print('===========')
    #     if obj1:
    #         for rec in obj1:
    #             print('rec',rec.class_type)

    # @api.model
    # def create(self,vals):
    #     res = super(SchoolSubject, self).create(vals)
    #     print('res--------------------',vals)
    #     obj = self.env['class.registration'].search([])
    #
    #     if vals['class_type'] == 'school':
    #         print('class_type--------------------', vals['class_type'])
    #         for rec in obj:
    #             print('rec--------------------', rec)
    #             if rec.class_type == vals['class_type'] and rec.teaching_class == vals['teaching_class']:
    #                 raise ValidationError('Already record created for this Class')
    #     if vals['class_type'] == 'jr_college':
    #         print('class_type--------------------', vals['class_type'])
    #         for rec in obj:
    #             print('rec--------------------', rec)
    #             if rec.class_type == vals['class_type'] and rec.teaching_jr_class == vals['teaching_jr_class'] and rec.clg_stream == vals['clg_stream']:
    #                 raise ValidationError("Already record created for Jr. College's, Class and Stream")
    #     if vals['class_type'] == 'graduation':
    #         print('class_type--------------------', vals['class_type'])
    #         for rec in obj:
    #             print('rec--------------------', rec)
    #             if rec.class_type == vals['class_type'] and rec.graduation_clg_stream == vals['graduation_clg_stream'] and rec.clg_stream == vals['clg_stream']:
    #                 raise ValidationError("Already record created for Graduation with Class and Stream")
    #     if vals['class_type'] == 'post_graduation':
    #         print('class_type--------------------', vals['class_type'])
    #         for rec in obj:
    #             print('rec--------------------', rec)
    #             if rec.class_type == vals['class_type'] and rec.post_graduation_clg_stream == vals['post_graduation_clg_stream'] and rec.clg_stream == vals['clg_stream']:
    #                 raise ValidationError("Already record created for Jr. College's, Class and Stream")
    #
    #
    #
    #     return res

