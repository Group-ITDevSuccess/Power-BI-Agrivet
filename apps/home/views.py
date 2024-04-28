import json
import uuid

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.home.models import Hebdo, Department, Family
from utils import write_log, are_valid_uuids


# Create your views here.
@login_required
def index(request):
    return render(request, 'home/index.html', {
        'path': request.path
    })


@csrf_exempt
def get_all_hebdo(request):
    print(request.GET)
    data = json.loads(request.GET.get('request'))
    if request.method == 'GET':
        hebdos = Hebdo.objects.filter(category__iexact=data.get('category')).annotate(
            department_name=F('department__name'),
            family_name=F('family__name'),
            qte_pta=F('saison__qte_pta'),
            pmp_pta=F('saison__pmp_pta'),
            pdv_pta=F('saison__pdv_pta'),
            id=F('saison__uid'),
            qte_realisation=F('saison__qte_realisation'),
            pmp_realisation=F('saison__pmp_realisation'),
            pdv_realisation=F('saison__pdv_realisation'),
            stock_realisation=F('saison__stock_realisation'),
            stock_prevision=F('saison__stock_prevision'),
            archived=F('saison__archived')
        ).values('uid', 'department_name', 'family_name', 'article', 'designation', 'archived', 'type', 'id', 'qte_pta',
                 'pmp_pta',
                 'pdv_pta',
                 'qte_realisation', 'pmp_realisation', 'pdv_realisation', 'stock_realisation', 'stock_prevision')
        datas = [{key: value for key, value in hebdo.items()} for hebdo in hebdos]
        # print(datas)
        return JsonResponse(datas, safe=False)
    else:
        return JsonResponse({'error': 'error', 'message': 'Invalide Méthode POST'}, safe=False, status=403)


@csrf_exempt
def create_or_update_hebdo(request):
    message = "Invalid Method"

    if request.method == 'POST':

        try:
            message = "Hebdo enregistrer avec Succès !"

            data = json.loads(request.body.decode('utf-8'))
            category = data['category']
            changes = data['changes']
            for change in changes:
                uid = are_valid_uuids(change['uid'])
                if uid:
                    hebdo, create = Hebdo.objects.get_or_create(uid=uid, category=category)
                    if not create:
                        message = "Hebdo modifier avec Succès !"
                    for key, value in change.items():
                        try:
                            if key not in ['uid']:
                                if key in ['department_name', 'family_name']:
                                    if key == 'department_name':
                                        value, _ = Department.objects.get_or_create(name=value)
                                        hebdo.department = value
                                    if key == 'family_name':
                                        value, _ = Family.objects.get_or_create(name=value)
                                        hebdo.family = value
                                else:
                                    if key == 'type':
                                        # print(f"TYPE : {value['id']}")
                                        value = value['id']

                                    # print(f"{key}={value}")
                                    setattr(hebdo, key, value)
                        except Exception as e:
                            write_log(str(e))
                            pass
                    hebdo.save()
                    # datas = [{key: value for key, value in data.items()} for data in hebdo]
                    return JsonResponse({"status": "success", 'message': message}, safe=False)
        except Exception as e:
            message = "Une erreur c'est survenue dans l'oppération !"
            write_log(str(e))
    return JsonResponse({"status": "error", 'message': message}, safe=False)


@csrf_exempt
def delete_hebdo_by_uid(request):
    try:
        data = json.loads(request.body)
        uid = are_valid_uuids(data.get('uid'))
        hebdo = Hebdo.objects.filter(uid__in=uid, category=data.get('category'))
        hebdo.delete()
        return JsonResponse({"status": "success", 'message': 'Suppression Terminer'}, safe=False)
    except Hebdo.DoesNotExist:
        message = "Hebdo n'existe pas !"
    except Exception as e:
        write_log(str(e))
        message = "Une erreur c'est produit !"
    return JsonResponse({'error': 'error', 'message': message}, safe=False)


@csrf_exempt
def generate_uid(request):
    uid = uuid.uuid4()
    data = {
        'uid': uid,
        'category': request.POST.get('category')
    }
    return JsonResponse(data, safe=False)
