from .models import LikedAnswer

def get_serialized_answers(request, answers):
    serialized_answers = []
    user = request.user

    for answer in answers:
        liked = False
        if user.is_authenticated:
            liked = LikedAnswer.objects.filter(user=user, answer=answer).exists()
        
        serialized_answers.append({
            'id': answer.id,
            'user': answer.user.username,
            'question': answer.question.id,
            'content': answer.content,
            'created_at': answer.created_at.isoformat(),
            'likes': answer.likes,
            'liked_status': liked
        })

    return serialized_answers
