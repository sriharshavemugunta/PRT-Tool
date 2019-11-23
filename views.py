import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

import sys ,os
from .models import prpo,userinfo,C_P_Received_By_Drop_Down,tokenblocklist,plantsDB,Appinfo,\
    approval_drop_down,logdata,SAP_drop_down,PO_Open_close_Drop_Down,Indent_drop_down,\
    solar_plantsDB,Nature_of_Requirement_Drop_Down,GAM_Wind_plant,solar_wind_plants,\
    hydro_plantsDB,Business_type_Drop_Down,yes_no_Drop_Down
from datetime import timedelta
import datetime as dt
from datetime import date
import jwt,json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
import ast
from calendar import timegm

def validation(request):
    auth = get_authorization_header(request).split()
    print('length of auth::\t',len(auth))

    if len(auth)==0:
        return JsonResponse({'message': "Internal server error",'success':2} )
    if len(auth) == 1:
        msg = 'Invalid token header '
        return JsonResponse({'message': msg,'success':2})
    elif len(auth) > 2:
        msg = 'Invalid token header'
        return JsonResponse({'message': msg,'success':2})
    try:
        print('auth[0]',auth[0])
        if auth[0].decode('utf-8').lower().strip() =='token':
            token = auth[1]
            print('token in def:', token)
            if token == "null":
                msg = 'Null token not allowed'
                return JsonResponse({'message': msg, 'success': 2})
            return authenticate_credentials(token)

    except UnicodeError:
        msg = 'Invalid token header. Token string should not contain invalid characters.'
        return JsonResponse({'message': msg,'success':2})

def authenticate_credentials(token):

    try:

        try:
            payload = jwt.decode(token, "SECRET_KEY", )
        except jwt.InvalidSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN",'success':2})
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "Session Expired ,Please login",'success':2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN",'success':2})
        username = payload['username']
        email = payload['email']
        time = payload['exp']
        print('time::', type(time))
        # msg = {'Error': "Token mismatch", 'status': "401"}
        try:
            # print(userinfo.objects.get(FIRST_NAME=email, WORK_EMAIL=userid))
            token1 = token.decode('utf-8')
            print('token1111::\t', token1.strip())

            if len(list(tokenblocklist.objects.using('SSO').filter(token=token1).values())) > 0:
                return JsonResponse({'message': "Session Expired ,Please login", 'success': 2})
            else:
                print('user in authenticationLL ::',username)

                user = userinfo.objects.using('SSO').filter(USERNAME=username).all()

                print('user in authenticationLL ::', user)
                for obj in user:
                    username_db = obj.USERNAME
                    email_db = obj.WORK_EMAIL

                    if username_db == username:
                       print('username in auth function::\t', username)

                       if time:
                            refresh_limit = dt.timedelta(days=1)
                            if isinstance(refresh_limit, timedelta):
                                # refresh_limit = refresh_limit.seconds
                                refresh_limit = (refresh_limit.days * 24 * 3600 + refresh_limit.seconds)
                            expiration_timestamp = time + int(refresh_limit)
                            now_timestamp = timegm(dt.datetime.utcnow().utctimetuple())
                            if now_timestamp > expiration_timestamp:
                                msg = 'Refresh has expired.'
                                # raise serializers.ValidationError(msg)
                                return JsonResponse({"msg": msg})
                            new_payload = {'username': username, 'email': email_db, 'exp': expiration_timestamp}
                            new_token = jwt.encode(new_payload, key='SECRET_KEY')
                            print('token in if condtions:', new_token)

                            return JsonResponse({'token': token.decode('utf-8'), 'username': username})
            if not username:
                return JsonResponse({'message': "INVALID_TOKEN",'success':2})

        except userinfo.DoesNotExist:
            return JsonResponse({'message': "Internal server error",'success':2})
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': "Session Expired ,Please login",'success':2})


def get_financial_year_budget(datestring):
  date = dt.datetime.strptime(datestring, "%Y-%m-%d").date()
  # initialize the current year
  year_of_date = date.year
  # initialize the current financial year start date
  financial_year_start_date = dt.datetime.strptime(str(year_of_date) + "-04-01", "%Y-%m-%d").date()
  if date < financial_year_start_date:
      return str(financial_year_start_date.year - 1) + '-' + str(financial_year_start_date.year)
  else:
      return str(financial_year_start_date.year) + '-' + str(financial_year_start_date.year + 1)

