from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from enum import Enum
class ClientGroup(models.Model):
    clientID = models.BigAutoField(primary_key=True)
    industry = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming added_by is just an integer field; you may need to adjust if it's a foreign key.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
    
class Account(models.Model):
    clientID = models.ForeignKey(ClientGroup, on_delete=models.CASCADE)
    account_number = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    account_name = models.CharField(max_length=255)
    account_role = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    abn = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE) # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} - {self.account_number}"
    
class ClientContract(models.Model):
    contract_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)  # Foreign key to Account model
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    role = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.account_number}"
class Deals(models.Model):
    deal_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)  # Foreign key to Account model
    deal_name = models.CharField(max_length=128)
    pricing = models.FloatField()
    duration = models.CharField(max_length=128)
    sla = models.CharField(max_length=128)
    deal_status = models.CharField(max_length=10)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class DealContract(models.Model):
    contract_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    deal_id = models.ForeignKey(Deals, on_delete=models.CASCADE)  # Foreign key to Account model
    contract_type = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, default=None)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contract_file = models.FileField(upload_to='contracts/', blank=True, null=True)  # FileField for file upload
class Department(models.Model):
    department_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    department_name = models.CharField(max_length=128)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Employee(models.Model):
    employee_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)  # Foreign key to Account model
    employee_name = models.CharField(max_length=128)
    employee_phone = models.CharField(max_length=128)
    employee_email = models.CharField(max_length=128)
    employee_pic = models.ImageField(upload_to='employee/', blank=True, null=True)  # FileField for file upload
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Timesheet(models.Model):
    # Foreign key to Department model
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    # Foreign key to Employee model
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    # Date as a field and part of the primary key
    date = models.DateField()

    # Start and end time fields
    start_time = models.TimeField()
    end_time = models.TimeField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Combine department, employee, and date to form a composite primary key
    class Meta:
        unique_together = ('department', 'employee', 'date')

    def __str__(self):
        return f"Timesheet for {self.employee.employee_name} on {self.date} in {self.department.department_name}"
class SupplierSkill(models.Model):
    skill_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    skill_name = models.CharField(max_length=128)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Supplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    external_reference = models.CharField(max_length=128)
    registration_number = models.CharField(max_length=128)
    business_name = models.CharField(max_length=128)
    business_address = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    status = models.BooleanField(default=1)
    industries = models.CharField(max_length=255, default='NULL')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class SupplierAgent(models.Model):
    agent_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    regions = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class SupplierTrades(models.Model):
    worker_id = models.BigAutoField(primary_key=True)
    # Foreign key to SupplierAgent model
    agent_id = models.ForeignKey(SupplierAgent, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    bank_name = models.CharField(max_length=128)
    account_holder_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    bsb = models.CharField(max_length=20)
    location=models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class SupplierContractorSkill(models.Model):
    contractor_skill_id = models.BigAutoField(primary_key=True)
    # Foreign key to SupplierTrades model
    worker_id = models.ForeignKey(SupplierTrades, on_delete=models.CASCADE)
    # Foreign key to SupplierSkill model
    skill_id = models.ForeignKey(SupplierSkill, on_delete=models.CASCADE)
    rates = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    license_name = models.CharField(max_length=128)
    license_status = models.BooleanField(default=1)
    accreditation = models.CharField(max_length=128)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class MaterialSupplier(models.Model):
    material_supplier_id = models.BigAutoField(primary_key=True)
    supplier_name = models.CharField(max_length=128)
    business_name = models.CharField(max_length=128)
    business_address = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    material_support_category = models.CharField(max_length=128)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class StoresBranch(models.Model):
    store_id = models.BigAutoField(primary_key=True)
    abn = models.CharField(max_length=50, unique=True)
    branch_name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    region_of_operation = models.CharField(max_length=128)
    branch_contact = models.CharField(max_length=128)
    # Foreign key to MaterialSupplier model
    material_supplier_id = models.ForeignKey(MaterialSupplier, on_delete=models.CASCADE)
    phone = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class MaterialInvoice(models.Model):
    material_invoice_id = models.BigAutoField(primary_key=True)
    # Foreign key to StoreBranch model
    store_branch_id = models.ForeignKey(StoresBranch, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0.00)
    approver = models.CharField(max_length=128)
    date_time = models.DateTimeField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class MaterialInvoiceItems(models.Model):
    material_invoice_item_id=models.BigAutoField(primary_key=True)
    # Foreign key to MaterialInvoice model
    material_invoice_id=models.ForeignKey(MaterialInvoice, on_delete=models.CASCADE)
    items = models.CharField(max_length=128)
    quantity = models.FloatField(default=1)
    individual_price = models.FloatField()  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=MaterialInvoiceItems)
@receiver(post_delete, sender=MaterialInvoiceItems)
def update_total_price(sender, instance, **kwargs):
    invoice = instance.material_invoice_id
    total_price = sum(item.individual_price*item.quantity for item in invoice.materialinvoiceitems_set.all())
    invoice.total_price = total_price
    invoice.save()
class WorkOrders(models.Model):
    work_order_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    contract_id = models.ForeignKey(DealContract, on_delete=models.CASCADE)
    supplier_list_id = models.CharField(max_length=128)
    work_order_type = models.CharField(max_length=128)
    work_order_status = models.BooleanField(default=1)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class JobOrders(models.Model):
    job_order_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    work_order_id = models.ForeignKey(WorkOrders, on_delete=models.CASCADE)
    job_desc = models.CharField(max_length=128)
    job_type = models.CharField(max_length=128)
    assignee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_status = models.BooleanField(default=1)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class ApprovalStatus(Enum):
    APPROVED = "Approved"
    DECLINED = "Declined"
class WorkOrderInvoice(models.Model):
    work_order_invoice_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    work_order_id = models.ForeignKey(WorkOrders, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approval_status = models.CharField(
        max_length=32,
        choices=[(status.name, status.value) for status in ApprovalStatus],
    )
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class JobOrderInvoice(models.Model):
    job_order_invoice_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    work_order_invoice_id = models.ForeignKey(WorkOrderInvoice, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2)
    rates = models.DecimalField(max_digits=10, decimal_places=2)
    abn = models.CharField(max_length=20)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.rates * self.total_hours
        super().save(*args, **kwargs)
class JobOrderTimesheet(models.Model):
    job_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    work_order_id = models.ForeignKey(WorkOrders, on_delete=models.CASCADE, blank=True,null= True)
    job_order_id = models.ForeignKey(JobOrders, on_delete=models.CASCADE)
    # Date as a field and part of the primary key
    date = models.DateField()

    # Start and end time fields
    start_time = models.TimeField()
    end_time = models.TimeField()
    approval_status = models.CharField(
        max_length=32,
        blank=True,null=True,
        choices=[(status.name, status.value) for status in ApprovalStatus],
    )
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Billing(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)  # Auto-increment primary key
    # Foreign key to Supplier model
    work_order_invoice_id = models.ForeignKey(WorkOrderInvoice, on_delete=models.CASCADE)
    material_invoice_id = models.ForeignKey(MaterialInvoice, on_delete=models.CASCADE, blank=True,null= True)
    work_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    material_invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null= True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust if this is a foreign key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)