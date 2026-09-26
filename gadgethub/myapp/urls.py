
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path("login_get/",views.login_get),
    path("logout_get/",views.logo_out),
    path("login_post/",views.login_post),
    path("admin_add_category_get/",views.admin_add_category_get),
    path("admin_add_category_post/", views.admin_add_category_post),
    path("admin_change_password/",views.admin_change_password),
    path("admin_change_password_post/",views.admin_change_password_post),
    path("admin_delete_category/<id>",views.admin_delete_category),
    path("admin_edit_category/<id>",views.admin_edit_category),
    path("admin_edit_category_post/",views.admin_edit_category_post),
    path("admin_sentreplay/<id>", views.admin_sentreplay),
    path("admin_sentreplay_post/",views.admin_sentreplay_post),
    path("admin_view_approved_seller/",views.admin_view_approved_seller),
    path("admin_view_products/",views.admin_view_products),
    path("admin_view_users/",views.admin_view_users),
    path("admin_viewcomplaint/",views.admin_viewcomplaint),
    path("admin_viewreviews/",views.admin_viewreviews),
    path("admin_viewsellers_and_approve_reject/",views.admin_viewsellers_and_approve_reject),
    path("admin_viewcategory/",views.admin_viewcategory),
    path("admin_home/",views.admin_home),
    path("admin_approve_sellers/<id>/",views.admin_approve_sellers),
    path("admin_reject_sellers/<id>/",views.admin_reject_sellers),
    path("admin_view_product/<id>/",views.admin_view_product),
    path("admin_view_stock_get/<id>/",views.admin_view_stock_get),



    #####sellers
    path("sellers_register_get/",views.sellers_register_get),
    path("sellers_register_post/",views.sellers_register_post),
    path("sellers_home/",views.sellers_home),
    path("seller_profile/",views.seller_profile),
    path("seller_edit_profile_get/",views.seller_edit_profile_get),
    path("seller_edit_profile_post/",views.seller_edit_profile_post),
    path("seller_add_product_get/",views.seller_add_product_get),
    path("seller_add_product_post/",views.seller_add_product_post),
    path("sellers_view_product_get/",views.sellers_view_product_get),
    path("sellers_delete_product/<id>/",views.sellers_delete_product),
    path("sellers_edit_product_get/<id>/",views.sellers_edit_product_get),
    path("sellers_edit_product_post/",views.sellers_edit_product_post),
    path("sellers_add_stock_get/<id>",views.sellers_add_stock_get),
    path("sellers_edit_stock_get/<id>",views.sellers_edit_stock_get),
    path("sellers_edit_stock_post/",views.sellers_edit_stock_post),
    path("seller_view_compliant_replay/",views.seller_view_compliant_replay),
    path("seller_sent_compliant_get/",views.seller_sent_compliant_get),
    path("seller_sent_complaint/",views.seller_sent_complaint),
    path("seller_sent_review_get/",views.seller_sent_review_get),
    path("seller_view_offers_get/<id>",views.seller_view_offers_get),
    path("seller_view_offers_get/<id>",views.seller_view_offers_get),
    path("sellers_add_offer_post/",views.sellers_add_offer_post),
    path("sellers_add_offer_get/<id>",views.sellers_add_offer_get),
    path("sellers_edit_offer_get/<id>",views.sellers_edit_offer_get),
    path("sellers_edit_offer_post/",views.sellers_edit_offer_post),
    path("seller_change_password_get/",views.seller_change_password),
    path("seller_change_password_post/",views.seller_change_password_post),
    path("admin_delete_offers/<id>",views.admin_delete_offers),
    path("seller_sent_review/",views.seller_sent_review),
    path("sellers_add_stock_post/",views.sellers_add_stock_post),
    # path("seller_view_stock_get",views.seller_view_stock),
    path("seller_view_stock_get/<id>",views.seller_view_stock_get),
    # path("seller_view_stock_get/<id>",views.seller_view_stock_get),
    #

    #==========User=============

    path("user_singup/",views.user_singup),
    path("user_signup_post/",views.user_signup_post),
    path("custmers_home/",views.custmers_home),
    path("customers_profile/",views.customers_profile),
    path("customers_edit_profile_get/",views.customers_edit_profile_get),
    path("customers_edit_profile_post/",views.customers_edit_profile_post),
    path('customers_product/<int:id>',views.customers_product),
    path("customers_view_near_by_sellers/",views.customers_view_near_by_sellers),
    path("customers_view_compliant_replay/",views.customers_view_compliant_replay),
    path("customers_sent_complaint/",views.customers_sent_complaint),
    path("customers_sent_compliant_get/",views.customers_sent_compliant_get),
    path("customers_sent_review_get/",views.customers_sent_review_get),
    path("customers_sent_review/",views.customers_sent_review),
    path("customers_change_password/",views.customers_change_password),
    path("customers_change_password_post/",views.customers_change_password_post),
    path("add_Favourite/<id>",views.add_Favourite),
    path("customers_product/<id>",views.customers_product),
    path("customers_view_favourates/",views.customers_view_favourates),
    path("forget_password_get/",views.forget_password_get),
    path("forget_password_post/",views.forget_password_post),
    path("customers_delete_favourites/<id>",views.customers_delete_favourites),

path("customers_view_product/",views.customers_view_product),
    path("toggle_favorite/<int:product_id>/", views.toggle_favorite),
    path("compare_product/<int:product_id>/", views.compare_product),






]