@csrf_exempt
def insert_new_form(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print('request in insert new form::', request)

        response = validation(request)
        print('response in insert new form::', response)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            print('response_dict', response_dict)

            if 'username' in response_dict.keys():
                user_name = response_dict['username']
                print('user_name',user_name)

                # user_role = list(userinfo.using('SSO').objects.filter(USERNAME=user_name, IS_ACTIVE=True).values())
                # print('.......,user_role......', user_role[0]['ROLE'])
                # # site entries  = l4
                # if 'L4-Executive Lead'.lower() in user_role[0]['ROLE'].lower():

                site_entry_data=prpo(date=form_data['date'],business_type=form_data['business_type'])
                site_entry_data.save()
                site_entry_data_r = list(prpo.objects.filter(Is_active=True).values())
                print('site_entry_data',site_entry_data_r)
                print('site_entry_data_r')


                return JsonResponse({'data':site_entry_data_r, 'success': 1})
            else:
                return JsonResponse(response_dict)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print(e)
            return JsonResponse({'message': 'Error in data insertion', 'success': 0})
# return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': "Method not allowed", 'success': 2})


@csrf_exempt
def upadte_new_form(request):
    if request.method == 'POST':
        print('.........request......', request)
        response = validation(request)
        print('.........responce......',response)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            if 'username' in response_dict.keys():
                user_name = response_dict['username']
                form_data = json.loads(request.body)
                Day_MM_YY = form_data['date'].split('-')
                day = Day_MM_YY[0]
                month = Day_MM_YY[1]
                year = Day_MM_YY[2]
                # #####################################
                # print('user_META::\n', request.META['HTTP_DOMAIN'])
                # domain = request.META['HTTP_DOMAIN']
                # print('......domain......', domain)
                print('......Site_Name.......',form_data['Site_Name'])

                # domain_details = list(Appinfo.objects.using('SSO').filter(DOMAIN_NAME=domain).values())
                # print('........domain_details........', domain_details)
                APPURL = "http://testpps.gits.lan/ui"
                # APPURL = "http://prt.greenko.net/ui"

                user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name,APP_URL=APPURL, IS_ACTIVE=True).values())
                # user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name, IS_ACTIVE=True).values())

                user_createdby_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_role[0]['CREATED_BY'],IS_ACTIVE=True).values())
                mainrole=user_createdby_role[0]['ROLE']
                cluster = list(plantsDB.objects.using('SSO').filter(plant_name=form_data['Site_Name'], business_name=form_data['business_type']).values('state_code'))
                status_requrment = prpo.objects.filter(id=form_data['id'], Is_active=True).values('status')
                print('status_requrment:::',status_requrment)
                if status_requrment is not None:
                    sat_requrment=status_requrment[0]['status']

                print('sat_requrment::::',sat_requrment)

                print('.......,user_role......', user_role[0]['ROLE'])
                fy_year = get_financial_year_budget(form_data['date'])
                site='L4-Executive Lead'
                approvals='APEX'
                c_p='L2-Cluster Lead'
                treasury='L1-HO Lead'
                w_o='L3-Site Lead'
                # prpo.objects.filter(id=form_data['id']).update(remarks=form_data['remarks'])
                prpo.objects.filter(id=form_data['id'],status='completed', Is_active=True).update(editable='no')
                prpo.objects.filter(id=form_data['id'],Is_active=True).update(remarks=form_data['remarks'],O_M_remarks=form_data['O_M_remarks'],C_P_Remarks=form_data['C_P_Remarks'])
                # L4--PO-site entry,PO-site stores
                if site.lower() in user_role[0]['ROLE'].lower():
                    print('came to L4')
                    print('..........Indent_Date............',form_data['Indent_Date'])
                    prpo.objects.filter(id=form_data['id'],Is_active=True).update(date=form_data['date'])



                    if form_data['Site_Name'].strip() !='' and form_data['Description_of_Material'].strip() !='':
                        if len(list(prpo.objects.filter(id=form_data['id'],Is_active=True,Site_Name=form_data['Site_Name'],Description_of_Material=form_data['Description_of_Material']))) ==0:
                            print('came to if')
                            prpo.objects.filter(id=form_data['id'],Is_active=True).update(Site_Name=form_data['Site_Name'],
                                   Cluster=cluster[0]['state_code'], SAP_status=form_data['SAP_status'],Indent_Type_WR_or_PR=form_data['Indent_Type_WR_or_PR'],
                                   Raised_by=form_data['Raised_by'],Indent_Date=form_data['Indent_Date'],
                                    Material_required_Date=form_data['Material_required_Date'],
                                   Site_Requisition_Ref_No=form_data['Site_Requisition_Ref_No'],
                                   Nature_of_Requirement=form_data['Nature_of_Requirement'],Part_number=form_data['Part_number'],
                                   Description_of_Material=form_data['Description_of_Material'],
                                   UOM=form_data['UOM'], Qty=form_data['Qty'], day=day, month=month, year=year,
                                   Financial_year=fy_year, editable='yes')
                            # ppo_data.save()
                            # print("..........ppo_data...........", ppo_data)
                            print('......SAP_status.....',prpo.objects.filter(id=form_data['id'],Is_active=True,).values('SAP_status'))

                            if form_data['Site_Name'].strip() != '' and form_data['Description_of_Material'].strip() != '':
                                status="Pending at Approvals"

                                prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                            # latest_obj=list(prpo.objects.filter(id__isnull=False).latest('id'))
                            # latest_obj = list(prpo.objects.order_by('id').values())[-1]
                            message_log = str(user_name) + ' has updated Site Entries at ' + str(dt.datetime.now())
                            comments = ''
                            data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                               message=message_log,
                                               comments=comments)
                            data_log.save()
                            # latest_obj1 = list(prpo.objects.filter(id=form_data['id']).values())

                            # print("..........latest_obj1...........",latest_obj1)
                            return JsonResponse({'message':'data entried succesfully','success': 1})
                        else:
                            if form_data['SAP_status'].strip() == 'SAP' and sat_requrment.strip() !='Cancelled':
                                if form_data['Site_Name'].strip() != '' and form_data['Description_of_Material'].strip() != '' :
                                    prpo.objects.filter(id=form_data['id'], Is_active=True).update(SAP_PR=form_data['SAP_PR'],Site_PR_no=form_data['Site_PR_no'],
                                                                                                   Closure_Performance=form_data['Closure_Performance'],
                                                                                                   Mail_received_date=form_data['Mail_received_date'])

                                    # latest_obj = list(prpo.objects.filter(id=form_data['id'], Is_active=True).values())
                                    message_log = str(user_name) + ' has updated SAP Details at ' + str(
                                        dt.datetime.now())
                                    comments = ''
                                    data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                       message=message_log,
                                                       comments=comments)
                                    data_log.save()
                                    # return JsonResponse({'message': 'data entried succesfully', 'data': latest_obj, 'success': 1})
                                    return JsonResponse({'message': 'data entried succesfully', 'success': 1})
                                else:
                                    return JsonResponse({'message': 'No Requirment', 'success': 1})
                            # if form_data['Indent_Type_WR_or_PR'].strip() == 'Supply' and sat_requrment.strip() != 'Cancelled':
                            #     prpo.objects.filter(id=form_data['id'], Indent_Type_WR_or_PR='Supply',Is_active=True).update(QA_QC_Certification=form_data['QA_QC_Certification'],
                            #                                                                                                  QA_QC_Approved=form_data['QA_QC_Approved'],
                            #                                                                                                  QA_QC_Remarks=form_data['QA_QC_Remarks'])
                            if form_data['Indent_Type_WR_or_PR'].strip() == 'Supply' and sat_requrment.strip() !='Cancelled' and form_data['QA_QC_Approved'].strip().lower() !='no':
                                prpo.objects.filter(id=form_data['id'],Indent_Type_WR_or_PR='Supply',Is_active=True).update(
                                                                                                           MRN_No=form_data['MRN_No'], MRN_Date=form_data['MRN_Date'],
                                                                                                       Invoice_No=form_data['Invoice_No'],
                                                                                                       Invoice_Date=form_data['Invoice_Date'],
                                                                                                       Invoice_Amount=form_data['Invoice_Amount'],
                                                                                                        Po_comments=form_data['Po_comments'],
                                                                                                       MRN_Received_or_HO=form_data['MRN_Received_or_HO'],editable='yes')
                                if form_data['MRN_No'] != '' and form_data['Invoice_No'] != '' and form_data['QA_QC_Approved'].strip().lower() !='yes':
                                    status = "Pending at  Accounts/Treasury"

                                    prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                                latest_obj = list(prpo.objects.filter(id=form_data['id'],Is_active=True).values())

                                message_log = str(user_name) + ' has updated PO - Site Stores at ' + str(dt.datetime.now())
                                comments = ''
                                data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                   message=message_log,
                                                   comments=comments)
                                data_log.save()

                                # print("..........latest_obj...........",latest_obj)
                                # return JsonResponse({'message': 'data entried succesfully', 'data': latest_obj, 'success': 1})
                                return JsonResponse({'message': 'data entried succesfully', 'success': 1})

                    else:
                        return JsonResponse({'message': 'Please Fill The Details Completely', 'success': 1})

                # elif approvals.lower() in user_role[0]['ROLE'].lower():
                #     print('apex')
                #     if len(list(prpo.objects.filter(date=form_data['date'],id=form_data['id'],Is_active=True,Site_Name=form_data['Site_Name']))) !=0:
                #         prpo.objects.filter(date=form_data['date'],id=form_data['id'],Is_active=True).update(SBU_Head=form_data['SBU_Head'],Dy_COO=form_data['Dy_COO'],
                #                                                                     COO=form_data['COO'],MAN=form_data['MAN'])
                #         if form_data['SBU_Head'] != '':
                #             status = "Pending at  C & P"
                #             prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                #         print('............form_data..........',form_data['id'])
                #         data=list(prpo.objects.filter(id=form_data['id'],Is_active=True).values())
                #         # print('..........data.........',data)
                #         message_log = str(user_name) + ' has Approved at ' + str(dt.datetime.now())
                #         comments = ''
                #         data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                #                            message=message_log,
                #                            comments=comments)
                #         data_log.save()
                #         return JsonResponse({'message': "Approved",'data':data,'success': 1})
                #     else:
                #         return JsonResponse({'message': "no material to approve", 'success': 1})

                #     print('satuus',satuus)
                elif c_p.lower() in user_role[0]['ROLE'].lower() and sat_requrment.strip() !='Cancelled' :
                    print('came to l2')
                    app_val = list(prpo.objects.filter(date=form_data['date'], id=form_data['id'], Is_active=True).values('SBU_Head'))
                    if 'approved' in app_val[0]['SBU_Head'].lower():
                    # if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],SBU_Head='Approved',Is_active=True))) != 0:
                        prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(
                            C_P_Received_Date=form_data['C_P_Received_Date'],
                            C_P_Received_by=form_data['C_P_Received_by'],
                            PR_or_WR_Open_or_IssuedDate=form_data['PR_or_WR_Open_or_IssuedDate'],
                            Pending_P_R_Age=no_days(form_data['PR_or_WR_Open_or_IssuedDate']),
                            P_R_Process_Status=form_data['P_R_Process_Status'],
                            PO_WO_Number=form_data['PO_WO_Number'], PO_WO_Dater=form_data['PO_WO_Dater'],
                            Vendor_Name=form_data['Vendor_Name'], PO_WO_Amount=form_data['PO_WO_Amount'],
                            PO_WO_Open_Closed=form_data['PO_WO_Open_Closed'],
                            Lead_Time_from_PR_to_PO=form_data['Lead_Time_from_PR_to_PO'],
                            Delivery_Date_as_per_PO_WO=form_data['Delivery_Date_as_per_PO_WO'],
                            PO_WO_Status=form_data['PO_WO_Status'])
                        if form_data['PO_WO_Open_Closed'].strip() == 'Close':
                            prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(P_I_Amount=form_data['P_I_Amount'],
                                                                                                                  Invoice_Sent_to_Account_Date=form_data['Invoice_Sent_to_Account_Date'])
                        print('updated')
                        if form_data['Vendor_Name'] != '' and form_data['PO_WO_Open_Closed'].strip()=='Close':
                            status = "Pending at  PO - Site Stores/WO - Certification Status"

                            prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                        message_log = str(user_name) + ' has updated C & P at ' + str(dt.datetime.now())
                        comments = ''
                        data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                           message=message_log,
                                           comments=comments)
                        data_log.save()
                        # return JsonResponse({'message': "successful entry",'data':list(prpo.objects.filter(id=form_data['id'],Is_active=True).values()),'success': 1})
                        return JsonResponse({'message': "successful entry",'success': 1})
                    else:
                        return JsonResponse({'message': "Material not approvied",'success': 1})

                elif c_p.lower() in mainrole.lower() and sat_requrment.strip() != 'Cancelled' and form_data['PR_or_WR_Open_or_IssuedDate'] is not None:
                    print('came to L2')
                    app_val=list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).values('SBU_Head'))
                    if 'approved' in app_val[0]['SBU_Head'].lower():

                    # if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'], SBU_Head='Approved',Is_active=True))) != 0:
                        prpo.objects.filter(date=form_data['date'], id=form_data['id'], Is_active=True).update(
                            PR_or_WR_Open_or_IssuedDate=form_data['PR_or_WR_Open_or_IssuedDate'],
                            Pending_P_R_Age=no_days(form_data['PR_or_WR_Open_or_IssuedDate']),
                            P_R_Process_Status=form_data['P_R_Process_Status'],
                            PO_WO_Number=form_data['PO_WO_Number'], PO_WO_Dater=form_data['PO_WO_Dater'],
                            Vendor_Name=form_data['Vendor_Name'], PO_WO_Amount=form_data['PO_WO_Amount'],
                            PO_WO_Open_Closed=form_data['PO_WO_Open_Closed'],
                            Lead_Time_from_PR_to_PO=form_data['Lead_Time_from_PR_to_PO'],
                            Delivery_Date_as_per_PO_WO=form_data['Delivery_Date_as_per_PO_WO'],
                            PO_WO_Status=form_data['PO_WO_Status'])
                        if form_data['PO_WO_Open_Closed'].strip() == 'Close':
                            prpo.objects.filter(date=form_data['date'], id=form_data['id'], Is_active=True).update(
                                P_I_Amount=form_data['P_I_Amount'],
                                Invoice_Sent_to_Account_Date=form_data['Invoice_Sent_to_Account_Date'])
                        print('updated')
                        if form_data['Vendor_Name'] != '' and form_data['PO_WO_Open_Closed'].strip().strip()=='Close':
                            status = "Pending at  PO - Site Stores/WO - Certification Status"
                            prpo.objects.filter(id=form_data['id'], Is_active=True).update(status=status)
                        message_log = str(user_name) + ' has updated C & P at ' + str(dt.datetime.now())
                        comments = ''
                        data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                           message=message_log,
                                           comments=comments)
                        data_log.save()
                        # return JsonResponse({'message': "successful entry", 'data': list(prpo.objects.filter(id=form_data['id'], Is_active=True).values()), 'success': 1})
                        return JsonResponse({'message': "successful entry", 'success': 1})
                    else:
                        return JsonResponse({'message': "Material not Approved", 'success': 1})


                elif w_o.lower() in user_role[0]['ROLE'].lower()and form_data['PO_WO_Open_Closed'].strip()=='Close'and sat_requrment.strip() !='Cancelled' and 'Service' in form_data['Indent_Type_WR_or_PR']:
                    print('came to l3')
                    if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],Indent_Type_WR_or_PR='Service',Vendor_Name='',Is_active=True))) != 0:
                        prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(
                        Site_Certification=form_data['Site_Certification'], QSD_Entry_Date=form_data['QSD_Entry_Date'],
                        QSD_Certified_Date=form_data['QSD_Certified_Date'])
                        if form_data['Site_Certification'] != '' and form_data['QSD_Entry_Date'] != '':
                            status = "Pending at  Accounts/Treasury"
                            prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                        message_log = str(user_name) + ' has updated WO - Certification Status at ' + str(dt.datetime.now())
                        comments = ''
                        data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                           message=message_log,
                                           comments=comments)
                        data_log.save()
                        # return JsonResponse({'message': "successfull",'data':list(prpo.objects.filter(id=form_data['id']).values()),'success': 1})
                        return JsonResponse({'message': "successfull",'success': 1})
                    else:
                        return JsonResponse({'message': " Suppy Requriment", 'success': 1})


                elif treasury.lower() in user_role[0]['ROLE'].lower()and sat_requrment.strip() !='Cancelled' and form_data['PO_WO_Open_Closed'].strip()=='Close':
                    if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True))) != 0:
                        print('came to l1')
                        prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(
                        Payment_Status=form_data['Payment_Status'], Payment_to_Vendor_Date=form_data['Payment_to_Vendor_Date'])
                        if form_data['Payment_Status'] != '':
                            status = "completed"
                            prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                        message_log = str(user_name) + ' has updated Accounts/Treasury at ' + str(dt.datetime.now())
                        comments = ''
                        data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                           message=message_log,
                                           comments=comments)
                        data_log.save()
                        # return JsonResponse({'message': "successfull",'data':list(prpo.objects.filter(id=form_data['id'],Is_active=True).values()),'success': 1})
                        return JsonResponse({'message': "successfull",'success': 1})
                    # else:
                    #     return JsonResponse({'message': " near C & P", 'success': 1})
                    # latest_obj = list(prpo.objects.order_by('id').values())[-1]

                elif approvals.lower() in user_role[0]['ROLE'].lower() or 'admin' in user_role[0]['ROLE'].lower():
                    print('User Role in Admin :: ', user_role[0]['ROLE'].lower())
                    status=''
                    if form_data['Site_Name']!='' and form_data['Description_of_Material']!='':
                        print('came to l4 and admin')
                        prpo.objects.filter(id=form_data['id'],Is_active=True).update(date=form_data['date'])
                        if len(list(prpo.objects.filter(id=form_data['id'],Is_active=True,Site_Name=form_data['Site_Name'],Description_of_Material=form_data['Description_of_Material'])))==0:
                            print('came to if')
                            prpo.objects.filter(id=form_data['id'],Is_active=True).update(Site_Name=form_data['Site_Name'],
                                   Cluster=cluster[0]['state_code'], SAP_status=form_data['SAP_status'],Indent_Type_WR_or_PR=form_data['Indent_Type_WR_or_PR'],
                                   Raised_by=form_data['Raised_by'],Indent_Date=form_data['Indent_Date'],
                                    Material_required_Date=form_data['Material_required_Date'],
                                   Site_Requisition_Ref_No=form_data['Site_Requisition_Ref_No'],
                                   Nature_of_Requirement=form_data['Nature_of_Requirement'],Part_number=form_data['Part_number'],
                                   Description_of_Material=form_data['Description_of_Material'],
                                   UOM=form_data['UOM'], Qty=form_data['Qty'], day=day, month=month, year=year,
                                   Financial_year=fy_year, editable='yes')
                            # ppo_data.save()
                            # print("..........ppo_data...........", ppo_data)
                            print('......SAP_status.....',prpo.objects.filter(id=form_data['id'],Is_active=True,).values('SAP_status'))
                            if form_data['Site_Name'].strip() != '' and form_data['Description_of_Material'].strip() != '':
                                status="Pending at Approvals"
                                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', status)
                                prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                            # latest_obj=list(prpo.objects.filter(id__isnull=False).latest('id'))
                            latest_obj = list(prpo.objects.order_by('id').values())[-1]
                            message_log = str(user_name) + ' has updated Site Entries at ' + str(dt.datetime.now())
                            comments = ''
                            data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                               message=message_log,
                                               comments=comments)
                            data_log.save()
                            latest_obj1 = list(prpo.objects.filter(id=form_data['id']).values())

                            print("..........latest_obj1...........",latest_obj1)
                            msg='data entried succesfully'

                        else:
                            msg=''
                            if form_data['SAP_status']=='SAP'and sat_requrment !='Cancelled':
                                if form_data['Site_Name'] != '' and form_data['Description_of_Material'] != '' :
                                    prpo.objects.filter(id=form_data['id'], Is_active=True).update(SAP_PR=form_data['SAP_PR'],
                                                                                                   Site_PR_no=form_data['Site_PR_no'],
                                                                                                   Closure_Performance=form_data['Closure_Performance'],
                                                                                                   Mail_received_date= form_data['Mail_received_date'])


                            # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', status)

                            if form_data['Site_Name'].strip() != '' and form_data['Description_of_Material'].strip() != '' and form_data['SAP_PR'].strip() !='':
                                status="SAP Updated"
                                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', status)
                                prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                            # latest_obj=list(prpo.objects.filter(id__isnull=False).latest('id'))
                            latest_obj = list(prpo.objects.order_by('id').values())[-1]
                            message_log = str(user_name) + ' has updated SAP Entries at ' + str(dt.datetime.now())
                            comments = ''
                            data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                               message=message_log,
                                               comments=comments)
                            data_log.save()
                            latest_obj1 = list(prpo.objects.filter(id=form_data['id']).values())

                            print("..........latest_obj1...........",latest_obj1)
                            msg='data entried succesfully'

                                # return JsonResponse({'message':'data entried succesfully','data': latest_obj,'success': 1})

                        # else:
                        #     msg = 'no requiment'
                            # return JsonResponse({'message': 'data entried succesfully', 'data': latest_obj, 'success': 1})

                    # if approvals.lower() in user_role[0]['ROLE'].lower():
                            print('came to l3 and admin')
                            # status=''
                            print('SBU_Head::::',form_data['SBU_Head'])
                            S_Head = form_data['SBU_Head']
                            Dy_COO = form_data['Dy_COO']
                            COO = form_data['COO']
                            MAN = form_data['MAN']

                            # if form_data['SBU_Head'] is not None :
                            if form_data['SBU_Head'] is not None and len(form_data['SBU_Head'].split('(')) == 1 and form_data['SBU_Head'].strip() != '' and form_data['SBU_Head'].strip() != '-' :
                                S_Head=form_data['SBU_Head'] +' ('+ str(datetime.date.today().strftime('%d-%m-%Y'))+')'

                            if form_data['Dy_COO'] is not None and len(form_data['Dy_COO'].split('('))==1 and form_data['Dy_COO'].strip() != '' and form_data['Dy_COO'].strip() != '-' :
                                Dy_COO=form_data['Dy_COO'] +' ('+ str(datetime.date.today().strftime('%d-%m-%Y'))+')'

                            if form_data['COO'] is not None and len(form_data['COO'].split('('))==1 and form_data['COO'].strip() != '' and form_data['COO'].strip() != '-' :
                                COO=form_data['COO'] +' ('+ str(datetime.date.today().strftime('%d-%m-%Y'))+')'

                            if  form_data['MAN'] is not None and len(form_data['MAN'].split('('))==1 and  form_data['MAN'].strip() != '' and form_data['MAN'].strip() != '-':
                                MAN=form_data['MAN'] +' ('+ str(datetime.date.today().strftime('%d-%m-%Y'))+')'


                            if len(list(prpo.objects.filter(date=form_data['date'],id=form_data['id'],Is_active=True,Site_Name=form_data['Site_Name']))) !=0:
                                prpo.objects.filter(date=form_data['date'],id=form_data['id'],Is_active=True).update(SBU_Head=S_Head,
                                                                                                                     Dy_COO=Dy_COO,COO=COO,MAN=MAN)

                                if 'Approved' in form_data['SBU_Head'] and ('Approved' in form_data['Dy_COO']  or '-' in form_data['Dy_COO'] or form_data['Dy_COO'].strip() != '') \
                                        and ('Approved' in form_data['COO'] or '-' in form_data['COO'] or form_data['COO'].strip() != '')and ('Approved' in form_data['MAN'] or '-' in form_data['MAN'] or form_data['MAN'].strip() != ''):
                                    status = "Pending at  C & P"
                                    prpo.objects.filter(id=form_data['id'], Is_active=True).update(status=status)
                                if form_data['SBU_Head'] == 'Cancel'or form_data['Dy_COO'] == 'Cancel'or form_data['COO'] == 'Cancel'or form_data['MAN'] == 'Cancel':
                                    status = "Cancelled"

                                    prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                                print('............form_data..........',form_data['id'])
                                data=list(prpo.objects.filter(id=form_data['id'],Is_active=True).values())
                                # print('..........data.........',data)
                                message_log = str(user_name) + ' has Approved at ' + str(dt.datetime.now())
                                comments = ''
                                data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                   message=message_log,
                                                   comments=comments)
                                data_log.save()
                                msg = 'Successful entry'

                                # return JsonResponse({'message': "Approved",'data':data,'success': 1})
                            else:
                                msg = "no material to approve"
                            #     return JsonResponse({'message': "no material to approve", 'success': 1})

                        # if approvals.lower() in user_role[0]['ROLE'].lower():
                        #     print('came to l2 and admin')
                            if 'Approved' in form_data['SBU_Head'] and sat_requrment.strip() != 'Cancelled' and form_data['PR_or_WR_Open_or_IssuedDate'] is  None:
                                prpo.objects.filter(date=form_data['date'], id=form_data['id'],
                                                        Is_active=True).update(
                                        C_P_Received_Date=form_data['C_P_Received_Date'],
                                        C_P_Received_by=form_data['C_P_Received_by'],)
                                if form_data['Vendor_Name'] != '' and form_data['PO_WO_Open_Closed'] == 'Close':
                                    status = "Pending at  PO - Site Stores/WO - Certification Status"
                                    prpo.objects.filter(id=form_data['id'], Is_active=True).update(status=status)
                                message_log = str(user_name) + ' has assigned the requirement to'+form_data['C_P_Received_by']+'at ' + str(dt.datetime.now())
                                comments = ''
                                data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                   message=message_log,
                                                   comments=comments)
                                data_log.save()
                                msg = "successful entry"
                            if 'Approved' in form_data['SBU_Head'] and sat_requrment.strip() != 'Cancelled' and form_data['PR_or_WR_Open_or_IssuedDate'] is not None:
                                print('came to l2 and admin')
                                if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True))) != 0:
                                    prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(
                                    C_P_Received_Date=form_data['C_P_Received_Date'],C_P_Received_by=form_data['C_P_Received_by'],
                                        PR_or_WR_Open_or_IssuedDate= form_data['PR_or_WR_Open_or_IssuedDate'],Pending_P_R_Age=no_days(form_data['PR_or_WR_Open_or_IssuedDate']),
                                        P_R_Process_Status=form_data['P_R_Process_Status'],
                                    PO_WO_Number=form_data['PO_WO_Number'],PO_WO_Dater= form_data['PO_WO_Dater'],
                                    Vendor_Name=form_data['Vendor_Name'],PO_WO_Amount=form_data['PO_WO_Amount'],
                                    PO_WO_Open_Closed=form_data['PO_WO_Open_Closed'],Lead_Time_from_PR_to_PO=form_data['Lead_Time_from_PR_to_PO'],
                                    Delivery_Date_as_per_PO_WO= form_data['Delivery_Date_as_per_PO_WO'],PO_WO_Status=form_data['PO_WO_Status'],
                                    P_I_Amount=form_data['P_I_Amount'],Invoice_Sent_to_Account_Date= form_data['Invoice_Sent_to_Account_Date'])
                                    if form_data['Vendor_Name'] != '' and form_data['PO_WO_Open_Closed'].strip()=='Close':
                                        status = "Pending at  PO - Site Stores/WO - Certification Status"
                                        prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                                    message_log = str(user_name) + ' has updated C & P at ' + str(dt.datetime.now())
                                    comments = ''
                                    data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                       message=message_log,
                                                       comments=comments)
                                    data_log.save()
                                    msg = "successful entry"
                                # return JsonResponse({'message': "successful entry",'data':list(prpo.objects.filter(id=form_data['id'],Is_active=True).values()),'success': 1})
                            elif  form_data['PR_or_WR_Open_or_IssuedDate'] is not None and form_data['Vendor_Name'].strip()!='':
                                msg = "Material not approvied"
                                return JsonResponse({'message': "PR or WR Open or IssuedDate is Required",'success': 1})
                        # if approvals.lower() in user_role[0]['ROLE'].lower():
                            if form_data['Indent_Type_WR_or_PR'].strip() == 'Supply' and sat_requrment.strip() != 'Cancelled':
                                prpo.objects.filter(id=form_data['id'], Indent_Type_WR_or_PR='Supply',Is_active=True).update(
                                    QA_QC_Certification=form_data['QA_QC_Certification'],
                                    QA_QC_Approved=form_data['QA_QC_Approved'],
                                    QA_QC_Remarks=form_data['QA_QC_Remarks'])

                                message_log = str(user_name) + ' has updated QA/QC Columns at ' + str(dt.datetime.now())
                                comments = ''
                                data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                   message=message_log,
                                                   comments=comments)
                                data_log.save()
                            if form_data['Indent_Type_WR_or_PR'].strip() == 'Supply' and sat_requrment.strip() != 'Cancelled' and form_data['QA_QC_Approved'].strip().lower() == 'yes':
                                print('came to if')
                                prpo.objects.filter(id=form_data['id'],Indent_Type_WR_or_PR='Supply',Is_active=True).update(
                                                                               MRN_No=form_data['MRN_No'],
                                                                               MRN_Date= form_data['MRN_Date'],
                                                                               Invoice_No=form_data['Invoice_No'],
                                                                               Invoice_Date= form_data['Invoice_Date'],
                                                                               Invoice_Amount=form_data['Invoice_Amount'],
                                                                               Po_comments=form_data['Po_comments'],
                                                                               MRN_Received_or_HO=form_data['MRN_Received_or_HO'],
                                                                                editable='yes')
                                if (form_data['MRN_No'].strip() != '' and form_data['Invoice_No'].strip() != '' and form_data['QA_QC_Approved'].strip().lower() == 'yes' ) :
                                    status = "Pending at  Accounts/Treasury"
                                    prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                                latest_obj = list(prpo.objects.filter(id=form_data['id'],Is_active=True).values())

                                message_log = str(user_name) + ' has updated PO - Site Stores at ' + str(dt.datetime.now())
                                comments = ''
                                data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                   message=message_log,
                                                   comments=comments)
                                data_log.save()

                                # print("..........latest_obj...........",latest_obj)
                                msg = 'data entried succesfully'
                            if form_data['Indent_Type_WR_or_PR'].strip() == 'Service'and form_data['PO_WO_Open_Closed'].strip()=='Close'and form_data['Vendor_Name'].strip() != '' and sat_requrment !='Cancelled' and form_data['Site_Certification'].strip() != '':
                                print('............Indent_Type_WR_or_PR:::..........',form_data['Indent_Type_WR_or_PR'])
                                print('came to l1 and admin')
                                if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],Indent_Type_WR_or_PR='Service' ,Is_active=True))) != 0:
                                    prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(
                                    Site_Certification=form_data['Site_Certification'], QSD_Entry_Date= form_data['QSD_Entry_Date'],
                                    QSD_Certified_Date= form_data['QSD_Certified_Date'])
                                    if form_data['Site_Certification'].strip() != '' and form_data['QSD_Entry_Date'].strip() != '':
                                        status = "Pending at  Accounts/Treasury"
                                        print(status)
                                        prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                                    message_log = str(user_name) + ' has updated WO - Certification Status at ' + str(dt.datetime.now())
                                    comments = ''
                                    data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                       message=message_log,
                                                       comments=comments)
                                    data_log.save()
                                    msg = "successful entry"
                                    # return JsonResponse({'message': "successfull",'data':list(prpo.objects.filter(id=form_data['id']).values()),'success': 1})
                                else:
                                    msg = " Suppy Requriment"
                            # else:
                            #     msg = " no Indent Type"
                            #     return JsonResponse({'message': " Suppy Requriment", 'success': 1})
                        # if approvals.lower() in user_role[0]['ROLE'].lower():
                        #     satuus=prpo.objects.filter(id=form_data['id'], Is_active=True).values('status')
                        #     print('satuus',satuus)
                            if form_data['P_I_Amount']!='' or form_data['QSD_Certified_Date']!='' and form_data['PO_WO_Open_Closed'].strip()=='Close'and sat_requrment !='Cancelled' and form_data['Payment_Status'] != '':
                            # if satuus[0]['status'] == "Pending at  Accounts/Treasury" and (form_data['P_I_Amount']!='' or form_data['QSD_Certified_Date']!=''):
                                if len(list(prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True))) != 0:
                                    print('came to l1 and admin')
                                    prpo.objects.filter(date=form_data['date'], id=form_data['id'],Is_active=True).update(
                                    Payment_Status=form_data['Payment_Status'], Payment_to_Vendor_Date= form_data['Payment_to_Vendor_Date'])
                                    if form_data['Payment_Status'] != '':
                                        status = "completed"
                                        prpo.objects.filter(id=form_data['id'],Is_active=True).update(status=status)
                                    message_log = str(user_name) + ' has updated Accounts/Treasury at ' + str(dt.datetime.now())
                                    comments = ''
                                    data_log = logdata(username=user_name, timestamp=dt.datetime.now(),
                                                       message=message_log,
                                                       comments=comments)
                                    data_log.save()
                                    msg = "successful entry"
                                    # return JsonResponse({'message': "successfull",'data':list(prpo.objects.filter(id=form_data['id'],Is_active=True).values()),'success': 1})
                                else:
                                    msg = " no ID"
                        # else:
                        #     msg = "at C&P"
                            return JsonResponse({'message': msg, 'success': 1})
                    else:
                        msg = 'no requrmnet'
                    return JsonResponse({'message':'successful entry', 'success': 1})
                else:
                    return JsonResponse({'message': "not valid user", 'success': 1})
            else:
                return JsonResponse(response_dict)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print(e)
            return JsonResponse({'message': 'Error in data insertion', 'success': 0})
        # return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': "Method not allowed", 'success': 2})

