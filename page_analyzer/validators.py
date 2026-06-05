from validators import url as url_validate


def validate_url(data: dict) -> dict:
    errors = {}
    name = data.get("name", "")

    if not name:
        errors["name"] = "Необходимо заполнить"
    elif len(name) > 255:
        errors["name"] = "URL превышает 255 символов"
    elif not url_validate(name):
        errors["name"] = "Некорректный URL"

    return errors