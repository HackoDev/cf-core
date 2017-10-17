from . import models


def social_links(request):
    return {
        'social_links': models.SocialLink.objects.all()
    }


def partners(request):
    return {
        'regular_partners': models.RegularPartner.objects.all(),
        'information_partners': models.InformationPartner.objects.all(),
    }