@csrf_exempt
def badges_data_retrival(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "Token is invalid", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            if 'username' in response_dict.keys():
                # data =
                try:
                    if len(request.GET['date']) == 0 and len(request.GET['Financial_year']) == 0:

                        return JsonResponse({'data': list(prpo.objects.filter(Is_active=True).values()), 'success': 1})

                    elif  len(request.GET['date']) != 0 and len(request.GET['Financial_year']) == 0:
                        date = request.GET['date']
                        # contact_number = request.GET['contact_number']
                        return JsonResponse({'data': list(prpo.objects.filter(date=date,Is_active=True).values()), 'success': 1})

                    elif  len(request.GET['Financial_year']) != 0:
                        Financial_year = request.GET['Financial_year']
                        # contact_number = request.GET['contact_number']
                        return JsonResponse({'data': list(prpo.objects.filter(Financial_year=Financial_year,Is_active=True).values()), 'success': 1})

                    else:
                        return JsonResponse({'message': 'key or value missing', 'success': 1})

                except:
                    return JsonResponse({'message': 'key or value missing', 'success': 1})
                # return JsonResponse({'message': 'Campaign Created successfully', 'success': 0})
            else:
                return JsonResponse(response_dict)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "Token is invalid", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "Token is invalid", 'success': 2})
        # return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def retriving_data(request):
    if request.method == 'GET':
        # form_data = json.loads(request.body)
        print('request in insert new form::', request)

        response = validation(request)
        # print('response in insert new form::', response)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            # print('response_dict', response_dict)

            if 'username' in response_dict.keys():
                user_name = response_dict['username']
                print('user_name', user_name)
                APPURL = "http://testpps.gits.lan/ui"
                # APPURL = "http://prt.greenko.net/ui"
                user_b_type = list(userinfo.objects.using('SSO').filter(USERNAME=user_name, APP_URL=APPURL, IS_ACTIVE=True).values('BUSINESS_TYPE'))
                print('....user_b_type...',user_b_type)
                print('....user_b_type...',user_b_type[0]['BUSINESS_TYPE'])
                b_type=user_b_type[0]['BUSINESS_TYPE']
                site_entry_data_r = list(prpo.objects.filter(business_type=b_type, Is_active=True).values())
                if b_type.strip().lower() =='all' or b_type.strip().lower() =='':
                    site_entry_data_r = list(prpo.objects.filter(Is_active=True).values())
                    count_data = prpo.objects.filter(Is_active=True).values().count()
                    return JsonResponse({'data': site_entry_data_r, 'count': count_data, 'success': 1})
                else:
                    site_entry_data_r = list(prpo.objects.filter(business_type=b_type, Is_active=True).values())
                    count_data = prpo.objects.filter(business_type=b_type,Is_active=True).values().count()
                    return JsonResponse({'data': site_entry_data_r, 'count': count_data, 'success': 1})
                # page_results = Paginator(site_entry_data_r, request.GET['size_of_page'])
                # ress = page_results.page(request.GET['offset'])
                # report_details = ress.object_list

                # count_data = prpo.objects.filter(Is_active=True).values().count()
                # return JsonResponse({'data': site_entry_data_r,'count':count_data, 'success': 1})
                # return JsonResponse({'data': report_details,'count':count_data,'success': 1})
            else:
                return JsonResponse(response_dict)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print(e)
            return JsonResponse({'message': 'Error in data retrival', 'success': 0})
    # return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': "Method not allowed", 'success': 2})

