from django.urls import path
from . import views
from .views import CustomPasswordChangeView
from django.contrib.auth.views import LogoutView
app_name='admin' #Define namespace
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('request-password-reset/', views.request_password_reset, name='request-password-reset'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('logout/', LogoutView.as_view(next_page='admin:login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_listing, name='users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/add_user/', views.add_user, name='add_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('client/create_client_group/', views.create_client_group, name='create_client_group'),
    path('client/client_group_list/', views.list_client_groups, name='client_group_list'),
    path('client/update_client_group/<int:client_id>/', views.update_client_group, name='update_client_group'),
    path('client/delete_client_group/', views.delete_client_group, name='delete_client_group'),
    path('client/create_account/', views.create_account, name='create_account'),
    path('client/client_account_list/', views.client_account_list, name='client_account_list'),
    path('client/update_client_account/<int:account_number>/', views.update_client_account, name='update_client_account'),
    path('client/delete_client_account/', views.delete_client_account, name='delete_client_account'),
    path('client/create_client_contract/', views.create_client_contract, name='create_client_contract'),
    path('client/client_contract_list/', views.client_contract_list, name='client_contract_list'),
    path('client/update_client_contract/<int:contract_id>/', views.update_client_contract, name='update_client_contract'),
    path('client/delete_client_contract/', views.delete_client_contract, name='delete_client_contract'),
    path('contracts/create_deal/', views.create_deal, name='create_deal'),
    path('contracts/deals/', views.deals_list, name='deals'),
    path('contracts/update_deal/<int:deal_id>/', views.update_deal, name='update_deal'),
    path('contracts/delete_deal/', views.delete_deal, name='delete_deal'),
    path('contracts/deal_contract_list/', views.deal_contract_list, name='deal_contract_list'),
    path('contracts/delete_deal_contract/', views.delete_deal_contract, name='delete_deal_contract'),
    path('contracts/create_deal_contract/', views.create_deal_contract, name='create_deal_contract'),
    path('contracts/update_deal_contract/<int:contract_id>/', views.update_deal_contract, name='update_deal_contract'),
    path('department/', views.department_list, name='department_list'),
    path('department/delete_department/', views.delete_department, name='delete_department'),
    path('department/create_department/', views.create_department, name='create_department'),
    path('department/update_department/<int:department_id>/', views.update_department, name='update_department'),
    path('employees/', views.employee_list, name='employees'),
    path('employees/delete_employee/', views.delete_employee, name='delete_employee'),
    path('employees/add_employee/', views.add_employee, name='add_employee'),
    path('employees/update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('employees/fetch_employees/', views.fetch_employees_by_department, name='fetch_employees'),
    path('employees/timesheets/', views.timesheet_list, name='timesheet_list'),
    path('employees/timesheets/create/', views.create_timesheet, name='create_timesheet'),
    path('employees/timesheets/update/<int:timesheet_id>/', views.update_timesheet, name='update_timesheet'),
    path('employees/timesheets/delete/', views.delete_timesheet, name='delete_timesheet'),
    path('supplier/skills/', views.skill_list, name='skill_list'),
    path('supplier/delete_skill/', views.delete_skill, name='delete_skill'),
    path('supplier/create_update_skill/', views.create_update_skill, name='create_skill'),
    path('supplier/create_update_skill/<int:skill_id>/', views.create_update_skill, name='update_skill'),
    path('supplier/', views.supplier_list, name='supplier_list'),
    path('supplier/delete_supplier/', views.delete_supplier, name='delete_supplier'),
    path('supplier/create_update_supplier/', views.create_update_supplier, name='create_supplier'),
    path('supplier/create_update_supplier/<int:supplier_id>/', views.create_update_supplier, name='update_supplier'),
    path('supplier/agent/', views.agent_list, name='agent_list'),
    path('supplier/delete_agent/', views.delete_agent, name='delete_agent'),
    path('supplier/create_update_agent/', views.create_update_agent, name='create_agent'),
    path('supplier/create_update_agent/<int:agent_id>/', views.create_update_agent, name='update_agent'),
    path('supplier/trades/', views.trades_list, name='trades_list'),
    path('supplier/delete_trades/', views.delete_trades, name='delete_trades'),
    path('supplier/create_update_trades/', views.create_update_trades, name='create_trades'),
    path('supplier/create_update_trades/<int:worker_id>/', views.create_update_trades, name='update_trades'),
    path('supplier/contractor_skills/', views.contractor_skill_list, name='contractor_skill_list'),
    path('supplier/delete_contractor_skill/', views.delete_contractor_skill, name='delete_contractor_skill'),
    path('supplier/create_update_contractor_skill/', views.create_update_contractor_skill, name='create_contractor_skill'),
    path('supplier/create_update_contractor_skill/<int:worker_id>/', views.create_update_contractor_skill, name='update_contractor_skill'),
    path('material_supplier/index/', views.material_supplier_list, name='material_supplier_list'),
    path('material_supplier/delete/', views.delete_material_supplier, name='delete_material_supplier'),
    path('material_supplier/create/', views.create_update_material_supplier, name='create_material_supplier'),
    path('material_supplier/update/<int:material_supplier_id>/', views.create_update_material_supplier, name='update_material_supplier'),
    path('material_supplier/store_branch/index/', views.store_branch_list, name='store_branch_list'),
    path('material_supplier/store_branch/delete/', views.delete_store_branch, name='delete_store_branch'),
    path('material_supplier/store_branch/create/', views.create_update_store_branch, name='create_store_branch'),
    path('material_supplier/store_branch/update/<int:store_id>/', views.create_update_store_branch, name='update_store_branch'),
    path('material_supplier/material_invoice/index/', views.material_invoice_list, name='material_invoice_list'),
    path('material_supplier/material_invoice/create/', views.create_material_invoice, name='create_material_invoice'),
    path('material_supplier/material_invoice/update/<int:material_invoice_id>/', views.update_material_invoice, name='update_material_invoice'),
    path('material_supplier/material_invoice/delete/', views.delete_material_invoice, name='delete_material_invoice'),
    path('generate_invoice_pdf/<int:invoice_id>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('operations/work_orders/index/', views.work_orders_list, name='work_orders_list'),
    path('operations/work_orders/create/', views.create_update_work_order, name='create_work_order'),
    path('operations/work_orders/update/<int:work_order_id>/', views.create_update_work_order, name='update_work_order'),
    path('operations/work_orders/delete/', views.delete_work_order, name='delete_work_order'),
    path('operations/job_orders/index/', views.job_orders_list, name='job_orders_list'),
    path('operations/job_orders/create/', views.create_update_job_order, name='create_job_order'),
    path('operations/job_orders/update/<int:job_order_id>/', views.create_update_job_order, name='update_job_order'),
    path('operations/job_orders/delete/', views.delete_job_order, name='delete_job_order'),path('operations/work_orders/index/', views.work_orders_list, name='work_orders_list'),
    path('operations/work_order_invoice/index/', views.work_order_invoice_list, name='work_order_invoice_list'),
    path('operations/work_order_invoice/create/', views.create_update_work_order_invoice, name='create_work_order_invoice'),
    path('operations/work_order_invoice/update/<int:id>/', views.create_update_work_order_invoice, name='update_work_order_invoice'),
    path('operations/work_order_invoice/delete/', views.delete_work_order_invoice, name='delete_work_order_invoice'),
    path('operations/job_order_invoice/index/', views.job_order_invoice_list, name='job_order_invoice_list'),
    path('operations/job_order_invoice/create/', views.create_update_job_order_invoice, name='create_job_order_invoice'),
    path('operations/job_order_invoice/update/<int:id>/', views.create_update_job_order_invoice, name='update_job_order_invoice'),
    path('operations/job_order_invoice/delete/', views.delete_job_order_invoice, name='delete_job_order_invoice'),
    path('operations/job_order_timesheet/index/', views.job_order_timesheet_list, name='job_order_timesheet_list'),
    path('operations/job_order_timesheet/create/', views.create_update_job_order_timesheet, name='create_job_order_timesheet'),
    path('operations/job_order_timesheet/update/<int:id>/', views.create_update_job_order_timesheet, name='update_job_order_timesheet'),
    path('operations/job_order_timesheet/delete/', views.delete_job_order_invoice, name='delete_job_order_timesheet'),
    path('employees/fetch_job_orders/', views.fetch_job_orders_by_workorder, name='fetch_job_orders'),
    path('finance/billing/', views.billing, name='billing'),
    path('finance/billing/create/', views.create_update_billing, name='create_billing'),
    path('finance/billing/update/<int:id>/', views.create_update_billing, name='update_billing'),
    path('finance/billing/delete/', views.delete_billing, name='delete_billing'),
    path('get-invoice-amounts/', views.get_invoice_amounts, name='get_invoice_amounts'),
]