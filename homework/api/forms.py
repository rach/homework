from wtforms import fields, Form, validators, Field, widgets


class GeoCoordField(Field):
    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return u','.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            coords = [x.strip() for x in valuelist[0].split(',')]

            if len(coords) != 2:
                raise ValueError(self.gettext('Not a valid coordinate value'))
            try:
                lat, lng = float(coords[0]), float(coords[1])
                if not -90 < lng < 90 or not -180 < lat < 180:
                    raise ValueError(self.gettext('Not a valid coordinate value'))
                self.data = (lat, lng)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid coordinate value'))


class ListingFilterForm(Form):
    status = fields.StringField(
        default='active',
        validators=[
            validators.Optional(),
            validators.AnyOf(['all', 'active', 'pending', 'sold'])
        ],
    )
    min_price = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    max_price = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    min_bed = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    max_bed = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    min_bath = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    max_bath = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    coord = GeoCoordField()
    distance = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ]
    )
    before = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=0)
        ]
    )
    after = fields.IntegerField(
        validators=[
            validators.Optional(),
            validators.NumberRange(min=0)
        ]
    )

    def validate_coord(self, field):
        if bool(self.distance.data) !=  bool(field.data):
            raise validators.ValidationError("distance and coord is required with coordinates")
