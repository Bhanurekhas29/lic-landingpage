from django.db import models


class SingletonModel(models.Model):
    """Base for models that must only ever have a single row (pk=1)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """Singleton: site-wide logo, brand name, tagline and header CTA button."""

    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Circle logo mark shown in the header.")
    site_name = models.CharField(max_length=100, default="LIC Agency")
    tagline = models.CharField(max_length=100, blank=True, help_text="Small text under the site name, e.g. CAREERS")

    cta_text = models.CharField(max_length=50, default="Apply Now", help_text="Header call-to-action button text.")
    cta_link = models.CharField(max_length=255, default="#apply", help_text="URL or in-page anchor, e.g. #apply")

    show_credit = models.BooleanField(default=True, help_text="Uncheck to hide the 'Designed and Developed by' strip below the footer.")
    credit_text = models.CharField(max_length=150, default="Designed and Developed by Vetri IT Systems")
    credit_link = models.URLField(default="https://vetriitsystems.com/")

    seo_title = models.CharField(max_length=70, blank=True, help_text="Browser tab / Google title tag. Leave blank to use site name and tagline.")
    meta_description = models.CharField(max_length=320, blank=True, help_text="Meta description shown in search results (about 150-160 characters).")

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


class EmailSettings(SingletonModel):
    """Singleton: Gmail SMTP details used to email new candidate applications."""

    email_host_user = models.EmailField("Sender Gmail address", blank=True, help_text="The Gmail address that sends the notification emails.")
    email_host_password = models.CharField("Gmail App Password", max_length=100, blank=True, help_text="A Gmail App Password (not the normal login password). Requires 2-Step Verification on that account.")
    default_from_email = models.EmailField("From address", blank=True, help_text="Must be the same as the sender Gmail address. Leave blank to use the sender address.")
    contact_receiver_email = models.EmailField("Receiver email", blank=True, help_text="The inbox that receives new applications. Leave blank to turn off email notifications.")

    def __str__(self):
        return "Email Settings"

    class Meta:
        verbose_name = "Email Settings"
        verbose_name_plural = "Email Settings"


class MenuItem(models.Model):
    """A single link in the header navigation menu."""

    label = models.CharField(max_length=50)
    link = models.CharField(max_length=255, help_text="In-page anchor (e.g. #about) or a full URL.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this menu item from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.label


class HeroSection(SingletonModel):
    """Singleton: the top hero/banner section with its application form copy."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    badge_text = models.CharField(max_length=100, blank=True, help_text="e.g. CAREER OPPORTUNITY, CHENNAI")

    heading = models.CharField(max_length=200, help_text="e.g. Build Your career as an LIC Insurance Agent.")
    description = models.TextField(blank=True)

    cta_text = models.CharField(max_length=50, default="Start Your Application")
    cta_link = models.CharField(max_length=255, default="#apply")

    secondary_cta_text = models.CharField(max_length=50, blank=True, help_text="Optional second button, e.g. Learn How It Works. Leave blank to hide.")
    secondary_cta_link = models.CharField(max_length=255, blank=True, default="#how-it-works")

    trust_badge_text = models.CharField(max_length=100, blank=True, help_text="e.g. Guided onboarding and training")

    # Application form copy
    form_eyebrow = models.CharField(max_length=100, blank=True, default="TAKE THE FIRST STEP")
    form_heading = models.CharField(max_length=150, blank=True, default="Apply for an Agency Opportunity")
    consent_text = models.CharField(
        max_length=300, blank=True,
        default="I consent to being contacted regarding this agency opportunity and agree to the applicable terms."
    )
    submit_button_text = models.CharField(max_length=50, default="Submit Application")

    def __str__(self):
        return "Hero Section"

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"


class HeroBullet(models.Model):
    """A single bullet point under the hero description, e.g. 'Flexible Work Opportunity'."""

    hero_section = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='bullets')
    text = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Hero Bullet Point"
        verbose_name_plural = "Hero Bullet Points"

    def __str__(self):
        return self.text


