from django.forms import model_to_dict
from rest_framework import generics, viewsets
from example.models import (
    Subject, Attempt, Answer,
    Student, Testing, Question
)
from example.serializers import (
    SubjectSerializer, AnswerSerializer,
    StudentSerializer, TestingSerializer,
    AttemptSerializer, QuestionSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


class SubjectApiViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class AnswerApiView(APIView):
    def get(self, request: Request) -> Response:
        ret = Answer.objects.all()
        return Response({"data": AnswerSerializer(ret, many=True).data})

    def post(self, request: Request) -> Response:
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_answer = Answer(
            text=request.data["text"],
            is_correct=request.data["is_correct"],
            question=request.data["question"]
        )
        return Response({"new_answer": AnswerSerializer(new_answer).data})


class StudentApiView(APIView):
    def get(self, request: Request) -> Response:
        ret = Student.objects.all()
        return Response({"data": StudentSerializer(ret, many=True).data})

    def post(self, request: Request) -> Response:
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"new_student": serializer.data})

    def patch(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs.get("pk", None)
        if pk is None:
            return Response({"error": "PUT method is not allowed"})
        try:
            instance = Student.objects.get(pk=pk)
        except:
            return Response({"error": "Objects does not exist"})

        serializer = StudentSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response({"update_student": serializer.data})


class AttemptView(generics.ListCreateAPIView):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer


class TestingListApiView(generics.ListCreateAPIView):
    queryset = Testing.objects.all()
    serializer_class = TestingSerializer


class QuestionDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
