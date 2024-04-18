
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from . models import *
from datetime import datetime
from django.utils import timezone
#from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
# from django.core.mail import send_mail
# from django.conf import Settings
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .models import Category
from .models import Subcategory
from .models import Product
from django.views.decorators.cache import *

def new_password(request):
    request.session['lid']
    if 'new_p' in request.POST:
        np=request.POST['np']
        cp=request.POST['cp']
        if np == cp:
            
            lg=Login.objects.get(pk=request.session['lid'])
            lg.password=cp
            lg.save()
            return HttpResponse("<script>alert('Password Successfully Changed.');window.location='/login_fun_page'</script>")
        else:
            return HttpResponse("<script>alert('Confirm password mismatched.');window.location='/new_password'</script>")
   

    return render(request,'new_password.html')



def enter_otp(request):
    print("#############", request.session['otp'])
    if 'et_otp' in request.POST:
        otp_v=int(request.POST['otp_v'])
        if otp_v == request.session['otp']:
            return HttpResponse("<script>alert('Successfully Verified.');window.location='/new_password'</script>")
        else:
            return HttpResponse("<script>alert('Invalid OTP.');window.location='/enter_otp'</script>")
   

    return render(request,'enter_otp.html')



def forgot_password(request):
    import random
    otp = random.randint(1000, 9999)
    request.session['otp'] = otp
    print(random.randint(1000, 9999))
    if 'forgot' in request.POST:
        uname = request.POST['uname']
        email = request.POST['email']
        try:
            uu = Login.objects.get(username=uname)
            if uu:
                if uu.type == "Doctors":
                    try:
                        ee = Doctors.objects.get(email=email)
                        if ee:
                            request.session['lid'] = uu.pk
                            send_mail(
                                'Forgot Password Request' + uname,
                                'Your OTP(One Time Password) is: ' + str(otp),
                                'swathysaji143@gmail.com',
                                [email],
                                fail_silently=False,
                            )
                            return HttpResponse("<script>alert('Check Your Email.');window.location='/enter_otp'</script>")
                        else:
                            return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
                    except:
                        return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
                elif uu.type == "user":
                    
                    try:
                        ee1 = Users.objects.get(email=email)
                        print(ee1.FullName, '//////////////////////////////////')
                        if ee1:
                            print('gggggggggggggggggggggggggggg')
                            request.session['lid'] = uu.pk
                            send_mail(
                                'Forgot Password Request' + uname,
                                'Your OTP(One Time Password) is: ' + str(otp),
                                'swathysaji143@gmail.com',
                                [email],
                                fail_silently=False,
                            )
                            return HttpResponse("<script>alert('Check Your Email.');window.location='/enter_otp'</script>")
                        else:
                            return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
                    except:
                        return HttpResponse("<script>alert('Invalid Email');window.location='/forgot_password'</script>")
            else:
                return HttpResponse("<script>alert('Invalid Username.');window.location='/forgot_password'</script>")
        except:
            return HttpResponse("<script>alert('Invalid Username.');window.location='/forgot_password'</script>")
    return render(request, 'forgot_password.html')



def index(request):
    return render(request, 'indexmain.html')


def doctor_index(request):
    dr=Doctors.objects.get(id=request.session['doc_id'])
    if dr:
        fns=dr.Name

    return render(request, 'doctor_index.html',{'fns':fns})



def landing_page(request):
    return render(request, 'landing_page.html')

def admin_home(request):
    return render(request, 'admin_home.html')
# def logout_view(request):
#     logout(request)
#     # Redirect to a specific page after logout
#     return redirect('admin_login') 


def logout_view(request):
    # Perform logout-related actions
    logout(request)

    # Redirect to the same page (refresh the page)
    return redirect('index')



