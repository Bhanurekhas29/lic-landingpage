from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import ApplicationForm
from .models import (
    HeroSection, WhyAgencySection, HowItWorksSection, WhoCanApplySection,
    EligibilitySection, TrainingSupportSection, DevelopmentOfficerSection,
    EarningsSection, TestimonialsSection, FAQSection, ReadyToExploreSection,
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
    if not settings.CONTACT_RECEIVER_EMAIL:
        return

    html_body = render_to_string('emails/application_notification.html', {'application': application})

    email = EmailMultiAlternatives(
        subject=f"New Candidate Application - {application.full_name}",
        body=f"New application from {application.full_name} ({application.mobile_number}, {application.email})",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECEIVER_EMAIL],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)
