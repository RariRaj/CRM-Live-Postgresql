from django.shortcuts import render,HttpResponse,redirect
from crm_app.models import *
from .forms import OrderForm ,CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
import math

# Create your views here.
def home(request):
    customer_details=Customer.objects.all()
    order=Order.objects.all().order_by('-date_created')[0:5]
    
    # last_customer=Customer.objects.last()
    # print(last_customer.name,last_customer.date_created)
    total_orders=Order.objects.all().count
    order_delivered=Order.objects.filter(status="Delivered").count()
    order_pending=Order.objects.filter(status="Pending").count()
    context={'customer_details':customer_details,'order_details':order,'order_count':total_orders,'order_delivered':order_delivered,'order_pending':order_pending}
   
    return render(request,'home.html',context)

def products(request):
    no_of_blocks=4
    page=request.GET.get('page')
    
    if page == None:
        page=1
    else :
        page=int(page)
    print(page)

    if page > 1:
        prev = page - 1
    else:
        prev = None

    product_details=Product.objects.all()
    length=product_details.count()
    

    if page < math.ceil(length/no_of_blocks):
        nxt = page + 1
    else:
        nxt = None
    
    product_details=product_details[(page-1)*no_of_blocks : page*no_of_blocks]
    
    context={'product_details':product_details,'nxt':nxt,'prev':prev}
    return render(request,'products.html',context)

def customer(request,id):
    customer_details=Customer.objects.get(pk=id)
    order_info=customer_details.order_set.all()
    #print(order_info)
    total_order=order_info.count()

    myFilter=OrderFilter(request.GET,queryset=order_info)
    order_info=myFilter.qs
    context={'customer_details':customer_details,'order_info':order_info,'total_order':total_order,'myFilter':myFilter}
    return render(request,'customer.html',context)

def createOrder(request,id):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'), extra=10)
    customer=Customer.objects.get(pk=id)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)

    #form=OrderForm(initial={'customer':customer})
    #context={'form':form}
    context={'formset':formset}
    if request.method=="POST":
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request,'create_order.html',context)
def updateOrder(request,id):
    order=Order.objects.get(pk=id)
    form=OrderForm(instance=order)
    context={'form':form}
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    
    return render(request,'update_order.html',context)

def deleteOrder(request,id):
    order_item=Order.objects.get(pk=id)
    context={'item':order_item}
    if request.method=="POST":
        order_item.delete()
        return redirect("/")
    
    return render(request,'delete_order.html',context)

def updateCustomer(request,id):
    customer=Customer.objects.get(pk=id)
    form=CustomerForm(instance=customer)
    context={'form':form}
    if request.method=="POST":
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid:
            form.save()
            return redirect("/")

    return render(request,'update_customer.html',context) 

def createCustomer(request):
    form=CustomerForm()
    context={'form':form}
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request,'create_customer.html',context)