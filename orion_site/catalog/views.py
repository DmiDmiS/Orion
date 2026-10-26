from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import BookingForm, ContractForm, RegisterForm
from .models import Apartment, BookingRequest, Contract, Favorite

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='login')

AREA_RANGES = {'50-100': (50, 100), '100-150': (100, 150)}


def ru_plural(n, forms):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return forms[0]
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return forms[1]
    return forms[2]


def _fav_ids(user):
    if user.is_authenticated:
        return set(Favorite.objects.filter(user=user).values_list('apartment_id', flat=True))
    return set()


def home(request):
    photos = Apartment.objects.exclude(image='')[:6]
    return render(request, 'home.html', {'photos': photos, 'sidebar': True})


def catalog(request):
    qs = Apartment.objects.all()
    q = request.GET.get('q', '').strip()
    rooms = request.GET.get('rooms', '').strip()
    areas = [a for a in request.GET.getlist('area') if a in AREA_RANGES]
    if q:
        qs = qs.filter(address__icontains=q)
    if rooms.isdigit():
        qs = qs.filter(rooms=int(rooms))
    if areas:
        cond = Q()
        for a in areas:
            low, high = AREA_RANGES[a]
            cond |= Q(area__gte=low, area__lte=high)
        qs = qs.filter(cond)
    count = qs.count()
    return render(request, 'catalog.html', {
        'apartments': qs, 'count': count, 'word': ru_plural(count, ('запись', 'записи', 'записей')),
        'q': q, 'rooms': rooms, 'area': areas, 'fav_ids': _fav_ids(request.user),
    })


def book(request, pk):
    apt = get_object_or_404(Apartment, pk=pk)
    initial = {'email': request.user.email} if request.user.is_authenticated else {}
    form = BookingForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        BookingRequest.objects.create(
            apartment=apt,
            client=request.user if request.user.is_authenticated else None,
            email=form.cleaned_data['email'],
        )
        messages.success(request, 'Заявка отправлена. Сотрудник свяжется с вами по e-mail.')
        return redirect('catalog')
    return render(request, 'book.html', {'apt': apt, 'form': form})


@login_required
def favorites(request):
    items = Apartment.objects.filter(favorite__user=request.user)
    return render(request, 'favorites.html', {'apartments': items, 'fav_ids': _fav_ids(request.user)})


@login_required
@require_POST
def favorite_toggle(request, pk):
    apt = get_object_or_404(Apartment, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, apartment=apt)
    if not created:
        fav.delete()
    nxt = request.POST.get('next', '')
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        nxt = 'catalog'
    return redirect(nxt)


def management(request):
    return render(request, 'management.html', {'sidebar': True})


@staff_required
def employees(request):
    people = get_user_model().objects.filter(is_staff=True).order_by('username')
    return render(request, 'employees.html', {'people': people, 'sidebar': True})


@staff_required
def requests_list(request):
    items = BookingRequest.objects.select_related('apartment', 'client', 'contract')
    return render(request, 'requests.html', {'items': items, 'sidebar': True})


@staff_required
def contract_create(request, pk):
    req = get_object_or_404(BookingRequest.objects.select_related('apartment', 'client'), pk=pk)
    if Contract.objects.filter(request=req).exists():
        messages.info(request, 'Договор по этой заявке уже составлен.')
        return redirect('contracts')
    form = ContractForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contract = form.save(commit=False)
        contract.request = req
        contract.total_cost = req.apartment.price
        contract.save()
        messages.success(request, f'Договор №{contract.pk} сохранён.')
        return redirect('contracts')
    return render(request, 'contract_form.html', {'form': form, 'req': req})


@staff_required
def contracts(request):
    items = Contract.objects.select_related('request__client', 'request__apartment')
    return render(request, 'contracts.html', {'items': items, 'today': date.today(), 'sidebar': True})


@staff_required
def reports(request):
    by_date = Contract.objects.values('signed_date').annotate(n=Count('id')).order_by('signed_date')
    by_month = (Contract.objects.exclude(status=Contract.CANCELLED)
                .annotate(m=TruncMonth('signed_date')).values('m')
                .annotate(total=Sum('total_cost')).order_by('m'))
    data = {
        'contracts': {'labels': [r['signed_date'].strftime('%d.%m') for r in by_date],
                      'values': [r['n'] for r in by_date]},
        'sales': {'labels': [r['m'].strftime('%m.%Y') for r in by_month],
                  'values': [r['total'] for r in by_month]},
    }
    return render(request, 'reports.html', {'chart_data': data, 'sidebar': True})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
        return redirect('catalog')
    return render(request, 'register.html', {'form': form})
