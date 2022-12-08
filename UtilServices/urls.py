from django.urls import path
from UtilServices import views
from UtilServices.views import *
from django.contrib.auth import views as auth_views
from .forms import *

urlpatterns = [
    path('',ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    
    
    path('cart/',views.show_cart,name='showcart'),
    path('buy/', views.buy_now, name='buy-now'),
    
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('paymentdone', views.payment_done, name='paymmentdone'),

    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('laptop/',views.laptop,name="laptop"),

    path('accounts/login/',auth_views.LoginView.as_view(
        template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(
        template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,
    success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(
        template_name='app/passwordchangedone.html'
    ),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='app/password_reset.html',
        form_class=MyPasswordResetForm
    ),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm
    ),name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ),name='password_reset_complete'),

    path('checkout/', views.checkout, name='checkout'),
    path('registration/',CustomerRegistrationView.as_view(),name="customerregistration"),

    #profile url
    path('profile/', ProfileView.as_view(), name='profile'),

    
] 
