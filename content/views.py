from allauth.core.internal.httpkit import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from content.templatetags import extras
from interaction.models import PostComment, Hashtag
from .forms import PostForm
from .models import Post,UserProfile
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    context = {'posts':posts,'user_info': request.user}
    return render(request,'homepage.html',context)
def profilepage(request,slug):
    profile = UserProfile.objects.get(username=slug)
    post=Post.objects.filter(author=slug)
    context = {'post':post,'profile':profile,'user_info': request.user}
    return render(request,'profile page.html', context)
def postpage(request,slug):
    post = Post.objects.get(slug=slug)
    comments=PostComment.objects.filter(post=post,parent=None)
    replies=PostComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post':post,'user_info': request.user,'comments':comments, 'replyDict': replyDict}

    return render(request,'postpage.html', context)
def search(request):
    query=request.GET.get('query')
    if len(query) > 78:
        posts = Post.objects.none()
    else:
        posts = Post.objects.filter(caption__icontains=query)
    if posts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    context = {'post':posts,'query': query}
    return render(request,'search.html',context)
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request,'authentication/loginpage.html')
def handleSignup(request):
    if request.method == 'POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if len(username) < 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('/login')

        if  username.isdigit():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/login')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('/login')
        # checks
        myUser=User.objects.create_user(username,'',pass1)
        myUser.first_name=fname
        myUser.last_name=lname
        myUser.save()
        login(request,myUser)
        messages.success(request, 'Account created for ' + fname)
        myUserProfile=UserProfile.objects.create(username=username,user=myUser)
        myUserProfile.save()
        return redirect('/')
    else:
        return HttpResponse('404 Not Found')
def handlelogin(request):
    if request.method == 'POST':
        username=request.POST['userlogin']
        password=request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/login")
    else:
        return render(request,'404.html')
def handlelogout(request):
    logout(request)
    messages.warning(request, "Successfully logged out")
    return redirect('/')
def editprofile(request):
    if request.user.is_authenticated:

        context = {'user_info': request.user}
        return render(request, "editprofile.html", context)
    else:
        messages.error(request, "You are not logged in")
        return redirect('/')
def postComment(request,):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        user=request.user
        postslug=request.POST.get('postslug')
        post=Post.objects.get(slug=postslug)
        parentSno = request.POST.get('parentSno')
        if parentSno=='':

            commentt=PostComment(comment=comment,user=user,post=post)
            commentt.save()
            messages.success(request, "Comment successfully posted")
        else:
            parent=PostComment.objects.get(sno=parentSno)
            comment = PostComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Reply successfully posted")

        return redirect(f"/post/{postslug}")
    else:
        return render(request,'404.html')
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(f'/post/{slug}')
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.userprofile  # adjust to your UserProfile model
            post.save()

            # Handle hashtags
            raw_tags = form.cleaned_data.get('hashtags')
            if raw_tags:
                tag_names = [tag.strip().lower().replace('#', '') for tag in raw_tags.split(',')]
                for name in tag_names:
                    if name:
                        tag_obj, created = Hashtag.objects.get_or_create(name=name)
                        post.hashtags.add(tag_obj)

            post.save()
            messages.success(request, "Post successfully created")
            return redirect('/')  # or wherever you want to redirect
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
@login_required
def follow_user(request, username):
    target_profile = get_object_or_404(UserProfile, username=username)
    user_profile = request.user.userprofile

    if user_profile != target_profile:
        if target_profile in user_profile.following.all():
            user_profile.following.remove(target_profile)  # Unfollow
        else:
            user_profile.following.add(target_profile)     # Follow

        return redirect(f'/profile/{target_profile.username}')
    


