import datetime
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserCreationForm
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import form_class, formset_class, rows_for
from .labels import label_for
from .registry import navigation, resources

PAGE_SIZE = 25


def _in_uzbek(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        with translation.override("uz"):
            return view(request, *args, **kwargs)

    return wrapper


def staff_required(view):
    @wraps(view)
    @_in_uzbek
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_active and request.user.is_staff):
            return redirect(f"{reverse('panel:login')}?next={request.get_full_path()}")
        return view(request, *args, **kwargs)

    return wrapper


def superuser_required(view):
    @wraps(view)
    @staff_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Bu bo'lim faqat bosh administrator uchun.")
        return view(request, *args, **kwargs)

    return wrapper


def _context(request, **extra):
    return {"nav": navigation(), "current": extra.get("resource"), **extra}


def _get(model, pk):
    from django.core.exceptions import ValidationError

    try:
        return model.objects.get(pk=pk)
    except (model.DoesNotExist, ValidationError, ValueError):
        raise Http404


def _resource(slug):
    resource = resources().get(slug)
    if resource is None:
        raise Http404
    return resource


# --- Login -------------------------------------------------------------------


@_in_uzbek
def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or reverse("panel:dashboard")
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}, request.is_secure()):
        next_url = reverse("panel:dashboard")
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(next_url)
    form = AuthenticationForm(request, data=request.POST or None)
    error = ""
    if request.method == "POST":
        if form.is_valid() and form.get_user().is_staff:
            login(request, form.get_user())
            return redirect(next_url)
        error = "Login yoki parol noto'g'ri."
    return render(request, "panel/login.html", {"form": form, "next": next_url, "error": error})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("panel:login")


# --- Dashboard ---------------------------------------------------------------


@staff_required
def dashboard(request):
    from core.models import ContactMessage, HeroSlide
    from news.models import NewsPost
    from prices.models import Price
    from products.models import ProductInquiry
    from services.models import Service

    week_ago = timezone.now() - datetime.timedelta(days=7)
    stats = [
        ("Yangi xabarlar (7 kun)", ContactMessage.objects.filter(created_at__gte=week_ago).count(), "messages"),
        ("Mahsulot so'rovlari (7 kun)", ProductInquiry.objects.filter(created_at__gte=week_ago).count(), "inquiries"),
        ("Faol xizmatlar", Service.objects.filter(is_active=True).count(), "services"),
        ("Faol tariflar", Price.objects.filter(is_active=True).count(), "prices"),
        ("Hero slaydlar", HeroSlide.objects.filter(is_active=True).count(), "hero"),
        ("Yangiliklar", NewsPost.objects.filter(is_active=True).count(), "news"),
    ]
    return render(
        request,
        "panel/dashboard.html",
        _context(
            request,
            stats=stats,
            latest_messages=ContactMessage.objects.all()[:5],
            latest_inquiries=ProductInquiry.objects.select_related("product")[:5],
        ),
    )


# --- Lists -------------------------------------------------------------------


def _cell(obj, spec):
    name, _, kind = spec.partition("|")
    value = getattr(obj, name, "")
    if callable(value):
        value = value()
    if kind == "thumb":
        return {"kind": "thumb", "url": value.url if value else ""}
    if kind in ("toggle", "bool"):
        return {"kind": kind, "value": bool(value)}
    if kind == "money":
        return {"kind": "text", "value": f"${value}" if value is not None else "—"}
    if kind == "date":
        return {"kind": "text", "value": timezone.localtime(value).strftime("%d.%m.%Y") if value else "—"}
    if kind == "datetime":
        return {"kind": "text", "value": timezone.localtime(value).strftime("%d.%m.%Y %H:%M") if value else "—"}
    if kind == "trunc":
        text = " ".join(str(value or "").split())
        return {"kind": "text", "value": text[:80] + ("…" if len(text) > 80 else "")}
    if kind == "email":
        return {"kind": "email", "value": value}
    return {"kind": "text", "value": value if value not in (None, "") else "—"}


@staff_required
def object_list(request, slug):
    resource = _resource(slug)
    qs = resource.model.objects.all()
    query = request.GET.get("q", "").strip()
    if query and resource.search:
        condition = Q()
        for name in resource.search:
            condition |= Q(**{f"{name}__icontains": query})
        qs = qs.filter(condition)
    active = request.GET.get("active", "")
    if active in ("1", "0") and hasattr(resource.model, "is_active"):
        qs = qs.filter(is_active=active == "1")
    filters = []
    for fk in resource.filters:
        related = resource.model._meta.get_field(fk).related_model
        selected = request.GET.get(fk, "")
        if selected:
            qs = qs.filter(**{f"{fk}_id": selected})
        filters.append({"name": fk, "options": related.objects.all(), "selected": selected, "label": label_for(fk)})
        qs = qs.select_related(fk)
    if not qs.ordered:
        qs = qs.order_by("pk")
    page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
    rows = [{"obj": obj, "cells": [_cell(obj, spec) for spec, _ in resource.columns]} for obj in page]
    return render(
        request,
        "panel/list.html",
        _context(
            request,
            resource=resource,
            page=page,
            rows=rows,
            headers=[h for _, h in resource.columns],
            query=query,
            active=active,
            filters=filters,
            has_active=hasattr(resource.model, "is_active"),
        ),
    )


