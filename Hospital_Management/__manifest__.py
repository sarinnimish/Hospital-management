{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Hospital Manage',
    'summary': 'Manage a Hospital',
    'description': '''A simple module to manage Hospital in Odoo.''',
    'author': 'Nimish sarin',
    'depends': ['base','stock','account','sale',],
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/record.xml',

        # data
        'data/record.xml',
       

        # report
        'report/management_reports.xml',
        'report/management_report_templates.xml',
        'report/patient_report_templates.xml',
        'report/patient_reports.xml',
        'report/prescription_report.xml',
        'report/prescription_report_templates.xml',

        # views
        'views/Hospital_views.xml',
        'views/Appoinments_views.xml',
        'views/patienticu_views.xml',
        'views/prescription_views.xml',
        'views/Apache_views.xml',
        'views/Ecg_views.xml',
        'views/Gcs_views.xml',
        'views/Pediatric_views.xml',
        'views/bed_transfer.xml',
        'views/Newborn_views.xml',
        'views/Labrequest_views.xml',
        'views/today_lab_views.xml',
        'views/Nursing_views.xml',
        'views/surgery_views.xml',
        'views/Medical_views.xml',
        'views/Patient_evaluation_views.xml',
        'views/Medicamant_views.xml',
        'controller/views/hospital_template.xml',
   
      
       
       

        # wizards
        'wizards/transfer_bed_wizard_views.xml',
        'wizards/lab_result_wizard_views.xml',
        'wizards/lab_resultinside_wizard_views.xml',
        'wizards/appoinment_evaluation_wizard_views.xml',
        'wizards/button_upload_wizard_views.xml',

        #configuration views
        'views/configuration/Labtesting_views.xml',
        'views/configuration/Labtesttype_views.xml',
        'views/configuration/Pathology_views.xml',
        'views/configuration/Diseases_views.xml',
        'views/configuration/Disease_categories_views.xml',
        'views/configuration/Disease_names_views.xml',
        'views/configuration/Medical_procedure_views.xml',
        'views/configuration/health_building_views.xml',
        'views/configuration/health_center_views.xml',
        'views/configuration/Health_units_views.xml',
        'views/configuration/Health_wards_views.xml',
        'views/configuration/Health_beds_views.xml',
        'views/configuration/Hospital_operating_views.xml',
        'views/configuration/operational_area_views.xml',
        'views/configuration/operational_sector_views.xml',
        'views/configuration/Physician_views.xml',
        'views/configuration/medicament_administration_views.xml',
        'views/configuration/medicament_form_views.xml',
        'views/configuration/Medicament_structure_views.xml',
        'views/configuration/medicament_categories_views.xml',
        'views/configuration/Insurance_company_views.xml',
        'views/configuration/Insurance_views.xml',
        'views/configuration/Genetic_risk_views.xml',
        'views/configuration/Misc_views.xml',
        'views/configuration/medicament_speciality_views.xml',
        'views/configuration/Medicament_units_views.xml',
        'views/configuration/occupation_views.xml',
        'views/configuration/ethnic_drugs_views.xml',
        'views/configuration/Drugs_views.xml',
        
        #menu
        'views/menu_items.xml',
        ],
    "assets": {
        "web.assets_backend": [
            '/Hospital_Management/static/src/js/button.js',
            '/Hospital_Management/static/src/xml/button_template.xml',
        ],

    },
    'installable': True,
    'application': True,
}