def login_fun_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
     
        try:
            
            q = Login.objects.get(username=username, password=password)
        
            print(q)
            request.session['id'] = q.pk
            if q:
                if q.type == 'admin':
                    return HttpResponse("<script>alert('login successful'); window.location='/admin_home'</script>")
                elif q.type == 'Doctors':
                    qd = Doctors.objects.get(LOGIN_id=request.session['id'])
                    if qd:
                        request.session['doc_id'] = qd.pk
                        request.session['doctor'] = username
                    return HttpResponse("<script>alert('login successful'); window.location='/doctor_index'</script>")
                elif q.type == 'user':
                    qr = Users.objects.get(LOGIN_id=request.session['id'])
                    if qr:
                        request.session['email']=qr.email
                        request.session['uid'] = qr.pk
                    return HttpResponse("<script>alert('login successful');window.location='/patient_index'</script>")
                elif q.type == 'seller':
                    qs = Seller.objects.get(LOGIN_id=request.session['id'])
                    if qs:
                        request.session['seller'] = username
                        request.session['sid'] = qs.pk
                    return HttpResponse("<script>alert('login successful'); window.location='/seller_index'</script>")

        except:
            return HttpResponse("<script>alert('Invalid Username or Password');window.location='/login_fun_page'</script>")       
    return render(request, 'login_fun_page.html')




def patient_index(request):
    usr=Users.objects.get(id=request.session['uid'])
    if usr:
        fn=usr.FullName

    return render(request, 'patient_index.html',{'fn':fn})

def seller_index(request):
    sr=Seller.objects.get(id=request.session['sid'])
    if sr:
        f=sr.Name
    return render(request,'seller_index.html',{'f':f}) 


def register_user(request):
    if request.method == 'POST':
        fullName = request.POST['fullName']
        place = request.POST['place']
        age = request.POST['age']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        qr=Login(username=email,password=password,type="user")
        qr.save()

        qc=Users(FullName=fullName,Age=age,Place=place,Gender=gender,phone=phone,email=email,LOGIN=qr)
        qc.save()
        return HttpResponse("<script>alert('User registration successfully');window.location='/login_fun_page'</script>") 
    return render(request,'register_user.html')

def patient_profile(request):
    patient_up=Users.objects.get(id=request.session['uid'])
    if request.method == 'POST':
       patient_up.FullName = request.POST['fullName'] 
       patient_up.Age = request.POST['age']
       patient_up.Place = request.POST['place']
       patient_up.Gender = request.POST['genderxxx']
       patient_up.email = request.POST['email']
       patient_up.save()
       return HttpResponse("<script>alert('Your Profile updated  successfully');window.location='/home_patient'</script>") 
    return render(request,'patient_profile.html',{'patient_up':patient_up})

def doctor_profile(request):
    doctor_up=Doctors.objects.get(id=request.session['doc_id'])
    if request.method == 'POST':
        doctor_up.Name = request.POST['Name'] 
        doctor_up.email = request.POST['email'] 
        doctor_up.specialization = request.POST['specialization']
        doctor_up.place = request.POST['place']
        doctor_up.gender = request.POST['genderxxx']
        doctor_up.phone = request.POST['phone']
        doctor_up.save()  
        return HttpResponse("<script>alert('Your Profile updated  successfully');window.location='/landing_page'</script>") 
    return render(request,'doctor_profile.html',{'doctor_up':doctor_up})

def register_seller(request):
    if request.method == "POST" :
        Sellername = request.POST['Name']
        phone = request.POST['phone']
        email = request.POST['email']
        brandname = request.POST['brand_name']
        password = request.POST['password']
        pics = request.FILES.get('pic')
        password = request.POST['password']
        date = request.POST.get('registration_date')
        qs=Login(username=email,password=password,type="seller")
        qs.save()

        qs=Seller(Name=Sellername,phone=phone,email=email,brand_name=brandname,pic=pics,registration_date=date,password=password,LOGIN=qs)
        qs.save()
        return HttpResponse("<script>alert('Seller registration successfully');window.location='/login_fun_page'</script>") 
    return render(request,'register_seller.html')



def register_doctor(request):
    if request.method == "POST" :
        Namess = request.POST['Name']
        place = request.POST['place']
        DOB = request.POST['DOB']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        specialization = request.POST['specialization']
        d = request.FILES['pictures']
        # print("==================================",type(profile_picture))
        # fss = FileSystemStorage()
        # file_name = fss.save(profile_picture.name, profile_picture)
        fs=FileSystemStorage()
        fn=fs.save(d.name,d)



        password = request.POST['password']
        dr=Login(username=email,password=password,type="Doctors")
        dr.save()
        qdr=Doctors(Name=Namess,dob=DOB,place=place,specialization=specialization,gender=gender,phone=phone,email=email,LOGIN=dr, 
                    pic=d
                    )
        qdr.save()
        return HttpResponse("<script>alert('Doctor registration successfully');window.location='/login_fun_page'</script>") 
    return render(request, "register_doctor.html")
    


