from flask_mail import Message
from app import mail


def send_email(
    subject, recipients, body, html_body=None, sender="noreply@quizmaster.com"
):
    """
    Send email with optional HTML formatting

    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        body: Plain text body
        html_body: Optional HTML body for rich formatting
        sender: Sender email address
    """
    msg = Message(
        subject=subject, recipients=recipients, body=body, html=html_body, sender=sender
    )
    mail.send(msg)


def create_email_template(title, content, footer_text=""):
    """
    Create a basic HTML email template

    Args:
        title: Email title/header
        content: Main content (HTML)
        footer_text: Optional footer text

    Returns:
        HTML string for email body
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 300;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .quiz-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                border-radius: 6px;
                overflow: hidden;
            }}
            .quiz-table th {{
                background-color: #f8f9fa;
                color: #495057;
                font-weight: 600;
                padding: 15px 12px;
                text-align: left;
                border-bottom: 2px solid #dee2e6;
            }}
            .quiz-table td {{
                padding: 12px;
                border-bottom: 1px solid #e9ecef;
            }}
            .quiz-table tr:last-child td {{
                border-bottom: none;
            }}
            .quiz-table tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            .stats-container {{
                display: flex;
                gap: 15px;
                margin: 20px 0;
                flex-wrap: wrap;
            }}
            .stat-box {{
                flex: 1;
                min-width: 120px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 6px;
                text-align: center;
            }}
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .stat-label {{
                font-size: 12px;
                opacity: 0.9;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #6c757d;
                font-size: 14px;
            }}
            .no-content {{
                text-align: center;
                padding: 40px 20px;
                color: #6c757d;
                font-style: italic;
            }}
            .greeting {{
                font-size: 16px;
                margin-bottom: 20px;
                color: #495057;
            }}
            @media (max-width: 600px) {{
                .container {{
                    margin: 10px;
                    border-radius: 0;
                }}
                .stats-container {{
                    flex-direction: column;
                }}
                .quiz-table {{
                    font-size: 14px;
                }}
                .quiz-table th, .quiz-table td {{
                    padding: 8px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 {title}</h1>
            </div>
            <div class="content">
                {content}
            </div>
            {f'<div class="footer">{footer_text}</div>' if footer_text else ''}
        </div>
    </body>
    </html>
    """
