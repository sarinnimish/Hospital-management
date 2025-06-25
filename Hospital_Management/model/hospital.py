from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Hospital(models.Model):
    _name = 'hospital.management'
    _description = 'Manage Hospital' 
    _rec_name='age'
    _rec_name = 'name' 

    
    name= fields.Char(string="Name" ,required=True)
    age=fields.Char(string="Age")
    Date_of_Birth= fields.Date(string='Date of Birth')  
    Marital_Status = fields.Selection([
        ('married','Married'),
        ('unmarried','Unmarried'),
        ('widow','Widow')],string="Marital Status")
    gender= fields.Selection([
       ('male', 'Male'),
       ('female', 'Female'),
       ('bisexual', 'Bisexual')], string='Gender')
    currency_id=fields.Many2one('res.currency',string="Currency",default=lambda self: self.env.company.currency_id.id,
                              readonly=True)
    company_id = fields.Many2one('res.company',string="Company", default=lambda self: self.env.company)
  

    # @api.depends('currency')
    # def _compute_is_same_currency(self):
    #  for record in self:
    #     if record.currency and self.env.company.currency_id.id:
    #         record.is_same_currency = record.currency == self.env.company.currency_id.id
    #     else:
    #         record.is_same_currency = False


    primary_doctor_care = fields.Many2one('physician',string="Primary Doctor Care")
    Address= fields.Char(string="Address")
    Patient_Image = fields.Binary(string = "")
    Blood_Type=fields.Selection([
        ('a+','A+'),
        ('a-','A-'),
        ('b+','B+'),
        ('b-','B-'),
        ('o+','O+'),
        ('o-','O-'),
        ('ab+','AB+'),
        ('ab-','AB-')
        ],string="Blood Type")
    Ethnic_Group=fields.Many2one('ethnic.group',string="Ethnic Group" )
    Rh=fields.Char(string="Rh" )
    Insurance=fields.Many2one('insurance.company',string="Insurance")
    phone=fields.Integer(string="Phone" )
    email=fields.Char(string="email" )
    Deceased=fields.Boolean(string="Deceased" )
    Family=fields.Char(string="Family" )
    Receivable=fields.Float(string="Receivable" )


    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                raise ValidationError("The name field cannot be empty.")
            if len(record.name) < 3:
                raise ValidationError("The name must be at least 3 characters long.")
            if not record.name.isalpha():
                raise ValidationError("The name must contain only alphabetic characters.")
            
    @api.onchange('Date_of_Birth')
    def _onchange_compute_patient_age(self):
        """Compute patient age in years, months, and days."""
        for record in self:
            if record.Date_of_Birth:
                today = date.today()
                dob = record.Date_of_Birth

                years = today.year - dob.year
                months = today.month - dob.month
                days = today.day - dob.day

                if days < 0:
                    months -= 1
                    days += (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days

                if months < 0:
                    years -= 1
                    months += 12

                record.age = f"{years} years, {months} months, {days} days"
            else:
                record.age = "0 years, 0 months, 0 days"

    def action_button(self):
        pass

class Appoinments(models.Model):
    _name = 'appoinments.management'
    _description = 'Manage Appoinments'  
    _rec_name = 'Patient_name' 
    _rec_name = 'apt_id'
    _rec_name='Appoinment_Date'

    Patient_name = fields.Many2one('hospital.management',string="Patient Name", required=True)
    prescription_id = fields.Many2one('prescription.management', string='Prescription')
    physician=fields.Many2one('health.center',string="Physician")
    Appoinment_Date=fields.Datetime(string="Appoinment Date", required=True )
    Appoinment_End=fields.Datetime(string="Appoinment End" , required=True)
    Patient_Status=fields.Char(string=" Patient Status" )
    Invoice_Exempt=fields.Boolean(string=" Invoice Exempt" )
    Status=fields.Char(string="Status" )
    Validity_Date=fields.Date(string="Validity Date" )
    health_centre=fields.Many2one('health.center.building',string="health centre", required=True )
    Inpatient_Registration=fields.Char(string="Inpatient Registration" )
    Duration=fields.Char(string=" Duration" )
    Urgency_Level=fields.Char(string="Urgency Level" , required=True)
    Invoice_to_Insurance=fields.Boolean(string="Invoice to Insurance" )
    Consultation_service=fields.Char(string="Consultation service" )
    speciality = fields.Char(string="Speciality")

    apt_id =fields.Char(string="Appoinment Id",copy=False, readonly=True, index=True ,default=lambda self: ('New'))
    
    def create(self, vals):
        if vals.get('apt_id',('New'))==('New'):
          vals['apt_id']=self.env['ir.sequence'].next_by_code('appoinments.management') or('New')
        result=super(Appoinments, self).create(vals)
        return result
    
    @api.onchange('physician')
    def _onchange_physician(self):
        if self.physician:
            self.speciality = self.Patient_name.primary_doctor_care.speciality
        else:
            self.speciality = False
    
    @api.constrains('Appoinment_Date', 'Appoinment_End')
    def _check_appointment_dates(self):
        for record in self:
            if record.Appoinment_End and record.Appoinment_Date and record.Appoinment_End <= record.Appoinment_Date:
                raise ValidationError("The appointment end date must be after the appointment start date.")
    
class Prescription(models.Model):
    _name = 'prescription.management'
    _description = 'Manage Prescriptions'  
    _rec_name = 'Patient_name'
    _rec_name = 'prescribing_doctor'
    
    Patient_name = fields.Many2one('hospital.management',string="Patient Name", required=True)
    prescription_detail_ids = fields.One2many(
        'prescription.detail','prescription_id')
    
    prescription_date=fields.Datetime(string="Prescription Date" )
    Login_user=fields.Many2one('res.users',string="Login User", required=True )
    pharmacy=fields.Many2one('health.center.building',string="Pharmacy", required=True )
    prescribing_doctor=fields.Many2one('health.center',string="Prescribing Doctor", required=True )
    Invoice_to_Insurance=fields.Boolean(string="Invoice to Insurance" )

    id =fields.Char(string=" ",copy=False, readonly=True, index=True ,default=lambda self: ('New'))
    
    def create(self, vals):
        if vals.get('id',('New'))==('New'):
          vals['id']=self.env['ir.sequence'].next_by_code('prescription.management') or('New')
        result=super(Prescription, self).create(vals)
        return result


class Prescriptiondetail(models.Model):
    _name = 'prescription.detail'
    _description = 'Prescription Details'  

    prescription_id = fields.Many2one('prescription.management', string='Prescription')
    Medicamant=fields.Many2one('medicament.misc',string="Medicamant", required=True )
    Indication=fields.Char(string="Indication" )
    Dose=fields.Float(string="Dose" , required=True)
    Dose_Unit=fields.Many2one('medicament.units',string="Dose Unit", required=True )
    Form=fields.Char(string="Form" )
    Frequency=fields.Integer(string="Frequency" , required=True)
    Quantity=fields.Integer(string="Quantity" , required=True)
    Treatment_Duration=fields.Char(string="Treatment Duration" )
    Treatment_Period=fields.Char(string="Treatment Period" )
    Allow_Substitution=fields.Boolean(string="Allow Substitution" )
    Comment=fields.Char(string="Comment" )



    

class Patienticu(models.Model):
    _name = 'patient.icu'
    _description = 'Manage Patient ICU'

    patienticu = fields.One2many(
        'mechanical.ventilation', 'duration', string='')

    reg_copy = fields.Char(string="Registration Code", readonly="True")
    registration_code = fields.Many2one('hospital.patient.hospitalization', string="Registration Code")
    admitted = fields.Boolean(string="Admitted", required=True)
    icu_admission = fields.Datetime(string="ICU Admission", required=True)
    duration = fields.Char(string="Duration", required=True)
    discharged = fields.Boolean(string="Discharged", required=True)
    # discharge = fields.Char(string="Discharge", required=True)

    @api.onchange('registration_code')
    def onchange_registration_code(self):
        for record in self:
            if record.registration_code:
                record.reg_copy = record.registration_code.ap_id
            else:
                record.reg_copy = ''

class Mechanical(models.Model):
     _name='mechanical.ventilation'
     _description='Manage Mechanical Ventilation'

     current=fields.Boolean(string="Current" , required=True)
     fromdate=fields.Datetime(string="From")
     duration=fields.Integer(string="Duration" , required=True)
     type=fields.Char(string="Type")
     remarks=fields.Char(string="Remarks")


class Apache(models.Model):
    _name='apache.score'
    _description='Manage Apache score'

    reg_copy = fields.Char(string="Registration Code", readonly="True")
    registration_code = fields.Many2one('hospital.patient.hospitalization', string="Registration Code")
    date=fields.Datetime(string="Date")
    score=fields.Integer(string="Score")
    age=fields.Integer(string="Age")
    temperature=fields.Float(string="Temperature")
    heart_rate=fields.Float(string="Heart Rate")
    flo2=fields.Float(string="Flo2")
    paco2=fields.Float(string="PaCO2")
    ph=fields.Float(string="PH")
    potassium=fields.Float(string="Potassium")
    hematcocrit=fields.Float(string="Hematcocrit")
    arf=fields.Boolean(string="ARF")
    map=fields.Integer(string="Map")
    respiratory_rate=fields.Integer(string="Respiratory Rate")
    pao2=fields.Integer(string="paO2")
    do2=fields.Integer(string="A-a DO2")
    sodium=fields.Integer(string="Sodium")
    creatinine=fields.Float(string="Creatinine")
    wbc=fields.Float(string="WBC")
    chronic_condition=fields.Boolean(string="Chronic Condition")

    @api.onchange('registration_code')
    def onchange_registration_code(self):
        for record in self:
            if record.registration_code:
                record.reg_copy = record.registration_code.ap_id
            else:
                record.reg_copy = ''

class ecg(models.Model):
    _name='ecg'
    _description='Manage ECG'

    reg_copy = fields.Char(string="Registration Code", readonly="True")
    registration_code = fields.Many2one('hospital.patient.hospitalization', string="Registration Code")
    date=fields.Datetime(string="Date")
    lead=fields.Integer(string="Lead")
    axis=fields.Char(string="Axis")
    rate=fields.Integer(string="Rate")
    pacemaker=fields.Char(string="Pacemaker")
    rhythm=fields.Char(string="rhythm")
    pr=fields.Integer(string="PR")
    qrs=fields.Integer(string="QRS")
    qt=fields.Integer(string="QT")
    st_segment=fields.Char(string="ST Segment")
    t_wave_inversion=fields.Boolean(string="T Wave Inversion")
    interpretation=fields.Char(string="Interpretation")
    
    @api.onchange('registration_code')
    def onchange_registration_code(self):
        for record in self:
            if record.registration_code:
                record.reg_copy = record.registration_code.ap_id
            else:
                record.reg_copy = ''

class gcs(models.Model):
    _name='gcs'
    _description='Manage GCS'

   
    reg_copy = fields.Char(string="Registration Code", readonly="True")
    registration_code = fields.Many2one('hospital.patient.hospitalization', string="Registration Code")
    date=fields.Datetime(string="Date")
    eyes=fields.Integer(string="Eyes")
    verbal=fields.Char(string="Verbal")
    motor=fields.Integer(string="Motor")
    glasgow=fields.Char(string="Glasgow")

     
    @api.onchange('registration_code')
    def onchange_registration_code(self):
        for record in self:
            if record.registration_code:
                record.reg_copy = record.registration_code.ap_id
            else:
                record.reg_copy = ''

class Pediatric(models.Model):
    _name='pediatric'
    _description='Manage Pediatric'
   
       
    ap_copy = fields.Char(string="Appoinment", readonly="True")
    appoinment = fields.Many2one('appoinments.management', string="Appoinment")
    patient=fields.Many2one('hospital.management',string="Patient" )
    date=fields.Datetime(string="Date")
    pcs_total=fields.Integer(string="Pcs Total")
    health_professional=fields.Many2one('res.users',string="Health Professional", required=True )

    @api.onchange('appoinment')
    def onchange_appoinment(self):
        for record in self:
            if record.appoinment:
                record.ap_copy = record.appoinment.apt_id
            else:
                record.ap_copy = ''

    check1=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="complaint of aches and pains")
    check2=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Spends more time alone")
    check3=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Tires easily, has little energy")
    check4=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Fidgety, unable to sit still")
    check5=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Has trouble with teacher")
    check6=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Less interested in school")
    check7=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Acts as if driven by a motor")
    check8=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Daydreams too much")
    check9=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Distracted easily")
    check10=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Is down on him or herself")
    check11=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Visits the doctor with doctor finding nothing wrong")
    check12=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Has trouble sleeping")
    check13=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Worries a lot")
    check14=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Feels he or she is bad")
    check15=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Takes unnecessary risks")
    check16=fields.Selection([
        ('never','Never'),
        ('sometimes','Sometimes'),
        ('often','Often'),
        ('always','Always')],string="Gets hurt frequently")
    

