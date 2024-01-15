# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'School Management',
    'version': '1.0.0',
    'summary': 'School Management Summary',
    'sequence': -101,
    'description': """
    School Management By Kapil.
    """,
    'author': 'Kapil',
    'category': '',
    'website': 'https://www.odoo.com/app/invoicing',
    'images': [],
    'depends': ['mail', 'product','website'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_admission_view.xml',
        'views/student_registration_view.xml',
        'views/teacher_registration_view.xml',
        'views/subject_registration_view.xml',
        'views/sports_registration_view.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