def adminmanage_doctor(request):
    if request.method == "POST":
        Namess = request.POST['Name']
        place = request.POST['place']
        DOB = request.POST['DOB']
        gender = request.POST['genderxxx']
        phone = request.POST['phone']
        email = request.POST['email']
        specialization = request.POST['specialization']
        password = request.POST['password']
        dr=Login(username=email,password=password,type="Doctors")
        dr.save()
        qdr=Doctors(Name=Namess,dob=DOB,place=place,specialization=specialization,gender=gender,phone=phone,email=email,LOGIN=dr)
        qdr.save()
        return HttpResponse("<script>alert('Doctor registration successfully');window.location='/login_fun'</script>") 
    return render(request, 'adminmanage_doctor.html')
    
def adminmando_view(request):
    docview=Doctors.objects.all()
    return render(request, 'adminmando_view.html',{'docview':docview})







def delete_doctor(request,id):
    docview=Doctors.objects.filter(LOGIN_id=id)
    docview.delete()
    dr=Login.objects.get(id=id)
    dr.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/admin_home'</script>")


def admin_update_doctor_details(request,id):
 qt=Doctors.objects.get(id=id)
 if request.method == "POST":   
    
    qt.Name=request.POST['firstname']
    qt.specialization=request.POST['specialization']
    qt.place=request.POST['place']
    qt.phone=request.POST['phone']
    qt.email=request.POST['email']
    qt.dob=request.POST['dob']
    qt.gender=request.POST['genderxxx']
    qt.save()
    return HttpResponse("<script>alert('Update Successfully');window.location='/admin_home'</script>")
 return render(request, 'admin_update_doctor_details.html',{'doc_up':qt})



def schedule_doctor(request):


 if request.method == "POST": 
    Date=request.POST['date']
    Timefrom=request.POST['timefrom']
    Timeto=request.POST ['timeto'] 
    sc=Schedule(date=Date,timefrom=Timefrom,timeto=Timeto)
    sc.save()
    return HttpResponse("<script>alert('Booking successfully');window.location='/schedule_doctor'</script>") 
 return render(request, "landingpage.html")


def adminmanage_user(request):
    if request.method == "POST":
        fullName = request.POST['fullName']
        place = request.POST['place']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        qr=Login(username=email,password=password,type="user")
        qr.save()
        qc=Users(FullName=fullName,Age=age,Place=place,Gender=gender,phone=phone,email=email,LOGIN=qr)
        qc.save()
        return HttpResponse("<script>alert('User registration Successfully');window.location='/login_fun'</script>")
    return render(request,'adminmanage_user.html')

def adminmanpa_view(request):
    docviews=Users.objects.all()
    return render(request, 'adminmanpa_view.html',{'docviews':docviews})

def delete_user(request,id):
    docviews=Users.objects.filter(LOGIN_id=id)
    docviews.delete()
    qr=Login.objects.get(id=id)
    qr.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/admin_home'</script>")



def admin_update_user(request,id):
 ur=Users.objects.get(id=id)
 if request.method == "POST":   
    ur.FullName=request.POST['fullName']
    ur.Place=request.POST['place']
    ur.phone=request.POST['phone']
    ur.email=request.POST['email']
    ur.Age=request.POST['age']
    ur.Gender=request.POST['gender']
    ur.Password=request.POST['password']
    ur.save()
    return HttpResponse("<script>alert('Update Successfully');window.location='/admin_home'</script>")
 return render(request, 'admin_update_user.html',{'docs_up':ur})













def schedule_form(request):
    from datetime import date
    cdate=date.today()
    if request.method == 'POST':
        date = request.POST['date']
        timefrom = request.POST['timefrom']
        timeto = request.POST['timeto']
        doctor_username = request.session.get('doctor')
        
        # Retrieve the doctor instance using the email
        doctor_instance = Doctors.objects.get(email=doctor_username)
        
        # Create a new Schedule instance with the retrieved Doctor instance
        sch = Schedule(DOCTOR=doctor_instance, date=date, timefrom=timefrom, timeto=timeto)
        sch.save()
        
        # Retrieve the updated doctor's schedule
        doctors_schedule = Schedule.objects.filter(DOCTOR=doctor_instance)
        
        return render(request, 'schedule_form.html', {'doctors_schedule': doctors_schedule,'cdate':cdate})
    
    # If it's a GET request, just display the form
    doctor_username = request.session.get('doctor')
    doctor_instance = Doctors.objects.get(email=doctor_username)
    sh = Schedule.objects.filter(DOCTOR=doctor_instance)
    
    return render(request, 'schedule_form.html', {'doctors_schedule': sh,'cdate':cdate})