class Newborn(models.Model):
    _name='newborn'
    _description='Manage Newborn'
    _rec_name = 'baby_id'
   
    newborn_list_ids = fields.One2many(
        'newbornlistview','newborn_id', string='')
    baby_image = fields.Binary(string = "")
    baby_id = fields.Char(string="Baby ID", required=True)
    baby_name=fields.Char(string="Baby's Name", required=True)
    mother=fields.Char(string="Mother", required=True)
    dob=fields.Date(string="Date of Birth", required=True)
    sex=fields.Selection([
        ('boy','Boy'),
        ('girl','Girl')],string="Sex")
    length=fields.Float(string="Length")
    weight=fields.Float(string="Weight", required=True)
    discharged=fields.Datetime(string="Discharged")
    doctor=fields.Many2one('health.center',string="Doctor In Charge", required=True)
    cephalic_perameter=fields.Integer(string="Cephalic Perameter")
    
    baby_id =fields.Char(string="",copy=False, readonly=True, index=True ,default=lambda self: ('New'))
    
    def create(self, vals):
        if vals.get('baby_id',('New'))==('New'):
          vals['baby_id']=self.env['ir.sequence'].next_by_code('newborn') or('New')
        result=super(Newborn, self).create(vals)
        return result
    
    
class Newbornlistview(models.Model):
    _name='newbornlistview'
    _description='Manage Newborn List View'

    newborn_id=fields.Many2one('newborn',string="Name")
    minute=fields.Integer(string="Minute")
    respiration=fields.Integer(string="Respiration")
    activity=fields.Integer(string="Activity")
    appearance=fields.Char(string="Appearance")
    pulse=fields.Integer(string="Pulse")
    agpar_score=fields.Integer(string="Agpar Score")
    grimace=fields.Char(string="Grimace")




