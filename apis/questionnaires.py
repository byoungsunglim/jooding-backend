import datetime
import json

import firebase_admin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from firebase_admin import firestore
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

db = firestore.client()

@api_view(["GET"])
def questionnaires(request):
    print("#")
    docs = db.collection(u'questionnaires').stream()

    results = []

    print(docs)
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    response = {
        "status_code": 200,
        "server_timestamp": datetime.datetime.now().isoformat(),
        "results": results
    }
    
    return HttpResponse(JSONRenderer().render(response), content_type="application/json")
