from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Labtesting(models.Model):
    _name='lab.testing'
    _description='Lab Testing Records'
    
    name=fields.Char(string="Name")
    code=fields.Char(string="Code")


class Labtesttype(models.Model):
    _name='lab.test.type'
    _description='Manages Lab Test Types'
    _rec_name='name'

    name=fields.Selection([
        ('bloodtest', 'Blood Test'),
        ('biospy', 'Biopsy'),
        ('angiography', 'Angiography')
    ], string="Name")

    
    labtest= fields.Char(string="Code", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(Labtesttype, self).create(vals)
        result.labtest = f"TEST0{result.id}"
        return result

    def get_id(self):
        return self.id


class Pathology(models.Model):
    _name='pathology.groups'
    _description='Manages Pathology groups'

    name=fields.Char(string="Name")
    short_description=fields.Char(string="Short Description")


    path_id= fields.Char(string="Code", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(Pathology, self).create(vals)
        result.path_id = f"LBG0{result.id}"
        return result

    def get_id(self):
        return self.id


class Diseases(models.Model):
    _name='diseases'
    _description='Store Diseases Categories'
    _rec_name='name'

    name=fields.Char(string="Name")
    disease_category=fields.Char(string="Disease Category")

    dis_id= fields.Char(string="Code", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(Diseases, self).create(vals)
        result.dis_id = f"DIS0{result.id}"
        return result

    def get_id(self):
        return self.id

class Diseasecategorystructure(models.Model):
    _name='disease.categories'
    _description='Store Disease categories Structure'
    _rec_name='category_name'

    category_name=fields.Char(string="Category Name")


class Diseasecategory(models.Model):
    _name='disease.name'
    _description='Store Disease categories Names'

    category_name=fields.Many2one('disease.categories',string="Category Name")


class Medicalprocedures(models.Model):
    _name='medical.procedures'
    _description='Store Medical Procedures'
    _rec_name='code'

    code=fields.Char(string="Code")
    long_text=fields.Char(string="Long Text")


class Healthcenterbuilding(models.Model):
    _name='health.center.building'
    _description='Store Health Center Buildings'
    _rec_name='build_institute'

    build_name=fields.Char(string="Name")
    build_institute=fields.Char(string="Institute")


class Healthcenter(models.Model):
    _name='health.center'
    _description='Store health centers'
    _rec_name='name'

    name=fields.Char(string="Name")
    phone=fields.Char(string="Phone" )
    email=fields.Char(string="email" )

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email format: %s" % record.email)

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r"^\d{10}$", str(record.phone)):
                raise ValidationError("Phone number must be 10 digits: %s" % record.phone)



class Healthcenterunits(models.Model):
    _name='health.center.units'
    _description='Manages All the health center units'
    rec_name='name'
    
    name=fields.Char(string="Name")
    institute = fields.Many2one('health.center.building',string="Institute")


class Healthcenterwards(models.Model):
    _name='health.center.wards'
    _description='Manages All the health center wards'

    name=fields.Char(string="Name")
    beds=fields.Integer(string="Number Of Beds")
    Gender= fields.Selection([
       ('male ward', 'Male ward'),
       ('female ward', 'Female ward'),
       ('bisexual', 'Bisexual')], string='Gender')
    institution= fields.Many2one('health.center.building',string="Institution")
    status=fields.Selection([
       ('beds available', 'Beds Available'),
       ('full', 'Full'),
       ], string='status')
    

class Healthcenterbeds(models.Model):
    _name='health.center.beds'
    _description='Manages All the health center Beds'
    _rec_name='bed'

    bed=fields.Char(string="Bed")
    Ward=fields.Char(string="Ward")
    status=fields.Selection([
       ('free', 'Free'),
       ('occupied', 'Occupied'),
       ], string='status')
    

class Hospitaloperatingrooms(models.Model):
    _name='hospital.operating.rooms'
    _description='Manages All The Hospitals Rooms'

    name=fields.Char(string="Name")
    institution=fields.Many2one('health.center.building',string="Institution")
    building=fields.Many2one('health.center.building',string="Building")
    unit=fields.Many2one('health.center.units',string="Unit")


class OperationalAreas(models.Model):
    _name = "operational.areas"
    _description = "This model stores and shows the operational areas in the hospital"

    name = fields.Char(string="Name",required=True)

class OperationalSector(models.Model):
    _name = "operational.sector"
    _description = "Model to store the oeprational sectors"

    name = fields.Char(string="Name",required=True)
    operation_area = fields.Char(string="Operational Area")

class Physician(models.Model):
    _name = "physician"
    _description = "This model stores and shows the physicians in the hospital"
    _rec_name='physician'
    _rec_name='speciality'

    physician=fields.Many2one('health.center',string="Physician")
    institution=fields.Many2one('health.center.building',string="Institution")
    speciality=fields.Char(string="Speciality")
    p_id= fields.Char(string="ID", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(Physician, self).create(vals)
        result.p_id= f"SHP00{result.id}"
        return result

    def get_id(self):
        return self.id


class Medicamantadministration(models.Model):
    _name="medicament.administration"
    _description="This shows Medicaments"

    route=fields.Char(string="Route")
    code=fields.Char(string="Code")

class Medicamentform(models.Model):
    _name="medicament.form"
    _description="This shows Medicament forms"

    form=fields.Char(string="Form")
    code=fields.Char(string="Code")

class Medicamentstructure(models.Model):
    _name="medicament.structure"
    _description="This shows Medicament categories Structure"

    category_name=fields.Char(string="Category Name")

class Medicamentcategories(models.Model):
    _name="medicament.categories"
    _description="This shows Medicament categories"

    category_name=fields.Char(string="Category Name")


class Insurancecompany(models.Model):
    _name="insurance.company"
    _description="This shows Insurance Companies"

    name=fields.Char(string="Name")
    phone=fields.Char(string="Phone")
    email=fields.Char(string="Email")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email format: %s" % record.email)

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r"^\d{10}$", str(record.phone)):
                raise ValidationError("Phone number must be 10 digits: %s" % record.phone)

class Insurance(models.Model):
    _name="insurance"
    _description="This shows Insurance"

    owner=fields.Char(string="Owner")
    insurance_type=fields.Char(string="Insurance Type")
    insurance_company=fields.Many2one('insurance.company',string="Insurance Company")
    category=fields.Char(string="Category")
    member_since=fields.Date(string="Member Since")
    expiration_date=fields.Date(string="Expiration Date")
    
    Ins_id= fields.Char(string="Number", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(Insurance, self).create(vals)
        result.Ins_id= f"I000{result.id}"
        return result

    def get_id(self):
        return self.id
    
class geneticrisks(models.Model):
    _name="genetic.risks"
    _description="This shows genetic risks"

    name=fields.Char(string="Name")
    official_longname=fields.Char(string="Official Long Nmae")
    affected_chromosome=fields.Char(string="Affected Chromosome")
    dominance=fields.Char(string="Dominance")



class MedicamentsMisc(models.Model):
    _name = "medicament.misc"
    _description = 'Model to store the details of medicines'
    _rec_name='name'

    name = fields.Char(string="Name",required=True)
    active_component = fields.Char(string="Active Component")
    category_id = fields.Char(string="Category")
    quantity_available = fields.Integer(string="Quantity Available")
    therapeutic_effect = fields.Char(string="Therapeutic Effect")
    pregnancy_warning = fields.Boolean(string="Pregnancy Warning")
    price = fields.Float(string="Price")


class MedicalSpeciality(models.Model):
    _name = "medical.speciality"
    _description = "specialities of doctor"
   
    description = fields.Char(string="Description")
    speciality_id= fields.Char(string="Code", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(MedicalSpeciality, self).create(vals)
        result.speciality_id= f"SP000{result.id}"
        return result

    def get_id(self):
        return self.id



class MedicamentUnits(models.Model):
    _name = "medicament.units"
    _description = "This model store the units of the medicine"
    _rec_name='unit'
    
    unit = fields.Char(string="Unit")
    description = fields.Char(string="Description")


class Occupation(models.Model):
    _name = "occupation"
    _description = "Creates the Occupations"

    occupation = fields.Char(string="Occupation")
    code = fields.Char(string="Code")

class Ethnic(models.Model):
    _name ="ethnic.group"
    _description="This model stores the Ethnic groups"
    _rec_name='ethnic_group'

    ethnic_group = fields.Char(string="Ethnic  Group")
    code = fields.Char(string="code")


class Drugs(models.Model):
    _name="recreational.drugs"
    _description="This model stores the recreational drugs"

    name=fields.Char(string="Name")
    category=fields.Char(string="Category")
    toxicity=fields.Selection([
        ('high', 'High'),
        ('low', 'Low'),
        ('none', 'None')
    ], string="Toxicity")
    dependance=fields.Selection([
        ('high', 'High'),
        ('low', 'Low'),
        ('none', 'None')
    ], string="Dependance")

    street_names=fields.Char(string="Street Names")


  

