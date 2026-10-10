from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.utils.text import slugify
import io
import qrcode

from scancv.ecv.models import Ecv

def home(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        city = request.POST.get("city", "").strip()
        skill = request.POST.get("skill", "").strip()
        if name and city and skill:
            base = slugify(name) or "cv"
            slug = base
            n = 2
            while Ecv.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1
            ecv = Ecv.objects.create(name=name, city=city, skill=skill, slug=slug)
            return redirect("public", slug=ecv.slug)
    return render(request, "home.html")

def public(request, slug):
    ecv = get_object_or_404(Ecv, slug=slug)
    return render(request, "public.html", {"ecv": ecv})

def qr_png(request, slug):
    ecv = get_object_or_404(Ecv, slug=slug)
    url = request.build_absolute_uri(f"/s/{ecv.slug}/")
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return HttpResponse(buf.getvalue(), content_type="image/png")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("s/<slug:slug>/", public, name="public"),
    path("s/<slug:slug>/qr.png", qr_png, name="qr"),
]
