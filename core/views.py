from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, get_connection
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import ApplicationForm
from .models import (
    HeroSection, WhyAgencySection, HowItWorksSection, WhoCanApplySection,
    EligibilitySection, TrainingSupportSection, DevelopmentOfficerSection,
    EarningsSection, TestimonialsSection, FAQSection, ReadyToExploreSection,
    EmailSettings,
)


def home(request):
    context = {
        'hero': HeroSection.load(),
        'why_agency': WhyAgencySection.load(),
        'how_it_works': HowItWorksSection.load(),
        'who_can_apply': WhoCanApplySection.load(),
        'eligibility': EligibilitySection.load(),
        'training_support': TrainingSupportSection.load(),
        'development_officer': DevelopmentOfficerSection.load(),
        'earnings': EarningsSection.load(),
        'testimonials': TestimonialsSection.load(),
        'faq': FAQSection.load(),
        'ready_to_explore': ReadyToExploreSection.load(),
    }
    return render(request, 'core/index.html', context)


@require_POST
def submit_application(request):
    form = ApplicationForm(request.POST)
    if form.is_valid():
        application = form.save()
        _send_application_emails(application)
        messages.success(request, "Thanks! Your application has been submitted. We'll contact you shortly.")
    else:
        messages.error(request, "Please correct the errors in the form and try again.")
    return redirect(request.META.get('HTTP_REFERER', '/') + '#apply')


def _send_application_emails(application):
    # Email details come from Admin > Authentication > Email Settings.
    # Any field left blank there falls back to the .env value.
    cfg = EmailSettings.load()
    host_user = cfg.email_host_user or settings.EMAIL_HOST_USER
    host_password = cfg.email_host_password or settings.EMAIL_HOST_PASSWORD
    from_email = cfg.default_from_email or host_user or settings.DEFAULT_FROM_EMAIL
    receiver = cfg.contact_receiver_email or settings.CONTACT_RECEIVER_EMAIL
    if not receiver:
        return

    html_body = render_to_string('emails/application_notification.html', {'application': application})

    connection = get_connection(username=host_user, password=host_password, fail_silently=True)
    email = EmailMultiAlternatives(
        subject=f"New Candidate Application - {application.full_name}",
        body=f"New application from {application.full_name} ({application.mobile_number}, {application.email})",
        from_email=from_email,
        to=[receiver],
        connection=connection,
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)
