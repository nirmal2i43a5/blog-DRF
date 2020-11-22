

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from .utils import get_read_time

from urllib.parse import quote_plus #for sharing content



@login_required
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm()
 
	# print(form.media)
	if request.method == 'POST':
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)#create but not save to db
			instance.user = request.user
			instance.save()
			# message success
			messages.success(request, "Successfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    
	instance = get_object_or_404(Post, slug=slug)

	
 
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	share_string = quote_plus(instance.content)#sharing my content to dif platform like fb,twitter and others
 
	# print(get_read_time(instance.content)) passing this content string to utils for checking read time

	#comment workflow started
 
	initial_data = {
			"content_type": instance.get_content_type,#check get_content_type decorator in posts/models.py
			#in this case post is my content_type
			"object_id": instance.id#we comment for particular post
	}

	form = CommentForm(request.POST or None, initial=initial_data)#initial is for django form but use instance for modelform
 
	if form.is_valid() and request.user.is_authenticated():
		# print(form.cleaned_data)
  		#i.e.{'content_type': 'post', 'object_id': 1, 'content': 'This is message'}
     
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)#this is akin to get_for_model
	
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		'''
           i am using request.POST.get instead of form.cleaned_data for parent_id because
            i dont use parent field in forms as it can create confusion in comment form 
            and may give data with repetitive result as we have already set initial_data in CommentForm
        '''
  
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		#when i create comment textarea i.e content is only seen but other fields are hidden type
  
		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,#content_type = c_type    =>gives error
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
  
  
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())#this clear the textarea value after submit data

	#calling comments property decorator in posts/models.py
	comments = instance.comments# or Comment.objects.filter_by_instance(instance) (gives same result)
	


 

	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
	}


	return render(request, "post_detail.html", context)


def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #call active() in models#.order_by("-timestamp")
 
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_list.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)



def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")