class Application(models.Model):
    """A lead submitted through the hero 'Apply for an Agency Opportunity' form."""

    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    qualification = models.CharField(max_length=150)
    consent_given = models.BooleanField(default=False)

    is_read = models.BooleanField(default=False, help_text="Mark as read once you've followed up.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return f"{self.full_name} ({self.created_at:%Y-%m-%d})"


class WhyAgencySection(SingletonModel):
    """Singleton: the 'Why Agency?' section with its feature cards."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="01", help_text="e.g. 01")
    eyebrow = models.CharField(max_length=100, blank=True, default="WHY AGENCY?")
    heading_regular = models.CharField(max_length=150, blank=True, help_text="e.g. More than a job.")
    heading_italic = models.CharField(max_length=150, blank=True, help_text="e.g. A Professional Opportunity.")
    intro = models.TextField(blank=True, help_text="Optional short paragraph under the heading.")

    def __str__(self):
        return "Why Agency Section"

    class Meta:
        verbose_name = "Why Agency Section"
        verbose_name_plural = "Why Agency Section"


class WhyAgencyFeature(models.Model):
    """A single feature card in the 'Why Agency?' section, e.g. 'Flexible Work'."""

    section = models.ForeignKey(WhyAgencySection, on_delete=models.CASCADE, related_name='features')
    icon = models.ImageField(upload_to='why_agency/', blank=True, null=True, help_text="Small line icon shown at the top of the card.")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this card from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Why Agency Feature"
        verbose_name_plural = "Why Agency Features"

    def __str__(self):
        return self.title


class TrainingSupportSection(SingletonModel):
    """Singleton: the 'Guidance at Every Step' training & support section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="05", help_text="e.g. 05")
    eyebrow = models.CharField(max_length=100, blank=True, default="TRAINING & SUPPORT")
    heading = models.CharField(max_length=200, help_text="e.g. Guidance at Every Step.")
    intro = models.TextField(blank=True, help_text="Optional short paragraph under the heading.")
    cta_text = models.CharField(max_length=50, blank=True, help_text="Optional button under the items, e.g. Start Your Application. Leave blank to hide.")
    cta_link = models.CharField(max_length=255, blank=True, default="#apply")

    image = models.ImageField(upload_to='training_support/', blank=True, null=True)
    image_caption = models.CharField(max_length=100, blank=True, help_text="e.g. Learn. Practise. Grow.")

    def __str__(self):
        return "Training & Support Section"

    class Meta:
        verbose_name = "Training & Support Section"
        verbose_name_plural = "Training & Support Section"


