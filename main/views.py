import datetime
import requests

from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.utils import translation
from googletrans import Translator

from plants_app.config import pagination
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from authentication.forms import EditRegisterForm
from plants_app import settings
from .common import generate_numbers, Carousel
from .forms import UserProfileForm, ContactForm, NewsletterUserSignUpForm, UserDeleteForm
from .models import UserProfile, NewsletterUser


# class NewsletterUserListView(ListView):
#     model = NewsletterUser
#     paginate_by = 10
#
#
# class NewsletterUserDetailView(ListView):
#     model = NewsletterUser


def cookie_policy_accepted(request):
    if request.COOKIES.get('cookie_accepted', None):
        return True
    return False


def cookie_policy(request):
    return {'cookie_accepted': cookie_policy_accepted(request)}


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT+1")
    response.set_cookie(key, value, max_age=max_age, expires=expires)


def accept_cookie_policy(request):
    if 'HTTP_REFERER' in request.META:
        response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        response = HttpResponseRedirect('/')
    set_cookie(response, 'cookie_accepted', 1, days_expire=365)

    return response


def policy(request):
    return render(request, 'main/cookie_policy.html')


def cookie_banner(request):
    return render(request, 'main/cookie_banner.html')


def home_page(request):
    images = Carousel.objects.all()
    weather = {}
    current_site = get_current_site(request)
    if request.method == 'POST':
        city = request.POST['city']  # Use your own api_key place api_key in place of appid ="your_api_key_here".
        lang = 'en'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}' \
              f'&units=metric&appid=84459d8299db831d56abee888bea5970&lang={lang}'
        current_datetime = datetime.datetime.now().strftime("%B %d,  %I:%M %p")
        city_weather = requests.get(url).json()

        if city_weather['cod'] == "404" or city == "":
            messages.info(request, 'Incorrect city name, try again.')
        else:
            weather = {
                'city': city_weather['name'],
                'country_code': city_weather['sys']['country'],
                'temperature': round(city_weather['main']['temp']),
                'description': city_weather['weather'][0]['description'],
                'feels_like': round(city_weather['main']['feels_like']),
                'icon': city_weather['weather'][0]['icon'],
                'datetime': current_datetime,
            }
    else:
        weather = {}

    return render(request, 'main/home_page.html', {'weather': weather, 'current_site': current_site, 'images': images})


def api_location(request):
    # geolocation = requests.get(
    #     "https://ipgeolocation.abstractapi.com/v1/?api_key=cf3d1c1feafd4da1ae1cdcbd33082d30&"
    #     "fields=ip_address,city").json()
    geolocation = requests.get(
        "https://api.ipgeolocation.io/ipgeo?apiKey=a7c32a635e30443e80765774d7381a6b&fields=ip,city").json()
    geo = {
        'city': geolocation['city'],
        # 'ip_address': geolocation['ip_address'],
    }
    city = geo['city']
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=84459d8299db831d56abee888bea5970'
    city_weather = requests.get(url).json()

    weather = {
        'city': city_weather['name'],
        'country_code': city_weather['sys']['country'],
        'temperature': round(city_weather['main']['temp']),
        'description': city_weather['weather'][0]['description'],
        'feels_like': round(city_weather['main']['feels_like']),
        'icon': city_weather['weather'][0]['icon'],
    }

    return render(request, 'main/location.html', {'weather': weather})


def translate_app(request):
    if request.method == "POST":
        lang = request.POST.get("lang", None)
        txt = request.POST.get("txt", None)
        translator = Translator()
        tr = translator.translate(text=txt, dest=lang)
        return render(request, 'main/translate.html', {"result": tr.text, "text": txt})
    return render(request, 'main/translate.html')


def about(request):
    return render(request, 'main/about.html')


@login_required(login_url='/authentication/login/')
def create_user_profile(request):
    instance, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been created successfully!")
            return redirect(to='create_user_profile')
    #     else:
    #         form = UserProfileForm(instance=request.user.userprofile)
    # else:
    #     form = UserProfileForm()

    return redirect('main:user_profile')
    # return render(request, 'main/create_user_profile.html', {'form': form})


@login_required(login_url='/authentication/login/')
def user_profile(request):
    if request.method == 'POST':
        register_form = EditRegisterForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Your account information has been successfully updated!')

        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been successfully updated!')

        else:
            messages.error(request, 'Something went wrong. You may have entered incorrect data.')
            if ValidationError:
                for error in list(profile_form.errors.values()):
                    messages.info(request, error)
                # messages.info(request, profile_form.errors)
        return redirect('main:user_profile')

    else:
        register_form = EditRegisterForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'main/user_profile.html', {'user': request.user, 'register_form': register_form,
                                                      'profile_form': profile_form})


@login_required
def delete_user(request):
    if request.method == 'POST':
        # delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('main:home_page')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    return render(request, 'main/delete_user.html', {'delete_form': delete_form})


