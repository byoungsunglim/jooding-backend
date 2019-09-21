import datetime
import json

import firebase_admin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from firebase_admin import credentials, firestore
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Use a service account
cred = credentials.Certificate('firebase-service-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@api_view(["POST"])
def registration(request):
    user_data = json.loads(request.body)
    users_ref = db.collection(u'users')

    query_ref = users_ref.where(u'email', u'==', user_data['email']).limit(1).stream()

    if query_ref is not None:
        for user in query_ref:
            user_id = user.id
            break
        users_ref.document(user_id).update(user_data)

        response = {
            "status_code": 200,
            "server_timestamp": datetime.datetime.now().isoformat(),
            "existing_user": user_data
        }

    else:
        users_ref.add(user_data)

        response = {
            "status_code": 200,
            "server_timestamp": datetime.datetime.now().isoformat(),
            "new_user": user_data
        }


    
    return HttpResponse(JSONRenderer().render(response), content_type="application/json")

@api_view(["GET"])
def profile(request, email):
    users_ref = db.collection(u'users')
    query_ref = users_ref.where(u'email', u'==', email).limit(1).stream()

    if query_ref is not None:
        for user in query_ref:
            user_data = user.to_dict()
            user_data['id'] = user.id
            break

        response = {
            "status_code": 200,
            "server_timestamp": datetime.datetime.now().isoformat(),
            "user": user_data
        }

    else:
        response = {
            "status_code": 400,
            "server_timestamp": datetime.datetime.now().isoformat(),
            "error": "No user data"
        }


    
    return HttpResponse(JSONRenderer().render(response), content_type="application/json")
