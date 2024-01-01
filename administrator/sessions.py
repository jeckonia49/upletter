from django.http import HttpResponseRedirect
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta

expiration_date = timezone.now()+timedelta(hours=10)

def get_administrator_has_viewed_latest_post(request, pk):
    # this function is to manioulate the session data
    
    if request.method=='POST':
        session = SessionStore()
        session['administrator_pk']=pk
        session.create()
        session_key = session.session_key
        # print(session_key)
        ss = Session.objects.get(session_key=session_key)
        request.session.set_test_cookie()
        print(ss.get_decoded())
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))