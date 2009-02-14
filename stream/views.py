from django.shortcuts import get_list_or_404, get_object_or_404
from models import Stream, Entry
from utils import render_to_response

def view_stream(request, pk):
    stream = get_object_or_404(Stream, pk=pk)
    return render_to_response(
        'view-stream.html',
        { 'entries': get_list_or_404(Entry, stream=stream) },
        request
    )

def update_feeds(pk=1):
    try:
        stream = Stream.objects.get(pk=pk)
        stream.update_feeds()
    except Stream.DoesNotExist:
        pass
