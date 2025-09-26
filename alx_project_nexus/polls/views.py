from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from .models import Poll, Option, Vote
from .serializers import PollSerializer, VoteSerializer, ResultSerializer
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Welcome to the Poll System!")

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def perform_create(self, serializer):
        serializer.save()

class VoteAPIView(APIView):
    def post(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            if not poll.is_active():
                return Response({'error': 'Poll has expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = VoteSerializer(data=request.data)
            if serializer.is_valid():
                option = serializer.validated_data['option']
                if not Option.objects.filter(id=option.id, poll=poll).exists():
                    return Response({'error': 'Invalid option'}, status=status.HTTP_400_BAD_REQUEST)
                
                user_ip = request.META.get('REMOTE_ADDR')
                Vote.objects.create(poll=poll, option=option, user_ip=user_ip)
                return Response({'message': 'Vote cast successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Poll.DoesNotExist:
            return Response({'error': 'Poll not found'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'error': 'You have already voted'}, status=status.HTTP_400_BAD_REQUEST)

class ResultsAPIView(APIView):
    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            results = Vote.objects.filter(poll=poll).values('option__id', 'option__text').annotate(vote_count=Count('option__id')).order_by('-vote_count')
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)
        except Poll.DoesNotExist:
            return Response({'error': 'Poll not found'}, status=status.HTTP_404_NOT_FOUND)