@csrf_exempt
def delete_new_form(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        response = validation(request)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            if 'username' in response_dict.keys():
                user_name = response_dict['username']
                # change to userinfo before production
                # user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name, IS_ACTIVE=True).values())
                # print('.......,user_role......', user_role[0]['ROLE'])
                # # site entries  = l4
                # if 'admin' in user_role[0]['ROLE'].lower():
                if len(list(prpo.objects.filter(date=form_data['date'],id=form_data['id'],Is_active=True)))!=0:
                    prpo.objects.filter(date=form_data['date'],id=form_data['id']).update(Is_active=False)
                    return JsonResponse({'message': 'row removed', 'success': 1})
                else:
                    return JsonResponse({'message': 'no row to remove', 'success': 1})



            else:
                return JsonResponse(response_dict)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print(e)
            return JsonResponse({'message': 'Error in data insertion', 'success': 0})

# return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': "Method not allowed", 'success': 2})

@csrf_exempt
def enable_disable(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        response = validation(request)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            if 'username' in response_dict.keys():
                user_name = response_dict['username']
                SAP_status=form_data['SAP_status']
                Indent_type=form_data['Indent_type']
                QA_QC_Certification=form_data['QA_QC_Certification']
                QA_QC_Approved=form_data['QA_QC_Approved']

                site = 'L4-Executive Lead'
                approvals = 'APEX'
                c_p = 'L2-Cluster Lead'
                treasury = 'L1-HO Lead'
                w_o = 'L3-Site Lead'
                site_colums = ['date', 'business_type','Site_Name','SAP_status', 'Indent_Type_WR_or_PR', 'Raised_by', 'Indent_Date', 'Material_required_Date','Site_Requisition_Ref_No',
                               'Nature_of_Requirement','Part_number', 'Description_of_Material', 'UOM','Qty']
                Q_A_Columns=['QA_QC_Certification','QA_QC_Approved','QA_QC_Remarks']
                PO_coulmns=['MRN_No', 'MRN_Date', 'Invoice_No', 'Invoice_Date', 'Invoice_Amount','MRN_Received_or_HO','Po_comments']
                sap=['SAP_PR', 'Site_PR_no', 'Closure_Performance', 'Mail_received_date']
                c_and_p_columns = ['C_P_Received_Date', 'C_P_Received_by','PR_or_WR_Open_or_IssuedDate','P_R_Process_Status','PO_WO_Number', 'PO_WO_Dater', 'Vendor_Name', 'PO_WO_Amount', 'PO_WO_Open_Closed', 'Lead_Time_from_PR_to_PO',
                                  'Delivery_Date_as_per_PO_WO', 'PO_WO_Status', 'P_I_Amount', 'Invoice_Sent_to_Account_Date']
                approvals_columns = ['SBU_Head', 'Dy_COO', 'COO', 'MAN']
                treasury_coulmns = ['Payment_Status', 'Payment_to_Vendor_Date']
                Q_and_D_coulmns =['Site_Certification', 'QSD_Entry_Date', 'QSD_Certified_Date']
                # domain = request.META['HTTP_DOMAIN']
                # print('......domain......', domain)
                #
                # domain_details = list(Appinfo.objects.using('SSO').filter(DOMAIN_NAME=domain).values())
                # print('........domain_details........', domain_details)
                # APPURL = "http://prt.greenko.net/ui"
                APPURL = "http://testpps.gits.lan/ui"
                user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name,APP_URL=APPURL,IS_ACTIVE=True).values())
                print('user_role::',user_role)
                # user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name,IS_ACTIVE=True).values())
                user_createdby_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_role[0]['CREATED_BY'], IS_ACTIVE=True).values())
                mainrole = user_createdby_role[0]['ROLE']
                data={}
                print('user_role[0]',user_role[0]['ROLE'])
                main_columns=site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+Q_and_D_coulmns+sap+PO_coulmns+Q_A_Columns
                with_sap=site_colums+sap
                with_supply=site_colums+PO_coulmns+sap
                for j in main_columns + ['Cluster'] + ['Pending_P_R_Age']:
                    data[j] = 'no'
                print('varsgdj::::',list(prpo.objects.filter(id=form_data['id'], status='completed', Is_active=True)))
                if len(list(prpo.objects.filter(id=form_data['id'], status='completed', Is_active=True))) ==0:

                    for j in ['remarks','O_M_remarks','C_P_Remarks']:
                        data[j]='yes'
                    if site.lower() in user_role[0]['ROLE'].lower():
                        if 'SAP' == SAP_status and '' == Indent_type :
                            print('1')
                            for i in with_sap:
                                data[i]='yes'
                        elif 'SAP' == SAP_status and QA_QC_Approved.lower() == 'yes' and 'Supply' == Indent_type:
                            for i in site_colums + c_and_p_columns + approvals_columns + treasury_coulmns + sap + Q_A_Columns + PO_coulmns:
                                    data[i] = 'yes'
                        elif 'Non SAP' in SAP_status and QA_QC_Approved.lower() == 'yes' and 'Supply' == Indent_type:
                            for i in site_colums + c_and_p_columns + approvals_columns + treasury_coulmns + Q_A_Columns + PO_coulmns:
                                data[i] = 'yes'
                        elif 'SAP'==SAP_status and 'Service' == Indent_type :
                            for i in with_sap:
                                data[i]='yes'
                        else:
                            for i in site_colums:
                                data[i]='yes'

                    elif approvals.lower() in user_role[0]['ROLE'].lower() or 'admin'.lower() in user_role[0]['ROLE'].lower():
                        if 'SAP' == SAP_status and '' == Indent_type :
                            print('1')
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap:
                                data[i]='yes'
                        elif 'SAP' == SAP_status and 'Supply' == Indent_type and '' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == '':
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap+[Q_A_Columns[0]]:
                                data[i]='yes'
                        elif 'Non SAP' == SAP_status and 'Supply' == Indent_type and '' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == '':
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap+[Q_A_Columns[0]]:
                                data[i]='yes'
                        elif 'SAP' == SAP_status and 'Supply' == Indent_type and 'no' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == '':
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap+[Q_A_Columns[0]]:
                                data[i]='yes'
                        elif 'SAP'==SAP_status and 'Supply' == Indent_type and 'yes' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == '':
                            print("5678")
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap+Q_A_Columns:
                                data[i]='yes'
                        elif 'SAP'==SAP_status and 'Service' == Indent_type :
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap+Q_and_D_coulmns:
                                data[i]='yes'
                        elif 'Non SAP' in SAP_status and 'Supply'== Indent_type and 'yes' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == '':
                            print("1234")
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+Q_A_Columns:
                                data[i]='yes'
                        elif 'SAP'==SAP_status and 'yes' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == 'no' and 'Supply' == Indent_type:
                            for i in site_colums+sap+Q_A_Columns:
                                data[i]='yes'
                        elif 'Non SAP'==SAP_status and 'yes' == QA_QC_Certification.lower()and QA_QC_Approved.lower() == 'no' and 'Supply' == Indent_type:
                            for i in site_colums+sap+Q_A_Columns:
                                data[i]='yes'
                        elif 'Non SAP' in SAP_status and 'Service'== Indent_type :
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+Q_and_D_coulmns:
                                data[i]='yes'
                        elif 'SAP'==SAP_status and QA_QC_Approved.lower() == 'yes' and 'Supply' == Indent_type:
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+sap+Q_A_Columns+PO_coulmns:
                                data[i]='yes'
                        elif 'Non SAP' in SAP_status and QA_QC_Approved.lower() == 'yes' and 'Supply' == Indent_type:
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+Q_A_Columns+PO_coulmns:
                                data[i]='yes'
                        else:
                            for i in site_colums+c_and_p_columns+approvals_columns+treasury_coulmns:
                                data[i] = 'yes'
                    elif c_p.lower() in mainrole.lower():
                        for i in c_and_p_columns[2:]:
                            data[i] = 'yes'
                    elif c_p.lower() in user_role[0]['ROLE'].lower():
                        for i in c_and_p_columns:
                            data[i] = 'yes'
                    elif w_o.lower() in user_role[0]['ROLE'].lower():
                        if 'Service' in Indent_type:
                            for i in Q_and_D_coulmns:
                                data[i] = 'yes'
                    elif treasury.lower() in user_role[0]['ROLE'].lower():
                        for i in treasury_coulmns:
                            data[i] = 'yes'
                else:
                    return JsonResponse({'message': 'Completed and Cannot be Edited','data':data, 'success': 1})
                return JsonResponse({'data': data ,'success': 1})



            else:
                return JsonResponse(response_dict)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print(e)
            return JsonResponse({'message': 'Error in data insertion', 'success': 0})

