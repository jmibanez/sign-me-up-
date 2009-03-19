from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from signmeup.models import SignupTopic, UserSignup
from signmeup import manager
from signmeup import forms
from signmeup.decorators import must_be_logged_in, admin_only
from google.appengine.ext import db
from google.appengine.api import users

import logging

def page_not_found(request, template_name='404.html'):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    t = loader.get_template(template_name) # You need to create a 404.html template.
    return HttpResponseNotFound(t.render(Context({'request_path': request.path})))

def home(request):
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect('/topics')

    topic_list = manager.get_signups_for(user)
    new_topics = manager.get_new_topics()

    return render_to_response('home.html', { 'user'       : user,
                                             'my_topics'  : topic_list,
                                             'new_topics' : new_topics,
                                             'logout_url' : users.create_logout_url('/')})



def all_topics(request):
    try:
        page = int(request.GET['page'])
    except KeyError:
        page = 1

    actual_page = page - 1
    next_page = (page + 1)
    topic_list = manager.get_topics_paged(actual_page)

    if len(topic_list) < 10:
        next_page = 0

    return render_to_response('topics.html', { 'topics'     : topic_list,
                                               'logout_url' : users.create_logout_url('/topics'),
                                               'next_page'  : next_page,
                                               'prev_page'  : (page - 1)})


@must_be_logged_in
def define_topic(request):
    u = users.get_current_user()

    if request.method == 'GET':
        f = forms.TopicForm()
    else:
        f = forms.TopicForm(request.POST)
        if f.is_valid():
            id = manager.define_topic(u, f)
            return HttpResponseRedirect('/topic/' + str(id))


    return render_to_response('new_topic.html', { 'user' : u, 'form' : f,
                                                  'logout_url' : users.create_logout_url('/topics') })


def view_topic(request, topic_id):
    u = users.get_current_user()
    topic = manager.get_topic(topic_id)
    if topic:
        if u == topic.owner:
            c = manager.get_signup_count(topic)
            return render_to_response('topic.html', { 'user'  : u, 
                                                      'topic' : topic,
                                                      'count' : c,
                                                      'logout_url' : users.create_logout_url('/topics') })
        else:
            return render_to_response('topic.html', { 'user' : u, 'topic': topic })
    else:
        return page_not_found(request)

@must_be_logged_in
def signup_topic(request, topic_id):
    u = users.get_current_user()
    signup = manager.signup_topic(u, topic_id)

    if signup:
        return render_to_response(signup[0] + '.html', { 'user' : u, 'topic' : signup[1],
                                                         'logout_url' : users.create_logout_url('/topics') })
    else:
        return page_not_found(request)

@must_be_logged_in
def view_topic_signups(request, topic_id):
    u = users.get_current_user()

    try:
        signup_list = manager.get_topic_signups_check_user(u, topic_id)
        if signup_list == None:
            return page_not_found(request)

        return render_to_response('topic_signups.html', { 'user' : u, 'signup_list' : signup_list,
                                                          'logout_url' : users.create_logout_url('/topics') })
    except 'NotAllowed':
        # FIXME: Proper error page!
        return page_not_found(request)

