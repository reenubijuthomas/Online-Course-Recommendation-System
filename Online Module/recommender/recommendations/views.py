from django.shortcuts import render, redirect
from course.models import Course, Rating
from main.models import UserProfiles
from django.contrib.auth.models import User, auth
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def recommendation(request):
    user_topics = []
    course_topics = {}

    content_probs = {}
    content_probs_nonzero = {}
    content_probs_sorted = []

    courses_content = []

    u1_likes = []
    u1_dislikes = []
    other_likes = {}
    other_dislikes = {}

    user_liked_courses = []
    user_disliked_courses = []
    other_liked_courses = {}
    other_disliked_courses = {}

    common_likes = []
    common_dislikes = []
    opposite_rating1 = []
    opposite_rating2 = []
    similarity = {}

    course_likes = {}
    course_dislikes = {}

    collab_probs = {}
    collab_probs_nonzero = {}
    collab_probs_sorted = []

    courses_collab = []

    hybrid_probs = {}
    hybrid_probs_nonzero = {}
    hybrid_probs_sorted = []

    courses_hybrid = []

    courses_content_final = []
    courses_collab_final = []
    courses_hybrid_final = []



    ###CONTENT BASED###
    try:
        user_profile = UserProfiles.objects.get(user=request.user)
    except UserProfiles.DoesNotExist:
        ##return render(request,"debug.html",{"result":"Complete your Profile to get recommendations"})
        return render(request,"msg.html")
    
    topics_str = user_profile.topics
    user_topics = [x.strip() for x in topics_str.split(',')]

    courses = Course.objects.all()

    for course in courses:
        course_topic_str = course.topics
        course_topic = [x.strip() for x in course_topic_str.split(',')]
        common_topics = list(set(user_topics).intersection(set(course_topic)))
        content_probs[course.pk] = len(common_topics) / len(course_topic)

    for i, j in content_probs.items():
        if j != float(0):
            content_probs_nonzero[i] = j

    content_probs_sorted = sorted(content_probs_nonzero, key=content_probs.get, reverse=True)

    courses_content = Course.objects.filter(pk__in=[x for x in content_probs_sorted])


###COLLABORATIVE FILTERING###


    u1_likes = Rating.objects.filter(user=request.user, rating="1")
    u1_dislikes = Rating.objects.filter(user=request.user, rating="-1")

    user_liked_courses = Course.objects.filter(pk__in=u1_likes.values_list('course', flat=True))
    user_disliked_courses = Course.objects.filter(pk__in=u1_dislikes.values_list('course', flat=True))

    users = User.objects.all()

    for user in users:
        if user != request.user:
            other_likes[user.pk] = Rating.objects.filter(user=user, rating="1")
            other_dislikes[user.pk] = Rating.objects.filter(user=user, rating="-1")

            other_liked_courses[user.pk] = Course.objects.filter(pk__in=other_likes[user.pk].values_list('course', flat=True))
            other_disliked_courses[user.pk] = Course.objects.filter(pk__in=other_dislikes[user.pk].values_list('course', flat=True))

            common_likes = list(set(user_liked_courses).intersection(set(other_liked_courses[user.pk])))
            common_dislikes = list(set(user_disliked_courses).intersection(set(other_disliked_courses[user.pk])))
            opposite_rating1 = list(set(user_liked_courses).intersection(set(other_disliked_courses[user.pk])))
            opposite_rating2 = list(set(user_disliked_courses).intersection(set(other_liked_courses[user.pk])))

            lst = [user_liked_courses, user_disliked_courses, other_liked_courses[user.pk], other_disliked_courses[user.pk]]
            total = list(set().union(*lst))

            if len(total) != 0:
                similarity[user.pk] = (len(common_likes) + len(common_dislikes) - len(opposite_rating1) - len(opposite_rating2)) / len(total)
            else:
                similarity[user.pk] = 0


    ratings = Rating.objects.all()

    for rating in ratings:
        if rating.course.pk not in course_likes.keys():
            course_likes[rating.course.pk] = []
        if rating.course.pk not in course_dislikes.keys():
            course_dislikes[rating.course.pk] = []


        if rating.rating == 1:
            course_likes[rating.course.pk].append(rating.user.pk)
        if rating.rating == -1:
            course_dislikes[rating.course.pk].append(rating.user.pk)


    for c in courses:
        if c.pk not in course_likes.keys():
            course_likes[c.pk] = []
        if c.pk not in course_dislikes.keys():
            course_dislikes[c.pk] = []

        similarity_sum_liked = 0
        similarity_sum_disliked = 0

        for i in course_likes[c.pk]:
            if (i==request.user.pk):
                continue
            similarity_sum_liked += similarity[i]

        for i in course_dislikes[c.pk]:
            if (i==request.user.pk):
                continue
            similarity_sum_disliked += similarity[i]

        liked_users = len(course_likes[c.pk])
        disliked_users = len(course_dislikes[c.pk])

        if (liked_users + disliked_users) != 0:
            prob_to_like = (similarity_sum_liked - similarity_sum_disliked) / (liked_users + disliked_users)
        else:
            prob_to_like = 0

        collab_probs[c.pk] = prob_to_like

        for i, j in collab_probs.items():
            if j != float(0):
                collab_probs_nonzero[i] = j

        collab_probs_sorted = sorted(collab_probs_nonzero, key=collab_probs.get, reverse=True)

        courses_collab = Course.objects.filter(pk__in=[x for x in collab_probs_sorted])



###HYBRID###


    for co in courses:
        hybrid_probs[co.pk] = content_probs[co.pk] * collab_probs[co.pk]

    for i, j in hybrid_probs.items():
        if j != float(0):
            hybrid_probs_nonzero[i] = j

    hybrid_probs_sorted = sorted(hybrid_probs_nonzero, key=collab_probs.get, reverse=True)

    courses_hybrid = Course.objects.filter(pk__in=[x for x in hybrid_probs_sorted])


###POST-PROCESSING###

    hybrid_list = []
    content_list = []
    collab_list = []


    for i in hybrid_probs_sorted:
        if Rating.objects.filter(user=request.user, course=Course.objects.get(pk=i)).exists():
            continue
        hybrid_list.append(i)


    for i in content_probs_sorted:
        if Rating.objects.filter(user=request.user, course=Course.objects.get(pk=i)).exists():
            continue
        if i in hybrid_list:
            continue
        content_list.append(i)

    for i in collab_probs_sorted:
        if Rating.objects.filter(user=request.user, course=Course.objects.get(pk=i)).exists():
            continue
        if i in hybrid_list:
            continue
        if i in content_list:
            continue
        collab_list.append(i)


    courses_content_final = Course.objects.filter(pk__in=[x for x in content_list])
    courses_collab_final = Course.objects.filter(pk__in=[x for x in collab_list])
    courses_hybrid_final = Course.objects.filter(pk__in=[x for x in hybrid_list])



    #    d_intersection = list(set(user_topics).intersection(set(course_topics[10])))
    #    d_prob = len(d_intersection)/len(course_topics[10])
    #    d_items = user_topics
    return render(request, "recommendation.html", {"hybrid":courses_hybrid_final,"content":courses_content_final, "collab":courses_collab_final})
