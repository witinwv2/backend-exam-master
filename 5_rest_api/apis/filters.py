import django_filters
from .models import School, Classroom, Teacher, Student

class SchoolFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']


class ClassroomFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(field_name='school__id')

    class Meta:
        model = Classroom
        fields = ['school', 'grade', 'section']


class TeacherFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(method='filter_by_school')
    classroom = django_filters.NumberFilter(field_name='classrooms__id')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender')

    class Meta:
        model = Teacher
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']

    def filter_by_school(self, queryset, name, value):
        return queryset.filter(classrooms__school__id=value).distinct()


class StudentFilter(django_filters.FilterSet):
    school = django_filters.NumberFilter(method='filter_by_school')
    classroom = django_filters.NumberFilter(field_name='classroom__id')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = django_filters.CharFilter(field_name='gender')

    class Meta:
        model = Student
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']

    def filter_by_school(self, queryset, name, value):
        return queryset.filter(classroom__school__id=value)
