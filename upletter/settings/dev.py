from .base import *


# APPLICATIONS | MY APPLICATIONS
LOCAL_APPS = [
    "accounts",
    "lands",
    "posts",
    "editors",
    "shop",
]
# THIRD PARTY APPLICATION FOR MAKINGTHE DEVELOMENT A SUCCESS

FRAMWORK_APPS = [
    "tinymce",
    "corsheaders",
    "ckeditor",
    "ckeditor_uploader",
]

# APPEND THESE APPS TO THE INSTALLED APPS BY DJANGO
INSTALLED_APPS += LOCAL_APPS
INSTALLED_APPS += FRAMWORK_APPS

# TINYMCE SETTINGS AND CONFIGARATIONS
TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = True
TINYMCE_DEFAULT_CONFIG = {
    "menubar": "file edit view insert format tools table help",
    "plugins": [
        'advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak',
        'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen', 'insertdatetime',
        'media', 'table', 'emoticons', 'template', 'help'
        ],
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    '| styles | a11ycheck ltr rtl | showcomments addcomment code',
    "custom_undo_redo_levels": 10,
   # To force a specific language instead of the Django current language.
}

# CKEDITOR SETTING ALSSO
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}


CORS_ALLOW_ALL_ORIGINS = True