def home_patient(request):
    docview=Doctors.objects.all()
    return render(request, 'home_patient.html',{'docview':docview})
    # return render(request, 'home_patient.html')



def view_slots(request, doctor_id):
    slots = Schedule.objects.filter(DOCTOR=doctor_id)
    return render(request, 'view_slots.html', { 'slots': slots})




def booking_doctor(request, id):
    print("......",request.session.get('uid'))
    current_date = timezone.now().date()
    print(current_date)
    myqr = Booking.objects.filter(SCHEDULE_id=id)
    print(myqr,"///////////////////////")
    if myqr:
        return HttpResponse("<script>alert('Already Booked Time');window.location='/home_patient'</script>")
    else:
        qr = Booking(SCHEDULE_id=id, USER_id=request.session.get('uid'), dateofbooking=current_date, Status='success')
        qr.save()

        subject = 'YOUR BOOKED APPOINTMENT'
        message = "Dear Sir/Madam,\nYour appointment has been successfully booked."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.session['email']]
        
        #send_mail(subject, message, email_from, recipient_list)

        
        return HttpResponse("<script>alert('Booked Successfully');window.location= '/home_patient'</script>")
    





def view_mybooking(request):
    uid = request.session.get('uid')
    bookings = Booking.objects.filter(USER=uid)
    return render(request, 'patient_view_mybook.html', {'bookings': bookings})
    # return render(request, 'home_patient.html')





def doctor_page(request):
    uid = request.session.get('doc_id')
    q = Schedule.objects.filter(DOCTOR_id=uid)
    
    all_bookings = []

    for schedule in q:
        sid = schedule.id
        bookings = Booking.objects.filter(SCHEDULE_id=sid)
        all_bookings.extend(bookings)


    return render(request, 'doctor_page.html', {'bookings': all_bookings})


def payment_check(request,b_id):
    current_date = timezone.now().date()

    if request.method == "POST":  

        qr = paymentss(booking_id_id=b_id, user_id_id=request.session.get('uid'),amount='300', date=current_date)
        qr.save()
        q=Booking.objects.get(id=b_id)
        if q:
            q.Status='paid'
            q.save()
            return HttpResponse("<script>alert('Payment success');window.location= '/mybookings'</script>")




        subject = 'PAYMENT SUCCESSFULL'
        message = "Dear Sir/Madam,\n Your Payment have  been successfully completed."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.session['email']]
        
        send_mail(subject, message, email_from, recipient_list)



    return render(request, 'payment_check.html')






def doctor_add_prescription(request,id):
    if request.method == "POST":
        medicine_name = request.POST['medicine_name']
        dosage = request.POST['dosage']
        ps=Prescriptions(medicine_name=medicine_name,dosage=dosage,BOOKING_id=id)
        ps.save()
    return render(request, 'doctor_add_prescription.html')

# def view_mypres(request):
#     uid=request.session.get('uid')
#     pre=Prescriptions.objects.all()
#     print("uuuuuuuuuuuuu",pre)
#     return render(request, 'view_pres.html',{pre:pre})

def user_view_pres(request):
    docviews=Prescriptions.objects.all()
    return render(request, 'user_view_pres.html',{'docviews':docviews})

def demoschedule(request):
    from datetime import date
    cdate=date.today()
    if request.method == 'POST':
        date = request.POST['date']
        timefrom = request.POST['timefrom']
        timeto = request.POST['timeto']
        doctor_username = request.session.get('doctor')
        
        # Retrieve the doctor instance using the email
        doctor_instance = Doctors.objects.get(email=doctor_username)
        
        # Create a new Schedule instance with the retrieved Doctor instance
        sch = Schedule(DOCTOR=doctor_instance, date=date, timefrom=timefrom, timeto=timeto)
        sch.save()
        
        # Retrieve the updated doctor's schedule
        doctors_schedule = Schedule.objects.filter(DOCTOR=doctor_instance)
        
        return render(request, 'schedule_form.html', {'doctors_schedule': doctors_schedule,'cdate':cdate})
    
    # If it's a GET request, just display the form
    doctor_username = request.session.get('doctor')
    doctor_instance = Doctors.objects.get(email=doctor_username)
    sh = Schedule.objects.filter(DOCTOR=doctor_instance)
    
    return render(request, 'demoschedule.html', {'doctors_schedule': sh,'cdate':cdate})