# return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': "Method not allowed", 'success': 2})

# @csrf_exempt
# def enable_disable(request):
#     if request.method == 'POST':
#         form_data = json.loads(request.body)
#         response = validation(request)
#         try:
#             try:
#                 response_data = response.content
#                 response_data = response_data.decode('utf-8')
#             except:
#                 return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
#             response_dict = ast.literal_eval(response_data)
#             if 'username' in response_dict.keys():
#                 user_name = response_dict['username']
#                 SAP_status=form_data['SAP_status']
#                 Indent_type=form_data['Indent_type']
#
#                 site = 'L4-Executive Lead'
#                 approvals = 'admin'
#                 c_p = 'L2-Cluster Lead'
#                 treasury = 'L1-HO Lead'
#                 w_o = 'L3-Site Lead'MRN_Received_or_HO
#                 site_colums = ['date', 'Site_Name','SAP_status', 'Indent_Type_WR_or_PR', 'Raised_by', 'Indent_Date', ' Material_required_Date','Site_Requisition_Ref_No',
#                                'Nature_of_Requirement','Part_number', 'Description_of_Material', 'UOM','Qty']
#                 PO_coulmns=['MRN_No', 'MRN_Date', 'Invoice_No', 'Invoice_Date', 'Invoice_Amount', 'MRN_Received_or_HO']
#                 sap=['SAP_PR', 'Site_PR_no', 'Closure_Performance', 'Mail_received_date']
#                 c_and_p_columns = ['C_P_Received_Date', 'C_P_Received_by','PR_or_WR_Open_or_IssuedDate', 'Pending_P_R_Age','P_R_Process_Status','PO_WO_Number', 'PO_WO_Dater', 'Vendor_Name', 'PO_WO_Amount', 'PO_WO_Open_Closed', 'Lead_Time_from_PR_to_PO',
#                                   'Delivery_Date_as_per_PO_WO', 'PO_WO_Status', 'P_I_Amount', 'Invoice_Sent_to_Account_Date']
#                 approvals_columns = ['SBU_Head', 'Dy_COO', 'COO', 'MAN']
#                 treasury_coulmns = ['Payment_Status', 'Payment_to_Vendor_Date']
#                 Q_and_D_coulmns =['Site_Certification', 'QSD_Entry_Date', 'QSD_Certified_Date']
#                 user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name, IS_ACTIVE=True).values())
#                 data={}
#                 main_columns=site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+Q_and_D_coulmns+sap+PO_coulmns
#                 with_sap=site_colums+sap
#                 with_supply=site_colums+PO_coulmns+sap
#                 for j in main_columns+['Cluster']:
#                     data[j]='no'
#                 if site.lower() in user_role[0]['ROLE'].lower():
#                     if 'SAP' == SAP_status and '' == Indent_type :
#                         print('1')
#                         for i in with_sap:
#                             data[i]='yes'
#                     elif 'SAP'==SAP_status and 'Supply' == Indent_type :
#                         for i in with_supply:
#                             data[i]='yes'
#                     elif 'Non SAP' in SAP_status and 'Supply'== Indent_type :
#                         for i in site_colums+PO_coulmns:
#                             data[i]='yes'
#                     else:
#                         for i in site_colums:
#                             data[i]='yes'
#
#                 elif approvals.lower() in user_role[0]['ROLE'].lower():
#                     for i in approvals_columns:
#                         data[i] = 'yes'
#                 elif c_p.lower() in user_role[0]['ROLE'].lower():
#                     for i in c_and_p_columns:
#                         data[i] = 'yes'
#                 elif w_o.lower() in user_role[0]['ROLE'].lower():
#                     if 'Service' in Indent_type:
#                         for i in Q_and_D_coulmns:
#                             data[i] = 'yes'
#                     else:
#                         return JsonResponse({'message':'Indent type is not Service' ,'success': 1})
#                 elif treasury.lower() in user_role[0]['ROLE'].lower():
#                     for i in treasury_coulmns:
#                         data[i] = 'yes'
#                 return JsonResponse({'data': data ,'success': 1})
#
#
#
#             else:
#                 return JsonResponse(response_dict)
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             print(type(e))  # the exception instance
#             print(e.args)  # arguments stored in .args
#             print(e)
#             return JsonResponse({'message': 'Error in data insertion', 'success': 0})
#
# # return JsonResponse({'message': "nothing", 'success': 2})
#     else:
#         return JsonResponse({'message': "Method not allowed", 'success': 2})
# @csrf_exempt
# def enable_disable(request):
#     if request.method == 'POST':
#         form_data = json.loads(request.body)
#         response = validation(request)
#         try:
#             try:
#                 response_data = response.content
#                 response_data = response_data.decode('utf-8')
#             except:
#                 return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
#             response_dict = ast.literal_eval(response_data)
#             if 'username' in response_dict.keys():
#                 user_name = response_dict['username']
#                 SAP_status=form_data['SAP_status']
#                 Indent_type=form_data['Indent_type']
#
#                 site = 'L4-Executive Lead'
#                 approvals = 'admin'
#                 c_p = 'L2-Cluster Lead'
#                 treasury = 'L1-HO Lead'
#                 w_o = 'L3-Site Lead'
#                 site_colums = ['date', 'Site_Name','SAP_status', 'Indent_Type_WR_or_PR', 'Raised_by', 'Indent_Date', ' Material_required_Date','Site_Requisition_Ref_No',
#                                'Nature_of_Requirement', 'Description_of_Material', 'UOM','Qty']
#                 PO_coulmns=['MRN_No', 'MRN_Date', 'Invoice_No', 'Invoice_Date', 'Invoice_Amount', 'MRN_Received_or_HO']
#                 sap=['SAP_PR', 'Site_PR_no', 'Closure_Performance', 'Mail_received_date']
#                 c_and_p_columns = ['C_P_Received_Date', 'C_P_Received_by','PR_or_WR_Open_or_IssuedDate', 'Pending_P_R_Age','P_R_Process_Status','PO_WO_Number', 'PO_WO_Dater', 'Vendor_Name', 'PO_WO_Amount', 'PO_WO_Open_Closed', 'Lead_Time_from_PR_to_PO',
#                                   'Delivery_Date_as_per_PO_WO', 'PO_WO_Status', 'P_I_Amount', 'Invoice_Sent_to_Account_Date']
#                 approvals_columns = ['SBU_Head', 'Dy_COO', 'COO', 'MAN']
#                 treasury_coulmns = ['Payment_Status', 'Payment_to_Vendor_Date']
#                 Q_and_D_coulmns =['Site_Certification', 'QSD_Entry_Date', 'QSD_Certified_Date']
#                 user_role = list(userinfo.objects.using('SSO').filter(USERNAME=user_name, IS_ACTIVE=True).values())
#                 data={}
#                 main_columns=site_colums+c_and_p_columns+approvals_columns+treasury_coulmns+Q_and_D_coulmns+sap+PO_coulmns
#                 with_sap=site_colums+sap
#                 with_supply=site_colums+PO_coulmns+sap
#                 for j in main_columns+['Cluster']:
#                     data[j]='no'
#                 if site.lower() in user_role[0]['ROLE'].lower():
#                     if 'SAP' == SAP_status and '' == Indent_type :
#                         print('1')
#                         for i in with_sap:
#                             data[i]='yes'
#                     elif 'SAP'==SAP_status and 'Supply' == Indent_type :
#                         for i in with_supply:
#                             data[i]='yes'
#                     elif 'Non SAP' in SAP_status and 'Supply'== Indent_type :
#                         for i in site_colums+PO_coulmns:
#                             data[i]='yes'
#                     else:
#                         for i in site_colums:
#                             data[i]='yes'
#
#                 elif approvals.lower() in user_role[0]['ROLE'].lower():
#                     for i in approvals_columns:
#                         data[i] = 'yes'
#                 elif c_p.lower() in user_role[0]['ROLE'].lower():
#                     for i in c_and_p_columns:
#                         data[i] = 'yes'
#                 elif w_o.lower() in user_role[0]['ROLE'].lower():
#                     if 'Service' in Indent_type:
#                         for i in Q_and_D_coulmns:
#                             data[i] = 'yes'
#                     else:
#                         return JsonResponse({'message':'Indent type is not Service' ,'success': 1})
#                 elif treasury.lower() in user_role[0]['ROLE'].lower():
#                     for i in treasury_coulmns:
#                         data[i] = 'yes'
#                 return JsonResponse({'data': data ,'success': 1})
#
#
#
#             else:
#                 return JsonResponse(response_dict)
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             print(type(e))  # the exception instance
#             print(e.args)  # arguments stored in .args
#             print(e)
#             return JsonResponse({'message': 'Error in data insertion', 'success': 0})
#
# # return JsonResponse({'message': "nothing", 'success': 2})
#     else:
#         return JsonResponse({'message': "Method not allowed", 'success': 2})

