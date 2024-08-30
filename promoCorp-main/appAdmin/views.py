from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import ClientGroup, Account, ClientContract, Deals, DealContract, Department, Employee, Timesheet, SupplierSkill, Supplier, SupplierAgent, SupplierTrades, SupplierContractorSkill, MaterialSupplier, StoresBranch, MaterialInvoice, MaterialInvoiceItems, WorkOrders, JobOrders, WorkOrderInvoice, JobOrderInvoice, JobOrderTimesheet, Billing
from .forms import LoginForm,CustomUserCreationForm,CustomPasswordResetForm,CustomPasswordChangeForm,CustomUserChangeForm,CustomUserAddEditForm,ClientGroupSearchForm,AccountForm, ClientGroupForm, ClientContractForm, DealForm, DealContractForm, DepartmentForm, EmployeeForm,TimesheetForm,SupplierSkillForm, SupplierForm, SupplierAgentForm, SupplierTradesForm, SupplierContractorSkillForm,MaterialSupplierForm, StoresBranchForm, MaterialInvoiceForm, MaterialInvoiceItemsFormSet, WorkOrdersForm, JobOrdersForm, WorkOrderInvoiceForm, JobOrderInvoiceForm, JobOrderTimesheetForm, BillingForm  # Import the form class
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy,reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from decimal import Decimal
def get_app_models():
    # This dictionary will hold apps and their models with URLs
    app_list = [
        {
            'app_label': "Dashboard",
            'label': 'Dashboard',
            'icon': 'tachometer-alt',
            'url': reverse(f'admin:dashboard')
        },
        {
            'app_label': "Users",
            'label': 'Users',
            'icon': 'user',
            'models': [{'label': 'Users', 'url': reverse(f'admin:users')}, {'label': 'Add User', 'url': reverse(f'admin:add_user')}]
        },
        {
            'app_label': "Clients",
            'label': 'Clients',
            'icon': 'industry',
            'models': [{'label': 'Client Groups', 'url': reverse(f'admin:client_group_list')}, {'label': 'Client Accounts', 'url': reverse(f'admin:client_account_list')}, {'label': 'Client Contracts', 'url': reverse(f'admin:client_contract_list')}]
        },
        {
            'app_label': "Contracts",
            'label': 'Contracts',
            'icon': 'file-contract',
            'models': [
                {'label': 'Deals', 'url': reverse(f'admin:deals')}, 
                {'label': 'Deal Contracts', 'url': reverse(f'admin:deal_contract_list')}
            ]
        },
        {
            'app_label': "Departments",
            'label': 'Departments',
            'icon': 'users',
            'models': [
                {'label': 'Departments', 'url': reverse(f'admin:department_list')},
                {'label': 'Employees', 'url': reverse(f'admin:employees')},
                {'label': 'Timesheet', 'url': reverse(f'admin:timesheet_list')}
            ]
        },
        {
            'app_label': "Supplier",
            'label': 'Supplier',
            'icon': 'warehouse',
            'models': [
                {'label': 'Skills', 'url': reverse(f'admin:skill_list')},
                {'label': 'Suppliers', 'url': reverse(f'admin:supplier_list')},
                {'label': 'Agents', 'url': reverse(f'admin:agent_list')},
                {'label': 'Trades', 'url': reverse(f'admin:trades_list')},
                {'label': 'Contractor Skills', 'url': reverse(f'admin:contractor_skill_list')}
            ]
        },
        {
            'app_label': "Operations",
            'label': 'Operations',
            'icon': 'cogs',
            'models': [
                {'label': 'Work Orders', 'url': reverse(f'admin:work_orders_list')},
                {'label': 'Work Order Invoice', 'url': reverse(f'admin:work_order_invoice_list')},
                {'label': 'Job Orders', 'url': reverse(f'admin:job_orders_list')},
                {'label': 'Job Order Invoice', 'url': reverse(f'admin:job_order_invoice_list')},
                {'label': 'Timesheet', 'url': reverse(f'admin:job_order_timesheet_list')}
            ]
        },
        {
            'app_label': "Material",
            'label': 'Material',
            'icon': 'cubes',
            'models': [
                {'label': 'Material Supplier', 'url': reverse(f'admin:material_supplier_list')},
                {'label': 'Stores - Branch Names', 'url': reverse(f'admin:store_branch_list')},
                {'label': 'Material Invoices', 'url': reverse(f'admin:material_invoice_list')}
            ]
        },
        {
            'app_label': "Finance",
            'label': 'Finance',
            'icon': 'money-bill',
            'models': [
                {'label': 'Billing', 'url': reverse(f'admin:billing')}
            ]
        }
    ]
    return app_list
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin:users')
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin:users')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('admin:users')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('admin:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def request_password_reset(request):
    # Create an instance of the PasswordResetForm
    form = CustomPasswordResetForm(request.POST or None)

    # Check if the form is valid
    if request.method == 'POST' and form.is_valid():
        # Get the list of email addresses from the form
        email = form.cleaned_data.get('email')
        # Try to get the user by email
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        # If the user exists, send password reset email
        if user:
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name='registration/password_reset_email.html'
            )
            # Optionally, redirect to a 'password reset done' page
            messages.success(request, 'Please check your email.')
            return redirect('admin:login')
    
    # Render the password reset request form
    return render(request, 'accounts/password_reset_request.html', {'form': form})
