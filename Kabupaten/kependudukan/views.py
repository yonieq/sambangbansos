from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Database.models import Warga
from .forms import RevisiNikForms


# Create your views here.

@login_required(login_url='KabupatenIndex')
@staff_member_required
def index(request):
    if request.method == 'POST':
        nomer = request.POST['nomer']
        data = Warga.objects.filter(Nik__contains=nomer)
        return render(request, 'kabupaten/kependudukan/pencarian.html', {'list': data})
    else:
        return render(request, 'kabupaten/kependudukan/pencarian.html', {list: None})


@login_required(login_url='KabupatenIndex')
@staff_member_required
def warga_forms(request, kode=None):
    if request.method == 'POST':
        warga = Warga.objects.get(pk=kode)
        form = RevisiNikForms(request.POST, instance=warga)
        if form.is_valid():
            form.save()
        return redirect('KabupatenKependudukanWargaList')
    else:
        if kode is not None:
            warga = Warga.objects.get(pk=kode)
            form = RevisiNikForms(instance=warga)
        else:
            form = RevisiNikForms
        return render(request, 'kabupaten/kependudukan/revisinikforms.html', {'form': form})
