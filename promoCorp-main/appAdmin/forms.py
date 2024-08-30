from django import forms
import re
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,AuthenticationForm,PasswordResetForm,PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import ClientGroup, ClientContract, Account, Deals, DealContract, Department, Employee, Timesheet, SupplierSkill, Supplier, SupplierAgent, SupplierTrades,SupplierContractorSkill, MaterialSupplier, StoresBranch, MaterialInvoice, MaterialInvoiceItems, WorkOrders, JobOrders, WorkOrderInvoice, JobOrderInvoice, JobOrderTimesheet, Billing
from django.core.validators import validate_email
from .validators import *
from django.forms import inlineformset_factory
class LoginForm(AuthenticationForm):
    # remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Remember me')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the 'form-control' class and placeholder to each field's widget
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define placeholder text for each field
        placeholder_texts = {
            'username': 'Enter your username',
            'email': 'Enter your email',
            'password1': 'Enter your password',
            'password2': 'Confirm your password'
        }
        
        # Add the 'form-control' class to each field's widget
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in placeholder_texts:
                field.widget.attrs['placeholder'] = placeholder_texts[field_name]

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the 'form-control' class and placeholder to each field's widget
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields or widgets here if needed
        # For example, add CSS classes to the form fields:
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Current password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm new password'})
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_active']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize each field's widget
        for field_name, field in self.fields.items():
            # Add the form-control class to each input
            field.widget.attrs.update({
                'class': 'form-control'
            })
            
            # Optionally add a placeholder if necessary
            # Customize placeholder text as needed
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Enter username'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'Enter email'
            # Add more fields and placeholder texts as needed
class CustomUserAddEditForm(UserCreationForm):
    User = get_user_model()
    first_name = forms.CharField(max_length=30, required=True, help_text='Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Enter your last name.')
    user_type = forms.CharField(max_length=30, required=True)
    is_superuser = forms.BooleanField(required=False, label='Superuser')
    is_staff = forms.BooleanField(required=False, label='Staff')
    is_active = forms.BooleanField(required=False, label='Status')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define placeholder text for each field
        placeholder_texts = {
            'first_name': 'Enter Firstname',
            'last_name': 'Enter Lastname',
            'username': 'Enter your username',
            'email': 'Enter your email',
            'password1': 'Enter your password',
            'password2': 'Confirm your password'
        }
        
        # Add the 'form-control' class to each field's widget
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in placeholder_texts:
                field.widget.attrs['placeholder'] = placeholder_texts[field_name]
class ClientGroupForm(forms.ModelForm):
    class Meta:
        model = ClientGroup
        fields = ['industry', 'company_name']
        widgets = {
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Industry', 'label': 'Industry'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name', 'label': 'Company Name'}),
        }
class ClientGroupSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=255, required=False)
class AccountForm(forms.ModelForm):
    clientID = forms.ModelChoiceField(
        queryset=ClientGroup.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'CLient Group'}),
        empty_label="Select Client Group",
        label='Client Group',
        required=True
    )

    class Meta:
        model = Account
        fields = ['clientID', 'account_name', 'account_role', 'location', 'abn']
        widgets = {
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Name', 'label': 'Account Name'}),
            'account_role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number', 'label': 'Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location', 'label': 'Location'}),
            'abn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ABN', 'label': 'Australia Business Number'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the account_number field
        self.fields['clientID'].label_from_instance = self.custom_label_from_instance

    def custom_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.industry} - {obj.company_name}"
class ClientContractForm(forms.ModelForm):
    account_number = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Account'}),
        empty_label="Select an account",
        label='Account Number',
        required=True
    )

    class Meta:
        model = ClientContract
        fields = ['account_number', 'name', 'phone_number', 'email', 'address', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name', 'label': 'Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number', 'label': 'Phone Number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email', 'label': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'label': 'Address'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Role', 'label': 'Role'}),
        }
class DealForm(forms.ModelForm):
    account_number = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Account'}),
        empty_label="Select an account",
        label='Account Number',
        required=True
    )
    # Define the choices for the status field
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('In-active', 'In-active')
    ]
    
    # Define a ChoiceField for the status field
    deal_status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,  # Specify if the field is required
        label='Status'  # The label to display for the field
    )

    class Meta:
        model = Deals
        fields = ['account_number', 'deal_name', 'pricing', 'duration', 'sla', 'deal_status']
        widgets = {
            'deal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Deal Name', 'label': 'Deal Name'}),
            'pricing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pricing', 'label': 'Pricing'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Duration', 'label': 'Duration'}),
            'sla': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SLAs', 'label': 'SLAs'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the account_number field
        self.fields['account_number'].label_from_instance = self.custom_label_from_instance

    def custom_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.account_number} - {obj.account_name}"