class TrainingSupportItem(models.Model):
    """A single guidance item, e.g. 'Product Training'."""

    section = models.ForeignKey(TrainingSupportSection, on_delete=models.CASCADE, related_name='items')
    icon = models.ImageField(upload_to='training_support/icons/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this item from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Training & Support Item"
        verbose_name_plural = "Training & Support Items"

    def __str__(self):
        return self.title


class DevelopmentOfficerSection(SingletonModel):
    """Singleton: the 'Guidance Beyond Recruitment' development officer section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="06", help_text="e.g. 06")
    eyebrow = models.CharField(max_length=100, blank=True, default="DEVELOPMENT OFFICER")
    heading = models.CharField(max_length=200, help_text="e.g. Guidance Beyond Recruitment")

    photo = models.ImageField(upload_to='development_officer/', blank=True, null=True)
    photo_badge_text = models.CharField(max_length=50, blank=True, default="Authorized")

    officer_name = models.CharField(max_length=100, help_text="e.g. DHINESH R")
    officer_title = models.CharField(max_length=150, help_text="e.g. DEVELOPMENT OFFICER, LIC OF INDIA")
    quote_text = models.TextField(blank=True)

    support_eyebrow = models.CharField(max_length=100, blank=True, default="DEDICATED PROFESSIONAL SUPPORT")
    footer_note = models.CharField(max_length=150, blank=True, help_text="e.g. Direct mentorship & regular review meetings.")

    cta_text = models.CharField(max_length=50, default="Start Your Application")
    cta_link = models.CharField(max_length=255, default="#apply")

    def __str__(self):
        return "Development Officer Section"

    class Meta:
        verbose_name = "Development Officer Section"
        verbose_name_plural = "Development Officer Section"


class DevelopmentOfficerSupportItem(models.Model):
    """A single support item, e.g. 'Recruitment Guidance'."""

    section = models.ForeignKey(DevelopmentOfficerSection, on_delete=models.CASCADE, related_name='support_items')
    icon = models.ImageField(upload_to='development_officer/icons/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this item from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Development Officer Support Item"
        verbose_name_plural = "Development Officer Support Items"

    def __str__(self):
        return self.title


class EarningsSection(SingletonModel):
    """Singleton: the 'Performance-Based Earnings' section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="07", help_text="e.g. 07")
    eyebrow = models.CharField(max_length=100, blank=True, default="EARNING STRUCTURE")
    heading = models.CharField(max_length=200, help_text="e.g. Performance-Based Earnings")
    subtitle = models.TextField(blank=True)

    side_script_line1 = models.CharField(max_length=100, blank=True, help_text="e.g. Your Work")
    side_script_line2 = models.CharField(max_length=100, blank=True, help_text="e.g. Creates Real Value")

    note_text = models.CharField(
        max_length=300, blank=True,
        help_text="e.g. Commission, incentives and other benefits are subject to applicable rules, terms, conditions and eligibility requirements."
    )

    def __str__(self):
        return "Earnings Section"

    class Meta:
        verbose_name = "Earnings Section"
        verbose_name_plural = "Earnings Section"


class EarningsFeature(models.Model):
    """A single earnings feature card, e.g. 'Performance-Based'."""

    section = models.ForeignKey(EarningsSection, on_delete=models.CASCADE, related_name='features')
    icon = models.ImageField(upload_to='earnings/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this card from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Earnings Feature"
        verbose_name_plural = "Earnings Features"

    def __str__(self):
        return self.title


class TestimonialsSection(SingletonModel):
    """Singleton: the 'Real people. Meaningful journeys.' testimonials section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="08", help_text="e.g. 08")
    eyebrow = models.CharField(max_length=100, blank=True, default="TESTIMONIALS")
    heading_regular = models.CharField(max_length=150, blank=True, help_text="e.g. Real people.")
    heading_italic = models.CharField(max_length=150, blank=True, help_text="e.g. Meaningful journeys.")
    subtitle = models.TextField(blank=True, help_text="Optional short paragraph under the heading.")

    def __str__(self):
        return "Testimonials Section"

    class Meta:
        verbose_name = "Testimonials Section"
        verbose_name_plural = "Testimonials Section"


class Testimonial(models.Model):
    """A single testimonial card."""

    section = models.ForeignKey(TestimonialsSection, on_delete=models.CASCADE, related_name='testimonials')
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    quote = models.TextField()
    name = models.CharField(max_length=100)
    role_text = models.CharField(max_length=100, help_text="e.g. Agency Partner · 3 Yrs")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False, help_text="Highlight this testimonial.")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this testimonial from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name


class FAQSection(SingletonModel):
    """Singleton: the 'Your questions, answered.' FAQ section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="09", help_text="e.g. 09")
    eyebrow = models.CharField(max_length=100, blank=True, default="FREQUENTLY ASKED QUESTIONS")
    heading_regular = models.CharField(max_length=150, blank=True, help_text="e.g. Your questions,")
    heading_italic = models.CharField(max_length=150, blank=True, help_text="e.g. answered.")
    subtitle = models.TextField(blank=True)

    def __str__(self):
        return "FAQ Section"

    class Meta:
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Section"


