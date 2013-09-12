import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def test(request):
    return HttpResponse(json.dumps({
        'mxit': request.mxit,
        'username': request.user.username,
    }, indent=2))