class DealContractForm(forms.ModelForm):
    deal_id = forms.ModelChoiceField(
        queryset=Deals.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Deal'}),
        empty_label="Select a Deal",
        label='Deal Name',
        required=True
    )
    class Meta:
        model = DealContract
        fields = ['deal_id', 'contract_type', 'start_date', 'end_date', 'contract_file']
        widgets = {
            'contract_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contract Type', 'label': 'Contract Type'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datetimepicker', 'placeholder': 'YYYY-MM-DD', 'label': 'Contract Start Date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datetimepicker', 'placeholder': 'YYYY-MM-DD', 'label': 'Contract End Date'}),
            # 'start_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Start Date', 'label': 'Contract Start Date'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the deal_id field
        self.fields['deal_id'].label_from_instance = self.custom_label_from_instance

    def custom_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.deal_name}"
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department', 'label': 'Department Name'})
        }
class EmployeeForm(forms.ModelForm):
    department_id = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Department'}),
        empty_label="Select Department",
        label='Department',
        required=True
    )
    class Meta:
        model = Employee
        fields = ['employee_name', 'employee_phone', 'employee_email', 'department_id', 'employee_pic']
        widgets = {
            'employee_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name', 'label': 'Name'}),
            'employee_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone', 'label': 'Phone Number'}),
            'employee_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email', 'label': 'Email Address'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the account_number field
        self.fields['department_id'].label_from_instance = self.custom_label_from_instance

    def custom_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.department_name}"
    def clean_contact(self):
        """Validate the contact field for Australian mobile phone number."""
        contact = self.cleaned_data['employee_phone']
        
        # Apply custom validation
        validate_australian_mobile_phone_number(contact)
        
        return contact
class TimesheetForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Department'}),
        empty_label="Select Department",
        label='Department',
        required=True
    )
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Employee'}),
        empty_label="Select Employee",
        label='Employee',
        required=True
    )
    class Meta:
        model = Timesheet
        fields = ['department', 'employee', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the account_number field
        self.fields['department'].label_from_instance = self.custom_department_label_from_instance
        self.fields['employee'].label_from_instance = self.custom_employee_label_from_instance

    def custom_department_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.department_name}"

    def custom_employee_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.employee_name}"
class SupplierSkillForm(forms.ModelForm):
    class Meta:
        model = SupplierSkill
        fields = ['skill_name']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Skill', 'label': 'Skill Name'})
        }
class SupplierForm(forms.ModelForm):
    # Define the choices for the status field
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'In-active')
    ]
    # Override the 'status' field to use a dropdown
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)
    class Meta:
        model = Supplier

        fields = ['registration_number', 'business_name', 'business_address', 'email', 'external_reference', 'industries', 'status']
        widgets = {
            'external_reference': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'industries': forms.TextInput(attrs={'class': 'form-control'})
        }
        # Override the __init__ method to assign the choices to the status field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.STATUS_CHOICES
        self.fields['status'].required = True
        self.fields['status'].label = 'Status'
        self.fields['status'].widget.attrs['class'] = 'form-control'
class SupplierAgentForm(forms.ModelForm):
    supplier_id = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Supplier'}),
        empty_label="Select Supplier",
        label='Supplier',
        required=True
    )
    class Meta:
        model = SupplierAgent

        fields = ['supplier_id', 'first_name', 'last_name', 'contact', 'regions']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'regions': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the account_number field
        self.fields['supplier_id'].label_from_instance = self.custom_supplier_label_from_instance

    def custom_supplier_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.business_name}"
    def clean_contact(self):
        """Validate the contact field for Australian mobile phone number."""
        contact = self.cleaned_data['contact']
        
        # Apply custom validation
        validate_australian_mobile_phone_number(contact)
        
        return contact
