from django.db import models

# Create your models here.


class prpo(models.Model):
    date=models.CharField(db_column='Date',max_length=100,blank=True,default='')
    day=models.CharField(db_column='day',max_length=100,blank=True,default='')
    month=models.CharField(db_column='month',max_length=100,blank=True,default='')
    year=models.CharField(db_column='year',max_length=100,blank=True,default='')
    Financial_year=models.CharField(db_column='Financial_year',max_length=100,blank=True,default='')
    business_type=models.CharField(db_column='business_type',max_length=100,blank=True,default='')
    Site_Name=models.CharField(db_column='Site_Name',max_length=100,blank=True,default='')
    SAP_status=models.CharField(db_column='SAP_status',max_length=100,blank=True,default='')
    Cluster=models.CharField(db_column='Cluster',max_length=100,blank=True,default='')
    Indent_Type_WR_or_PR=models.CharField(db_column='Indent_Type_WR_or_PR',max_length=100,blank=True,default='')
    Raised_by=models.CharField(db_column='Raised_by',max_length=100,blank=True,default='')
    Indent_Date=models.CharField(db_column='Indent_Date',max_length=100,blank=True,null=True)
    Material_required_Date=models.CharField(db_column='Material_required_Date',max_length=100,blank=True,null=True)
    Site_Requisition_Ref_No=models.CharField(db_column='Site_Requisition_Ref_No',max_length=100,blank=True,default='')
    Nature_of_Requirement=models.CharField(db_column='Nature_of_Requirement',max_length=100,blank=True,default='')
    Part_number=models.CharField(db_column='Part_number',max_length=100,blank=True,default='')
    Description_of_Material=models.CharField(db_column='Description_of_Material',max_length=100,blank=True,default='')
    UOM=models.CharField(db_column='UOM',max_length=100,blank=True,default='')
    Qty=models.CharField(db_column='Qty',max_length=100,blank=True,default='')
    C_P_Received_Date = models.CharField(db_column='C_P_Received_Date', max_length=100, blank=True, null=True)
    C_P_Received_by = models.CharField(db_column='C_P_Received_by', max_length=100, blank=True, default='')
    PR_or_WR_Open_or_IssuedDate= models.CharField(db_column='PR_or_WR_Open_or_Issued', max_length=100, blank=True, null=True)
    Pending_P_R_Age= models.CharField(db_column='Pending_P_R_Age', max_length=100, blank=True, default='')
    P_R_Process_Status = models.CharField(db_column='P_R_Process_Status', max_length=100, blank=True, default='')
    PO_WO_Number = models.CharField(db_column='PO_WO_Number', max_length=100, blank=True, default='')
    PO_WO_Dater = models.CharField(db_column='PO_WO_Dater', max_length=100, blank=True,null=True)
    Vendor_Name = models.CharField(db_column='Vendor_Name', max_length=100, blank=True, default='')
    PO_WO_Amount = models.CharField(db_column='PO_WO_Amount', max_length=100, blank=True, default='')
    Lead_Time_from_PR_to_PO= models.CharField(db_column='Lead_Time_from_PR_to_PO', max_length=100, blank=True, default='')
    Delivery_Date_as_per_PO_WO= models.CharField(db_column='Delivery_Date_as_per_PO_WO', max_length=100, blank=True, null=True)
    PO_WO_Status= models.CharField(db_column='PO_WO_Status', max_length=100, blank=True, default='')
    PO_WO_Open_Closed = models.CharField(db_column='PO_WO_Open_Closed', max_length=100, blank=True, default='')
    P_I_Amount= models.CharField(db_column='P_I_Amount', max_length=100, blank=True, default='')
    Invoice_Sent_to_Account_Date= models.CharField(db_column='Invoice_Sent_to_Account_Date', max_length=100, blank=True,null=True)
    QA_QC_Certification = models.CharField(db_column='QA_QC_Certification', max_length=100, blank=True,default='')
    QA_QC_Approved= models.CharField(db_column='QA_QC_Approved', max_length=100, blank=True,default='')
    QA_QC_Remarks= models.CharField(db_column='QA_QC_Remarks', max_length=100, blank=True,default='')
    MRN_No= models.CharField(db_column='MRN_No', max_length=100, blank=True, default='')
    MRN_Date= models.CharField(db_column='MRN_Date', max_length=100, blank=True,null=True)
    Invoice_No= models.CharField(db_column='Invoice_No', max_length=100, blank=True, default='')
    Invoice_Date= models.CharField(db_column='Invoice_Date', max_length=100, blank=True,null=True)
    Invoice_Amount= models.CharField(db_column='Invoice_Amount', max_length=100, blank=True, default='')
    MRN_Received_or_HO = models.CharField(db_column='MRN_Received_or_HO', max_length=100, blank=True, default='')
    Po_comments = models.CharField(db_column='Po_comments', max_length=100, blank=True, default='')
    Site_Certification = models.CharField(db_column='Site_Certification', max_length=100, blank=True, default='')
    QSD_Entry_Date= models.CharField(db_column='QSD_Entry_Date', max_length=100, blank=True,null=True)
    QSD_Certified_Date= models.CharField(db_column='QSD_Certified_Date', max_length=100, blank=True,null=True)
    Payment_Status = models.CharField(db_column='Payment_Status', max_length=100, blank=True, default='')
    Payment_to_Vendor_Date= models.CharField(db_column='Payment_to_Vendor_Date', max_length=100, blank=True,null=True)
    SBU_Head = models.CharField(db_column='SBU_Head', max_length=100, blank=True, default='')
    Dy_COO = models.CharField(db_column='Dy_COO', max_length=100, blank=True, default='')
    COO = models.CharField(db_column='COO', max_length=100, blank=True, default='')
    MAN = models.CharField(db_column='MAN', max_length=100, blank=True, default='')
    C_P_Remarks= models.CharField(db_column='C_P_Remarks', max_length=100, blank=True, default='')
    O_M_remarks = models.CharField(db_column='O_M_remarks',max_length=100, blank=True, default='')
    SAP_PR = models.CharField(db_column='SAP_PR',max_length=100, blank=True, default='')
    Site_PR_no = models.CharField(db_column='Site_PR_no',max_length=100, blank=True, default='')
    Closure_Performance = models.CharField(db_column='Closure_Performance',max_length=100, blank=True, default='')
    Mail_received_date = models.CharField(db_column='Mail_received_date',max_length=100, blank=True,null=True)
    status = models.CharField(db_column='status',max_length=100, blank=True, default='')
    remarks = models.CharField(db_column='Remarks',max_length=100, blank=True, default='')
    Is_active = models.CharField(db_column='Is_active',max_length=100, blank=True, default=True)
    editable= models.CharField(db_column='editable',max_length=100, blank=True, default='')

