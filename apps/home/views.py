from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from apps.home.models import Hebdo


# Create your views here.
@login_required
def index(request):
    return render(request, 'home/index.html', {
        'path': request.path
    })


def get_all_hebdo(request):
    print(request.GET)
    if request.method == 'GET':
        hebdo = Hebdo.objects.all().annotate(
            department_name=F('department__name'),
            family_name=F('family__name'),
        ).values('department_name', 'family_name', 'article', 'designation', 'type', 'qte_pta', 'pmp_pta', 'pdv_pta',
                 'qte_realisation', 'pmp_realisation', 'pdv_realisation', 'stock_realisation', 'stock_prevision')
        data = dict(hebdo)

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid Method'}, safe=False, status=403)
