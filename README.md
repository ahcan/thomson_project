# thomson_project
module request:
	+rest-fremawork: pip install djangorestframework
					pip install markdown       # Markdown support for the browsable API.
					pip install django-filter  # Filtering support
	+requests
	+pytz
	+tzlocal
    +django-recaptcha 
    + otp: django-two-factor-auth