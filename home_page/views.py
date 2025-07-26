import csv
import os
import logging

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def main_page(request):
    if request.method == "POST":
        full_name = request.POST.get('fullName', '').strip()
        email = request.POST.get('email', '').strip().lower()

        if full_name and email:
            # مسیر ذخیره‌سازی: به جای روت، در فولدر data
            csv_dir = os.path.join(settings.BASE_DIR, 'data')
            os.makedirs(csv_dir, exist_ok=True)  # اگر نبود بسازش

            csv_path = os.path.join(csv_dir, 'user_data.csv')

            # بررسی اینکه ایمیل قبلاً ثبت شده یا نه
            existing_emails = set()
            if os.path.isfile(csv_path):
                try:
                    with open(csv_path, mode='r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            existing_emails.add(row['Email'].strip().lower())
                except Exception as e:
                    logger.error(f"Error reading CSV: {e}")
                    messages.error(request, "Server error while checking your email.")
                    return redirect('main_page')

            if email in existing_emails:
                messages.error(request, "You have already joined the waiting list before.")
                return redirect('main_page')

            # ذخیره اطلاعات در CSV
            file_exists = os.path.isfile(csv_path)
            try:
                with open(csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    if not file_exists:
                        writer.writerow(['Full Name', 'Email'])
                    writer.writerow([full_name, email])
            except Exception as e:
                logger.error(f"Failed to write to CSV: {e}")
                messages.error(request, "Something went wrong while saving your data.")
                return redirect('main_page')

            # ارسال ایمیل تاییدیه
            subject = "Welcome to AskiMate Waiting List!"
            message = (
                f"Hello {full_name},\n\n"
                f"Thank you for joining the AskiMate waiting list! "
                f"We'll keep you updated with the latest news and updates.\n\n"
                f"Best regards,\nThe AskiMate Team"
            )

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                messages.success(request, "Thank you for joining the waiting list! A confirmation email has been sent.")
            except Exception as e:
                logger.error(f"Email not sent to {email}: {e}")
                messages.warning(request, "You joined the list, but confirmation email failed to send.")

            return redirect('main_page')
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'home_page/main_page.html')


def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('contact_name', '').strip()
        email = request.POST.get('contact_email', '').strip()
        message = request.POST.get('contact_message', '').strip()

        if not (name and email and message):
            messages.error(request, "All fields are required.")
            return redirect('main_page')

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # ارسال ایمیل به تیم
            send_mail(
                subject="New Contact Form Submission",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['askimatetest@gmail.com'],
                fail_silently=False,
            )

            # ارسال تاییدیه به کاربر
            user_subject = "We received your message at AskiMate!"
            user_message = (
                f"Hi {name},\n\n"
                f"Thanks for reaching out to us! "
                f"We’ve received your message and will get back to you as soon as possible.\n\n"
                f"Your message:\n{message}\n\n"
                f"Best,\nAskiMate Team"
            )

            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully.")
        except Exception as e:
            logger.error(f"Error sending contact form email: {e}")
            messages.error(request, "Something went wrong. Please try again later.")

        return redirect('main_page')

    return redirect('main_page')
