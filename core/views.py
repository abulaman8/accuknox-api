from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.utils import authed, is_valid_email
from core.models import FriendRequest


@api_view(['GET'])
@authed()
def search_users(request):
    data = request.GET
    page = data.get('page', 1)
    query = data.get('query').strip().lower()
    if is_valid_email(query):
        user = User.objects.prefetch_related(
            'profile').filter(email=query).first()
        if user:
            return Response([{
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
            }], status=status.HTTP_200_OK)
    else:
        first_name_q = Q(first_name__icontains=query)
        last_name_q = Q(last_name__icontains=query)
        username_q = Q(username__icontains=query)
        users = User.objects.prefetch_related('profile').filter(
            first_name_q | last_name_q | username_q).all()
        paginated = Paginator(users, 10)
        users = paginated.get_page(page)

        return Response([{
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        } for user in users], status=status.HTTP_200_OK)


@api_view(['POST'])
@authed()
def send_friend_request(request):
    data = request.data
    to_user = data.get('user')
    if not to_user:
        return Response({"error": "To user is required"}, status=status.HTTP_400_BAD_REQUEST)
    from_user = request.user
    if from_user == to_user:
        return Response({"error": "You can't send friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(email=to_user).first()
    if not user:
        return Response({"error": "To user not found"}, status=status.HTTP_404_NOT_FOUND)
    if FriendRequest.objects.filter(from_user=from_user, to_user=user).exists():
        return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
    last_3 = FriendRequest.objects.filter(
        from_user=from_user).order_by('-created_at').all()[:3]
    times = [r.created_at.minute for r in last_3]
    if len(times) == 3 and times[0] == times[1] == times[2]:
        return Response({"error": "You can only 3 send friend requests in 1 minute"}, status=status.HTTP_400_BAD_REQUEST)
    FriendRequest.objects.create(from_user=from_user, to_user=user)
    return Response({"message": "Friend request sent successfully"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authed()
def manage_friend_request(request, action):
    data = request.data
    if action not in ['accept', 'reject']:
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
    from_user = data.get('user')
    from_user = User.objects.filter(email=from_user).first()
    if not from_user:
        return Response({"error": "From user is required"}, status=status.HTTP_400_BAD_REQUEST)
    to_user = request.user
    friend_request = FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user).first()
    if not friend_request:
        return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)
    if action == 'reject':
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({"message": "Friend request rejected successfully"}, status=status.HTTP_200_OK)
    elif action == 'accept':
        if friend_request.status == 'accepted':
            return Response({"error": "Friend request already accepted"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({"message": "Friend request accepted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authed()
def get_friends(request):
    user = request.user
    friends = user.sent_requests.prefetch_related(
        'to_user',
    ).filter(status='accepted', from_user=user).all()
    return Response([{
        "email": req.to_user.email,
        "first_name": req.to_user.first_name,
        "last_name": req.to_user.last_name,
        "username": req.to_user.username,
    } for req in friends], status=status.HTTP_200_OK)


@api_view(['GET'])
@authed()
def pending_requests(request):
    user = request.user
    pending = user.received_requests.prefetch_related(
        'from_user',
    ).filter(status='pending', to_user=user).all()
    return Response([{
        "email": req.from_user.email,
        "first_name": req.from_user.first_name,
        "last_name": req.from_user.last_name,
        "username": req.from_user.username,
    } for req in pending], status=status.HTTP_200_OK)
