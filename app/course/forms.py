from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from .models import Courses


class add_course_form(FlaskForm):
    Course_Code = StringField('Course Code', validators=[DataRequired(), Length(min=5, max=10)], render_kw={'class': 'form-control form-group'})
    Course_Name = StringField('Course Name', validators=[DataRequired(), Length(min=10, max=100)], render_kw={'class': 'form-control form-group'})
    Course_description = TextAreaField('Enter Description', [DataRequired()], render_kw={'class': 'form-control form-group'})
    resources_link = StringField('Resources Link', render_kw={'class': 'form-control form-group'})
    submit = SubmitField('Add Course', render_kw={'class': 'btn btn-info btn-pill', 'style': 'height : 50px;'})

    def validate_Course_Code(self, Course_Code):
        c = Courses.query.filter_by(course_code=Course_Code.data).first()
        if c is not None:
            raise ValidationError('Please Use a Different Code')

    def validate_Course_Name(self, Course_Name):
        c = Courses.query.filter_by(Course_name=Course_Name.data).first()
        if c is not None:
            raise ValidationError('Please Use a Different Course Name')
