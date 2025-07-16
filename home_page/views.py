import csv
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

def main_page(request):
    if request.method == "POST":
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')

        if full_name and email:
            csv_path = os.path.join(settings.BASE_DIR, 'user_data.csv')

            existing_emails = set()
            if os.path.isfile(csv_path):
                with open(csv_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        existing_emails.add(row['Email'].strip().lower())

            if email.strip().lower() in existing_emails:
                messages.error(request, "You have already joined the waiting list before.")
                return redirect('main_page')

            file_exists = os.path.isfile(csv_path)
            with open(csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                if not file_exists:
                    writer.writerow(['Full Name', 'Email'])
                writer.writerow([full_name, email])

            # ارسال ایمیل تایید به کاربر
            subject = "Welcome to AskiMate Waiting List!"
            message = f"Hello {full_name},\n\nThank you for joining the AskiMate waiting list! We'll keep you updated with the latest news and updates.\n\nBest regards,\nThe AskiMate Team"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, "Thank you for joining the waiting list! A confirmation email has been sent.")
            except Exception as e:
                messages.warning(request, "You joined the waiting list, but we couldn't send the confirmation email.")

            return redirect('main_page')
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'home_page/main_page.html')


def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('contact_name')
        email = request.POST.get('contact_email')
        message = request.POST.get('contact_message')

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # ایمیل به تیم AskiMate
            send_mail(
                subject="New Contact Form Submission",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['askimatetest@gmail.com'],
                fail_silently=False,
            )

            # ایمیل تایید به کاربر
            user_subject = "We received your message at AskiMate!"
            user_message = f"Hi {name},\n\nThanks for reaching out to us! We’ve received your message and will get back to you as soon as possible.\n\nYour message:\n{message}\n\nBest,\nAskiMate Team"
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully.")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again later.")

        return redirect('main_page')

    return redirect('main_page')
