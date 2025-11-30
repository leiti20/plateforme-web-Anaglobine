from django.shortcuts import redirect
from functools import wraps

def patient_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('user_id') and request.session.get('user_type') == 'patient':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view
