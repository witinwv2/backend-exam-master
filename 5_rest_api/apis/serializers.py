from rest_framework import serializers
from .models import School, Classroom, Teacher, Student

class TeacherListSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Classroom.objects.all()
    )

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms']


class TeacherSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        many=True
    )

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms']

    def create(self, validated_data):
        classrooms = validated_data.pop('classrooms', [])
        teacher = Teacher.objects.create(**validated_data)
        teacher.classrooms.set(classrooms)
        return teacher

    def update(self, instance, validated_data):
        classrooms = validated_data.pop('classrooms', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if classrooms is not None:
            instance.classrooms.set(classrooms)

        return instance




class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender']


class ClassroomSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Classroom
        fields = ['id', 'school', 'grade', 'section']


class ClassroomDetailSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    teachers = TeacherListSerializer(many=True, read_only=True)
    students = StudentListSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'school', 'grade', 'section', 'teachers', 'students']




class StudentSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), write_only=True, source='classroom')

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom', 'classroom_id']


class SchoolSerializer(serializers.ModelSerializer):
    classroom_count = serializers.IntegerField(read_only=True)
    teacher_count = serializers.IntegerField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'short_name', 'address', 'classroom_count', 'teacher_count', 'student_count']
