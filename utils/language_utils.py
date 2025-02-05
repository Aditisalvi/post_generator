import pycountry

def get_all_languages():
    return sorted(
        [(language.name, language.alpha_2) for language in pycountry.languages if hasattr(language, "alpha_2")],
        key=lambda x: x[0]
    )
