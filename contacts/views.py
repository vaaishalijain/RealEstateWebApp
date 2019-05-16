from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail

# Create your views here.
def contact(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    realtor_email = request.POST['realtor_email']
    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_contacted: 
        messages.error(request, 'You have already made an enquiry for this listing')
        return redirect('/listings/'+listing_id)
    else:
      user_id = 0

    contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

    contact.save()

    # send mail
    send_mail(
      'Property Listing Inquiry',
      'There has been and inquiry for ' + listing + '. Sign into admin panel for more info',
      'support@realestate.co',
      [realtor_email],
      fail_silently = False
    )

    messages.success(request, 'Your request has been submitted, a realtor will get back to you shortly')

    return redirect('/listings/'+listing_id)