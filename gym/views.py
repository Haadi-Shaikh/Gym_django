from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import RegisterForm
from .models import MembershipPlan, Subscription


def home(request):
    plans = MembershipPlan.objects.all()[:3]
    return render(request, 'gym/home.html', {'plans': plans})


def plan_list(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'gym/plans.html', {'plans': plans})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    subscriptions = request.user.subscriptions.select_related('plan')
    for subscription in subscriptions:
        subscription.refresh_status()

    active_subscription = subscriptions.filter(status=Subscription.STATUS_ACTIVE).first()
    context = {
        'active_subscription': active_subscription,
        'subscriptions': subscriptions,
    }
    return render(request, 'gym/dashboard.html', context)


@login_required
def profile_view(request):
    latest_subscription = request.user.subscriptions.select_related('plan').first()
    if latest_subscription:
        latest_subscription.refresh_status()
    return render(
        request,
        'gym/profile.html',
        {'latest_subscription': latest_subscription},
    )


@login_required
def select_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, id=plan_id)

    if request.method == 'POST':
        today = timezone.localdate()
        active_subscription = request.user.subscriptions.filter(status=Subscription.STATUS_ACTIVE).first()
        if active_subscription:
            active_subscription.status = Subscription.STATUS_EXPIRED
            active_subscription.save(update_fields=['status'])

        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=today,
            end_date=today + timedelta(days=max(plan.duration - 1, 0)),
        )
        messages.success(
            request,
            f'You have successfully selected the {subscription.plan.name} plan.',
        )
        return redirect('dashboard')

    return render(request, 'gym/select_plan.html', {'plan': plan})
