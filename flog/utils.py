from .extensions import db

from datetime import datetime

def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%d-%b-%Y')
    except ValueError:
        raise ValueError("Incorrect data format")

def mongo_to_dict(obj):
    return_data = []

    if isinstance(obj, db.DynamicDocument):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in ("id",):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], db.DateTimeField):
            if data:
                return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.StringField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], db.IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], db.ListField):
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], db.EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))
        elif isinstance(obj._fields[field_name], db.DictField):
            return_data.append((field_name, data))

    return dict(return_data)