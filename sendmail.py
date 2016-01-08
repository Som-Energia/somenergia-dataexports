#!/usr/bin/env python
# -*- encoding: utf8 -*-

from consolemsg import step

mdtemplate = u"""\
<html>
<head>
<style>
em {{
    color: red;
}}
strong {{
    color: green;
}}
</style>
</head>
<body>
{}
</body>
</html>
"""

ansitemplate = u"""\
<html>
<head>
<style>
{style}
</style>
</head>
<body>
<div class='ansi_terminal'>
{body}
</div>
</body>
</html>
"""

def _unicode(string):
     if hasattr(str, 'decode'):
         return string.decode('utf8')
     return string


def sendMail(
        sender,
        recipients,
        subject,
        text=None,
        html=None,
        md=None,
        ansi=None,
        cc=[],
        bcc=[],
        replyto=[],
        attachments = [],
        template=None,
        params = {},
        ):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.encoders import encode_base64

    from config import smtp

    msg = MIMEMultipart()
    msg['Subject'] = subject
    # TODO: check address format
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    if cc: msg['CC'] = ', '.join(cc)
    if bcc: msg['BCC'] = ', '.join(bcc)
    if replyto: msg['Reply-To'] = ', '.join(replyto)

    recipients = recipients + (cc if cc else []) + (bcc if bcc else [])

    for filename in attachments:
        step("Attaching {}...".format(filename))
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filename, "rb").read())
        encode_base64(part)

        part.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(filename.replace('"', '')))

        msg.attach(part)

    if md:
        step("Formating markdown input...")
        import markdown
        text = md # TODO: Format plain text
        html = mdtemplate.format(
            markdown.markdown(md, output_format='html')
            )

    if ansi:
        step("Formating ansi input...")
        import deansi
        text = ansi # TODO: Clean ansi sequences
        html = ansitemplate.format(
            style = deansi.styleSheet(),
            body = deansi.deansi(ansi),
            )


    content = MIMEMultipart('alternative')

    if text:
        content.attach(MIMEText(text,'plain','utf8'))

    if html:
        step("Adapting html to mail clients...")
        import premailer
        html = premailer.transform(html)
        content.attach(MIMEText(html,'html','utf8'))

    msg.attach(content)

    step("Connecting to {host}:{port} as {user}...".format(**smtp))
    server = smtplib.SMTP(smtp['host'], smtp['port'])
    server.starttls()
    server.login(smtp['user'], smtp['password'])
    step("Sending...")
    server.sendmail(sender, recipients, msg.as_string())
    step("Disconnecting...")
    server.quit()


def main():
    import sys

    args = parseArgs()

    if args.body is not None:
        content = args.body
    elif args.bodyfile is not None:
        with open(args.bodyfile) as f:
            content = _unicode(f.read())
    else:
        content = _unicode(sys.stdin.read())

    sys.stdout.write(content)

    sendMail(
        sender = args.sender,
        recipients = args.recipients,
        subject = args.subject,
        cc = args.cc,
        bcc = args.bcc,
        replyto = args.replyto,
        attachments = args.attachments,
        template = args.template,
        **{args.format: content}
        )


def parseArgs():
    import argparse
    parser = argparse.ArgumentParser(
        description="Sends an email.",
        )
    parser.add_argument(
        '--from',
        required=True,
        dest='sender',
        help="Message sender ('From:' header)",
        )
    parser.add_argument(
        '-s',
        '--subject',
        required=True,
        dest='subject',
        help="Message subject ('Subject:' header)",
        )
    parser.add_argument(
        '--to',
        dest='recipients',
        required=True,
        metavar='recipient',
        action='append',
        help="Message recipient ('To:' header)",
        )

    parser.add_argument(
        '--body',
        metavar="TEXT",
        help="Message body (defaults to stdin)",
        )

    parser.add_argument(
        '--bodyfile',
        metavar="BODYFILE",
        help="File containing the message body (defaults to stdin)",
        )

    parser.add_argument(
        '--cc',
        dest='cc',
        action='append',
        help="Message copy recipient ('CC:' header)",
        )

    parser.add_argument(
        '--bcc',
        dest='bcc',
        action='append',
        help="Message hidden copy recipient ('BCC:' header), recipients won't see this copy",
        )

    parser.add_argument(
        '--replyto',
        dest='replyto',
        action='append',
        help="Default address to reply at ('Reply-To:' header)",
        )

    parser.add_argument(
        '--format',
        choices = "html md text ansi".split(),
        default = 'text',
        metavar='FORMAT',
        help="Format for the body. "
            "'md' takes markdown and generates both html and text. "
            "'ansi' does the same, turning ANSI color codes in html or stripping them for text."
            ,
        )

    parser.add_argument(
        '--template',
        help="Alternative template for the html body.",
        )

    parser.add_argument(
        dest='attachments',
        metavar="FILE",
        nargs='*',
        help="File to attach",
        )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()



