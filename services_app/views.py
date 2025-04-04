from django.shortcuts import render
from django.http import HttpResponse,request
from django.views import View
from database import create_connection
from django.conf import settings


from django.shortcuts import render, get_object_or_404, redirect
import os
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Prepare update query


# Create your views here.
class logout(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect("home_page")


class user_home(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_category")
        data = cur.fetchall()

        if username is None:
            #return redirect('login')
            return render(request,"login.html")

        print("------------->  DATA : ",data)

        return render(request, "user_home.html", context={"data":data,"username":username})

    def post(self, request, *args, **kwargs):

        username = request.session.get("username")
        password = request.session.get("password")
        uer_id = request.session.get("user_id")

        if username is None:
            return redirect('login')
        return render(request, "user_home.html")

class about_us(View):
    def get(self, request, *args, **kwargs):
        return render(request, "about_us.html")

    def post(self, request, *args, **kwargs):
        return render(request, "about_us.html")

class emergency_services(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username",None)
        if not username:
            return redirect('login')

        #category_id = request.POST.get("category_id")
        conn = create_connection()
        cur = conn.cursor()
        
        c_name = "Emergency"
        
        cur.execute("SELECT c_id FROM mstr_category WHERE c_name = %s", (c_name,))
        c_id = cur.fetchone()

        cur.execute("SELECT * FROM mstr_service WHERE c_id = %s", (c_id[0],))
        data = cur.fetchall()

        return render(request, "emergency_services.html", {"data": data, "category_name": c_name, "username": username})

    def post(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')

        #category_id = request.POST.get("category_id")
        conn = create_connection()
        cur = conn.cursor()
        
        c_name = "Emergency"
        
        cur.execute("SELECT c_id FROM mstr_category WHERE c_name = %s", (c_name,))
        c_id = cur.fetchone()

        cur.execute("SELECT * FROM mstr_service WHERE c_id = %s", (c_id[0],))
        data = cur.fetchall()

        return render(request, "emergency_services.html", {"data": data, "category_name": c_name, "username": username})


class services(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        return render(request, 'services.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')

        category_id = request.POST.get("category_id")
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT c_name FROM mstr_category WHERE c_id = %s", (category_id,))
        c_name = cur.fetchone()

        cur.execute("SELECT * FROM mstr_service WHERE c_id = %s", (category_id,))
        data = cur.fetchall()

        return render(request, "services.html", {"data": data, "category_name": c_name, "username": username})


""" 
class select_provider(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name= 'select_provider.html')

    def post(self, request, *args, **kwargs):
        
        service_id = request.POST.get("service_id")
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_service where s_id = %s",(service_id,))
        service_data = cur.fetchone()
        
        print("---------------------->  SERVI : ",service_data)
        
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select service_provider_id from service_provider_services where s_id = %s",(service_id,))
        data = cur.fetchall()
        
        cur.execute("select price from service_provider_services where s_id = %s",(service_id,))
        price = cur.fetchone()

        if data:
            service_provider_id = data[0][0]  
            cur.execute("SELECT id, username, email, phone FROM mstr_service_provider WHERE id = %s", (service_provider_id,))
            sp_data = cur.fetchall()

        #print("------------------------->  DATA : ",sp_data)

        return render(request, "select_provider.html",
                      context={"data":sp_data,
                               "service_id":service_data[0],
                               "service_name":service_data[2],
                               "service_description":service_data[3],
                               "service_image":service_data[4],
                               "price":price}) """


class select_provider(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        if username is None:
            return redirect('login')
        return render(request, 'select_provider.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        user_id = request.session.get('user_id', None)
        location_id = request.session.get('location_id', None)
        
        service_id = request.POST.get("service_id")

        if username is None:
            return redirect('login')
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_service where s_id = %s", (service_id,))
        service_data = cur.fetchone()
        
        print("---------------------->  SERVI : ", service_data)
        
    
        sp_data = None 

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select service_provider_id from service_provider_services where s_id = %s", (service_id,))
        data = cur.fetchall()
        
        cur.execute("select price from service_provider_services where s_id = %s", (service_id,))
        price = cur.fetchone()

        
        if data:
            service_provider_id = data[0][0]
            cur.execute("SELECT id, first_name, email, phone FROM mstr_service_provider WHERE id = %s and location_id = %s", (service_provider_id,location_id))
            sp_data = cur.fetchall()

        
        if not sp_data:
            sp_data = []

        return render(request, "select_provider.html", 
                      context={"data": sp_data,
                               "service_id": service_data[0],
                               "service_name": service_data[2],
                               "service_description": service_data[3],
                               "service_image": service_data[4],
                               "price": price,
                               "username":username})

class subscription(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        return render(request, template_name= 'subscription.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get('username', None)

        if username is None:
            return redirect('login')

        sp_id = request.POST.get("sp_id")
        service_id = request.POST.get("service_id")

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_service where s_id = %s", (service_id,))
        service_data = cur.fetchone()

        print("---------------------->  SERVI : ", service_data)

        sp_data = None 

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select service_provider_id from service_provider_services where s_id = %s", (service_id,))
        data = cur.fetchall()

        cur.execute("select price from service_provider_services where s_id = %s", (service_id,))
        price = cur.fetchone()

        if data:
            service_provider_id = data[0][0]
            cur.execute("SELECT id, first_name, email, phone FROM mstr_service_provider WHERE id = %s", (service_provider_id,))
            sp_data = cur.fetchone()

        print("provider name : ",sp_data)

        if not sp_data:
            sp_data = []

        return render(request, "subscription.html", 
                      context={"data": sp_data,
                               "service_id": service_data[0],
                               "service_name": service_data[2],
                               "service_description": service_data[3],
                               "price": price,
                               "username":username})

        return render(request, "subscription.html")

class add_to_cart(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        return render(request, template_name= 'add_to_cart.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        if username is not None:
            sp_id = request.POST.get("sp_id")
            service_id = request.POST.get("service_id")

            conn = create_connection()
            cur = conn.cursor()
            cur.execute("select * from mstr_service where s_id = %s",(service_id,))
            service_data = cur.fetchone()

            cur.execute("select * from service_provider_services where s_id = %s",(service_id,))
            price = cur.fetchone()

            cur.execute("select * from mstr_service_provider where id = %s",(sp_id,))
            sp_data = cur.fetchone()

            return render(request, "add_to_cart.html",{"sp_data":sp_data,"service_data":service_data,"price":price, "username":username})
        else:
            return redirect('login')


""" 
class payment(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name= 'payment.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        user_id = request.session.get('user_id', None)

        start_date = request.POST.get("startdate")
        end_date = request.POST.get("enddate")
        price = request.POST.get("price")

        service_id = request.POST.get("service_id")
        sp_id = request.POST.get("sp_id")

        date = request.POST.get("date")
        time = request.POST.get("time")
        address = request.POST.get("address")
        
        if start_date and end_date is not None:

            pass

        #print("DATA : ", service_id, " ", sp_id , " ", date , " ", time , " ", address)

        return render(request, 'payment.html', context={
                'sp_id': sp_id,
                'service_id': service_id,
                'address': address,
                "date":date,
                "time":time,
                "username":username}) """



class payment(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        return render(request, template_name='payment.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        user_id = request.session.get('user_id', None)

        start_date_str = request.POST.get("startdate")
        end_date_str = request.POST.get("enddate")
        price_str = request.POST.get("price")
        service_id = request.POST.get("service_id")
        sp_id = request.POST.get("sp_id")
        date = request.POST.get("date")
        time = request.POST.get("time")
        address = request.POST.get("address")
        username = request.session.get("username")
        
        if not username:
            return redirect('login')

        if start_date_str and end_date_str and price_str:
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            price = float(price_str)

            total_days = (end_date - start_date).days
            total_amount = total_days * price

        else:
            total_days = 0
            total_amount = 0

        return render(request, 'payment.html', context={
            'sp_id': sp_id,
            'service_id': service_id,
            'address': address,
            'date': date,
            'time': time,
            'username': username,
            'start_date': start_date_str,
            'end_date':end_date_str,
            'total_amount': total_amount,
        })


class confirm_payment(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        return render(request, 'confirm_payment.html')
    
    def post(self, request, *args, **kwargs):
        
        user_id = request.session.get('user_id', None)
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        sp_id = request.POST.get("sp_id")
        service_id = request.POST.get("service_id")
        address = request.POST.get("address")
        
        date = request.POST.get("date")
        time = request.POST.get("time")
        
        start_date = request.POST.get("startdate")
        end_date = request.POST.get("enddate")
        total_amount = request.POST.get("total_amount")
        
        print(start_date," ",end_date," ",total_amount)
        
        
        if start_date and end_date is not None:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("select id from service_provider_services where service_provider_id = %s and s_id = %s",(sp_id, service_id))
            sp_service_id = cur.fetchone()
            
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("""insert into subscriptions (user_id, sp_id, p_service_id, from_date, to_date, address, total_amount) 
                            values (%s, %s, %s, %s, %s, %s, %s)""", (int(user_id), int(sp_id), int(sp_service_id[0]), start_date, end_date, address, float(total_amount) ))
                conn.commit()
                cur.close()
                
                return render(request,"confirm_payment.html")

            except Exception as e:
                print("Error white adding order : ",e)
            
        
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select id, price from service_provider_services where service_provider_id = %s and s_id = %s", (sp_id,service_id))
        sp_service_id = cur.fetchone()

        print("time ", time)

        try:
            cur = conn.cursor()
            cur.execute("""insert into orders (user_id, sp_id, p_service_id, address, bill_amount, datetime, booking_date, booking_time, status) 
                        values (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)""", (int(user_id), int(sp_id), int(sp_service_id[0]), address, int(sp_service_id[1]),date,time,"initiated" ))
            conn.commit()
            cur.close()

            return render(request,"confirm_payment.html")
            
        except Exception as e:
            print("Error white adding order : ",e)

        return render(request, 'confirm_payment.html')

class orders(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        user_id = request.session.get('user_id', None)
        username = request.session.get("username",None)
        if not username:
            return redirect('login')
        
        if username and user_id is not None:
        
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("select * from orders where user_id = %s",(user_id,))
            data = cur.fetchall()

            orders = []
            for row in data:
                sp_id = row[2]
                cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                sp_name = cur.fetchone()

                if sp_name:
                    sp_service_id = row[3]

                    cur.execute("SELECT s_id FROM service_provider_services WHERE id = %s", (sp_service_id,))
                    s_id = cur.fetchone()

                    cur.execute("SELECT * FROM mstr_service WHERE s_id = %s", (s_id[0],))
                    service_name = cur.fetchone()

                    order_info = {
                        "order": row,
                        "sp_name": sp_name[0] if sp_name else "Unknown",
                        "service_name": service_name[2] if service_name else "Unknown"
                    }
                    orders.append(order_info)

            return render(request, 'orders.html', context={"orders":orders,"username":username})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        return render(request, 'orders.html')

class user_subscriptions(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        user_id = request.session.get('user_id', None)
        
        if not username:
            return redirect('login')
        
        subscriptions = []

        if username and user_id:
            if user_id:
                print("USER_ID : ", user_id)
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM subscriptions where user_id = %s", (user_id,))
                data = cur.fetchall()

                print("----------------------->  DATA : ", data)

                for row in data:
                    user_id = row[1]
                    cur.execute("SELECT first_name FROM mstr_user WHERE id = %s", (user_id,))
                    cust_name = cur.fetchone()

                    if cust_name:
                        s_id = row[3]
                        cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                        service_name = cur.fetchone()

                        service_id = row[3]  
                        cur.execute("SELECT service_provider_id, s_id FROM service_provider_services WHERE id = %s", (service_id,))
                        sp = cur.fetchone()

                        sp_id, s_id = sp
                        cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                        sp_name = cur.fetchone()

                        cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                        service_name = cur.fetchone()

                        subscription_info = {
                            "subscription": row,
                            "service_name": service_name[0] if service_name else "Unknown",
                            "sp_name": sp_name[0] if sp_name else "Unknown"
                        }

                        subscriptions.append(subscription_info)

                print("----------------------->  Subscriptions : ", subscriptions)
            else:
                print("No service provider found with the given username and password.")
        else:
            return redirect('login')

        return render(request, 'user_subscriptions.html', context={"subscriptions":subscriptions,"username":username})

            
        #return render(request, 'user_subscriptions.html')
    def post(self, request, *args, **kwargs):
        return render(request, 'user_subscriptions.html')

class signup(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name= 'signup.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        password = request.POST.get("password")
        usertype = request.POST.get("usertype")
        
        print(username)
        
        if usertype == "customer":
            is_sp = 0
        else: is_sp = 1
        
        conn = create_connection()
        
        cur = conn.cursor()
        cur.execute("select id,city_name from mstr_location where city_name = %s",(city,))
        d = cur.fetchone()
        
        if d is not None:
            l_id = d[0]
        else:
            cur = conn.cursor()
            q = """INSERT INTO mstr_location 
            (city_name) values (%s); """
            cur.execute(q,(city,))
            conn.commit()

            cur.execute("select id,city_name from mstr_location where city_name = %s",(city,))
            d = cur.fetchone()
            
            l_id = d[0]

        if is_sp == 1:
            cur = conn.cursor()
            q = """INSERT INTO mstr_service_provider 
            (username, first_name, last_name, email, phone, password, location_id, is_service_provider) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s); """
            cur.execute(q,(username,first_name,last_name,email,phone,password,l_id,is_sp))
            conn.commit()
        else:
            cur = conn.cursor()
            q = """INSERT INTO mstr_user
            (username, first_name, last_name, email, phone, password, location_id, is_service_provider) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s); """
            cur.execute(q,(username,first_name,last_name,email,phone,password,l_id,is_sp))
            conn.commit()
            
        request.session['username'] = username
        request.session['password'] = password

        return render(request, template_name= 'signup.html')

class login(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name= 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if both username and password are provided
        if username and password:
            conn = create_connection()
            cur = conn.cursor()

            cur.execute("SELECT username, password FROM mstr_admin WHERE username=%s AND password=%s", (username, password))
            admin = cur.fetchone()
            if admin is not None:
                return redirect('admin_dashboard')

            cur.execute("SELECT username, password FROM mstr_service_provider WHERE username=%s AND password=%s", (username, password))
            service_provider = cur.fetchone()

            if service_provider is not None:
                request.session['username'] = username
                request.session['password'] = password
                
                cur = conn.cursor()
                cur.execute("select id from mstr_service_provider where username=%s and password=%s", (username, password))
                sp_id = cur.fetchone()
                
                request.session["user_id"] = sp_id[0]
                
                return redirect('sp_orders')

            cur.execute("SELECT username, password FROM mstr_user WHERE username=%s AND password=%s", (username, password))
            user = cur.fetchone()

            if user is not None:
                request.session['username'] = username
                request.session['password'] = password
                
                cur = conn.cursor()
                cur.execute("select id, location_id from mstr_user where username=%s and password=%s", (username, password))
                user_id = cur.fetchone()
                
                request.session["user_id"] = user_id[0]
                request.session["location_id"] = user_id[1]
                                
                return redirect('home_page')

        return render(request, 'login.html')

class sp_orders(View):
    def get(self, request, *args, **kwargs):
        conn = create_connection()
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        
        if not username:
            return redirect('login')

        sp_id = request.session.get('user_id', None)
        orders = []

        if username and password:
            if sp_id:
                print("SP_ID : ", sp_id)
                
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM orders where sp_id = %s ORDER BY datetime DESC", (sp_id,))
                data = cur.fetchall()

                print("----------------------->  DATA : ", data)

                for row in data:
                    user_id = row[1]
                    cur.execute("SELECT first_name FROM mstr_user WHERE id = %s", (user_id,))
                    cust_name = cur.fetchone()


                    if cust_name:
                        s_id = row[3]
                        cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                        service_name = cur.fetchone()

                        order_info = {
                            "order": row,
                            "customer_name": cust_name[0] if cust_name else "Unknown",
                            "service_name": service_name[0] if service_name else "Unknown"
                        }
                        orders.append(order_info)

                print("----------------------->  Orders: ", orders)
            else:
                print("No service provider found with the given username and password.")
        else:
            print("Username or password is missing.")

        return render(request, 'sp_orders.html', context={"orders":orders})

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("update orders set status = %s where id = %s",("Complete",order_id))
        
        return redirect('sp_orders')


class sp_order_details(View):
    def get(self, request, *args, **kwargs):
        
        username = request.session.get("username")
        if not username:
            return redirect('login')
        return render(request, 'admin_order_details.html')

    def post(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        order_id = request.POST.get("order_id")

        conn = create_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM orders where id = %s",(order_id,))
        data = cur.fetchall()

        print("----------------------->  DATA : ",data)

        orders = []

        for row in data:
            user_id = row[1]
            cur.execute("SELECT first_name, email, phone FROM mstr_user WHERE id = %s", (user_id,))
            cust_details = cur.fetchone()

            service_id = row[3]  
            cur.execute("SELECT service_provider_id, s_id FROM service_provider_services WHERE id = %s", (service_id,))
            sp = cur.fetchone()

            if sp:
                sp_id, s_id = sp
                cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                sp_name = cur.fetchone()
                
                cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                service_name = cur.fetchone()
                
                order_info = {
                    "order": row,
                    "cust_details": cust_details if cust_details else "Unknown",
                    "sp_name": sp_name if sp_name else "Unknown",
                    "service_name": service_name if service_name else "Unknown"
                }
                orders.append(order_info)
        
        return render(request, 'sp_order_details.html', context={"orders":orders})


class sp_subscriptions(View):
    def get(self, request, *args, **kwargs):
        
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        conn = create_connection()
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        sp_id = request.session.get('user_id', None)
        
        subscriptions = []
        if username and password:
            if sp_id:
                print("SP_ID : ", sp_id)
                
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM subscriptions where sp_id = %s", (sp_id,))
                data = cur.fetchall()

                print("----------------------->  DATA : ", data)

                for row in data:
                    user_id = row[1]
                    cur.execute("SELECT first_name FROM mstr_user WHERE id = %s", (user_id,))
                    cust_name = cur.fetchone()

                    if cust_name:
                        s_id = row[3]
                        cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                        service_name = cur.fetchone()
                        
                        service_id = row[3]  
                        cur.execute("SELECT service_provider_id, s_id FROM service_provider_services WHERE id = %s", (service_id,))
                        sp = cur.fetchone()
                     
                        sp_id, s_id = sp
                        cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                        sp_name = cur.fetchone()
                        
                        cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                        service_name = cur.fetchone()


                        subscription_info = {
                            "subscription": row,
                            "customer_name": cust_name[0] if cust_name else "Unknown",
                            "service_name": service_name[0] if service_name else "Unknown",
                            "sp_name": sp_name[0] if sp_name else "Unknown"
                        }
                        
                        subscriptions.append(subscription_info)

                print("----------------------->  Subscriptions : ", subscriptions)
            else:
                print("No service provider found with the given username and password.")
        else:
            print("Username or password is missing.")

        return render(request, 'sp_subscriptions.html', context={"subscriptions":subscriptions})

        #return render(request, 'sp_subscriptions.html')

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        
        return render(request, 'sp_subscriptions.html')

class sp_services(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from service_provider_services")
        data = cur.fetchall()

        services_with_category = []
        for row in data:
            c_id = row[2]  
            cur.execute("select c_name from mstr_category where c_id = %s", (c_id,))
            c_name = cur.fetchone()  

            s_id = row[3]
            cur.execute("select s_name, s_description, s_image from mstr_service where s_id = %s", (s_id,))
            sp_service = cur.fetchone()

            if c_name:
                services_with_category.append((row, c_name[0], sp_service))

        print("----------------------->  DATA : ", services_with_category)

        return render(request, template_name='sp_services.html', context={"data": services_with_category})



    def post(self, request, *args, **kwargs):
        
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        sp_id = request.session.get('user_id', None)
        
        edit = request.POST.get("edit")
        if edit:
            print("EDIT")
            return redirect('sp_edit_service',service_id = int(edit))


        delete = request.POST.get("delete")

        if delete:
            print("DELETE")

            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("select p_service_id from orders where p_service_id = %s and sp_id = %s",(int(delete),sp_id))
                d = cur.fetchall()
                if len(d) > 0:
                    return HttpResponse("Service is being used by customers can not be deleted")
                else:
                    cur = conn.cursor()
                    cur.execute("delete from service_provider_services where id = %s",(int(delete),))
                    conn.commit()

                    return redirect('sp_services')
            except Exception as e:
                print(f"Error: {e}")

# class sp_add_service(View):
#     def get(self, request, *args, **kwargs):
        
#         username = request.session.get("username")
#         if not username:
#             return redirect('login')

#         sp_service_id = kwargs.get("service_id")

#         conn = create_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT c_id, s_id, price FROM service_provider_services")
#         sp_services = cur.fetchall()

#         if len(sp_services) > 0:
#             service_data = sp_services[0]
#             print("sp_services[0]: ", service_data)
#             print("Service ID: ", service_data[0])  
#             print("Service Name: ", service_data[1])  
#             print("Price: ", service_data[2])
#         else:
#             print("No services available for this category.")


#         sp_services = [list(category) for category in sp_services]
#         print("sp_services[1] : ", sp_services)

#         print("sp_services[1] : ", service_data[1])

#         conn = create_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT c_id, c_name FROM mstr_category")
#         categories = cur.fetchall()

#         cur.execute("SELECT s_id FROM service_provider_services WHERE id = %s", (sp_service_id,))
#         service = cur.fetchone()
        
#         category_name = "No category found"

        
#         if service:
#             cat_id = service_data[0]
#             print("Service Category ID: ", cat_id)
        
#             cur.execute("SELECT c_name FROM mstr_category WHERE c_id = %s", (cat_id,))
#             category_name = cur.fetchone()
#             print("Category Name:", category_name)


#         categories = [list(category) for category in categories]

#         print("------------------->  CATEGORIES : ", categories[0])

#         conn.close()
        
#         return render(request, 'sp_add_service.html', context={
#             "categories": categories,
#             "service": service,
#             "cat_name": category_name[0] if category_name else "No category found",
#             "price": service_data[2] if service_data else "No service available",
#         })


#     def post(self, request, *args, **kwargs):
        
#         username = request.session.get("username")
#         if not username:
#             return redirect('login')
        
#         service_id = request.POST.get("sp_service_id")
        
#         sp_id = request.session.get('user_id', None)

#         if service_id:

#             s_id = request.POST.get("service_id")
#             c_id = request.POST.get("category_id")
#             price = request.POST.get("price")

#             try:
#                 conn = create_connection()
#                 cur = conn.cursor()
#                 cur.execute("""
#                     update service_provider_services set s_id = %s, c_id = %s, price = %s
#                     where s_id = %s
#                 """, [int(s_id), int(c_id), int(price), service_id])
#                 conn.commit()
#                 return redirect('sp_services')
#             except Exception as e:
#                 print(f"Error: {e}")


#         category_id = request.POST.get("category_id")
#         service_id = request.POST.get("service_id")
#         price = request.POST.get("price")

#         try:
#             conn = create_connection()
#             cur = conn.cursor()
            
#             cur.execute("""
#                 INSERT INTO service_provider_services (service_provider_id, c_id, s_id, price)
#                 VALUES (%s, %s, %s, %s)
#             """, [int(sp_id), int(category_id), int(service_id), int(price)])
            
#             conn.commit()
#             return redirect('sp_services')

#         except Exception as e:
#             print(f"Error: {e}")
#             return render(request, 'sp_add_service.html', {'message': 'An error occurred while adding the category'})


class sp_add_service(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')

        sp_service_id = kwargs.get("service_id")

        conn = create_connection()
        cur = conn.cursor()

        cur.execute("SELECT c_id, s_id, price FROM service_provider_services")
        sp_services = cur.fetchall()

        if len(sp_services) > 0:
            service_data = sp_services[0]
        else:
            service_data = [None, None, None]  # Default values to avoid UnboundLocalError

        sp_services = [list(category) for category in sp_services]

        cur.execute("SELECT DISTINCT c_id, c_name FROM mstr_category")
        categories = cur.fetchall()
        
        cur.execute("SELECT s_id FROM service_provider_services WHERE id = %s", (sp_service_id,))
        service = cur.fetchone()
        
        category_name = "No category found"
        if service:
            cat_id = service_data[0]
            cur.execute("SELECT c_name FROM mstr_category WHERE c_id = %s", (cat_id,))
            category = cur.fetchone()
            if category:
                category_name = category[0]
        
        categories = [list(category) for category in categories]
        
        conn.close()
        
        return render(request, 'sp_add_service.html', context={
            "categories": categories,
            "service": service,
            "cat_name": category_name,
            "price": service_data[2] if service_data[2] is not None else "No service available",
        })

    def post(self, request, *args, **kwargs):
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        service_id = request.POST.get("sp_service_id")
        sp_id = request.session.get('user_id', None)

        if service_id:
            s_id = request.POST.get("service_id")
            c_id = request.POST.get("category_id")
            price = request.POST.get("price")

            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE service_provider_services 
                    SET s_id = %s, c_id = %s, price = %s
                    WHERE s_id = %s
                """, [int(s_id), int(c_id), int(price), service_id])
                conn.commit()
                conn.close()
                return redirect('sp_services')
            except Exception as e:
                print(f"Error: {e}")

        category_id = request.POST.get("category_id")
        service_id = request.POST.get("service_id")
        price = request.POST.get("price")

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO service_provider_services (service_provider_id, c_id, s_id, price)
                VALUES (%s, %s, %s, %s)
            """, [int(sp_id), int(category_id), int(service_id), int(price)])
            conn.commit()
            conn.close()
            return redirect('sp_services')
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'sp_add_service.html', {'message': 'An error occurred while adding the category'})



class fetch_services(View):
    def get(self, request, *args, **kwargs):
        
        username = request.session.get("username")
        if not username:
            return redirect('login')
        
        category_id = request.GET.get('category_id')

        if category_id:
            conn = create_connection()
            cur = conn.cursor()

            # Fetch services based on category
            cur.execute("SELECT s_id, s_name FROM mstr_service WHERE c_id = %s", [category_id])
            services = cur.fetchall()

            conn.close()

            return JsonResponse({'services': services})
        return JsonResponse({'services': []})




#-----------------------------  ADMIN VIEWS  -----------------------------------------


def handle_uploaded_file(f):
    
    filename = f.name
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
    
    print("PATH : ",file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return file_path  


class admin_dashboard(View):
    def get(self, request, *args, **kwargs):
        conn = create_connection()
        
        cur = conn.cursor()
        cur.execute("select count(id) from mstr_service_provider")
        sp = cur.fetchone()
        
        cur.execute("select count(id) from orders")
        orders = cur.fetchone()
        
        cur.execute("select count(id) from mstr_user")
        users = cur.fetchone()
        
        print("SP : ",sp)
        print("ORDERS : ",orders)
        print("USERS : ",users)

        return render(request, template_name= 'admin_dashboard.html', context={"service_providers":sp, "orders": orders, "users":users})

class admin_categories(View):
    def get(self, request, *args, **kwargs):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_category")
        data = cur.fetchall()
        print("----------------------->  DATA : ",data)
        return render(request, template_name= 'admin_categories.html', context={"data":data})
    
    def post(self, request, *args, **kwargs):
        edit = request.POST.get("edit")
        if edit:
            print("EDIT")
            return redirect('admin_edit_category',category_id = int(edit))

        delete = request.POST.get("delete")
        if delete:
            print("DELETE")
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("select c_id from mstr_service where c_id = %s",(int(delete),))
                d = cur.fetchall()
                print("----------------->> DELETE CAT : ",d)
                if len(d) > 0:
                    return HttpResponse("Category is being used can not be deleted")
                else:
                    cur = conn.cursor()
                    cur.execute("delete from mstr_category where c_id = %s",(int(delete),))
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")

        return redirect('admin_categories')

class admin_services(View):
    def get(self, request, *args, **kwargs):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_service")
        data = cur.fetchall()

        services_with_category = []
        for row in data:
            c_id = row[1]  
            cur.execute("select c_name from mstr_category where c_id = %s", (c_id,))
            c_name = cur.fetchone()  
            if c_name:
                services_with_category.append((row, c_name[0]))

        print("----------------------->  DATA : ", services_with_category)

        return render(request, template_name='admin_services.html', context={"data": services_with_category})

    def post(self, request, *args, **kwargs):
        edit = request.POST.get("edit")
        if edit:
            print("EDIT")
            return redirect('admin_edit_services',service_id = int(edit))
        
        
            """ conn = create_connection()
            cur = conn.cursor()
            
            cur.execute("select * from mstr_service where s_id = %s",(edit,))
            service = cur.fetchone()
            
            cur.execute("select * from mstr_category where c_id = %s",(service[1],))
            category_name = cur.fetchone()
            
            cur.execute("select * from mstr_category")
            category = cur.fetch_all() """
            
            
            
            return render(request,'admin_add_service.html',context={"service":service,"category":category,"category_name":category_name})
        
        delete = request.POST.get("delete")
        if delete:
            print("DELETE")

            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("select s_id from service_provider_services where s_id = %s",(int(delete),))
                d = cur.fetchall()
                if d is not None:
                    return HttpResponse("Service is being used can not be deleted")
                else:
                    cur = conn.cursor()
                    cur.execute("delete from mstr_service where s_id = %s",(int(delete),))
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
            
            
        return redirect('admin_services')

class admin_service_providers(View):
    def get(self, request, *args, **kwargs):

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_service_provider")
        data = cur.fetchall()
        print("----------------------->  DATA : ",data)

        sp = []
        for row in data:
            l_id = row[7]
            
            cur.execute("select city_name from mstr_location where id = %s", (l_id,))
            city_name = cur.fetchone()  

            if city_name:
                sp.append((row, city_name[0]))


        return render(request, template_name= 'admin_sp.html', context={"data":sp})

class admin_orders(View):
    def get(self, request, *args, **kwargs):
        conn = create_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM orders")
        data = cur.fetchall()
        
        print("----------------------->  DATA : ",data)

        orders = []
        
        for row in data:
            user_id = row[1]
            cur.execute("SELECT first_name FROM mstr_user WHERE id = %s", (user_id,))
            cust_name = cur.fetchone()
            
            service_id = row[3]  
            cur.execute("SELECT service_provider_id, s_id FROM service_provider_services WHERE id = %s", (service_id,))
            sp = cur.fetchone()
            
            if sp:
                sp_id, s_id = sp
                cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                sp_name = cur.fetchone()
                
                cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                service_name = cur.fetchone()
                
                order_info = {
                    "order": row,
                    "customer_name": cust_name[0] if cust_name else "Unknown",
                    "service_provider_name": sp_name[0] if sp_name else "Unknown",
                    "service_name": service_name[0] if service_name else "Unknown"
                }
                orders.append(order_info)
        
        print("----------------------->  Orders: ", orders)
        return render(request, 'admin_orders.html', context={"orders": orders})

class admin_subscriptions(View):
    def get(self, request, *args, **kwargs):
        
        conn = create_connection()
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        sp_id = request.session.get('user_id', None)
        
        subscriptions = []
        
        
            
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM subscriptions")
        data = cur.fetchall()

        print("----------------------->  DATA : ", data)

        for row in data:
            user_id = row[1]
            cur.execute("SELECT first_name FROM mstr_user WHERE id = %s", (user_id,))
            cust_name = cur.fetchone()

            if cust_name:
                s_id = row[3]
                cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                service_name = cur.fetchone()
                
                service_id = row[3]  
                cur.execute("SELECT service_provider_id, s_id FROM service_provider_services WHERE id = %s", (service_id,))
                sp = cur.fetchone()
                
                sp_id, s_id = sp
                cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                sp_name = cur.fetchone()
                
                cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                service_name = cur.fetchone()


                subscription_info = {
                    "subscription": row,
                    "customer_name": cust_name[0] if cust_name else "Unknown",
                    "service_name": service_name[0] if service_name else "Unknown",
                    "sp_name": sp_name[0] if sp_name else "Unknown"
                }

                subscriptions.append(subscription_info)

        print("----------------------->  Subscriptions : ", subscriptions)



        return render(request, 'admin_subscriptions.html', context={"subscriptions":subscriptions})

        #return render(request, 'sp_subscriptions.html')

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        
        return render(request, 'admin_subscriptions.html')

class admin_customers(View):
    def get(self, request, *args, **kwargs):
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from mstr_user")
        data = cur.fetchall()
        print("----------------------->  DATA : ",data)
        
        user = []
        for row in data:
            l_id = row[7]
            
            cur.execute("select city_name from mstr_location where id = %s", (l_id,))
            city_name = cur.fetchone()  

            if city_name:
                user.append((row, city_name[0]))
        
        return render(request, template_name= 'admin_customers.html', context={"data":user})
    
class admin_add_category(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get("category_id")
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mstr_category WHERE c_id = %s", [category_id])
        category = cur.fetchone()

        print("-----------------------> Category : ", category)
        
        return render(request, 'admin_add_category.html', context={"categories": category})


    def post(self, request, *args, **kwargs):
        
        category_id = request.POST.get("category_id")
        
        if category_id:
            name = request.POST.get("name")
            description = request.POST.get("description")
            image = request.FILES.get("image")  

            file_path = handle_uploaded_file(image)
            filename = image.name
            
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("""
                    update mstr_category set c_name = %s,  c_description = %s, c_image = %s
                    where c_id = %s
                """, [name, description, filename, category_id])
                conn.commit()
                return redirect('admin_categories')
            except Exception as e:
                print(f"Error: {e}")
        

        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        file_path = handle_uploaded_file(image)
        filename = image.name
        
        print(filename)

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO mstr_category (c_name, c_description, c_image)
                VALUES (%s, %s, %s)
            """, (name, description, filename))

            create_connection().commit()

            return render(request, 'admin_add_category.html', {'message': 'Category added successfully'})

        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'admin_add_category.html', {'message': 'An error occurred while adding the category'})
    
class admin_add_service(View):
    def get(self, request, *args, **kwargs):
        service_id = kwargs.get("service_id")
        
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mstr_category")
        categories = cur.fetchall()
        

        category_name = ""

        cur.execute("SELECT * FROM mstr_service WHERE s_id = %s", [service_id])
        service = cur.fetchone()

        if service:
            cat_id = service[1]
            print("Service Category ID: ", cat_id)
        
            cur.execute("SELECT c_name FROM mstr_category WHERE c_id = %s", [cat_id])
            category_name = cur.fetchone()
            print("Category Name:", category_name)

        print("-----------------------> Categories: ", categories)
        print("-----------------------> Service: ", service)
        
        return render(request, 'admin_add_service.html', context={
            "categories": categories,
            "service": service,
            "cat_name": category_name[0] if category_name else "Select Category"
        })


    def post(self, request, *args, **kwargs):
        
        service_id = request.POST.get("service_id")
        
        if service_id:
            name = request.POST.get("name")
            description = request.POST.get("description")
            image = request.FILES.get("image")  
            category = request.POST.get("category")
            
            file_path = handle_uploaded_file(image)
            filename = image.name
            
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute("""
                    update mstr_service set s_name = %s, c_id = %s, s_description = %s, s_image = %s
                    where s_id = %s
                """, [name, int(category), description, filename, service_id])
                conn.commit()
                return redirect('admin_services')
            except Exception as e:
                print(f"Error: {e}")
        
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get("image")  
        category = request.POST.get("category")

        file_path = handle_uploaded_file(image)
        filename = image.name
        
        print(filename)

        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO mstr_service (s_name, c_id, s_description, s_image)
                VALUES (%s, %s, %s, %s)
            """, [name, int(category), description, filename])
            conn.commit()
            return redirect('admin_services')

        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'admin_add_service.html', {'message': 'An error occurred while adding the category'})

class admin_sp_services(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin_sp_services.html')

    
    def post(self, request, *args, **kwargs):
        
        sp_id = request.POST.get("sp_id")
        conn = create_connection()
        cur = conn.cursor() 
        cur.execute("select * from service_provider_services where service_provider_id = %s",(sp_id,))
        data = cur.fetchall()
        
        print("------------------------>  DATA : ",data)
        services = []
        for row in data:
            sp_id = row[1]
            cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
            sp_name = cur.fetchone()
            
            category_id = row[2]
            cur.execute("SELECT c_name FROM mstr_category WHERE c_id = %s", (category_id,))
            category_name = cur.fetchone()
            
            service_id = row[3]
            cur.execute("SELECT s_name, s_description, s_image FROM mstr_service WHERE s_id = %s", (service_id,))
            service_details = cur.fetchone()


            service_info = {
                "service": row,
                "sp_name": sp_name,
                "category_name": category_name,
                "service_details":service_details
            }
            services.append(service_info)
            
        
        return render(request, 'admin_sp_services.html', context={"services":services})
    
class admin_order_details(View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'admin_order_details.html')
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id")
        
        conn = create_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM orders where id = %s",(order_id,))
        data = cur.fetchall()
        
        print("----------------------->  DATA : ",data)

        orders = []
        
        for row in data:
            user_id = row[1]
            cur.execute("SELECT first_name, email, phone FROM mstr_user WHERE id = %s", (user_id,))
            cust_details = cur.fetchone()
            
            service_id = row[3]  
            cur.execute("SELECT service_provider_id, s_id FROM service_provider_services WHERE id = %s", (service_id,))
            sp = cur.fetchone()

            if sp:
                sp_id, s_id = sp
                cur.execute("SELECT first_name FROM mstr_service_provider WHERE id = %s", (sp_id,))
                sp_name = cur.fetchone()
                
                cur.execute("SELECT s_name FROM mstr_service WHERE s_id = %s", (s_id,))
                service_name = cur.fetchone()
                
                order_info = {
                    "order": row,
                    "cust_details": cust_details if cust_details else "Unknown",
                    "sp_name": sp_name if sp_name else "Unknown",
                    "service_name": service_name if service_name else "Unknown"
                }
                orders.append(order_info)
        
        return render(request, 'admin_order_details.html', context={"orders":orders})