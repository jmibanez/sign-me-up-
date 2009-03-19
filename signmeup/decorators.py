# Decorators for views
from google.appengine.api import users
from django.http import HttpResponseRedirect


def must_be_logged_in(view_fun):
    def check_user(*args, **kwds):
        assert len(args) >= 1, 'Must be a view function with at least one function'

        request = args[0]
        u = users.get_current_user()
        if not u:
            return HttpResponseRedirect(users.create_login_url(request.path))
        
        return view_fun(*args, **kwds)

    return check_user

def admin_only(view_fun):
    def check_admin(*args, **kwds):
        if not users.is_current_user_admin():
            return HttpResponseRedirect('/')

        return view_fun(*args, **kwds)

    return check_admin
