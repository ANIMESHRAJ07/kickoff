import logging
import os
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)


def send_registration_confirmation(
    full_name: str,
    sap_id: str,
    branch: str,
    phone: str,
    study_year: str,
) -> bool:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SMTP_FROM_EMAIL")

    email_domain = os.getenv("COLLEGE_EMAIL_DOMAIN", "dit.edu.in")
    recipient = f"{sap_id}@{email_domain}"

    if not all((smtp_host, smtp_username, smtp_password, sender_email)):
        logger.warning("Confirmation email skipped because SMTP is not fully configured")
        return False

    message = EmailMessage()
    message["Subject"] = "Registration confirmed: CodeGenX KICKOFF '26 | 25 Sep | 4-6 PM"
    message["From"] = sender_email
    message["To"] = recipient
    message.set_content(
        f"Hi {full_name},\n\n"
        "Your registration for CodeGenX KICKOFF '26 is confirmed.\n\n"
        "EVENT DETAILS\n"
        "Date: 25 September\n"
        "Time: 4:00 PM - 6:00 PM\n"
        "Venue: Visvesvaraya 105\n"
        "Host: CodeGenX, DIT University\n\n"
        f"Branch: {branch}\n"
        f"SAP ID: {sap_id}\n"
        f"Phone: {phone}\n"
        f"Year: {study_year}\n"
        f"Contact number: {phone}\n\n"
        "WHAT TO EXPECT\n"
        "- Talk to seniors and mentors\n"
        "- Scribble, create, and have fun\n"
        "- Share, learn, and explore\n"
        "- Meet new people and discover CodeGenX\n\n"
        "No experience needed - just come curious.\n\n"
        "Questions? Contact Tripti Maurya (95558 25627) or "
        "Sujal Srivastava (86042 00290).\n\n"
        "We look forward to seeing you there!\n\n"
        "CodeGenX"
    )
    message.add_alternative(
        f"""
<!doctype html>
<html>
  <body style="margin:0;background:#070724;color:#f4f2ff;font-family:Arial,sans-serif;">
    <div style="max-width:640px;margin:0 auto;background:#0b0a35;">
      <div style="padding:42px 36px;background:linear-gradient(135deg,#09062e,#15004b);text-align:center;">
        <p style="margin:0;color:#fff200;font-size:13px;letter-spacing:4px;">CODEGENX PRESENTS</p>
        <h1 style="margin:16px 0 8px;color:#16dcff;font-size:48px;line-height:1;text-shadow:0 0 14px #16dcff;">KICKOFF<span style="color:#ff25d8;">'26</span></h1>
        <p style="margin:0;color:#f4f2ff;font-size:16px;letter-spacing:2px;">MEET. CREATE. CONNECT.</p>
      </div>
      <div style="padding:34px 36px;background:#111044;">
        <p style="margin:0 0 14px;color:#f4f2ff;font-size:17px;">Hi {full_name},</p>
        <p style="margin:0 0 26px;color:#d8d7ef;font-size:16px;line-height:1.6;">Your registration is confirmed. We are excited to have you at the CodeGenX technical club introduction event.</p>
        <div style="padding:22px;border:1px solid #16dcff;background:#09082d;">
          <p style="margin:0 0 12px;color:#fff200;font-size:12px;letter-spacing:2px;">EVENT DETAILS</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">DATE</strong>&nbsp;&nbsp; 25 September</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">TIME</strong>&nbsp;&nbsp; 4:00 PM - 6:00 PM</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">VENUE</strong>&nbsp; Visvesvaraya 105</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">HOST</strong>&nbsp;&nbsp; DIT University / CodeGenX</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">BRANCH</strong>&nbsp; {branch}</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">SAP ID</strong>&nbsp; {sap_id}</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">PHONE</strong>&nbsp;&nbsp; {phone}</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">YEAR</strong>&nbsp;&nbsp; {study_year}</p>
          <p style="margin:7px 0;color:#f4f2ff;"><strong style="color:#16dcff;">CONTACT</strong>&nbsp; {phone}</p>
        </div>
        <p style="margin:26px 0 8px;color:#ff25d8;font-size:13px;letter-spacing:2px;">WHAT TO EXPECT</p>
        <p style="margin:0;color:#d8d7ef;line-height:1.8;">Talk to seniors and mentors<br>Scribble, create, and have fun<br>Share, learn, and explore<br>Meet new people and discover CodeGenX</p>
        <p style="margin:26px 0 0;color:#d8d7ef;line-height:1.6;">No experience needed - just come curious.</p>
      </div>
      <div style="padding:20px 36px;background:#070724;color:#aaa8c9;font-size:12px;line-height:1.6;">
        Questions? Tripti Maurya: 95558 25627 | Sujal Srivastava: 86042 00290<br>
        CodeGenX, DIT University
      </div>
    </div>
  </body>
</html>
""",
        subtype="html",
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException):
        logger.exception("Confirmation email failed for %s", recipient)
        return False

    logger.info("Confirmation email sent to %s", recipient)
    return True
