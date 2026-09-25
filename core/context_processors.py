from .models import ContactInfo


def contact_info(request):
    info = ContactInfo.objects.filter(is_active=True).prefetch_related("locations").first()
    return {"site_contact_info": info}
