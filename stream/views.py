from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.encoding import force_unicode
from models import Stream, Entry, RssFeed
from utils import render_to_response

def view_stream(request, pk):
    """
    View Stream
    
    Retrieves stream from pk.
    
    If request is made via AJAX, returns JSON serialized list of entries.
    
    Templates: ``stream/view-stream.html``
    Context:
        entries
            queryset of stream's entries
    """
    stream = get_object_or_404(Stream, pk=pk)
    if request.is_ajax():
        import simplejson as json
        data = list()
        entries = Entry.objects.filter(stream=stream)[:10]
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
        'stream/view-stream.html',
        { 'entries':  Entry.objects.filter(stream=stream)[:100] },
        request
    )

def update_feeds(pk=1):
    """
    Update Feeds
    
    Not meant to be called via web, meant for CRON job to update site's primary
    feed.
    """
    try:
        stream = Stream.objects.get(pk=pk)
        stream.update_feeds()
    except Stream.DoesNotExist:
        pass