class LabRequests(models.Model):
    _name = 'lab.requests'
    _description = 'Manage Lab Requests'
   
    
    request_id = fields.Char(default=lambda self: ('New'), readonly=True)
    patient_name = fields.Many2one('hospital.management', string="Patient", required=True)
    test_type = fields.Many2one('lab.test.type',string="Test Type")
    date = fields.Datetime(string="Date", required=True)
    doctor = fields.Many2one('prescription.management', string="Doctor In Charge", required=True)
    invoice_to_insurance = fields.Boolean(string="Invoice to Insurance")
    request = fields.Char(string="Request", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('tested', 'Tested'),
        ('cancel', 'Cancel')
    ], string="State", default='draft')

    def action_confirm(self):
        """Mark the lab request as tested"""
        for record in self:
            record.state = 'tested'

    def create(self, vals):
        if vals.get('request', 'New') == 'New':
            vals['request'] = self.env['ir.sequence'].next_by_code('lab.requests') or 'New'
        result = super(LabRequests, self).create(vals)
        return result
    
    def action_open_test_wizard(self):
        """Function to open the Lab test wizard"""
        return {
            'name': ('Create Lab Result'),
            'type': 'ir.actions.act_window',
            'res_model': 'lab.result.1',
            'view_mode': 'form',
            'view_id': self.env.ref('Hospital_Management.lab_result_1_wizard_form').id,
            'target': 'new',
            'context': {'default_request_id': self.id} 
        }

    def action_cancel(self):
        """Mark test as Cancelled"""
        self.state = 'cancel'

    def action_open_lab_test_invoice_wizard(self):
            return {
                'type': 'ir.actions.act_window',
                'name': 'Lab Test Invoice Confirmation',
                'res_model': 'lab.test.invoice.confirmation.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_test_type': self.id},
            }


