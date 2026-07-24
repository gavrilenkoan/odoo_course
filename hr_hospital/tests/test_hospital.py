from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHospitalModels(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_intern = cls.env.ref('hr_hospital.doctor_category_intern')
        cls.category_specialist = cls.env.ref('hr_hospital.doctor_category_specialist')

        cls.doctor = cls.env['hospital.doctor'].create({
            'name': 'Dr. Test',
            'specialization': 'Therapy',
            'category_id': cls.category_specialist.id,
        })
        cls.patient = cls.env['hospital.patient'].create({
            'name': 'Test Patient',
        })

    def test_compute_age(self):
        doctor = self.env['hospital.doctor'].create({
            'name': 'Dr. Age',
            'specialization': 'Cardiology',
            'category_id': self.category_specialist.id,
            'birth_date': fields.Date.today() - relativedelta(years=30),
        })
        self.assertEqual(doctor.age, 30)

    def test_intern_requires_mentor(self):
        with self.assertRaises(ValidationError):
            self.env['hospital.doctor'].create({
                'name': 'Intern No Mentor',
                'specialization': 'Surgery',
                'category_id': self.category_intern.id,
            })

    def test_done_visit_is_protected(self):
        visit = self.env['hospital.visit'].create({
            'name': 'Visit 1',
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
        })
        visit.action_done()
        self.assertEqual(visit.status, 'done')
        self.assertTrue(visit.visit_datetime)

        with self.assertRaises(ValidationError):
            visit.write({'scheduled_datetime': fields.Datetime.now()})
        with self.assertRaises(ValidationError):
            visit.unlink()

    def test_disease_recursion_blocked(self):
        parent = self.env['hospital.disease'].create({'name': 'Cardio'})
        child = self.env['hospital.disease'].create({
            'name': 'Arrhythmia',
            'parent_id': parent.id,
        })
        with self.assertRaises(UserError):
            parent.parent_id = child

    def test_disease_display_name(self):
        parent = self.env['hospital.disease'].create({'name': 'Respiratory'})
        child = self.env['hospital.disease'].create({
            'name': 'Flu',
            'parent_id': parent.id,
        })
        self.assertEqual(child.display_name, 'Respiratory / Flu')