from .models import Category

def category_product(request):
    if request.method == 'POST':
        categoryName = request.POST.get('name')
        print(categoryName)
        if categoryName:
            # Create a new category object and save it
            Category.objects.create(name=categoryName)
            messages.success(request, 'Category added successfully')
            # Redirect to the same page after adding the category
            categories = Category.objects.all()
            context = {
                "categories": categories,
            }
            print(categories)
            return render(request, 'category_page.html', context)
        else:
            messages.error(request, 'Category name cannot be empty')

    # Fetch existing categories for display
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    print(categories)
    return render(request, 'category_page.html', context)

  

    
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            messages.success(request, 'Category deleted successfully')
        except Category.DoesNotExist:
            messages.error(request, 'Category not found')
    # Redirect to category_product view after deleting the category
    return redirect('seller_index')
    #return HttpResponse("<script>alert('deleted successfully');window.location='/seller_index'</script>")     



def sub_category(request):
    if request.method == 'POST':
        subcategoryname = request.POST.get('name')
        print(subcategoryname)
        category_id = request.POST.get('category_id')
        print(category_id)
        if subcategoryname and category_id:
            category = Category.objects.get(id=category_id)
            scat = Subcategory.objects.create(name=subcategoryname, category=category)
            messages.success(request, 'Subcategory added successfully')
            # Redirect to some appropriate page after adding the subcategory
            return redirect('product_list')
        else:
            messages.error(request, 'Subcategory name or category ID cannot be empty')

    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'add_subcategory.html', context)
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Category, Subcategory, Seller