class approval_drop_down(models.Model):
    approval_data=models.CharField(db_column='approval_data',max_length=100, blank=True, null=True)

class SAP_drop_down(models.Model):
    SAP_drop_data=models.CharField(db_column='SAP_drop_data',max_length=100, blank=True, null=True)

class Indent_drop_down(models.Model):
    Indent_drop_data=models.CharField(db_column='Indent_drop_data',max_length=100, blank=True, null=True)

class Nature_of_Requirement_Drop_Down(models.Model):
    Nature_of_Requirement_drop_data=models.CharField(db_column='Nature_of_Requirement_drop_data',max_length=100, blank=True, null=True)

class PO_Open_close_Drop_Down(models.Model):
    PO_Open_close_drop_data=models.CharField(db_column='PO_Open_close_drop_data',max_length=100, blank=True, null=True)

class C_P_Received_By_Drop_Down(models.Model):
    C_P_Received_By_drop_data=models.CharField(db_column='C_P_Received_By_drop_data',max_length=100, blank=True, null=True)

class Business_type_Drop_Down(models.Model):
    Business_type_drop_data= models.CharField(db_column='Business_type_drop_data', max_length=200, blank=True, null=True)

class yes_no_Drop_Down(models.Model):
    yes_no_drop_data= models.CharField(db_column='yes_no_drop_data', max_length=200, blank=True, null=True)

class logdata(models.Model):
    username = models.CharField(db_column='USER_NAME', max_length=200)  # Field name made lowercase.
    timestamp = models.CharField(db_column='TIMESTAMP', max_length=200)  # Field name made lowercase.
    message = models.CharField(db_column='MESSAGE', max_length=500)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=500,null=True,blank=True)  # Field name made lowercase.

class userinfo(models.Model):
    EMPLOYEE_ID = models.IntegerField()
    FIRST_NAME = models.CharField(max_length=100, blank=True, null=True)
    LAST_NAME = models.CharField(max_length=100, blank=True, null=True)
    WORK_EMAIL = models.CharField(max_length=100, blank=True, null=True)
    CREATE_DATE = models.DateTimeField(auto_now_add=True, blank=True)
    USERNAME=models.CharField(max_length=100, blank=True, null=True)
    CREATED_BY=models.CharField(max_length=100, blank=True, null=True)
    ROLE =  models.CharField(max_length=100, blank=True, null=True)
    PROJECT = models.CharField(max_length=100, blank=True, null=True)
    APP_ID = models.CharField(max_length=100, blank=True, null=True)
    APP_URL = models.CharField(max_length=100, blank=True, null=True)
    BUSINESS_TYPE = models.CharField(max_length=100, blank=True, null=True)
    IS_ACTIVE = models.BooleanField(max_length=100, blank=True, null=True)
    USER_SOURCE = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Identity_userinfo'

    # MOBILE_NO = models.IntegerField(blank=True, null=True)
    # PASSWORD=models.CharField(max_length=100, blank=True, null=True)

