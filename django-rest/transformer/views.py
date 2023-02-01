from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Transformer
from .serializers import TransformerSerializer
import os
import json
# from py_linq import Enumerable



def HarFileFilter(request):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	file_ = (os.path.join(PROJECT_ROOT, 'HCILite.json'))#sample.'HAR_2023_01_28 23_03_38.json'
	requestURL=(request.get_raw_uri()).replace('http://127.0.0.1:8000/api/v1/transformer?idz=', '/')
	with open(file_, 'r') as f:
			json_object = json.loads(f.read())
			# passing = json_object.where(lambda y: y.request_method == request.method) 
			for x in json_object:				
				str=x["request_path"]				
				# replaceString=str.replace('http://192.168.150.209:8081/', '')
				if str == requestURL:
					if hasattr(request.POST, 'data')==False:						
							return JsonResponse(json.loads(x["response_content"]["text"]))					
					if hasattr(x['request_postData'], 'params')==False:						
							return JsonResponse(json.loads(x["response_content"]["text"]))
					reqBody=request.POST['data']
					reqBodyData=x['request_postData']['params'][0]['value']
					if reqBody==reqBodyData:
						return JsonResponse(json.loads(x["response_content"]["text"]))
								

@csrf_exempt
def transformer_list(request):
	"""
	List all transformers, or create a new transformer
	"""
	methodType=request.method 
	if methodType == 'POST':
		fileContent=request.GET.get('idz')
		return HarFileFilter(request)

	if methodType != 'qqGET':
		PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
		file_ = (os.path.join(PROJECT_ROOT, 'HCILite.json'))#sample.'HAR_2023_01_28 23_03_38.json'
		requestURL='http://192.168.150.209:8081/auth/login'
		fileContent=request.GET.get('idz')
		requestURL=fileContent
		UrlContent= request.path#'/api/v1/transformer'
		if "?" in fileContent:
			splitStr=(fileContent).split("?", 1)
			requestURL=splitStr[0]+"?"+splitStr[1]
		
		#http://127.0.0.1:8000/api/v1/transformer?idz=
		requestURL=(request.get_raw_uri()).replace('http://127.0.0.1:8000/api/v1/transformer?idz=', '/')

		with open(file_, 'r') as f:
			json_object = json.loads(f.read())
			for x in json_object:
				str=x["request_url"]
				str=x["request_path"]
				
				replaceString=str.replace('http://192.168.150.209:8081/', '')
				if str == requestURL:

				#if x["request_url"] == requestURL:
					return JsonResponse(json.loads(x["response_content"]["text"]))
					#return JsonResponse(x["response_content"]["text"], safe=False)    		
		#print(type(json_object))
		# transformer = Transformer.objects.all()
		# serializer = TransformerSerializer(transformer, many=True)
		# data='{"name":"John", "age":30, "car":null}'
		#return JsonResponse(data, safe=False)
		#return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = TransformerSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def transformer_detail(request, pk):
	try:
		transformer = Transformer.objects.get(pk=pk)
	except Transformer.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = TransformerSerializer(transformer)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = TransformerSerializer(transformer, data=data)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		transformer.delete()
		return HttpResponse(status=204)



@csrf_exempt
def transformer_list2(request):
	"""
	List all transformers, or create a new transformer
	"""
	if request.method != 'qqGET':
		PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
		file_ = (os.path.join(PROJECT_ROOT, 'HCILite.json'))#sample.'HAR_2023_01_28 23_03_38.json'
		requestURL='http://192.168.150.209:8081/auth/login'
		fileContent=request.GET.get('idz')
		requestURL=fileContent
		UrlContent= request.path#'/api/v1/transformer'
		if "?" in fileContent:
			splitStr=(fileContent).split("?", 1)
			requestURL=splitStr[0]+"?"+splitStr[1]
		
		#http://127.0.0.1:8000/api/v1/transformer?idz=
		requestURL=(request.get_raw_uri()).replace('http://127.0.0.1:8000/api/v1/transformer?idz=', '/')

		with open(file_, 'r') as f:
			json_object = json.loads(f.read())
			for x in json_object:
				str=x["request_url"]
				str=x["request_path"]
				
				replaceString=str.replace('http://192.168.150.209:8081/', '')
				if str == requestURL:

				#if x["request_url"] == requestURL:
					return JsonResponse(json.loads(x["response_content"]["text"]))
					#return JsonResponse(x["response_content"]["text"], safe=False)    		
		#print(type(json_object))
		# transformer = Transformer.objects.all()
		# serializer = TransformerSerializer(transformer, many=True)
		# data='{"name":"John", "age":30, "car":null}'
		#return JsonResponse(data, safe=False)
		#return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = TransformerSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