def product_list(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            productname = request.POST.get('productname')
            productdescription = request.POST.get('productdescription')
            productprice = request.POST.get('productprice')
            productdiscount = request.POST.get('productdiscount')
            productquantityavailable = request.POST.get('productquantityavailable')
            
            productingredients = request.POST.get('productingredients')
          
            productusageinstructions = request.POST.get('productusageinstructions')
            productcertificate = request.FILES.get('productcertificate')
            productexpirydate = request.POST.get('productexpirydate')
            productmanufacturer = request.POST.get('productmanufacturer')
            category_id = request.POST.get('category')  # Get the selected category ID
            subcategory_id = request.POST.get('subcategory')  # Get the selected subcategory ID
            seller_id = request.POST.get('seller')  # Get the selected seller ID
            product_image = request.FILES.get('product_image')
            # Get the Category, Subcategory, and Seller objects based on the selected IDs
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
            seller = Seller.objects.get(id=seller_id)

            # Create and save the new product
            pr = Product.objects.create(
                name=productname,
                description=productdescription,
                price=productprice,
                discount=productdiscount,
                quantity_available=productquantityavailable,
                product_image=product_image ,
               
                ingredients=productingredients,
               
                usage_instructions=productusageinstructions,
                certifications=productcertificate,
                expiry_date=productexpirydate,
                manufacturer=productmanufacturer,
                category=category,  # Assign the category to the product
                subcategory=subcategory,  # Assign the subcategory to the product
                seller=seller  # Assign the seller to the product
                
            )

            # Redirect to prevent form resubmission on page refresh
            return redirect('product_display')
        except ObjectDoesNotExist:
            # Handle the case where the specified objects do not exist
            return HttpResponseServerError("One of the selected objects does not exist.")
        except Exception as e:
            # Handle other exceptions
            return HttpResponseServerError(f"An error occurred: {e}")
    else:
        # Handle GET request to render the page with the form
        products = Product.objects.all()
        categories = Category.objects.all()  # Fetch all categories
        subcategories = Subcategory.objects.all()  # Fetch all subcategories
        sellers = Seller.objects.all()  # Fetch all sellers
        return render(request, 'ayurproduct_list.html', {'products': products, 'categories': categories, 'subcategories': subcategories, 'sellers': sellers})
    

def added_products(request):
     # Fetch all added products
    products = Product.objects.all()
     
    return render(request, 'added_product.html', {'products': products})      

from django.shortcuts import render, get_object_or_404
def update_product_details(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        # Update product details based on the POST data
        product.name = request.POST['productname']
        product.description = request.POST['productdescription']
        product.price = request.POST['productprice']
        product.discount = request.POST['productdiscount']
        product.quantity_available = request.POST['productquantityavailable']
        product.ingredients = request.POST['productingredients']
        product.usage_instructions = request.POST['productusageinstructions']
        product.certifications = request.FILES.get('productcertificate')
        product.expiry_date = request.POST['productexpirydate']
        product.manufacturer = request.POST['productmanufacturer']
        product.category_id = request.POST.get('category')  # corrected method
        product.subcategory_id = request.POST.get('subcategory')  # corrected method
        product.seller_id = request.POST.get('seller')  # corrected method
        product.product_image = request.FILES.get('product_image')
        product.save()
        return render(request, 'seller_index.html')  # Redirect to a success page or any other desired page
    else:
        # Render the edit product form with the product details
        categories = Category.objects.all()  # Assuming you have a Category model
        subcategories = Subcategory.objects.all()  # Assuming you have a Subcategory model
        sellers = Seller.objects.all()  # Assuming you have a Seller model
        return render(request, 'edit_product.html', {'product': product, 'categories': categories, 'subcategories': subcategories, 'sellers': sellers})
    
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('category') 

def search_products(request):
    query = request.GET.get('query')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()
    
    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, 'added_product.html', context)


from django.shortcuts import render
from .models import Product

def patient_product_list(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, 'patient_product_list.html', {'products': products})



def user_add_product_to_carts1(request, pid, pname, rate, quantity):
    today = date.today()
    print(today)

    lid = request.session['id']

    c = Users.objects.filter(LOGIN_id=lid)
    if c:
        cid = c[0].id
        print(cid)

    if request.method == "POST":
        qty = int(request.POST['qty'])
        amount = float(request.POST['amount'])
        ttotal = float(request.POST['total'])

        if qty <= int(quantity):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            q = P_booking.objects.filter(user_id=cid, p_status='pending')
            if q:
                oid = q[0].id
                total = float(q[0].p_amount)
                print("omaster_id...............", oid)
                print("total...............", total)

                q2 = P_bookingchild.objects.filter(P_booking_id=oid, product_id=pid)
                if q2:
                    od_id = q2[0].id
                    t_qty = int(q2[0].quantity)
                    t_amt = float(q2[0].book_amount)
                    print("odetail_id......", od_id)
                    print("t_qty........", t_qty)
                    print("t_amt........", t_amt)

                    c_qty = t_qty + qty

                    if c_qty > int(quantity):
                        return HttpResponse("<script>alert('OUT OF STOCK');window.location='/patient_product_list';</script>")
                    else:
                        oup = P_bookingchild.objects.get(id=od_id)
                        oup.book_amount = str(t_amt + ttotal)
                        oup.quantity = str(t_qty + qty)
                        oup.save()

                        up = P_booking.objects.get(id=oid)
                        up.p_amount = str(total + ttotal)
                        up.save()
                else:
                    q3 = P_bookingchild(book_amount=str(ttotal), quantity=str(qty), P_booking_id=oid, product_id=pid)
                    q3.save()
                    up1 = P_booking.objects.get(id=oid)
                    up1.p_amount = str(total + ttotal)
                    up1.save()
                    return HttpResponse("<script>alert('ADD TO CART....!!');window.location='/patient_product_list';</script>")

            else:
                oid = P_booking(p_amount=str(ttotal), p_date=str(today), p_status='pending', user_id=cid)
                oid.save()
                q3 = P_bookingchild(book_amount=str(ttotal), quantity=str(qty), P_booking_id=oid.id, product_id=pid)
                q3.save()
                return HttpResponse("<script>alert('ADD TO CART....!!');window.location='/patient_product_list';</script>")

        else:
            return HttpResponse("<script>alert('Enter Less Quantity....!!');window.location='/patient_product_list';</script>")

    ss = {}
    ss['products'] = pname
    ss['amount'] = rate
    return render(request, 'user_add_product_to_carts1.html', ss)






















def user_view_cart_pdt(request):
    sid=request.session['uid']
    q=P_booking.objects.filter(user_id=sid,p_status='pending').order_by('-id')
    if q:
        status=q[0].p_status
        if status == "paid":
            return HttpResponse("<script>alert('cart is empty....!!');window.location='/patient_index/';</script>")
    return render(request,'user_view_cart_pdt.html',{'q':q})


def user_view_cartdetailspdt(request,id):
    q=P_bookingchild.objects.filter(P_booking_id=id)
    return render(request,'user_view_cartdetailspdt.html',{'q':q})


# def user_make_payment_pdt(request,id,total):
#     today=date.today()
#     print(today)
  
#     if request.method=="POST":
#         q=pdt_payment(pdt_amount=total,pdt_date=today,booking_id=id)
#         q.save()

#         q1=booking.objects.get(booking_id=id)
#         q1.book_status='paid'
#         q1.save()    
#         return HttpResponse("<script>alert('Payment Completed....!!!');window.location='/userhome';</script>")
#     return render(request,'user_make_payment_pdt.html',{'total':total})

def default(request, am, id):
    import razorpay

    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    amount = int(float(am) * 100)  # Convert to float, multiply by 100, and then convert to integer
    print("lkkkkk", am)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {'razorpay_api_key': razorpay_api_key,
               'amount': order_data['amount'],
               'currency': order_data['currency'],
               'order_id': order['id'],
               }

    return render(request, 'payment.html', {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'booking_id': id
    })



def finish_payment(request, booking_id):
    cdate = date.today()
    # Update booking status to "paid"
    P_booking.objects.filter(id=booking_id).update(p_status="paid")
    
    if request.method == "POST":
        # Check if payment for the current date and booking ID exists
        payment_exists = Payment.objects.filter(date=cdate, py_status="paid", user_id=request.session['uid'], P_booking_id=booking_id).exists()
        
        if not payment_exists:
            # Create a new payment record
            payment = Payment.objects.create(date=cdate, py_status="paid", user_id=request.session['uid'], P_booking_id=booking_id)
            payment.save()
        
    return HttpResponse("<script>alert('Paid successfully');window.location='/patient_index'</script>")

from django.shortcuts import render, redirect
from .models import Bookings, Room
from datetime import datetime, timedelta

def book_treatment(request):
    if request.method == 'POST':
        room_type = request.POST.get('room')
        date_start = request.POST.get('date_start')
        treatment_type = request.POST.get('treatment_type')
        food_plan = request.POST.get('food_plan')
        number_of_days = int(request.POST.get('number_of_days'))

        # Calculate end date based on start date and number of days
        end_date = (datetime.strptime(date_start, "%Y-%m-%d") + timedelta(days=number_of_days)).strftime("%Y-%m-%d")

        # Get or create a room based on the selected type
        room, _ = Room.objects.get_or_create(room_type=room_type)

        # Create booking object
        booking = Bookings.objects.create(
            room=room,
            date_start=date_start,
            treatment_type=treatment_type,
            food_plan=food_plan,
            number_of_days=number_of_days,
            status='pending'
        )
        
        return redirect('booking_success')  # Redirect to booking success page
    else:
        return render(request, 'book_treatment.html')

def booking_success(request):
    return render(request, 'booking_success.html')

def view_bookings(request):
    bookings = Bookings.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})


def admin_view_treatment(request):
    bookings = Bookings.objects.all()
    return render(request, 'admin_view_treatment.html', {'bookings': bookings})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404  # Import get_object_or_404 if needed
from .models import Bookings
def delete_booking(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.delete()
        return JsonResponse({'success': True})  # Return success response
    except Bookings.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Booking not found'}, status=404)
    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Bookings,Login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_confirmation_email(user_email, booking):
    subject = "Treatment Booking Confirmation"
    message = render_to_string('confirmation_email.html', {
        'room': booking.room,
        'date_start': booking.date_start,
        'treatment_type': booking.treatment_type,
        'food_plan': booking.food_plan,
        'number_of_days': booking.number_of_days,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

def approve_booking(request, user_id, booking_id):
    if request.method == 'POST':
        user = get_object_or_404(Login, pk=user_id)
        booking = get_object_or_404(Bookings, pk=booking_id)
        booking.status = 'approved'
        booking.save()
        send_confirmation_email(user.email, booking)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)