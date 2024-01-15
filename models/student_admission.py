from odoo import api,fields,models,_
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class SchoolStudent(models.Model):
    _name = 'student.admission'
    _description = 'School Student Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'stud_name'

    stud_name = fields.Many2one('student.registration','Student Name')
    stud_admission_type = fields.Selection(related='stud_name.student_admission_type', string='Admission Type')
    stud_age = fields.Integer('Age',related='stud_name.student_age')
    stud_gender = fields.Selection('Gender',related='stud_name.student_gender')
    stud_address = fields.Char('Address',related='stud_name.student_address')
    stud_admission_reg_date = fields.Date('Admission Reg. Date', default=fields.Date.context_today, readonly=True)
    stud_class = fields.Selection(related='stud_name.stud_class',string='Student Class')
    sub_name = fields.Many2many('school.subject', string='Subjects')
    class_teacher = fields.Many2one(string='Class Teacher',related='stud_name.class_teacher')
    teaching_jr_class = fields.Selection([('cls11', 'Class 11'), ('cls12', 'Class 12')],'Student Class')
    clg_stream = fields.Selection('College Stream', related='stud_name.clg_stream')
    teaching_jr_class = fields.Selection('Student Class', related='stud_name.teaching_jr_class')
    graduation_clg_stream = fields.Selection('Graduation', related='stud_name.graduation_clg_stream')
    post_graduation_clg_stream = fields.Selection('Post Graduation', related='stud_name.post_graduation_clg_stream')


    @api.onchange('stud_name')
    def onchange_stud_name(self):
        print('stud_name', self.stud_name)
        if self.stud_admission_type == 'school':
            obj = self.env['class.registration'].search([('teaching_class', '=', self.stud_class)])
            print('+++++++++++++++++++++++obj', obj)
            self.sub_name = obj.subject
        elif self.stud_admission_type == 'jr_college':
            obj1 = self.env['class.registration'].search(['&', ('teaching_jr_class', '=', self.teaching_jr_class),
                                                          ('clg_stream', '=', self.clg_stream)])
            print('++++++++++++++++++++++++obj1', obj1)
            self.sub_name = obj1.subject
        elif self.stud_admission_type == 'graduation' and self.clg_stream in ['science', 'commerce','arts'] and self.graduation_clg_stream in ['b_com', 'b_a', 'bsc', 'bca', 'bcs']:
            obj2 = self.env['class.registration'].search(['&', ('clg_stream', '=', self.clg_stream), ('graduation_clg_stream', '=', self.graduation_clg_stream)])
            print('++++++++++++++++++++++++obj2', obj2)
            self.sub_name = obj2.subject
        elif self.stud_admission_type == 'post_graduation' and self.clg_stream in ['science', 'commerce','arts'] and self.post_graduation_clg_stream in [
            'm_com', 'm_a', 'msc', 'mca', 'mcs']:
            obj3 = self.env['class.registration'].search(
                ['&', ('clg_stream', '=', self.clg_stream),
                 ('post_graduation_clg_stream', '=', self.post_graduation_clg_stream)])
            print('++++++++++++++++++++++++obj3', obj3)
            self.sub_name = obj3.subject

    # @api.onchange('stud_admission_type')
    # def onchange_stud_admission_type(self):
    #     obj = self.env['class.registration'].search(['&',('teaching_jr_class','=', self.teaching_jr_class),('clg_stream','=', self.clg_stream)])
    #     print('obj of onchange stud_admission_type',obj)
    #
    #     if obj:
    #         #self.class_teacher = obj.class_teacher.teacher_name
    #         self.sub_name = obj.class_teacher.sub_name + obj.subject
    #     else:
    #         raise ValidationError("{}'s Student Registration form is Incomplete".format(self.stud_name.student_name))

    # @api.onchange("stud_class")
    # def onchange_stud_name(self):
    #     print('---------------------------stud_class', self.stud_class)
    #     obj = self.env['class.registration'].search([('teaching_class','=',self.stud_class)])
    #     print('---------------------------obj', obj.class_teacher.teacher_name)
    #     if obj:
    #         #self.class_teacher = obj.class_teacher.teacher_name
    #         self.sub_name = obj.subject
    #
    #     else:
    #         if not obj.class_teacher.teacher_name:
    #             raise ValidationError('No Class Teacher Assign for this Student Class')