class tokenblocklist(models.Model):
    token = models.CharField(max_length=500, null=True, blank=True)
    user = models.CharField(db_column='User',max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Identity_tokenblocklist'

class Appinfo(models.Model):

    APP_NAME = models.CharField(max_length= 200)
    APP_URL = models.CharField(max_length= 200,blank=True, null=True)
    DOMAIN_NAME = models.CharField(max_length=200, blank=True, null=True)
    CREATE_DATE = models.DateTimeField(auto_now_add=True, blank=True)
    CREATED_BY = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Identity_appinfo'

class solar_plantsDB(models.Model):
     type = models.CharField(db_column='type', max_length=100) # Field name made lowercase.
     PlantName = models.CharField(db_column='name', max_length=100) # Field name made lowercase.
     obj_id = models.TextField(db_column='object_id', max_length=100) # AutoField.
     _id = models.AutoField(db_column='_id', max_length=100, primary_key=True, unique=True) # AutoField.
     class Meta:
         managed = False
         db_table = 'solar_plantsDB'


class plantsDB(models.Model):
    plant_id = models.IntegerField(db_column='PLANT_ID')  # Field name made lowercase.
    business_id = models.IntegerField(db_column='BUSINESS_ID')  # Field name made lowercase.
    business_name = models.CharField(db_column='BUSINESS_NAME', max_length=150)  # Field name made lowercase.
    company_id = models.IntegerField(db_column='COMPANY_ID')
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=200)  # Field name made lowercase.
    office_name = models.CharField(db_column='OFFICE_NAME', max_length=100)  # Field name made lowercase.
    state_code = models.CharField(db_column='STATE_CODE', max_length=20)  # Field name made lowercase.
    plant_code = models.CharField(db_column='PLANT_CODE', max_length=200)  # Field name made lowercase.
    plant_name = models.CharField(db_column='PLANT_NAME', max_length=200)  # Field name made lowercase.
    office_id = models.IntegerField(db_column='OFFICE_ID')
    plant_capacity = models.IntegerField(db_column='PLANT_CAPACITY')
    display_order = models.IntegerField(db_column='DISPLAY_ORDER')
    geo_latitude = models.FloatField(db_column='GEO_LATITUDE')
    geo_logitude = models.FloatField(db_column='GEO_LONGITUDE')
    active_status = models.BooleanField(db_column='ACTIVE_STATUS')
    display_status = models.BooleanField(db_column='DISPLAY_STATUS')
    id = models.TextField(db_column='_id', max_length=100, primary_key=True,unique=True)  # AutoField.
    class Meta:
        managed = False
        db_table = 'PlantsDB'



class GAM_Wind_plant(models.Model):

    Site = models.CharField(db_column='Site', max_length=200,blank=True, null=True)
    Entity = models.CharField(db_column='Entity', max_length=200,blank=True, null=True)
    SPVName = models.CharField(db_column='SPVName', max_length=200,blank=True, null=True)
    State = models.CharField(db_column='State', max_length=200,blank=True, null=True)
    Location= models.CharField(db_column='Location', max_length=200,blank=True, null=True)
    OEM= models.CharField(db_column='OEM', max_length=200,blank=True, null=True)
    RDHH= models.CharField(db_column='RD/HH', max_length=200,blank=True, null=True)
    Cap_MW = models.CharField(db_column='Cap (MW)', max_length=200,blank=True, null=True)
    WTG_Count = models.CharField(db_column='WTG (Count)', max_length=200,blank=True, null=True)
    EachWTGCapacity_KW = models.CharField(db_column='EachWTG Capacity(KW)', max_length=200,blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'DGRapp_gam_wind_plant'


class solar_wind_plants(models.Model):
    type = models.CharField(db_column='type', max_length=100)  # Field name made lowercase.
    PlantName = models.CharField(db_column='name', max_length=100)  # Field name made lowercase.
    obj_id = models.TextField(db_column='object_id', max_length=100)  # AutoField.
    _id = models.AutoField(db_column='_id', max_length=100, primary_key=True, unique=True)  # AutoField.
    class Meta:
        managed = False
        db_table = 'DGRapp_solar_wind_plants'

class hydro_plantsDB(models.Model):

    plant_name = models.TextField(db_column='Company Name', max_length=100)  # Field name made lowercase.
    code = models.TextField(db_column='Code', max_length=100)  # Field name made lowercase.
    location = models.TextField(db_column='Location', max_length=100)  # Field name made lowercase.
    unit = models.TextField(db_column='UNITS', max_length=100)  # Field name made lowercase.
    plant_cap = models.TextField(db_column='Plant Capacity (MW)', max_length=100)  # Field name made lowercase.
    cod = models.TextField(db_column='COD', max_length=100)  # Field name made lowercase.
    plant_cap_unit = models.TextField(db_column='Capacity per Unit', max_length=100)  # Field name made lowercase.
    _id = models.AutoField(db_column='_id', max_length=100, primary_key=True, unique=True)  # AutoField.
    class Meta:
        managed = False
        db_table = 'HydroPlantsDB'



