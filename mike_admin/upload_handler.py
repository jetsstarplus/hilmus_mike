def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.aac', '.ogg', '.mp3', '.wav', 'm4a', 'flac', 'mp4', 'wma']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    