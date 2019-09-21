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
    new_user = json.loads(request.body)
    users_ref = db.collection(u'users')

    city_ref.add(new_user)

    response = {
        "status_code": 200,
        "server_timestamp": datetime.datetime.now().isoformat(),
        "data": new_user
    }

    return HttpResponse(JSONRenderer().render(response), content_type="application/json")