def contact(request):
    current_site = get_current_site(request)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'New request: {form.cleaned_data["subject"]}'
            plaintext = template.loader.get_template('main/contact_form.txt')
            htmltemp = template.loader.get_template('main/contact_form.html')
            from_email = form.cleaned_data['email']
            body = {
                'message': form.cleaned_data['message'],
                'name': form.cleaned_data['name'],
                'domain': current_site.domain,
                'email': from_email
            }
            to_email = settings.EMAIL_HOST_USER
            send_to_me = form.cleaned_data['send_to_me']
            text_content = plaintext.render(body)
            html_content = htmltemp.render(body)
            try:
                if send_to_me:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email, from_email],
                                                 headers={'Reply-To': "email@gmail.com"})
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()
                else:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email],
                                                 headers={'Reply-To': "email@gmail.com"})
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, 'Your request message has been send successfully.')
            return redirect('main:contact')
        else:
            messages.info(request, "You must confirm reCAPTCHA")
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


@staff_member_required
def newsletter_users(request):
    users = NewsletterUser.objects.all()
    pages = pagination(request, users, 5)

    template = 'main/newsletter/newsletter_users_list.html'
    context = {
        'newsletter_users': pages,
        'page_obj': pages
    }
    return render(request, template, context)


@staff_member_required
def newsletter_user_delete(request, pk):
    newsletter_user = NewsletterUser.objects.get(id=pk)
    if request.method == 'POST':
        newsletter_user.delete()
        messages.success(request, 'Newsletter user has been deleted.')
        return redirect('main:newsletter_users')

    return render(request, 'main/newsletter/newsletter_user_delete.html', {'item': newsletter_user})


def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request,
                             'Your email address already exists in our newsletter list!',
                             'alert alert-warning alert-dismissible')
        else:
            instance.save()
            messages.success(request,
                             'Your email has been added to the newsletter list!',
                             'alert alert-success alert-dismissible')

            subject = "Thank you for joining our newsletter."
            plaintext = template.loader.get_template('main/newsletter/sign_up_email.txt')
            htmtext = template.loader.get_template('main/newsletter/sign_up_email.html')
            current_site = get_current_site(request)
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            content = {
                'domain': current_site.domain,
                'email': instance.email
            }
            text_content = plaintext.render(content)
            html_content = htmtext.render(content)
            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email,
                                             headers={'Reply-To': "email@gmail.com"})
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

    return render(request, 'main/newsletter/newsletter_sign_up.html', {'form': form})


# def newsletter_signup(request):
#     form = NewsletterUserSignUpForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         if NewsletterUser.objects.filter(email=instance.email).exists():
#             messages.warning(request,
#                              'Your email address already exists in our newsletter list!',
#                              'alert alert-warning alert-dismissible')
#         else:
#             instance.save()
#             messages.success(request,
#                              'Your email has been added to the newsletter list!',
#                              'alert alert-success alert-dismissible')
#             subject = "Thank you for joining our newsletter."
#             from_email = settings.EMAIL_HOST_USER
#             to_email = [instance.email]
#             with open(settings.NEWSLETTER_ROOT / 'main/newsletter/sign_up_email.txt') as f:
#                 signup_message = f.read()
#             message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
#             html_template = get_template('main/newsletter/sign_up_email.html').render()
#             message.attach_alternative(html_template, "text/html")
#             message.send()
#
#     return render(request, 'main/newsletter/newsletter_sign_up.html', {'form': form})


def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request,
                             'Your email address has been removed from our newsletter list!',
                             'alert alert-success alert-dismissible')

            subject = "You have successfully unsubscribed from our newsletter."
            plaintext = template.loader.get_template('main/newsletter/unsubscribe_email.txt')
            htmtext = template.loader.get_template('main/newsletter/unsubscribe_email.html')
            current_site = get_current_site(request)
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            content = {
                'domain': current_site.domain,
            }
            text_content = plaintext.render(content)
            html_content = htmtext.render(content)
            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email,
                                             headers={'Reply-To': "email@gmail.com"})
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

        else:
            messages.warning(request,
                             'Your email address is not in our newsletter list.',
                             'alert alert-warning alert-dismissible')

    return render(request, 'main/newsletter/newsletter_unsubscribe.html', {'form': form})


def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


def signup_redirect(request):
    messages.error(request, "You can't log in using this email, because user account already exists with this email.")
    messages.info(request,
                  "Go log in to your account first, connect your google email to existing user account and then try logging in again.")
    return redirect("authentication:login_user")


# def translate_website(request):
#     if 'language' in request.GET and request.GET['language']:
#         language = request.GET['language']
#         if language in ['en', 'pl', 'es']:
#             if language == 'pl':
#                 translation.activate(language)
#             if language == 'en':
#                 translation.activate(language)
#             if language == 'es':
#                 translation.activate(language)


def api_avatars(request):
    numbers = generate_numbers()
    if request.method == 'GET':
        gender = request.GET['gender']
        if gender != 'male' and gender != 'female':
            messages.info(request, 'You must enter correct gender [female/male].')
        else:
            url = f"https://joeschmoe.io/api/v1/{gender}/random"
            response = requests.request("GET", url)
            resp = HttpResponse(response, headers={'Content-Type': 'image/svg',
                                                   'Content-Disposition': f'attachment; filename = "avatar_{gender}{numbers}.svg"'})
            return resp

    return redirect('main:user_profile')


def show_avatars(request):
    return render(request, 'main/show_api_avatars.html')
