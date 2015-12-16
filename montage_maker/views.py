from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import render_to_response

from montage_maker.models import MontageElementContainer
from montage_maker.models import MontageElement
from montage_maker.models import Montage

from montage_maker.forms import MontageCreateForm

from filetransfers.api import prepare_upload

#from django.core.urlresolvers import reverse



#from lib.moviepy.editor import VideoFileClip

# Simple view to load a form that recieves the raw data for a montage
def create_montage(request):

	if request.method == 'POST':
	    form = MontageCreateForm(request.POST, request.FILES)
	    print(dir(form))
	    if form.is_valid():
	    	print("hello")
	        montageElementContainer = MontageElementContainer(title = request.POST['title'])
	        montageElementContainer.save()

	        for file in request.FILES.getlist('files'):
	                montageElement = MontageElement(video_file=file, container=montageElementContainer)
	                montageElement.save()

	        # contextDict for data to be passed to next view
	        contextDict = {}
	        contextDict['title']                   = request.POST['title']
	        contextDict['montageElementContainer'] = montageElementContainer
	        contextDict['uid']                     = montageElementContainer.auto_increment_id

	        template = loader.get_template('montage_maker/builder.html')
	        context = RequestContext(request, contextDict)
	        return HttpResponse(template.render(context))

	else:
		#view_url = reverse('upload.views.upload_handler')
		upload_url, upload_data = prepare_upload(request, 'montage_maker/builder.html')
		form = MontageCreateForm()
	    # Render list page with the documents and the form
		return render_to_response(
	    	'montage_maker/create_montage.html',
	    	{'form': form, 'upload_url': upload_url, 'upload_data': upload_data},
	    	context_instance=RequestContext(request)
		)

# Finished product
def montagify(request):

        montageElementContainer = MontageElementContainer.objects.get(auto_increment_id=request.POST['montageElementContainer'])

        clips = []

        for file in montageElementContainer.montageelement_set.all():
                start_sec = request.POST["start-sec-" + str(file.video_file)]
                start_min = request.POST["start-min-" + str(file.video_file)]
                end_sec = request.POST["end-sec-" + str(file.video_file)]
                end_min = request.POST["end-min-" + str(file.video_file)]

                start_point = 60*int(start_min) + int(start_sec)
                end_point = 60*int(end_min) + int(end_sec)

                videoFileClip = VideoFileClip("media/" + str(file.video_file)).subclip(start_point, end_point)
                clips.append(videoFileClip)

        video = concatenate_videoclips(clips)

        montage = Montage(video_file=video, container=montageElementContainer)

        contextDict = {}
        contextDict['montage'] = montage

        template = loader.get_template('montagemaker/montagify.html')
        context = RequestContext(request, contextDict)
        return HttpResponse(template.render(context))

