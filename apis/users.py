import datetime
import json

import firebase_admin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from firebase_admin import firestore
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response



@api_view(["POST"])
def registration(request):
    db = firestore.client()
    user_data = json.loads(request.body)
    users_ref = db.collection(u'users')

    query_ref = users_ref.document(user_data['email']).get()

    if query_ref.exists:
        users_ref.document(user_data['email']).update(user_data)

        response = {
            "status_code": 200,
            "server_timestamp": datetime.datetime.now().isoformat(),
            "existing_user": user_data
        }

    else:
        users_ref.document(user_data['email']).set(user_data)

        response = {
            "status_code": 200,
            "server_timestamp": datetime.datetime.now().isoformat(),
            "new_user": user_data
        }


    
    return HttpResponse(JSONRenderer().render(response), content_type="application/json")

@api_view(["GET"])
def account(request, email):
    db = firestore.client()
    user_data = {}
    users_ref = db.collection(u'users')
    query_ref = users_ref.document(email).get()

    if query_ref.exists:
        user_data = query_ref.to_dict()

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