@csrf_exempt
def application_list(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
                app_origin = request.GET['app_name']
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    username = response_dict['username']

                    apps_list = list(userinfo.objects.using('SSO').filter(USERNAME=username,IS_ACTIVE=True).values())
                    project_details = []

                    for obj in apps_list:
                        appurl = obj['APP_URL']

                        details = list(Appinfo.objects.using('SSO').filter(APP_URL=appurl).values())
                        print('details::\t',details)
                        app_url = details[0]['APP_URL']
                        app_name = details[0]['APP_NAME']
                        if app_origin != app_name:
                            project_details.append({'app_name': app_name, 'app_url': app_url})
                        unique = {each['app_name']: each for each in project_details}.values()

                    if len(project_details)!=0:
                        return JsonResponse({'details': list(unique), 'success': 1})
                    else:
                        return JsonResponse({ 'success': 0,'message':'No other projects assigned'})
                except:
                    return JsonResponse({ 'success': 0,'message':'No other projects assigned'})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def approval_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(approval_drop_down.objects.filter().values('approval_data'))
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in data insertion', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def log_data_retrival(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(logdata.objects.filter().values())
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def SAP_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(SAP_drop_down.objects.filter().values('SAP_drop_data'))
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def PO_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(PO_Open_close_Drop_Down.objects.filter().values('PO_Open_close_drop_data'))
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def C_P_Received_by_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(C_P_Received_By_Drop_Down.objects.filter().values('C_P_Received_By_drop_data'))

                    return JsonResponse({ 'success': 1,'data':sorted(site_entry_data_r, key=lambda i: i['C_P_Received_By_drop_data'])})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def Indent_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(Indent_drop_down.objects.filter().values('Indent_drop_data'))
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def Requirement_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(Nature_of_Requirement_Drop_Down.objects.filter().values('Nature_of_Requirement_drop_data'))
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def Business_type_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    Businesstype_Drop_Down = list(Business_type_Drop_Down.objects.filter().values('Business_type_drop_data'))
                    return JsonResponse({ 'success': 1,'data':Businesstype_Drop_Down})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def yes_no_data_dropdown(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                print('response::\t',response)
                response_data = response.content
                response_data = response_data.decode('utf-8')
                print('response_data::\t',response_data)
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})

            response_dict = ast.literal_eval(response_data)
            print('keys::\t',response_dict.keys())
            if 'username' in response_dict.keys():
                try:
                    site_entry_data_r = list(yes_no_Drop_Down.objects.filter().values('yes_no_drop_data'))
                    return JsonResponse({ 'success': 1,'data':site_entry_data_r})
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(type(e))  # the exception instance
                    print(e.args)  # arguments stored in .args
                    print(e)
                    return JsonResponse({'message': 'Error in drop down', 'success': 0})

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response
    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