class TodayLabRequest(models.Model):

    _name = "today.lab.request"
    _description = "This model shows today's draft lab request"

    request = fields.Char(string="Request")
    test_type = fields.Many2one('lab.test.type',string="Test Type")
    test_date = fields.Datetime(string="Date")
    patient_id = fields.Many2one("hospital.management",string="Patient",required=True)
    patient_doctor = fields.Many2one('prescription.management',string="Doctor",required=True)
    state = fields.Selection([
        ('pending','Pending'),
        ('completd','Completed')
    ],required=True)


class Nursing(models.Model):
    _name="nursing"
    _description="this model shows the ambulatory care of patient"
    _rec_name='base_condition'
    
    # nursing_list_ids = fields.One2many(
    #     'nursinglistview','Id', string='')
    warning=fields.Boolean(string="Warning")
    name=fields.Char(string="Name")
    patient_id = fields.Many2one("hospital.management",string="Patient",required=True)
    start=fields.Datetime(string="Start")
    health_professional=fields.Many2one('prescription.management',string="Health Professional",required=True)
    evolution=fields.Many2one("hospital.management",string="Related Evalution")
    base_condition=fields.Many2one('diseases',string="Base Condition")
    session=fields.Integer("Session")
    ordering_physician=fields.Many2one('prescription.management',string="Ordering Physician",required=True)
    end=fields.Datetime(string="End")
    next_session=fields.Datetime(string="Next Session")
    procedure_ids = fields.Many2many("nursinglistview")