@staff_required
@require_POST
def toggle_active(request, slug, pk):
    resource = _resource(slug)
    obj = _get(resource.model, pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active"])
    state = "saytda ko'rinadi" if obj.is_active else "saytdan yashirildi"
    messages.success(request, f"\"{obj}\" {state}.")
    back = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(back, {request.get_host()}, request.is_secure()):
        back = reverse("panel:list", args=[slug])
    return redirect(back)


# --- Create / edit -----------------------------------------------------------


def _sections(resource, form):
    return [{"title": title, "rows": rows_for(form, specs)} for title, specs in resource.sections]


def _inline_blocks(resource, formsets):
    blocks = []
    for inline, formset in zip(resource.inlines, formsets):
        blocks.append(
            {
                "inline": inline,
                "formset": formset,
                "forms": [{"form": f, "rows": rows_for(f, inline.fields)} for f in formset.forms],
                "empty": {"form": formset.empty_form, "rows": rows_for(formset.empty_form, inline.fields)},
            }
        )
    return blocks


@staff_required
def object_edit(request, slug, pk=None):
    resource = _resource(slug)
    if resource.readonly:
        if pk is None:
            raise Http404
        return _object_view(request, resource, pk)
    obj = _get(resource.model, pk) if pk else None
    if obj is None and not resource.can_add:
        raise Http404
    Form = form_class(resource, editing=obj is not None)
    form = Form(request.POST or None, request.FILES or None, instance=obj)
    formsets = [
        formset_class(resource, inline)(
            request.POST or None, request.FILES or None, instance=obj, prefix=inline.name
        )
        for inline in resource.inlines
    ]
    if request.method == "POST":
        if form.is_valid() and all(fs.is_valid() for fs in formsets):
            with transaction.atomic():
                item = form.save(commit=False)
                if obj is None and hasattr(item, "created_by_id") and not item.created_by_id:
                    item.created_by = request.user
                item.save()
                form.save_m2m()
                for fs in formsets:
                    fs.instance = item
                    for child in fs.save(commit=False):
                        if hasattr(child, "created_by_id") and not child.created_by_id:
                            child.created_by = request.user
                        child.save()
                    for child in fs.deleted_objects:
                        child.delete()
            messages.success(request, f"{resource.singular} saqlandi.")
            if "_continue" in request.POST:
                return redirect("panel:edit", slug=slug, pk=item.pk)
            if "_addanother" in request.POST:
                return redirect("panel:add", slug=slug)
            return redirect("panel:list", slug=slug)
        messages.error(request, "Saqlanmadi: qizil bilan belgilangan joylarni to'g'rilang.")
    readonly_values = [
        (resource.model._meta.get_field(n).verbose_name, getattr(obj, n)) for n in resource.readonly_on_edit
    ] if obj else []
    return render(
        request,
        "panel/form.html",
        _context(
            request,
            resource=resource,
            obj=obj,
            form=form,
            sections=_sections(resource, form),
            inline_blocks=_inline_blocks(resource, formsets),
            readonly_values=readonly_values,
            has_translations=any(s.endswith("*") for _, specs in resource.sections for s in specs),
        ),
    )


def _object_view(request, resource, pk):
    obj = _get(resource.model, pk)
    fields = []
    for _title, specs in resource.sections:
        for name in specs:
            value = getattr(obj, name)
            if name == "created_at":
                value = timezone.localtime(value).strftime("%d.%m.%Y %H:%M")
            fields.append((label_for(name), value, name))
    return render(request, "panel/detail.html", _context(request, resource=resource, obj=obj, fields=fields))


@staff_required
def object_delete(request, slug, pk):
    resource = _resource(slug)
    obj = _get(resource.model, pk)
    if request.method == "POST":
        name = str(obj)
        obj.delete()
        messages.success(request, f"\"{name}\" o'chirildi.")
        return redirect("panel:list", slug=slug)
    return render(request, "panel/confirm_delete.html", _context(request, resource=resource, obj=obj))


# --- Account -----------------------------------------------------------------


@staff_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Parol o'zgartirildi.")
        return redirect("panel:dashboard")
    return render(request, "panel/simple_form.html", _context(request, form=form, title="Parolni o'zgartirish",
                                                             button="Parolni saqlash"))


class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")


@superuser_required
def users(request):
    people = get_user_model().objects.filter(is_staff=True).order_by("username")
    return render(request, "panel/users.html", _context(request, people=people))


@superuser_required
def user_add(request):
    form = NewUserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = True
        user.is_superuser = request.POST.get("is_superuser") == "on"
        user.save()
        messages.success(request, f"\"{user.username}\" qo'shildi.")
        return redirect("panel:users")
    return render(request, "panel/simple_form.html", _context(
        request, form=form, title="Yangi administrator", button="Qo'shish", superuser_checkbox=True))


@superuser_required
def user_password(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk, is_staff=True)
    form = SetPasswordForm(person, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        if person == request.user:
            update_session_auth_hash(request, person)
        messages.success(request, f"\"{person.username}\" uchun yangi parol o'rnatildi.")
        return redirect("panel:users")
    return render(request, "panel/simple_form.html", _context(
        request, form=form, title=f"{person.username}: yangi parol", button="Parolni saqlash"))


@superuser_required
@require_POST
def user_toggle(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk, is_staff=True)
    if person == request.user:
        messages.error(request, "O'zingizni o'chira olmaysiz.")
    else:
        person.is_active = not person.is_active
        person.save(update_fields=["is_active"])
        messages.success(request, f"\"{person.username}\" {'faollashtirildi' if person.is_active else 'bloklandi'}.")
    return redirect("panel:users")