class FAQItem(models.Model):
    """A single frequently asked question."""

    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, related_name='items')
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this question from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"

    def __str__(self):
        return self.question


class ReadyToExploreSection(SingletonModel):
    """Singleton: the closing 'Ready to Explore Your Agency Journey?' CTA section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    background_image = models.ImageField(upload_to='ready_to_explore/', blank=True, null=True)
    eyebrow = models.CharField(max_length=150, blank=True, help_text="e.g. A PROFESSIONAL JOURNEY STARTS WITH A FIRST STEP")

    heading_regular = models.CharField(max_length=150, blank=True, help_text="e.g. Ready to Explore Your")
    heading_highlight = models.CharField(max_length=100, blank=True, help_text="e.g. Agency Journey? (shown in the accent color)")

    subtitle = models.TextField(blank=True)

    cta_text = models.CharField(max_length=50, default="Start Your Application")
    cta_link = models.CharField(max_length=255, default="#apply")

    def __str__(self):
        return "Ready to Explore Section"

    class Meta:
        verbose_name = "Ready to Explore Section"
        verbose_name_plural = "Ready to Explore Section"


class ReadyToExploreFeature(models.Model):
    """A single small feature tag, e.g. 'Training & Guidance'."""

    section = models.ForeignKey(ReadyToExploreSection, on_delete=models.CASCADE, related_name='features')
    icon = models.ImageField(upload_to='ready_to_explore/icons/', blank=True, null=True)
    text = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this item from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Ready to Explore Feature"
        verbose_name_plural = "Ready to Explore Features"

    def __str__(self):
        return self.text


class ContactInfo(SingletonModel):
    """Singleton: site-wide contact details, used in the footer and contact section."""

    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True, help_text="Number used for the WhatsApp floating button.")
    address_line = models.CharField(max_length=200, blank=True, help_text="e.g. Agency Recruitment Desk Chennai")

    def __str__(self):
        return "Contact Info"

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"


class SocialLink(models.Model):
    """A single social media link, e.g. Facebook, Instagram."""

    platform = models.CharField(max_length=50, help_text="e.g. Facebook, Instagram, LinkedIn")
    icon = models.ImageField(upload_to='social_icons/', blank=True, null=True)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this link from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.platform


class FooterSection(SingletonModel):
    """Singleton: the site footer."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove the footer from the live site.")

    logo = models.ImageField(upload_to='footer/', blank=True, null=True)
    brand_name = models.CharField(max_length=100, default="LIC Agency Careers")
    description = models.TextField(blank=True)

    information_heading = models.CharField(max_length=50, blank=True, default="INFORMATION")
    contact_heading = models.CharField(max_length=50, blank=True, default="CONTACT")

    disclaimer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=150, blank=True, help_text="e.g. © 2026 LIC Agency Careers. All rights reserved.")
    bottom_note_text = models.CharField(max_length=150, blank=True, help_text="e.g. This recruitment page is for informational purposes only.")

    def __str__(self):
        return "Footer Section"

    class Meta:
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Section"


class FooterLink(models.Model):
    """A single link in the footer 'Information' column, e.g. 'Privacy Policy'."""

    section = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255, help_text="In-page anchor or a full URL.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this link from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return self.label


