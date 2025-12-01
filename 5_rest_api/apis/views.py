from rest_framework import viewsets
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import School, Classroom, Teacher, Student
from .serializers import (
    SchoolSerializer,
    ClassroomSerializer, ClassroomDetailSerializer,
    TeacherSerializer, TeacherListSerializer,
    StudentSerializer, StudentListSerializer,
)
from .filters import SchoolFilter, ClassroomFilter, TeacherFilter, StudentFilter


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SchoolFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            classroom_count=Count('classrooms', distinct=True),
            teacher_count=Count('classrooms__teachers', distinct=True),
            student_count=Count('classrooms__students', distinct=True),
        )
        return qs


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related('school').prefetch_related('teachers', 'students').all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassroomFilter

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return ClassroomDetailSerializer
        return ClassroomSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related('classrooms').all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('classroom', 'classroom__school').all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer
