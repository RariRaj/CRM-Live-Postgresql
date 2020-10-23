from django.shortcuts import render,HttpResponse,redirect
from crm_app.models import *
from .forms import OrderForm ,CustomerForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
import math
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

# Create your views here.

@unauthenticated_user
def registration(request):
    #form=UserCreationForm()
    form=CreateUserForm()
    if request.method=="POST":
        #form=UserCreationForm(request.POST)
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

            
            
            messages.success(request,'Account is created for'+ " "+username)
            return redirect('/login')
        else:
            print("error")

    # else:
    #     form=CreateUserForm()




    context={'form':form}

    return render(request,'registration.html',context)
@unauthenticated_user
def loginPage(request):


    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')

    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
@admin_only
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


@login_required(login_url='/login')
@admin_only
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


@login_required(login_url='/login')
@admin_only
def customer(request,id):
    customer_details=Customer.objects.get(pk=id)
    order_info=customer_details.order_set.all()
    #print(order_info)
    total_order=order_info.count()

    myFilter=OrderFilter(request.GET,queryset=order_info)
    order_info=myFilter.qs
    context={'customer_details':customer_details,'order_info':order_info,'total_order':total_order,'myFilter':myFilter}
    return render(request,'customer.html',context)


@login_required(login_url='/login')
@admin_only
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


@login_required(login_url='/login')
@admin_only
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


@login_required(login_url='/login')
@admin_only
def deleteOrder(request,id):
    order_item=Order.objects.get(pk=id)
    context={'item':order_item}
    if request.method=="POST":
        order_item.delete()
        messages.success(request,"Order has been deleted...")
        return redirect("/")
    
    return render(request,'delete_order.html',context)


@login_required(login_url='/login')
@admin_only
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


@login_required(login_url='/login')
@admin_only
def createCustomer(request):
    form=CustomerForm()
    context={'form':form}
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request,'create_customer.html',context)


@login_required(login_url='/login')
@allowed_users(allowed_roles=['customer'])
def userHome(request):
    orders=request.user.customer.order_set.all()
    #print(orders)
    total_orders=orders.count()
    order_delivered=orders.filter(status="Delivered").count()
    order_pending=orders.filter(status="Pending").count()
    context={'orders':orders,'order_count':total_orders,'order_delivered':order_delivered,'order_pending':order_pending}
    return render(request,'users.html',context)


@login_required(login_url='/login')
@allowed_users(allowed_roles=['customer'])
def userSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    context={'form':form}
    if request.method=="POST":
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            messages.info(request,"Profile updated successfully")
            #return redirect("settings")
    
    return render(request,'settings.html',context)