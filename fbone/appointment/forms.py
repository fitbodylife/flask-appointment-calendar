from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, TextField, TextAreaField,
                     SubmitField, DateTimeField, SelectField)
from wtforms.validators import Required, Length, Email
from flask.ext.wtf.html5 import EmailField

from ..user import User
from ..utils import (USERNAME_LEN_MIN, USERNAME_LEN_MAX)

EMAIL_LEN_MIN = 4
EMAIL_LEN_MAX = 64

CONTENT_LEN_MIN = 16
CONTENT_LEN_MAX = 1024

TIMEZONES = {
    "TZ1": [("-8.0", "(GMT -8:00) Pacific Time (US & Canada)"),
            ("-7.0", "(GMT -7:00) Mountain Time (US & Canada)"),
            ("-6.0", "(GMT -6:00) Central Time (US & Canada), Mexico City"),
            ("-5.0", "(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima")],
    "TZ2": [("8.0", "(GMT +8:00) Beijing, Perth, Singapore, Hong Kong")],
    "TZ3": [("-12.0", "(GMT -12:00) Eniwetok, Kwajalein"),
            ("-11.0", "(GMT -11:00) Midway Island, Samoa"),
            ("-10.0", "(GMT -10:00) Hawaii"),
            ("-9.0", "(GMT -9:00) Alaska"),
            ("-8.0", "(GMT -8:00) Pacific Time (US & Canada)"),
            ("-7.0", "(GMT -7:00) Mountain Time (US & Canada)"),
            ("-6.0", "(GMT -6:00) Central Time (US & Canada), Mexico City"),
            ("-5.0", "(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima"),
            ("-4.0", "(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz"),
            ("-3.5", "(GMT -3:30) Newfoundland"),
            ("-3.0", "(GMT -3:00) Brazil, Buenos Aires, Georgetown"),
            ("-2.0", "(GMT -2:00) Mid-Atlantic"),
            ("-1.0", "(GMT -1:00 hour) Azores, Cape Verde Islands"),
            ("0.0", "(GMT) Western Europe Time, London, Lisbon, Casablanca"),
            ("1.0", "(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris"),
            ("2.0", "(GMT +2:00) Kaliningrad, South Africa"),
            ("3.0", "(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg"),
            ("3.5", "(GMT +3:30) Tehran"),
            ("4.0", "(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi"),
            ("4.5", "(GMT +4:30) Kabul"),
            ("5.0", "(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent"),
            ("5.5", "(GMT +5:30) Bombay, Calcutta, Madras, New Delhi"),
            ("5.75", "(GMT +5:45) Kathmandu"),
            ("6.0", "(GMT +6:00) Almaty, Dhaka, Colombo"),
            ("7.0", "(GMT +7:00) Bangkok, Hanoi, Jakarta"),
            ("8.0", "(GMT +8:00) Beijing, Perth, Singapore, Hong Kong"),
            ("9.0", "(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk"),
            ("9.5", "(GMT +9:30) Adelaide, Darwin"),
            ("10.0", "(GMT +10:00) Eastern Australia, Guam, Vladivostok"),
            ("11.0", "(GMT +11:00) Magadan, Solomon Islands, New Caledonia"),
            ("12.0", "(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka")]
}


class SelectOptgroupField(SelectField):
    """
    Monkey-patched SelectField to make it support one-level optgroup.
    """
    pass


class MakeAppointmentForm(Form):
    next = HiddenField()

    first_name = TextField(u'Your first name.',
                           [Required(),
                            Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    last_name = TextField(u'Your last name.',
                          [Required(),
                           Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    email = EmailField(u'Email',
                       [Required(),
                        Email(),
                        Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)])
    start_datetime = DateTimeField(u'Start Time')
    end_datetime = DateTimeField(u'End Time')
    timezone = SelectOptgroupField(u'Timezone',
                                   choices=TIMEZONES)
    content = TextAreaField(u'Content',
                            [Required(),
                             Length(CONTENT_LEN_MIN, CONTENT_LEN_MAX)])
    submit = SubmitField('OK')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')