class SupplierTradesForm(forms.ModelForm):
    agent_id = forms.ModelChoiceField(
        queryset=SupplierAgent.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Supplier Agent'}),
        empty_label="Select Supplier Agent",
        label='Supplier Agent',
        required=True
    )
    class Meta:
        model = SupplierTrades

        fields = ['agent_id', 'first_name', 'last_name', 'contact', 'bank_name', 'account_holder_name', 'account_number', 'bsb', 'location']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bsb': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label text of the account_number field
        self.fields['agent_id'].label_from_instance = self.custom_supplier_agent_label_from_instance

    def custom_supplier_agent_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.first_name} {obj.last_name}"
    def clean_contact(self):
        """Validate the contact field for Australian mobile phone number."""
        contact = self.cleaned_data['contact']
        
        # Apply custom validation
        validate_australian_mobile_phone_number(contact)
        
        return contact
    def clean_account_number(self):
        """Validate the account_number field."""
        account_number = self.cleaned_data['account_number']
        
        # Apply custom validation
        validate_account_number(account_number)
        
        return account_number

    def clean_bsb(self):
        """Validate the bsb field."""
        bsb_number = self.cleaned_data['bsb']
        
        # Apply custom validation
        validate_bsb_number(bsb_number)
        
        return bsb_number
class SupplierContractorSkillForm(forms.ModelForm):
    worker_id = forms.ModelChoiceField(
        queryset=SupplierTrades.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Trades'}),
        empty_label="Select Trades(Contractor)",
        label='Trades(Contractor)',
        required=True
    )
    skill_id = forms.ModelChoiceField(
        queryset=SupplierSkill.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Skill'}),
        empty_label="Select Skill",
        label='Skill',
        required=True
    )
    # Define the choices for the status field
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'In-active')
    ]
    # Override the 'status' field to use a dropdown
    license_status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)
    class Meta:
        model = SupplierContractorSkill

        fields = ['worker_id', 'skill_id', 'rates', 'license_name', 'accreditation', 'license_status']
        widgets = {
            'rates': forms.TextInput(attrs={'class': 'form-control'}),
            'license_name': forms.TextInput(attrs={'class': 'form-control'}),
            'accreditation': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['license_status'].choices = self.STATUS_CHOICES
        self.fields['license_status'].required = True
        self.fields['license_status'].label = 'License Status'
        self.fields['license_status'].widget.attrs['class'] = 'form-control'
        
        # Customize the label text of the account_number field
        self.fields['worker_id'].label_from_instance = self.custom_supplier_trades_label_from_instance
        self.fields['skill_id'].label_from_instance = self.custom_supplier_skills_label_from_instance

    def custom_supplier_trades_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.first_name} {obj.last_name}"

    def custom_supplier_skills_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"{obj.skill_name}"
class MaterialSupplierForm(forms.ModelForm):
    class Meta:
        model = MaterialSupplier
        fields = ['supplier_name', 'business_name', 'business_address', 'phone', 'email', 'material_support_category']
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Supplier', 'label': 'Supplier Name'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Business Name', 'label': 'Business Name'}),
            'business_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Business Address', 'label': 'Business Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone', 'label': 'Phone - Support Queries'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email', 'label': 'Email - Support Queries'}),
            'material_support_category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category', 'label': 'Material Supply Category'}),
        }
    def clean_contact(self):
        """Validate the contact field for Australian mobile phone number."""
        phone = self.cleaned_data['phone']
        
        # Apply custom validation
        validate_australian_mobile_phone_number(phone)
        
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Enter a valid email address.')
        return email
class StoresBranchForm(forms.ModelForm):
    material_supplier_id = forms.ModelChoiceField(
        queryset=MaterialSupplier.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Material Supplier'}),
        empty_label="Select Material Supplier",
        label='Material Supplier',
        required=True
    )
    class Meta:
        model = StoresBranch
        fields = ['material_supplier_id', 'abn', 'branch_name', 'address', 'region_of_operation', 'branch_contact', 'phone', 'email']
        widgets = {
            'abn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ABN', 'label': 'ABN'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Branch Name', 'label': 'Branch Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'label': 'Address'}),
            'region_of_operation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Region of Operation', 'label': 'Region of Operation'}),
            'branch_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Branch Contact', 'label': 'Branch Contact'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone', 'label': 'Phone'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email', 'label': 'Email'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material_supplier_id'].label_from_instance = self.custom_material_suppliers_label_from_instance

    def custom_material_suppliers_label_from_instance(self, obj):
        return f"{obj.supplier_name}"
    def clean_contact(self):
        """Validate the contact field for Australian mobile phone number."""
        phone = self.cleaned_data['phone']
        
        # Apply custom validation
        validate_australian_mobile_phone_number(phone)
        
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Enter a valid email address.')
        return email
    def clean_abn(self):
        abn = self.cleaned_data['abn']
        validate_abn(abn)
        return abn