@login_required
def dashboard(request):
    app_list = get_app_models()
    user_count = User.objects.count()
    client_count = ClientGroup.objects.count()
    contract_count = Deals.objects.count()
    department_count = Department.objects.count()
    employee_count = Employee.objects.count()
    supplier_count = Supplier.objects.count()
    material_count = MaterialSupplier.objects.count()
    return render(request, 'dashboard.html', {'app_list': app_list, 'user_count': user_count, 'client_count': client_count, 'contract_count': contract_count, 'department_count': department_count, 'employee_count': employee_count, 'supplier_count': supplier_count,'material_count': material_count})
@login_required
def user_listing(request):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    app_list = get_app_models()
    User = get_user_model()  # Get the custom user model
    users = User.objects.all()  # Query to get all users
    return render(request, 'accounts/users.html', {'app_list': app_list, 'users': users, 'app_label':'Users'})

def add_user(request):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    app_list = get_app_models()
    if request.method == 'POST':
        form = CustomUserAddEditForm(request.POST)
        if request.POST["user_type"] == 1:
            form.instance.is_superuser = 1
        elif request.POST["user_type"] == 2:
            form.instance.is_staff =  1
        else:
            form.instance.is_superuser = 0
            form.instance.is_superuser = 0
        if form.is_valid():
            if request.POST["user_type"] == '1':
                form.instance.is_superuser = True
            elif request.POST["user_type"] == '2':
                form.instance.is_staff =  True
            else:
                form.instance.is_superuser = False
                form.instance.is_superuser = False
            form.save()
            messages.success(request, 'User has been created successfully.')
            return redirect('admin:users')
    else:
        form = CustomUserAddEditForm()
    
    context = {
        'app_list': app_list,
        'form': form, 'app_label':'Users'
    }
    return render(request, 'accounts/add_user.html', context)
def edit_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    app_list = get_app_models()
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            if request.POST["user_type"] == '1':
                form.instance.is_superuser = True
            elif request.POST["user_type"] == '2':
                form.instance.is_staff =  True
            else:
                form.instance.is_superuser = False
                form.instance.is_superuser = False
            form.save()
            messages.success(request, 'User has been updated successfully.')
            return redirect('admin:users')
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
        'app_list': app_list,
    }
    return render(request, 'accounts/edit_user.html', context)

def delete_user_view(request, user_id):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect(reverse('admin:users'))

    return render(request, 'adminlte/confirm_delete_user.html', {'user': user})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'  # Specify the path to your custom HTML template
    success_url = reverse_lazy('password_change_done')  # Specify the URL to redirect to after a successful password change
# CLient DOmain Code Start
@login_required
def create_client_group(request):
    app_list = get_app_models()
    if request.method == 'POST':
        form = ClientGroupForm(request.POST)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            client_group = form.save(commit=False)
            client_group.added_by = user  # Set the added_by field to the logged-in user's ID
            client_group.save()
            return redirect('admin:client_group_list')  # Redirect to the list view
    else:
        form = ClientGroupForm()
    return render(request, 'clientgroups/create_client_group.html', {'form': form, 'app_list':app_list})
