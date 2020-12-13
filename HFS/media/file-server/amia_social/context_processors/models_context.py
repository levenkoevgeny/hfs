from social_profile.models import EducationalInstitution, Language, LanguageLevel, Specialty, Skill, Interest


def models_context(request):

    return {'educational': EducationalInstitution.objects.all(),
            'language_levels': LanguageLevel.objects.all(),
            'languages': Language.objects.all(),
            'specialties': Specialty.objects.all(),
            'skills': Skill.objects.all(),
            'interests': Interest.objects.all(),
            }