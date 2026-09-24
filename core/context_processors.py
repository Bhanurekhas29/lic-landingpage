from .models import SiteSettings, MenuItem, FooterSection, ContactInfo, SocialLink, LegalPages


def site_settings(request):
    return {
        'site_settings': SiteSettings.load(),
        'menu_items': MenuItem.objects.filter(is_active=True).order_by('order', 'id'),
        'footer': FooterSection.load(),
        'contact_info': ContactInfo.load(),
        'social_links': SocialLink.objects.filter(is_active=True),
        'legal_pages': LegalPages.load(),
    }