@login_required
def list_client_groups(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = ClientGroup.objects.select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(industry__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'clientgroups/list_client_groups.html', {'search_form': search_form,
        'client_groups': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def update_client_group(request, client_id):
    app_list = get_app_models()
    client_group = ClientGroup.objects.get(pk=client_id)
    if request.method == 'POST':
        form = ClientGroupForm(request.POST, instance=client_group)
        if form.is_valid():
            form.save()
            return redirect('admin:client_group_list')
    else:
        form = ClientGroupForm(instance=client_group)
    return render(request, 'clientgroups/update_client_group.html', {'form': form, 'app_list':app_list})
@login_required
def delete_client_group(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client_group = get_object_or_404(ClientGroup, clientID=client_id)
        client_group.delete()
        # Add a success message
        messages.success(request, 'Client group was successfully deleted.')
        return redirect('admin:client_group_list')
@login_required
def client_account_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = Account.objects.select_related('added_by').select_related('clientID').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(account_number__icontains=search_query) |
            Q(account_name__icontains=search_query) |
            Q(account_role__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(abn__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'clientgroups/list_client_accounts.html', {'search_form': search_form,
        'client_accounts': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_account(request):
    app_list = get_app_models()
    clientgroups = ClientGroup.objects.all()
    if request.method == 'POST':
        form = AccountForm(request.POST)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            client_group = form.save(commit=False)
            client_group.added_by = user  # Set the added_by field to the logged-in user's ID
            client_group.save()
            return redirect('admin:client_account_list')  # Redirect to the list view
    else:
        form = AccountForm()
    return render(request, 'clientgroups/create_client_account.html', {'form': form, 'app_list':app_list, 'clientgroups':clientgroups})
@login_required
def update_client_account(request,account_number):
    app_list = get_app_models()
    clientgroups = ClientGroup.objects.all()
    client_account = Account.objects.get(pk=account_number)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=client_account)
        if form.is_valid():
            form.save()
            return redirect('admin:client_account_list')  # Redirect to the list view
    else:
        form = AccountForm(instance=client_account)
    return render(request, 'clientgroups/create_client_account.html', {'form': form, 'app_list':app_list, 'clientgroups':clientgroups, 'account_number': account_number})
@login_required
def delete_client_account(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        client_account = get_object_or_404(Account, account_number=account_number)
        client_account.delete()
        # Add a success message
        messages.success(request, 'Client account was successfully deleted.')
        return redirect('admin:client_account_list')
# Client Contract Domain CRUD COde Start here
@login_required
def client_contract_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = ClientContract.objects.select_related('added_by').select_related('account_number').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(account_number__account_name__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'clientgroups/list_client_contracts.html', {'search_form': search_form,
        'client_contracts': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_client_contract(request):
    if request.method == 'POST':
        contract_id = request.POST.get('contract_id')
        client_contract = get_object_or_404(ClientContract, contract_id=contract_id)
        client_contract.delete()
        # Add a success message
        messages.success(request, 'Client contract was successfully deleted.')
        return redirect('admin:client_contract_list')
@login_required
def create_client_contract(request):
    app_list = get_app_models()
    clientaccounts = Account.objects.all()
    if request.method == 'POST':
        form = ClientContractForm(request.POST)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            client_group = form.save()
            return redirect('admin:client_contract_list')  # Redirect to the list view
    else:
        form = ClientContractForm()
    return render(request, 'clientgroups/create_client_contract.html', {'form': form, 'app_list':app_list, 'clientaccounts':clientaccounts})
@login_required
def update_client_contract(request,contract_id):
    app_list = get_app_models()
    clientaccounts = Account.objects.all()
    client_contract = ClientContract.objects.get(pk=contract_id)
    if request.method == 'POST':
        form = ClientContractForm(request.POST, instance=client_contract)
        if form.is_valid():
            form.save()
            return redirect('admin:client_contract_list')  # Redirect to the list view
    else:
        form = ClientContractForm(instance=client_contract)
    return render(request, 'clientgroups/create_client_contract.html', {'form': form, 'app_list':app_list, 'clientaccounts':clientaccounts, 'contract_id': contract_id})
# end code client domain
# Start Contract Domain Code Here
def deals_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = Deals.objects.select_related('added_by').select_related('account_number').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(account_number__account_name__icontains=search_query) |
            Q(deal_name__icontains=search_query) |
            Q(pricing__icontains=search_query) |
            Q(duration__icontains=search_query) |
            Q(sla__icontains=search_query) |
            Q(deal_status__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'contracts/deals.html', {'search_form': search_form,
        'deals': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_deal(request):
    if request.method == 'POST':
        deal_id = request.POST.get('deal_id')
        deal = get_object_or_404(Deals, deal_id=deal_id)
        deal.delete()
        # Add a success message
        messages.success(request, 'Deal was successfully deleted.')
        return redirect('admin:deals')
@login_required
def create_deal(request):
    app_list = get_app_models()
    if request.method == 'POST':
        form = DealForm(request.POST)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            client_group = form.save()
            return redirect('admin:deals')  # Redirect to the list view
    else:
        form = DealForm()
    return render(request, 'contracts/create_deal.html', {'form': form, 'app_list':app_list})
@login_required
def update_deal(request,deal_id):
    app_list = get_app_models()
    deals = Deals.objects.get(pk=deal_id)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deals)
        if form.is_valid():
            form.save()
            return redirect('admin:deals')  # Redirect to the list view
    else:
        form = DealForm(instance=deals)
    return render(request, 'contracts/create_deal.html', {'form': form, 'app_list':app_list, 'deal_id': deal_id})
# Start Contract Domain Code Here
def deal_contract_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = DealContract.objects.select_related('added_by').select_related('deal_id').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(deal_id__deal_name__icontains=search_query) |
            Q(contract_type__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'contracts/deal_contract_list.html', {'search_form': search_form,
        'deal_contracts': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_deal_contract(request):
    if request.method == 'POST':
        contract_id = request.POST.get('contract_id')
        deal = get_object_or_404(DealContract, contract_id=contract_id)
        deal.delete()
        # Add a success message
        messages.success(request, 'Deal was successfully deleted.')
        return redirect('admin:deals')
@login_required
def create_deal_contract(request):
    app_list = get_app_models()
    if request.method == 'POST':
        form = DealContractForm(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        print(request.FILES)
        if form.is_valid():
            client_group = form.save()
            return redirect('admin:deal_contract_list')  # Redirect to the list view
    else:
        form = DealContractForm()
    return render(request, 'contracts/create_update_deal_contract.html', {'form': form, 'app_list':app_list})
@login_required
def update_deal_contract(request,contract_id):
    app_list = get_app_models()
    dealcontract = DealContract.objects.get(pk=contract_id)
    if request.method == 'POST':
        form = DealContractForm(request.POST, request.FILES, instance=dealcontract)
        if form.is_valid():
            form.save()
            return redirect('admin:deal_contract_list')  # Redirect to the list view
    else:
        form = DealContractForm(instance=dealcontract)
    return render(request, 'contracts/create_update_deal_contract.html', {'form': form, 'app_list':app_list, 'contract_id': contract_id})
# end Contract domain code here
#Start Department Domain Code here
@login_required
def department_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = Department.objects.select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(department_id__icontains=search_query) |
            Q(department_name__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'departments/department_list.html', {'search_form': search_form,
        'departments': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_department(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        department = get_object_or_404(Department, department_id=department_id)
        department.delete()
        # Add a success message
        messages.success(request, 'Department was successfully deleted.')
        return redirect('admin:department_list')
@login_required
def create_department(request):
    app_list = get_app_models()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:department_list')  # Redirect to the list view
    else:
        form = DepartmentForm()
    return render(request, 'departments/create_update_department.html', {'form': form, 'app_list':app_list})
@login_required
def update_department(request,department_id):
    app_list = get_app_models()
    department = DealContract.objects.get(pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('admin:deal_contract_list')  # Redirect to the list view
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/create_update_department.html', {'form': form, 'app_list':app_list, 'department_id': department_id})
@login_required
def employee_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the Employee queryset
    queryset = Employee.objects.select_related('added_by').select_related('department_id').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(department_id__department_name__icontains=search_query) |
            Q(employee_name__icontains=search_query) |
            Q(employee_email__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'employee/employees.html', {'search_form': search_form,
        'employees': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = get_object_or_404(Employee, employee_id=employee_id)
        employee.delete()
        # Add a success message
        messages.success(request, 'Employee was successfully deleted.')
        return redirect('admin:employees')
@login_required
def add_employee(request):
    app_list = get_app_models()
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:employees')  # Redirect to the list view
    else:
        form = EmployeeForm()
    return render(request, 'employee/create_update_employee.html', {'form': form, 'app_list':app_list})
@login_required
def update_employee(request,employee_id):
    app_list = get_app_models()
    employee = Employee.objects.get(pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('admin:employees')  # Redirect to the list view
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee/create_update_employee.html', {'form': form, 'app_list':app_list, 'employee_id': employee_id})
@login_required
def fetch_employees_by_department(request):
    # Get the department_id from the request parameters
    department_id = request.GET.get('department_id')
    
    if department_id:
        # Query employees based on the department_id
        employees = Employee.objects.filter(department_id=department_id)
        
        # Create a list of dictionaries containing employee_id and employee_name
        employee_data = [{'id': emp.employee_id, 'name': emp.employee_name} for emp in employees]
        
        # Return the list as JSON response
        return JsonResponse({'employees': employee_data})
    
    # Return an empty response if no department_id is provided
    return JsonResponse({'employees': []})
@login_required
def timesheet_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the Employee queryset
    queryset = Timesheet.objects.select_related('added_by').select_related('department').select_related('employee').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(department__department_name__icontains=search_query) |
            Q(employee__icontains__employee_name=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'timesheet/timesheet.html', {'search_form': search_form,
        'timesheets': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_timesheet(request):
    app_list = get_app_models()
    if request.method == 'POST':
        print(request.POST)
        form = TimesheetForm(request.POST)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:timesheet_list')  # Redirect to the list view
    else:
        form = TimesheetForm()
    return render(request, 'timesheet/create_update_timesheet.html', {'form': form, 'app_list':app_list})
@login_required
def update_timesheet(request, timesheet_id):
    app_list = get_app_models()
    timesheet = get_object_or_404(Timesheet, pk=timesheet_id)
    if request.method == 'POST':
        form = TimesheetForm(request.POST, instance=timesheet)
        if form.is_valid():
            form.save()
            return redirect('admin:timesheet_list')
    else:
        form = TimesheetForm(instance=timesheet)
    return render(request, 'timesheet/create_update_timesheet.html', {'form': form, 'app_list':app_list, 'timesheet_id': timesheet_id})
@login_required
def delete_timesheet(request):
    timesheet_id = request.POST.get('timesheet_id')
    timesheet = get_object_or_404(Timesheet, timesheet_id=timesheet_id)
    timesheet.delete()
    # Add a success message
    messages.success(request, 'Timesheet was successfully deleted.')
    return redirect('admin:timesheet_list')
#end Department Code here
#Start Supplier Skill Code here
@login_required
def skill_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = SupplierSkill.objects.select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(skill_id__icontains=search_query) |
            Q(skill_name__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'suppliers/skill_list.html', {'search_form': search_form,
        'skills': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_skill(request):
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        skill = get_object_or_404(SupplierSkill, skill_id=skill_id)
        skill.delete()
        # Add a success message
        messages.success(request, 'Skill was successfully deleted.')
        return redirect('admin:skill_list')
@login_required
def create_update_skill(request, skill_id=None):
    app_list = get_app_models()
    if skill_id:
        skill = get_object_or_404(SupplierSkill, pk=skill_id)
    else:
        skill = None
    if request.method == 'POST':
        form = SupplierSkillForm(request.POST,instance=skill)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:skill_list')  # Redirect to the list view
    else:
        form = SupplierSkillForm(instance=skill)
    return render(request, 'suppliers/create_update_skills.html', {'form': form, 'app_list':app_list})
# Create Supplier Code Start Here
@login_required
def supplier_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = Supplier.objects.select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(supplier_id__icontains=search_query) |
            Q(external_reference__icontains=search_query) |
            Q(registration_number__icontains=search_query) |
            Q(business_name__icontains=search_query) |
            Q(business_address__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'suppliers/supplier_list.html', {'search_form': search_form,
        'suppliers': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_supplier(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
        supplier.delete()
        # Add a success message
        messages.success(request, 'Supplier was successfully deleted.')
        return redirect('admin:supplier_list')
@login_required
def create_update_supplier(request, supplier_id=None):
    app_list = get_app_models()
    if supplier_id:
        supplier = get_object_or_404(Supplier, pk=supplier_id)
    else:
        supplier = None
    if request.method == 'POST':
        form = SupplierForm(request.POST,instance=supplier)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:supplier_list')  # Redirect to the list view
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/create_update_supplier.html', {'form': form, 'app_list':app_list})
#Create Supplier Agent Code here
@login_required
def agent_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = SupplierAgent.objects.select_related('added_by').select_related('supplier_id').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(supplier_id__icontains__business_name=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(contact__icontains=search_query) |
            Q(regions__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'suppliers/agent_list.html', {'search_form': search_form,
        'agents': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_agent(request):
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        agent = get_object_or_404(SupplierAgent, supplier_id=agent_id)
        agent.delete()
        # Add a success message
        messages.success(request, 'Supplier agent was successfully deleted.')
        return redirect('admin:agent_list')
@login_required
def create_update_agent(request, agent_id=None):
    app_list = get_app_models()
    if agent_id:
        agent = get_object_or_404(Supplier, pk=agent_id)
    else:
        agent = None
    if request.method == 'POST':
        form = SupplierAgentForm(request.POST,instance=agent)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:agent_list')  # Redirect to the list view
    else:
        form = SupplierAgentForm(instance=agent)
    return render(request, 'suppliers/create_update_agent.html', {'form': form, 'app_list':app_list})
#Create Supplier Trades Code here
@login_required
def trades_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = SupplierTrades.objects.select_related('added_by').select_related('agent_id').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(supplier_id__icontains__business_name=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(contact__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'suppliers/trades_list.html', {'search_form': search_form,
        'trades': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_trades(request):
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        trades = get_object_or_404(SupplierTrades, worker_id=worker_id)
        trades.delete()
        # Add a success message
        messages.success(request, 'Supplier Trades was successfully deleted.')
        return redirect('admin:trades_list')
@login_required
def create_update_trades(request, worker_id=None):
    app_list = get_app_models()
    if worker_id:
        trades = get_object_or_404(SupplierTrades, pk=worker_id)
    else:
        trades = None
    if request.method == 'POST':
        form = SupplierTradesForm(request.POST,instance=trades)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:trades_list')  # Redirect to the list view
    else:
        form = SupplierTradesForm(instance=trades)
    return render(request, 'suppliers/create_update_trades.html', {'form': form, 'app_list':app_list})
#Create Supplier Contractor Skill Code here
@login_required
def contractor_skill_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = SupplierContractorSkill.objects.select_related('added_by').select_related('worker_id').select_related('skill_id').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(skill_id__icontains__skill_name=search_query) |
            Q(rates__icontains=search_query) |
            Q(license_name__icontains=search_query) |
            Q(accreditation__icontains=search_query)|
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'suppliers/contractor_skill_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_contractor_skill(request):
    if request.method == 'POST':
        contractor_skill_id = request.POST.get('contractor_skill_id')
        contractor_skill = get_object_or_404(SupplierContractorSkill, contractor_skill_id=contractor_skill_id)
        contractor_skill.delete()
        # Add a success message
        messages.success(request, 'Contractor skill was successfully deleted.')
        return redirect('admin:contractor_skill_list')
@login_required
def create_update_contractor_skill(request, contractor_skill_id=None):
    app_list = get_app_models()
    if contractor_skill_id:
        contractor_skill = get_object_or_404(SupplierContractorSkill, pk=contractor_skill_id)
    else:
        contractor_skill = None
    if request.method == 'POST':
        form = SupplierContractorSkillForm(request.POST,instance=contractor_skill)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:contractor_skill_list')  # Redirect to the list view
    else:
        form = SupplierContractorSkillForm(instance=contractor_skill)
    return render(request, 'suppliers/create_update_contractor_skill.html', {'form': form, 'app_list':app_list})
#Material Domain Code Start Here
#Start Material Supplier Code here
@login_required
def material_supplier_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = MaterialSupplier.objects.select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(supplier_name__icontains=search_query) |
            Q(business_name__icontains=search_query) |
            Q(business_address__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(material_support_category__icontains=search_query)|
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'material_supplier/material_supplier_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_material_supplier(request):
    if request.method == 'POST':
        material_supplier_id = request.POST.get('id')
        material_supplier = get_object_or_404(MaterialSupplier, material_supplier_id=material_supplier_id)
        material_supplier.delete()
        # Add a success message
        messages.success(request, 'Material Supplier was successfully deleted.')
        return redirect('admin:material_supplier_list')
@login_required
def create_update_material_supplier(request, material_supplier_id=None):
    app_list = get_app_models()
    if material_supplier_id:
        material_supplier = get_object_or_404(MaterialSupplier, pk=material_supplier_id)
    else:
        material_supplier = None
    if request.method == 'POST':
        form = MaterialSupplierForm(request.POST,instance=material_supplier)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:material_supplier_list')  # Redirect to the list view
    else:
        form = MaterialSupplierForm(instance=material_supplier)
    return render(request, 'material_supplier/create_update_material_supplier.html', {'form': form, 'app_list':app_list})
#End Material Supplier Code here
#Start Material Supplier Code here
@login_required
def store_branch_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = StoresBranch.objects.select_related('material_supplier_id').select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(abn__icontains=search_query) |
            Q(branch_name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(branch_contact__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(region_of_operation__icontains=search_query)|
            Q(material_supplier_id__supplier_name__icontains=search_query)|
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'material_supplier/store_branch_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def delete_store_branch(request):
    if request.method == 'POST':
        store_id = request.POST.get('id')
        store_branch = get_object_or_404(StoresBranch, store_id=store_id)
        store_branch.delete()
        # Add a success message
        messages.success(request, 'Material Supplier was successfully deleted.')
        return redirect('admin:store_branch_list')
@login_required
def create_update_store_branch(request, store_id=None):
    app_list = get_app_models()
    if store_id:
        material_supplier = get_object_or_404(StoresBranch, pk=store_id)
    else:
        material_supplier = None
    if request.method == 'POST':
        form = StoresBranchForm(request.POST,instance=material_supplier)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:store_branch_list')  # Redirect to the list view
    else:
        form = StoresBranchForm(instance=material_supplier)
    return render(request, 'material_supplier/create_update_store_branch.html', {'form': form, 'app_list':app_list})
#End Material Supplier Code here
@login_required
def material_invoice_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = MaterialInvoice.objects.select_related('store_branch_id').select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(approver__icontains=search_query) |
            Q(store_branch_id__abn__icontains=search_query)|
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'material_supplier/material_invoice_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
def create_material_invoice(request):
    app_list = get_app_models()# Create an instance of the search form
    if request.method == 'POST':
        invoice_form = MaterialInvoiceForm(request.POST)
        items_formset = MaterialInvoiceItemsFormSet(request.POST)

        if invoice_form.is_valid() and items_formset.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.added_by = request.user  # Assuming the user is logged in
            
            # Calculate the total price from the items
            total_price = sum([form.cleaned_data.get('individual_price', 0)*form.cleaned_data.get('quantity', 0) for form in items_formset])
            invoice.total_price = total_price
            
            invoice.save()

            items_formset.instance = invoice
            items_formset.save()

            messages.success(request, 'Material Invoice created successfully.')
            return redirect('admin:material_invoice_list')  # Redirect to a list of invoices or another page

    else:
        invoice_form = MaterialInvoiceForm()
        items_formset = MaterialInvoiceItemsFormSet()

    return render(request, 'material_supplier/create_material_invoice.html', {
        'invoice_form': invoice_form,
        'items_formset': items_formset,
        'app_list': app_list
    })
def update_material_invoice(request, material_invoice_id):
    app_list = get_app_models()# Create an instance of the search form
    # Retrieve the existing MaterialInvoice instance
    material_invoice = get_object_or_404(MaterialInvoice, pk=material_invoice_id)

    if request.method == 'POST':
        invoice_form = MaterialInvoiceForm(request.POST, instance=material_invoice)
        items_formset = MaterialInvoiceItemsFormSet(request.POST, instance=material_invoice)

        if invoice_form.is_valid() and items_formset.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.added_by = request.user  # Assuming the user is logged in
            # Calculate the total price from the items
            total_price = sum([form.cleaned_data.get('individual_price', 0)*form.cleaned_data.get('quantity', 0) for form in items_formset])
            invoice.total_price = total_price
            invoice.save()

            items_formset.instance = invoice
            items_formset.save()

            messages.success(request, 'Material Invoice updated successfully.')
            return redirect('admin:material_invoice_list')  # Redirect to a list of invoices or another page

    else:
        invoice_form = MaterialInvoiceForm(instance=material_invoice)
        items_formset = MaterialInvoiceItemsFormSet(instance=material_invoice)

    return render(request, 'material_supplier/create_material_invoice.html', {
        'invoice_form': invoice_form,
        'items_formset': items_formset,
        'app_list': app_list
    })
def delete_material_invoice(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('id')
        material_invoice = get_object_or_404(MaterialInvoice, material_invoice_id=invoice_id)
        material_invoice.delete()
        # Add a success message
        messages.success(request, 'Material Invoice and its items deleted successfully.')
        return redirect('admin:material_invoice_list')
def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(MaterialInvoice, pk=invoice_id)
    items = MaterialInvoiceItems.objects.filter(material_invoice_id=invoice)

    html_string = render_to_string('material_invoice_pdf.html', {'invoice': invoice, 'items': items})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{invoice_id}.pdf'
    html.write_pdf(target=response)

    return response
#End Material Domain
@login_required
def work_orders_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = WorkOrders.objects.select_related('contract_id__deal_id').select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(supplier_list_id__icontains=search_query) |
            Q(work_order_type__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'operations/work_orders_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_update_work_order(request, work_order_id=None):
    app_list = get_app_models()
    if work_order_id:
        work_order = get_object_or_404(WorkOrders, pk=work_order_id)
    else:
        work_order = None
    if request.method == 'POST':
        form = WorkOrdersForm(request.POST,instance=work_order)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:work_orders_list')  # Redirect to the list view
    else:
        form = WorkOrdersForm(instance=work_order)
    return render(request, 'operations/create_update_work_orders.html', {'form': form, 'app_list':app_list})
@login_required
def delete_work_order(request):
    if request.method == 'POST':
        work_order_id = request.POST.get('id')
        work_order = get_object_or_404(WorkOrders, work_order_id=work_order_id)
        work_order.delete()
        # Add a success message
        messages.success(request, 'Work Order was successfully deleted.')
        return redirect('admin:work_orders_list')
@login_required
def job_orders_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = JobOrders.objects.select_related('work_order_id').select_related('assignee').select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(job_desc__icontains=search_query) |
            Q(job_type__icontains=search_query) | 
            Q(assignee__employee_name__icontains=search_query) |
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'operations/job_orders_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_update_job_order(request, job_order_id=None):
    app_list = get_app_models()
    if job_order_id:
        job_order = get_object_or_404(JobOrders, pk=job_order_id)
    else:
        job_order = None
    if request.method == 'POST':
        form = JobOrdersForm(request.POST,instance=job_order)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:job_orders_list')  # Redirect to the list view
    else:
        form = JobOrdersForm(instance=job_order)
    return render(request, 'operations/create_update_job_orders.html', {'form': form, 'app_list':app_list})
@login_required
def delete_job_order(request):
    if request.method == 'POST':
        job_order_id = request.POST.get('id')
        job_order = get_object_or_404(JobOrders, job_order_id=job_order_id)
        job_order.delete()
        # Add a success message
        messages.success(request, 'Job Order was successfully deleted.')
        return redirect('admin:job_orders_list')
@login_required
def work_order_invoice_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = WorkOrderInvoice.objects.select_related('work_order_id').select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(approval_status__icontains=search_query) |
            Q(amount__icontains=search_query) | 
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'operations/work_order_invoice_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_update_work_order_invoice(request, id=None):
    app_list = get_app_models()
    if id:
        instance = get_object_or_404(WorkOrderInvoice, pk=id)
    else:
        instance = None
    if request.method == 'POST':
        form = WorkOrderInvoiceForm(request.POST,instance=instance)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:work_order_invoice_list')  # Redirect to the list view
    else:
        form = WorkOrderInvoiceForm(instance=instance)
    return render(request, 'operations/create_update_work_order_invoice.html', {'form': form, 'app_list':app_list})
@login_required
def delete_work_order_invoice(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        object = get_object_or_404(WorkOrderInvoice, work_order_invoice_id=id)
        object.delete()
        # Add a success message
        messages.success(request, 'Work Order Invoice was successfully deleted.')
        return redirect('admin:work_order_invoice_list')
@login_required
def job_order_invoice_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the client group queryset
    queryset = JobOrderInvoice.objects.select_related('work_order_invoice_id').select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(work_order_invoice_id__icontains=search_query) |
            Q(total_amount__icontains=search_query) | 
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'operations/job_order_invoice_list.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_update_job_order_invoice(request, id=None):
    app_list = get_app_models()
    if id:
        instance = get_object_or_404(JobOrderInvoice, pk=id)
    else:
        instance = None
    if request.method == 'POST':
        form = JobOrderInvoiceForm(request.POST,instance=instance)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:job_order_invoice_list')  # Redirect to the list view
    else:
        form = JobOrderInvoiceForm(instance=instance)
    return render(request, 'operations/create_update_job_order_invoice.html', {'form': form, 'app_list':app_list})
@login_required
def delete_job_order_invoice(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        object = get_object_or_404(JobOrderInvoice, job_order_invoice_id=id)
        object.delete()
        # Add a success message
        messages.success(request, 'Job Order Invoice was successfully deleted.')
        return redirect('admin:job_order_invoice_list')
@login_required
def job_order_timesheet_list(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the Employee queryset
    queryset = JobOrderTimesheet.objects.select_related('added_by').select_related('job_order_id').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'operations/timesheet.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_update_job_order_timesheet(request, id=None):
    app_list = get_app_models()
    if id:
        instance = get_object_or_404(JobOrderTimesheet, pk=id)
    else:
        instance = None
    if request.method == 'POST':
        form = JobOrderTimesheetForm(request.POST,instance=instance)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:job_order_timesheet_list')  # Redirect to the list view
    else:
        form = JobOrderTimesheetForm(instance=instance)
    return render(request, 'operations/create_update_job_order_timesheet.html', {'form': form, 'app_list':app_list})
@login_required
def delete_job_order_timesheet(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        object = get_object_or_404(JobOrderTimesheet, job_id=id)
        object.delete()
        # Add a success message
        messages.success(request, 'Job timesheet was successfully deleted.')
        return redirect('admin:job_order_timesheet_list')
@login_required
def fetch_job_orders_by_workorder(request):
    # Get the department_id from the request parameters
    work_order_id = request.GET.get('work_order_id')
    
    if work_order_id:
        # Query employees based on the department_id
        joborders = JobOrders.objects.filter(work_order_id=work_order_id)
        
        # Create a list of dictionaries containing employee_id and employee_name
        job_order_data = [{'id': joborder.job_order_id, 'name': joborder.job_desc} for joborder in joborders]
        
        # Return the list as JSON response
        return JsonResponse({'joborders': job_order_data})
    
    # Return an empty response if no department_id is provided
    return JsonResponse({'joborders': []})
@login_required
def billing(request):
    app_list = get_app_models()# Create an instance of the search form
    search_form = ClientGroupSearchForm(request.GET)
    search_query = request.GET.get('search_query', '')
    sort_order = request.GET.get('sort_order', '-created_at')  # Default sort by created_at descending

    # Get the Employee queryset
    queryset = Billing.objects.select_related('added_by').all()

    # If there is a search query, filter the queryset based on the query
    if search_query:
        queryset = queryset.filter(
            Q(added_by__username__icontains=search_query)
        )
    # Sort the queryset based on the sort_order
    queryset = queryset.order_by(sort_order)
    return render(request, 'finance/billing.html', {'search_form': search_form,
        'dataset': queryset, 'sort_order': sort_order, 'app_list':app_list})
@login_required
def create_update_billing(request, id=None):
    app_list = get_app_models()
    if id:
        instance = get_object_or_404(Billing, pk=id)
    else:
        instance = None
    if request.method == 'POST':
        form = BillingForm(request.POST,instance=instance)
        user = User.objects.get(id=request.user.id)
        form.instance.added_by = user
        form.is_valid()
        if form.is_valid():
            form.save()
            return redirect('admin:billing')  # Redirect to the list view
    else:
        form = BillingForm(instance=instance)
    return render(request, 'finance/create_update_billing.html', {'form': form, 'app_list':app_list})
@login_required
def delete_billing(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        object = get_object_or_404(Billing, transaction_id=id)
        object.delete()
        # Add a success message
        messages.success(request, 'Billing was successfully deleted.')
        return redirect('admin:billing')
def get_invoice_amounts(request):
    work_order_invoice_id = request.GET.get('work_order_invoice_id')
    material_invoice_id = request.GET.get('material_invoice_id')

    data = {}

    if work_order_invoice_id:
        try:
            work_order_invoice = WorkOrderInvoice.objects.get(work_order_invoice_id=work_order_invoice_id)
            data['work_order_amount'] = str(work_order_invoice.total_amount)  # Convert Decimal to string
        except WorkOrderInvoice.DoesNotExist:
            data['work_order_amount'] = str(Decimal('0.00'))  # Use Decimal for consistency

    if material_invoice_id:
        try:
            material_invoice = MaterialInvoice.objects.get(material_invoice_id=material_invoice_id)
            data['material_invoice_amount'] = str(material_invoice.total_price)  # Convert Decimal to string
        except MaterialInvoice.DoesNotExist:
            data['material_invoice_amount'] = str(Decimal('0.00'))  # Use Decimal for consistency

    work_order_amount = Decimal(data.get('work_order_amount', '0.00'))
    material_invoice_amount = Decimal(data.get('material_invoice_amount', '0.00'))
    data['total_amount'] = str(work_order_amount + material_invoice_amount)  # Convert sum to string

    return JsonResponse(data)
#end Department Code here