class MaterialInvoiceForm(forms.ModelForm):
    store_branch_id = forms.ModelChoiceField(
        queryset=StoresBranch.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'ABN'}),
        empty_label="Select ABN",
        label='ABN',
        required=True
    )
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',  # HTML5 datetime-local input
            'class': 'form-control',
            'placeholder': 'Select a date and time',
            'format': '%Y-%m-%dT%H:%M'  # Ensure the format matches the HTML5 input
        }),
        input_formats=['%Y-%m-%dT%H:%M']  # Expected input format
    )
    class Meta:
        model = MaterialInvoice
        fields = ['store_branch_id', 'total_price', 'approver', 'date_time']
        widgets = {
            'total_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Total Price', 'label': 'Total Price'}),
            'approver': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Approver', 'label': 'Approver'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store_branch_id'].label_from_instance = self.custom_abn_label_from_instance

    def custom_abn_label_from_instance(self, obj):
        return f"{obj.abn}"
class MaterialInvoiceItemsForm(forms.ModelForm):
    class Meta:
        model = MaterialInvoiceItems
        fields = ['items', 'quantity', 'individual_price']
        widgets = {
            'items': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Item', 'label': 'Items'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity', 'label': 'Quantity'}),
            'individual_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price', 'label': 'Individual Price'})
        }

MaterialInvoiceItemsFormSet = inlineformset_factory(
    MaterialInvoice,
    MaterialInvoiceItems,
    form=MaterialInvoiceItemsForm,
    extra=1,  # Number of extra forms to display
    can_delete=True, 
    # formset=BaseMaterialInvoiceFormSet
)

class WorkOrdersForm(forms.ModelForm):
    contract_id = forms.ModelChoiceField(
        queryset=DealContract.objects.select_related('deal_id').all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Deal'}),
        empty_label="Select a Deal",
        label='Deal Name',
        required=True
    )
    # Define the choices for the status field
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'In-active')
    ]
    # Override the 'status' field to use a dropdown
    work_order_status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)
    class Meta:
        model = WorkOrders
        fields = ['contract_id', 'supplier_list_id', 'work_order_type', 'work_order_status']
        widgets = {
            'supplier_list_id': forms.TextInput(attrs={'class': 'form-control'}),
            'work_order_type': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_order_status'].choices = self.STATUS_CHOICES
        self.fields['work_order_status'].required = True
        self.fields['work_order_status'].label = 'Work Order Status'
        self.fields['work_order_status'].widget.attrs['class'] = 'form-control'# Customize the label text of the account_number field
        self.fields['contract_id'].label_from_instance = self.custom_deal_contract_label_from_instance

    def custom_deal_contract_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.contract_id} - {obj.deal_id.deal_name}"

class JobOrdersForm(forms.ModelForm):
    assignee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Assignee'}),
        empty_label="Select Assignee",
        label='Assignee',
        required=True
    )
    work_order_id = forms.ModelChoiceField(
        queryset=WorkOrders.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Work Order'}),
        empty_label="Select Work Order",
        label='Work Order',
        required=True
    )
    # Define the choices for the status field
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'In-active')
    ]
    # Override the 'status' field to use a dropdown
    job_status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)
    class Meta:
        model = JobOrders
        fields = ['work_order_id', 'assignee', 'job_desc', 'job_type', 'job_status']
        widgets = {
            'job_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_status'].choices = self.STATUS_CHOICES
        self.fields['job_status'].required = True
        self.fields['job_status'].label = 'Job Status'
        self.fields['job_desc'].label = 'Job Description'
        self.fields['job_status'].widget.attrs['class'] = 'form-control'
        # Customize the label text of the account_number field
        self.fields['assignee'].label_from_instance = self.custom_assignee_label_from_instance
        self.fields['work_order_id'].label_from_instance = self.custom_work_order_label_from_instance

    def custom_assignee_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.employee_id} - {obj.employee_name}"
    def custom_work_order_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.supplier_list_id} - {obj.work_order_type}"
