from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import KYCForm

def home(request):
    return render(request, 'core/index.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def kyc(request):
    user = request.user
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # for demo, bump KYC level to “1” as soon as they submit
            form.instance.kyc_level = 1
            form.save()
            return redirect('core:dashboard')
    else:
        form = KYCForm(instance=user)
    return render(request, 'core/kyc.html', {'form': form})

