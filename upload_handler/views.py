import json

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError, JsonResponse

from django.views.decorators.cache import never_cache


@never_cache
def upload_progress(request):
    """
    A view to report back on upload progress.
    Return JSON object with information about the progress of an upload.

    Copied from:
    http://djangosnippets.org/snippets/678/

    See upload.py for file upload handler.
    """
    #import ipdb
    #ipdb.set_trace()
    progress_id = None
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = "{}_{}".format(request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        print(json.dumps(data))
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseServerError(
            'Server Error: You must provide X-Progress-ID header or query param.')