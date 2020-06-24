class UIDB64Converter:
    regex = r'[0-9A-Za-z_\-]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class TokenConverter:
    regex = r'[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