@csrf_exempt
def plants_drop_down(request):
    if request.method == 'GET':
        response = validation(request)
        try:
            try:
                response_data = response.content
                response_data = response_data.decode('utf-8')
            except:
                return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
            response_dict = ast.literal_eval(response_data)
            if 'username' in response_dict.keys():
                business_type = request.GET['business_type']
                if business_type.lower() == 'wind':
                    details = list(plantsDB.objects.using('SSO').filter(business_name='Wind').values('plant_name'))
                    print('wind details::\t', details)
                    plantdetails = []
                    for lis in details:
                        plantdetails.append({"Project": lis['plant_name']})

                    unique = {each['Project']: each for each in plantdetails}.values()
                    dataout = {"data": sorted(list(unique), key=lambda i: i['Project']), 'success': 1}

                    return JsonResponse(dataout)
                elif business_type.lower() == 'solar':
                    # details = list(solar_wind_plants.objects.using('Main_DGR').filter(type='SOLAR').values())
                    details=list(solar_plantsDB.objects.using('dgr').filter().all().values('PlantName'))
                    plantdetails = []
                    for lis in details:
                        plantdetails.append({"Project": lis['PlantName']})
                    unique = {each['Project']: each for each in plantdetails}.values()
                    dataout = {"data":  sorted(list(unique), key=lambda i: i['Project']), 'success': 1}

                    return JsonResponse(dataout)
                elif business_type.lower() == 'hydro':
                    details = list(hydro_plantsDB.objects.using('Main_DGR').filter().values())
                    plantdetails = []
                    for lis in details:
                        plantdetails.append({"Project": lis['code']})
                    unique = {each['Project']: each for each in plantdetails}.values()
                    dataout = {"data":  sorted(list(unique), key=lambda i: i['Project']), 'success': 1}

                    return JsonResponse(dataout)

                elif business_type.lower() == 'biomass':
                    # details = list(GAM_Wind_plant.objects.using('Main_DGR').filter().values())
                    # plantdetails = []
                    # for lis in details:
                    #     plantdetails.append({"Project": lis['project_name']})
                    dataout = {"data": [], 'success': 1}
                    return JsonResponse(dataout)

                # unique = {each['plant_name']: each for each in plant_names}.values()


        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        except jwt.DecodeError:
            return JsonResponse({'message': "INVALID_TOKEN", 'success': 2})
        return response

    else:
        return JsonResponse({'message': 'Method not allowed', 'success': 0})

