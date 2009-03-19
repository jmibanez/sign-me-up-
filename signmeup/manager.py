from signmeup.models import SignupTopic, UserSignup
from google.appengine.ext import db
from google.appengine.api import memcache

import logging
import pickle
import datetime, time

def get_signups_for(u):
    signups = UserSignup.all()
    signups.filter('user =', u)

    return signups

def already_signed_up_for(t):
    signups = UserSignup.all()
    signups.filter('topic =', t)

    s = signups.fetch(1)
    if s:
        return True
    else:
        return False

def get_new_topics(n=10):
    topics = SignupTopic.all()
    topics.order('-timestamp')

    # Only recent n
    return topics.fetch(n)

def get_topics_paged(page, pagesize=10):
    topics = SignupTopic.all()
    topics.order('-timestamp')

    return topics.fetch(pagesize, (page * pagesize))

def define_topic(user, topic_form):
    topic = SignupTopic(owner = user,
                        name = topic_form.cleaned_data['name'],
                        description = topic_form.cleaned_data['description'])
    topic.put()

    return topic.key()

def get_topic(id):
    try:
        r = db.get(db.Key(id))
    except db.BadKeyError:
        r = None

    return r

def get_signup_count(topic):
    return get_topic_signups(topic).count()

def signup_topic(user, topic_id):
    topic = get_topic(topic_id)
    if not topic:
        return None

    # First check that we haven't already signed up
    if already_signed_up_for(topic):
        return ('already_signed_up', topic)
    else:
        s = UserSignup(user = user, topic = topic)
        s.put()
        return ('thanks', topic)

def get_topic_signups_check_user(user, topic_id):
    topic = get_topic(topic_id)
    if not topic:
        return None

    if topic.owner != user:
        raise 'NotAllowed'

    return get_topic_signups(topic)

def get_topic_signups(topic):
    signups = UserSignup.all()
    signups.filter('topic =', topic)
    return signups