class WorkOrderInvoiceForm(forms.ModelForm):
    work_order_id = forms.ModelChoiceField(
        queryset=WorkOrders.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Work Order'}),
        empty_label="Select Work Order",
        label='Work Order',
        required=True
    )
    class Meta:
        model = WorkOrderInvoice
        fields = [
            'work_order_id',
            'total_amount',
            'approval_status'
        ]
        widgets = {
            'work_order_id': forms.Select(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['approval_status'].required = True
        self.fields['approval_status'].label = 'Approval Status'
        self.fields['approval_status'].label = 'Approval Status'
        self.fields['approval_status'].widget.attrs['class'] = 'form-control'
        self.fields['work_order_id'].label_from_instance = self.custom_work_order_label_from_instance
    def custom_work_order_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.supplier_list_id} - {obj.work_order_type}"
class JobOrderInvoiceForm(forms.ModelForm):
    work_order_invoice_id = forms.ModelChoiceField(
        queryset=WorkOrderInvoice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Work Order Invoice'}),
        empty_label="Select Work Order Invoice",
        label='Work Order Invoice',
        required=True
    )
    class Meta:
        model = JobOrderInvoice
        fields = [
            'work_order_invoice_id',
            'total_hours',
            'rates',
            'abn'
        ]
        widgets = {
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'rates': forms.NumberInput(attrs={'class': 'form-control'}),
            'abn': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_hours'].label = 'Total Hours'
        self.fields['abn'].label = 'ABN'
        self.fields['work_order_invoice_id'].label_from_instance = self.custom_work_order_invoice_label_from_instance
    def custom_work_order_invoice_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.work_order_invoice_id}"
    def clean_abn(self):
        abn = self.cleaned_data['abn']
        validate_abn(abn)
        return abn
class JobOrderTimesheetForm(forms.ModelForm):
    work_order_id = forms.ModelChoiceField(
        queryset=WorkOrders.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Work Order'}),
        empty_label="Select Work Order",
        label='Work Order',
        required=True
    )
    job_order_id = forms.ModelChoiceField(
        queryset=JobOrders.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Job'}),
        empty_label="Select Job",
        label='Job',
        required=True
    )
    class Meta:
        model = JobOrderTimesheet
        fields = ['work_order_id', 'job_order_id', 'date', 'start_time', 'end_time', 'approval_status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['approval_status'].required = True
        self.fields['approval_status'].label = 'Approval Status'
        self.fields['approval_status'].widget.attrs['class'] = 'form-control'
        
        # Customize the label text of the account_number field
        self.fields['job_order_id'].label_from_instance = self.job_label_from_instance
        self.fields['work_order_id'].label_from_instance = self.work_order_label_from_instance

    def job_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.job_order_id} - {obj.job_desc}"
    def work_order_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.supplier_list_id} - {obj.work_order_type}"
class BillingForm(forms.ModelForm):
    work_order_invoice_id = forms.ModelChoiceField(
        queryset=WorkOrderInvoice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Work Order Invoice'}),
        empty_label="Select Work Order",
        label='Work Order Invoice',
        required=True
    )
    material_invoice_id = forms.ModelChoiceField(
        queryset=MaterialInvoice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'label':'Material Invoice'}),
        empty_label="Select Material Invoice",
        label='Material Invoice ID',
        required=True
    )
    class Meta:
        model = Billing
        fields = ['work_order_invoice_id', 'material_invoice_id', 'work_order_amount', 'material_invoice_amount', 'total_amount']
        widgets = {
            'work_order_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'material_invoice_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_order_amount'].label = 'Work Order Amount'
        self.fields['material_invoice_amount'].label = 'Material Invoice Amount'
        self.fields['total_amount'].label = 'Total Amount'

        if self.instance and self.instance.pk:
            self.fields['work_order_amount'].initial = self.instance.work_order_invoice_id.total_amount
            self.fields['material_invoice_amount'].initial = self.instance.material_invoice_id.total_price
        
        # Customize the label text of the account_number field
        self.fields['material_invoice_id'].label_from_instance = self.material_label_from_instance
        self.fields['work_order_invoice_id'].label_from_instance = self.work_order_label_from_instance

    def material_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.material_invoice_id}"
    def work_order_label_from_instance(self, obj):
        """
        Customize the options text by combining two fields from the Account model.
        """
        # Combine the two fields you want to display as the options text
        return f"#{obj.work_order_invoice_id}"