def no_days(date):#in str
    if date is not None:
        datetimeFormat = '%Y-%m-%d%H:%M:%S.%f'
        k_split = date.split('T')
        k_s_split = k_split[1].split('Z')
        fianl1 = k_split[0] + k_s_split[0]

        # date2 = '2016-03-10'
        date_now = str(datetime.datetime.now())

        date_now_split = date_now.split(' ')

        fianl2 = date_now_split[0] + date_now_split[1]

        diff = datetime.datetime.strptime(fianl1, datetimeFormat) \
               - datetime.datetime.strptime(fianl2, datetimeFormat)
        return diff.days
    else:
        return ''


#######################################without sso################################

@csrf_exempt
def dummy_insert(request):
    if request.method == 'GET':
        try:
            list1=['Trinadh KNVN','Pavani','GKBV Kumar','Prasad KTAS','Rajesh DN','Ram Prasad C','Murali','Azad','Zeba','Khaleel','Mounika','Arun','Bhanu Kumar','Sravan','Aruna','Rajashekar Reddy']
            # list1=['Yes','No']
            # form_data = json.loads(request.body)


                # user_role = list(userinfo.using('SSO').objects.filter(USERNAME=user_name, IS_ACTIVE=True).values())
                # print('.......,user_role......', user_role[0]['ROLE'])
                # # site entries  = l4
            for i in list1:
                approval_entry_data = C_P_Received_By_Drop_Down(C_P_Received_By_drop_data=i)
                approval_entry_data.save()
                # if 'L4-Executive Lead'.lower() in user_role[0]['ROLE'].lower():
            # Critical Spares/Commodities/engineering products/ Services

                # site_entry_data = prpo(date=form_data['date'])
                # site_entry_data.save()41
                # site_entry_data_r = list(prpo.objects.filter().values())
                # print('site_entry_data_r',site_entry_data_r)
                # print('site_entry_data_r', site_entry_data_r)

            return JsonResponse({'data': 'inserted', 'success': 1})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(type(e))  # the exception instance
            print(e.args)  # arguments stored in .args
            print(e)
            return JsonResponse({'message': 'Error in data insertion', 'success': 0})
    # return JsonResponse({'message': "nothing", 'success': 2})
    else:
        return JsonResponse({'message': "Method not allowed", 'success': 2})