class HowItWorksSection(SingletonModel):
    """Singleton: the 'How It Works' timeline/steps section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="02", help_text="e.g. 02")
    eyebrow = models.CharField(max_length=100, blank=True, default="HOW IT WORKS")
    heading_regular = models.CharField(max_length=150, blank=True, help_text="e.g. A simple path")
    heading_italic = models.CharField(max_length=150, blank=True, help_text="e.g. to Start Your Agency Journey.")

    def __str__(self):
        return "How It Works Section"

    class Meta:
        verbose_name = "How It Works Section"
        verbose_name_plural = "How It Works Section"


class HowItWorksStep(models.Model):
    """A single step in the 'How It Works' timeline, e.g. '01 Apply'."""

    section = models.ForeignKey(HowItWorksSection, on_delete=models.CASCADE, related_name='steps')
    step_number = models.CharField(max_length=10, help_text="e.g. 01")
    icon = models.ImageField(upload_to='how_it_works/', blank=True, null=True, help_text="Small line icon shown next to the step title.")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this step from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "How It Works Step"
        verbose_name_plural = "How It Works Steps"

    def __str__(self):
        return f"{self.step_number} - {self.title}"


class WhoCanApplySection(SingletonModel):
    """Singleton: the 'Who Can Consider This Opportunity' section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="03", help_text="e.g. 03")
    eyebrow = models.CharField(max_length=100, blank=True, default="OPEN TO POSSIBILITY")
    heading = models.CharField(max_length=200, help_text="e.g. Who Can Consider This Opportunity?")
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='who_can_apply/', blank=True, null=True)

    def __str__(self):
        return "Open To Possibility Section"

    class Meta:
        verbose_name = "Open To Possibility Section"
        verbose_name_plural = "Open To Possibility Section"


class WhoCanApplyItem(models.Model):
    """A single eligible-audience item, e.g. '01 Working Professionals'."""

    section = models.ForeignKey(WhoCanApplySection, on_delete=models.CASCADE, related_name='items')
    number = models.CharField(max_length=10, help_text="e.g. 01")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, help_text="Optional short line shown under the title.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this item from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Open To Possibility Item"
        verbose_name_plural = "Open To Possibility Items"

    def __str__(self):
        return f"{self.number} - {self.title}"


class EligibilitySection(SingletonModel):
    """Singleton: the 'Key requirements to get started' eligibility section."""

    is_active = models.BooleanField(default=True, help_text="Uncheck to remove this section from the live site.")

    number_badge = models.CharField(max_length=10, blank=True, default="04", help_text="e.g. 04")
    eyebrow = models.CharField(max_length=100, blank=True, default="ELIGIBILITY")
    heading = models.CharField(max_length=200, help_text="e.g. Key requirements to get started.")

    note_text = models.CharField(
        max_length=300, blank=True,
        help_text="e.g. Eligibility and appointment are subject to applicable LIC and regulatory requirements."
    )

    def __str__(self):
        return "Eligibility Section"

    class Meta:
        verbose_name = "Eligibility Section"
        verbose_name_plural = "Eligibility Section"


class EligibilityRequirement(models.Model):
    """A single eligibility requirement card, e.g. 'Education'."""

    section = models.ForeignKey(EligibilitySection, on_delete=models.CASCADE, related_name='requirements')
    icon = models.ImageField(upload_to='eligibility/', blank=True, null=True, help_text="Icon shown in the circle above the title.")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this card from the site.")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Eligibility Requirement"
        verbose_name_plural = "Eligibility Requirements"

    def __str__(self):
        return self.title


class LegalPages(SingletonModel):
    """Singleton: text content for the Privacy Policy, Terms & Conditions and Disclaimer
    popups opened from the footer links. This is a single-page site, so these are shown
    as an on-page popup rather than separate pages."""

    privacy_policy_title = models.CharField(max_length=100, default="Privacy Policy")
    privacy_policy_content = models.TextField(blank=True, help_text="Plain text or basic HTML shown in the popup.")

    terms_title = models.CharField(max_length=100, default="Terms & Conditions")
    terms_content = models.TextField(blank=True, help_text="Plain text or basic HTML shown in the popup.")

    disclaimer_title = models.CharField(max_length=100, default="Disclaimer")
    disclaimer_content = models.TextField(blank=True, help_text="Plain text or basic HTML shown in the popup.")

    def __str__(self):
        return "Legal Pages"

    class Meta:
        verbose_name = "Legal Pages"
        verbose_name_plural = "Legal Pages"