class Nursinglistview(models.Model):
    _name='nursinglistview'
    _description='Manage Nursing List View'
    _rec_name='code'
    
    
    code=fields.Many2one('medical.procedures',string="Code")
    comments=fields.Many2one('medical.procedures',string="Comments")  


class Surgery(models.Model):
    _name = 'surgery'
    _description = 'Manages Surgery Lists'
    _rec_name = 'description'
    
    patient_id = fields.Many2one("hospital.management", string="Patient Name")
    code = fields.Many2one('nursinglistview', string="Code")
    description = fields.Char(string="Description")
    base_condition = fields.Char(string="Base Condition")
    surgery_classification = fields.Selection([
        ('required', 'Required'),
        ('not required', 'Not Required'),
    ], string="Surgery Classification")
    date_of_surgery = fields.Datetime(string="Date of the surgery")
    age = fields.Char(string="Patient Age", readonly=True)
    surgeon = fields.Many2one('appoinments.management', string="Surgeon", readonly=True)
    extra_info = fields.Char(string="Extra Info")

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                # Fetch related nursing details
                patient_nursing_details = self.env['nursing'].search([('patient_id', '=', record.patient_id.id)], limit=1)
                if patient_nursing_details:
                    record.base_condition = patient_nursing_details.base_condition
                    if patient_nursing_details.procedure_ids:
                        record.code = patient_nursing_details.procedure_ids[0].id
                        record.description = patient_nursing_details.procedure_ids[0].comments
                
                # Fetch patient details
                record.age = record.patient_id.age
                record.surgeon = self.env['appoinments.management'].search([('Patient_name', '=', record.patient_id.id)], limit=1).id
                record.extra_info = record.patient_id.Address


class Medical(models.Model):
    _name='medical.service'
    _description='Manages Medical Services'
    
    medical_list_ids = fields.One2many(
        'medical.list','Id', string='')
    
    description=fields.Many2one('surgery',string="Description")
    base_condition=fields.Many2one('nursing',string="Base Condition")
    patient=fields.Many2one('hospital.management',string="Patient")
    date = fields.Datetime(string="Date", required=True)
    status=fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], string="Status", default='draft')

    def action_confirm(self):
        """Mark the lab request as tested"""
        for record in self:
            record.status = 'confirmed'

    Med_id= fields.Char(string="Name", required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        result = super(Medical, self).create(vals)
        result.Med_id= f"MEDSR0{result.id}"
        return result

    def get_id(self):
        return self.id
   
class Medicallist(models.Model):
    _name='medical.list'
    _description='manages Medical Lists'
    
    Id=fields.Integer(string="Id")
    invoice=fields.Boolean(string="Invoice")
    description=fields.Many2one('surgery',string="Description")
    product=fields.Integer(string="Product")
    qty=fields.Integer(string="Qty")
    from_date=fields.Datetime(string="From Date")
    to_date=fields.Datetime(string="To Date")



class MedicamentList(models.Model):

    _name = 'medicament'
    _description = 'Model to store the details of medicines'

    name = fields.Char(string="Name",required=True)
    active_component = fields.Char(string="Active Component")
    category = fields.Selection([
        ('antibiotics','Anitibiotics'),
        ('cough-syrup','Cough Syrup')
    ])
    quantity_available = fields.Integer(string="Quantity Available")
    therapeutic_effect = fields.Char(string="Therapeutic Effect")
    pregnancy_warning = fields.Char(string="Pregnancy Warning")
    price = fields.Integer(string="Price")


class PatientEvaluation(models.Model):

    _name = "patient.evaluation"
    _description = "This model shows the patient evaluation information"

    patient_id = fields.Many2one("hospital.management",string="Patient",required=True)
    start_evalutaion = fields.Datetime(string="Start Evaluation")
    chief_complaint = fields.Char(string="Chief Complaint")
    evaluation_type = fields.Char(string="Type")
    end_of_evaluation = fields.Datetime(string="End of Evaluation")
    doctor = fields.Char(string="Doctor", readonly=True)
    body_mass_index = fields.Float(string="Body Mass Index")
    systolic_pressure = fields.Float(string="Systolic Pressure")
    diastolic_pressure = fields.Float(string="Diastolic Pressure")
    presumptive_diagnosis = fields.Integer(string="Presumptive Diagnosis")
    next_appointment = fields.Char(string="Next Appointment")


    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.doctor = record.patient_id.primary_doctor_care
            else:
                record.doctor = ""
