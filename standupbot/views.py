import json
import random

from django.conf import settings
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from slackclient import SlackClient

from .models import Question, Answer, User

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
SLACK_COMMON_CHANNEL = getattr(settings, 'SLACK_COMMON_CHANNEL', None)
TEXT_NO_MORE_QUESTIONS = getattr(settings, 'TEXT_NO_MORE_QUESTIONS', None)
TEXT_STANDUP_IS_DONE = getattr(settings, 'TEXT_STANDUP_IS_DONE', None)
TEXT_NO_USER = getattr(settings, 'TEXT_NO_USER', None)
TEXT_CHANNEL_MESSAGE = getattr(settings, 'TEXT_CHANNEL_MESSAGE', None)
TEXT_NEW_DAY = getattr(settings, 'TEXT_NEW_DAY', None)
TEXT_REMINDER = getattr(settings, 'TEXT_REMINDER', None)
IMAGE_REMINDER = getattr(settings, 'IMAGE_REMINDER', None)

SLACK_SEND_IM_METHOD = 'chat.postMessage'

slack_client = SlackClient(SLACK_BOT_USER_TOKEN)


@api_view(['GET', 'POST'])
def health_check(request):
    return Response({"message": "It works!"}, status=status.HTTP_200_OK)


def send_message(channel, text, attachments=None):
    slack_client.api_call(method=SLACK_SEND_IM_METHOD,
                          channel=channel,
                          attachments=attachments,
                          text=text)

@api_view(['GET'])
def send_first_question_to_all_users(request):
    users = User.objects.filter(is_active=True)
    first_question = Question.objects.filter(is_active=True).order_by('order_number').first()
    for u in users:
        send_message(channel=u.channel_id, text=TEXT_NEW_DAY)
        send_message(channel=u.channel_id, text='*{}*'.format(first_question.text))
    return Response({'response': 'ok'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def send_standup_reminder(request):
    users = User.objects.filter(is_active=True)
    number_of_active_questions = Question.objects.filter(is_active=True).count()
    today_date = datetime.today().date()

    for u in users:
        users_answers = Answer.objects.filter(user=u, date=today_date).count()
        if users_answers < number_of_active_questions:
            print("User {} haven't completed standup".format(u.name))
            attachments = [{
                'image_url': IMAGE_REMINDER
            }]
            print(attachments)
            send_message(channel=u.channel_id, text=TEXT_REMINDER, attachments=attachments)
    return Response({'response': 'ok'}, status=status.HTTP_200_OK)


def send_question_to_user(question, user):
    send_message(channel=user.channel_id, text='*{}*'.format(question.text))


def generate_random_color():
    random_generator = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (random_generator(), random_generator(), random_generator())


def send_answers_to_common_channels(user):
    today_date = datetime.today().date()
    answers = Answer.objects.order_by('created_at').filter(user=user,
                                                           date=today_date)
    attachments = []
    for a in answers:
        attachments.append({
            'title': a.question.text,
            'text': a.text,
            'color': generate_random_color()
        })
    greetings_text = TEXT_CHANNEL_MESSAGE.format(user.slack_id)
    send_message(SLACK_COMMON_CHANNEL, text=greetings_text, attachments=attachments)


class Events(APIView):
    def create_answer(self, user, text, question):
        today_date = datetime.today().date()
        answer = Answer(text=text, date=today_date, user=user, question=question)
        answer.save()

    def handle_answer_for_a_first_question(self, user, text):
        question_query = Question.objects.filter(is_active=True).order_by('order_number')
        first_question = question_query.first()
        self.create_answer(user, text, first_question)

        if question_query.count() > 1:
            return question_query[1]
        else:
            send_message(user.channel_id, text=TEXT_STANDUP_IS_DONE)
            send_answers_to_common_channels(user=user)

    def handle_middle_answer(self, latest_answer, user, text):
        prev_question = latest_answer.question

        # send next question
        question_query = Question.objects.filter(
            order_number__gt=prev_question.order_number,
            is_active=True
        ).order_by('order_number')

        question = question_query.first()
        left_questions = question_query.count() - 1

        if question is None:
            # send survey is done
            print('no more questions')
            send_message(user.channel_id, text=TEXT_NO_MORE_QUESTIONS)
            return

        # answer for a next_question
        self.create_answer(user, text, question)
        # send next question

        # check_for_the_last_question
        if left_questions == 0:
            print('Last question was sent')
            send_message(user.channel_id, text=TEXT_STANDUP_IS_DONE)
            send_answers_to_common_channels(user=user)
        else:
            return question_query[1]

    def process_user_message(self, user, text, channel):
        today_date = datetime.today().date()
        latest_answer = Answer.objects.order_by('-created_at').filter(user=user,
                                                                      date=today_date).first()
        if latest_answer is None:
            # answer for a first question
            print('answer for a first question')
            question_to_send = self.handle_answer_for_a_first_question(user, text)
        else:
            # answer for a middle question
            print('answer for a middle question')
            print(latest_answer)
            question_to_send = self.handle_middle_answer(latest_answer, user, text)

        if question_to_send is not None:
            send_question_to_user(question_to_send, user)

    def post(self, request, *args, **kwargs):
        slack_message = request.data

        print(json.dumps(slack_message))

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)

        if 'event' in slack_message:
            event_message = slack_message.get('event')

            if event_message.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            slack_user_id = event_message.get('user')
            text = event_message.get('text')
            channel = event_message.get('channel')

            try:
                user = User.objects.get(slack_id=slack_user_id)
                if user.channel_id is None or len(user.channel_id) == 0:
                    print('channel id is None')
                    user.channel_id = channel
                    user.save()
                if user.is_active:
                    self.process_user_message(user, text, channel)
            except Exception as e:
                print('User not found exception')
                print(e)
                send_message(channel=channel, text=TEXT_NO_USER)

        return Response(status=status.HTTP_200_OK)
