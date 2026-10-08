from django import forms
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect

from .models import (
    SiteSettings, MenuItem, HeroSection, HeroBullet, Application,
    WhyAgencySection, WhyAgencyFeature,
    HowItWorksSection, HowItWorksStep,
    WhoCanApplySection, WhoCanApplyItem,
    EligibilitySection, EligibilityRequirement,
    TrainingSupportSection, TrainingSupportItem,
    DevelopmentOfficerSection, DevelopmentOfficerSupportItem,
    EarningsSection, EarningsFeature,
    TestimonialsSection, Testimonial,
    FAQSection, FAQItem,
    ReadyToExploreSection, ReadyToExploreFeature,
    ContactInfo, SocialLink, FooterSection, FooterLink,
    LegalPages, EmailSettings,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one SiteSettings row, no add/delete."""

    fieldsets = (
        (None, {'fields': ('logo', 'site_name', 'tagline', 'cta_text', 'cta_link')}),
        ("SEO", {'fields': ('seo_title', 'meta_description')}),
        ("Developer Credit (below footer)", {'fields': ('show_credit', 'credit_text', 'credit_link')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return redirect(reverse('admin:core_sitesettings_change', args=[obj.pk]))


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')


class HeroBulletInline(admin.TabularInline):
    model = HeroBullet
    extra = 1
    fields = ('text', 'order')


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one HeroSection row, no add/delete."""

    inlines = [HeroBulletInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Banner", {'fields': ('background_image', 'badge_text', 'heading', 'description')}),
        ("Call to Action", {'fields': ('cta_text', 'cta_link', 'secondary_cta_text', 'secondary_cta_link', 'trust_badge_text')}),
        ("Application Form", {'fields': ('form_eyebrow', 'form_heading', 'consent_text', 'submit_button_text')}),
    )

    def has_add_permission(self, request):
        return not HeroSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = HeroSection.load()
        return redirect(reverse('admin:core_herosection_change', args=[obj.pk]))


class WhyAgencyFeatureInline(admin.TabularInline):
    model = WhyAgencyFeature
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active')


@admin.register(WhyAgencySection)
class WhyAgencySectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one WhyAgencySection row, no add/delete."""

    inlines = [WhyAgencyFeatureInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading_regular', 'heading_italic', 'intro')}),
    )

    def has_add_permission(self, request):
        return not WhyAgencySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = WhyAgencySection.load()
        return redirect(reverse('admin:core_whyagencysection_change', args=[obj.pk]))


class HowItWorksStepInline(admin.TabularInline):
    model = HowItWorksStep
    extra = 1
    fields = ('step_number', 'icon', 'title', 'description', 'order', 'is_active')


@admin.register(HowItWorksSection)
class HowItWorksSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one HowItWorksSection row, no add/delete."""

    inlines = [HowItWorksStepInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading_regular', 'heading_italic')}),
    )

    def has_add_permission(self, request):
        return not HowItWorksSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = HowItWorksSection.load()
        return redirect(reverse('admin:core_howitworkssection_change', args=[obj.pk]))


class WhoCanApplyItemInline(admin.TabularInline):
    model = WhoCanApplyItem
    extra = 1
    fields = ('number', 'title', 'description', 'order', 'is_active')


@admin.register(WhoCanApplySection)
class WhoCanApplySectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one WhoCanApplySection row, no add/delete."""

    inlines = [WhoCanApplyItemInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading', 'subtitle')}),
        ("Image", {'fields': ('image',)}),
    )

    def has_add_permission(self, request):
        return not WhoCanApplySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = WhoCanApplySection.load()
        return redirect(reverse('admin:core_whocanapplysection_change', args=[obj.pk]))


class EligibilityRequirementInline(admin.TabularInline):
    model = EligibilityRequirement
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active')


@admin.register(EligibilitySection)
class EligibilitySectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one EligibilitySection row, no add/delete."""

    inlines = [EligibilityRequirementInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading')}),
        ("Note", {'fields': ('note_text',)}),
    )

    def has_add_permission(self, request):
        return not EligibilitySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = EligibilitySection.load()
        return redirect(reverse('admin:core_eligibilitysection_change', args=[obj.pk]))


class TrainingSupportItemInline(admin.TabularInline):
    model = TrainingSupportItem
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active')


@admin.register(TrainingSupportSection)
class TrainingSupportSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one TrainingSupportSection row, no add/delete."""

    inlines = [TrainingSupportItemInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading', 'intro')}),
        ("Image", {'fields': ('image', 'image_caption')}),
        ("Call to Action", {'fields': ('cta_text', 'cta_link')}),
    )

    def has_add_permission(self, request):
        return not TrainingSupportSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = TrainingSupportSection.load()
        return redirect(reverse('admin:core_trainingsupportsection_change', args=[obj.pk]))


class DevelopmentOfficerSupportItemInline(admin.TabularInline):
    model = DevelopmentOfficerSupportItem
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active')


@admin.register(DevelopmentOfficerSection)
class DevelopmentOfficerSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one DevelopmentOfficerSection row, no add/delete."""

    inlines = [DevelopmentOfficerSupportItemInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading')}),
        ("Officer Profile", {'fields': ('photo', 'photo_badge_text', 'officer_name', 'officer_title', 'quote_text')}),
        ("Support Panel", {'fields': ('support_eyebrow', 'footer_note', 'cta_text', 'cta_link')}),
    )

    def has_add_permission(self, request):
        return not DevelopmentOfficerSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = DevelopmentOfficerSection.load()
        return redirect(reverse('admin:core_developmentofficersection_change', args=[obj.pk]))


class EarningsFeatureInline(admin.TabularInline):
    model = EarningsFeature
    extra = 1
    fields = ('icon', 'title', 'description', 'order', 'is_active')


@admin.register(EarningsSection)
class EarningsSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one EarningsSection row, no add/delete."""

    inlines = [EarningsFeatureInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading', 'subtitle')}),
        ("Side Script Text", {'fields': ('side_script_line1', 'side_script_line2')}),
        ("Note", {'fields': ('note_text',)}),
    )

    def has_add_permission(self, request):
        return not EarningsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = EarningsSection.load()
        return redirect(reverse('admin:core_earningssection_change', args=[obj.pk]))


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    fields = ('photo', 'name', 'role_text', 'quote', 'order', 'is_featured', 'is_active')


@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one TestimonialsSection row, no add/delete."""

    inlines = [TestimonialInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading_regular', 'heading_italic', 'subtitle')}),
    )

    def has_add_permission(self, request):
        return not TestimonialsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = TestimonialsSection.load()
        return redirect(reverse('admin:core_testimonialssection_change', args=[obj.pk]))


class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1
    fields = ('question', 'answer', 'order', 'is_active')


@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one FAQSection row, no add/delete."""

    inlines = [FAQItemInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Heading", {'fields': ('number_badge', 'eyebrow', 'heading_regular', 'heading_italic', 'subtitle')}),
    )

    def has_add_permission(self, request):
        return not FAQSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = FAQSection.load()
        return redirect(reverse('admin:core_faqsection_change', args=[obj.pk]))


class ReadyToExploreFeatureInline(admin.TabularInline):
    model = ReadyToExploreFeature
    extra = 1
    fields = ('icon', 'text', 'order', 'is_active')


@admin.register(ReadyToExploreSection)
class ReadyToExploreSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one ReadyToExploreSection row, no add/delete."""

    inlines = [ReadyToExploreFeatureInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Banner", {'fields': ('background_image', 'eyebrow', 'heading_regular', 'heading_highlight', 'subtitle')}),
        ("Call to Action", {'fields': ('cta_text', 'cta_link')}),
    )

    def has_add_permission(self, request):
        return not ReadyToExploreSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = ReadyToExploreSection.load()
        return redirect(reverse('admin:core_readytoexploresection_change', args=[obj.pk]))


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one ContactInfo row, no add/delete."""

    fields = ('phone', 'email', 'whatsapp_number', 'address_line')

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = ContactInfo.load()
        return redirect(reverse('admin:core_contactinfo_change', args=[obj.pk]))


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('label', 'url', 'order', 'is_active')


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one FooterSection row, no add/delete."""

    inlines = [FooterLinkInline]
    fieldsets = (
        ("Visibility", {'fields': ('is_active',)}),
        ("Brand", {'fields': ('logo', 'brand_name', 'description')}),
        ("Column Headings", {'fields': ('information_heading', 'contact_heading')}),
        ("Bottom Text", {'fields': ('disclaimer_text', 'copyright_text', 'bottom_note_text')}),
    )

    def has_add_permission(self, request):
        return not FooterSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = FooterSection.load()
        return redirect(reverse('admin:core_footersection_change', args=[obj.pk]))


@admin.register(LegalPages)
class LegalPagesAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one LegalPages row, no add/delete.

    This is a single-page site, so these show as an on-page popup (opened from the
    footer links) rather than separate pages.
    """

    fieldsets = (
        ("Privacy Policy", {'fields': ('privacy_policy_title', 'privacy_policy_content')}),
        ("Terms & Conditions", {'fields': ('terms_title', 'terms_content')}),
        ("Disclaimer", {'fields': ('disclaimer_title', 'disclaimer_content')}),
    )

    def has_add_permission(self, request):
        return not LegalPages.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = LegalPages.load()
        return redirect(reverse('admin:core_legalpages_change', args=[obj.pk]))


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'email', 'city', 'is_read', 'created_at')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'city', 'created_at')
    search_fields = ('full_name', 'mobile_number', 'email', 'city')
    readonly_fields = ('full_name', 'mobile_number', 'email', 'city', 'qualification', 'consent_given', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    """Singleton admin: always edits the one EmailSettings row, no add/delete."""

    fields = ('email_host_user', 'email_host_password', 'default_from_email', 'contact_receiver_email')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'email_host_password':
            field.widget = forms.PasswordInput(render_value=True, attrs={'autocomplete': 'new-password'})
        return field

    def has_add_permission(self, request):
        return not EmailSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = EmailSettings.load()
        return redirect(reverse('admin:core_emailsettings_change', args=[obj.pk]))
