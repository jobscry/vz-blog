from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.encoding import force_unicode
from models import Stream, Entry, RssFeed
from utils import render_to_response

def view_stream(request, pk):
    stream = get_object_or_404(Stream, pk=pk)
    entries = Entry.objects.filter(stream=stream)[:25]
    if request.is_ajax():
        import simplejson as json
        data = list()
        for entry in entries:
            data.append({
                'feed': entry.feed.title,
                'title': entry.title,
                'link': entry.link,
                'published_on': entry.published_on.isoformat()
            })
        response = HttpResponse(mimetype='application/json')
        response.write(
            json.dumps(data)
        )
        return response

    return render_to_response(
        'view-stream.html',
        { 'entries':  entries },
        request
    )

def update_feeds(pk=1):
    try:
        stream = Stream.objects.get(pk=pk)
        stream.update_feeds()
    except Stream.DoesNotExist:
        pass
