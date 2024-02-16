from django.test import TestCase, Client
from machine.slot_machine import Slot_machine
from unittest.mock import Mock, patch
from machine.models import User, Roll
from machine import slot_machine_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        Token.objects.create(user=User.objects.create(
            username='test', password='test', balance=1000))
        self.token = Token.objects.get(user__username='test')
        for i in range(5):
            Roll.objects.create(cost=20, user=User.objects.get(
                username='test'), board_info='[]', winings_multiplier=5, scatter_multiplier=0)

    def test_roll_machine(self):
        mock_slot_machine_roll_machine = Mock(
            return_value=(5, "", [], 0, [-1, -1, -1, -1, -1]))
        with patch.object(Slot_machine, 'roll_machine', mock_slot_machine_roll_machine):
            response = self.client.post(
                reverse('roll'), {'cost': 20}, HTTP_AUTHORIZATION="Token " + str(self.token))
            self.assertEqual(response.status_code, 200)
            response_json = response.json()
            self.assertEqual(response_json['cost'], 20)
            self.assertEqual(response_json['winings_multiplier'], 5)
            self.assertEqual(response_json['scatter_multiplier'], 0)
            self.assertEqual(response_json['result'], 100)

    def test_roll_with_wrong_cost(self):
        mock_slot_machine_roll_machine = Mock(
            return_value=(5, "", [], 0, [-1, -1, -1, -1, -1]))
        with patch.object(Slot_machine, 'roll_machine', mock_slot_machine_roll_machine):
            response = self.client.post(
                reverse('roll'), {'cost': 0}, HTTP_AUTHORIZATION="Token " + str(self.token))
            self.assertEqual(response.status_code, 400)

            response = self.client.post(
                reverse('roll'), {'cost': -1}, HTTP_AUTHORIZATION="Token " + str(self.token))
            self.assertEqual(response.status_code, 400)

            response = self.client.post(
                reverse('roll'), {'cost': 1001}, HTTP_AUTHORIZATION="Token " + str(self.token))
            self.assertEqual(response.status_code, 400)

    def test_user_addMoney(self):
        response = self.client.post(reverse('addMoney'), {
                                    'amount': 100}, HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['balance'], 1100)

    def test_user_addMoney_with_wrong_amount(self):
        response = self.client.post(reverse('addMoney'), {
                                    'amount': 0}, HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('addMoney'), {
                                    'amount': -1}, HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 400)

    def test_user_info(self):
        response = self.client.get(
            reverse('user'), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['balance'], 1000)
        self.assertEqual(response_json['username'], 'test')

    def test_user_rollHistory(self):
        response = self.client.get(
            reverse('rollHistory'), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        for i in range(5):
            self.assertEqual(response_json[i]['cost'], 20)
            self.assertEqual(response_json[i]['winings_multiplier'], 5)
            self.assertEqual(response_json[i]['scatter_multiplier'], 0)

    def test_user_statistics(self):
        response = self.client.get(
            reverse('statistics'), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()

        self.assertEqual(response_json['max_amount_won'], 100)
        self.assertEqual(response_json['total_amoounth_won'], 100*5)
        self.assertEqual(response_json['amount_won_per_spin'], 100)
        self.assertEqual(response_json['total_amount_bet'], 20*5)
        self.assertEqual(response_json['average_bet'], 20)
        self.assertEqual(response_json['max_multiplyer'], 5)
        self.assertEqual(response_json['average_multiplyer'], 5)
        self.assertEqual(response_json['std_bet'], 0)
        self.assertEqual(response_json['std_won'], 0)
        self.assertEqual(response_json['std_multiplyer'], 0)

    def test_userHistory(self):
        response = self.client.get(
            reverse('userHistory', args=[1]), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['cost'], 20)
        self.assertEqual(response_json['winings_multiplier'], 5)
        self.assertEqual(response_json['scatter_multiplier'], 0)
        self.assertEqual(response_json['result'], 100)

    def test_user_history_with_wrong_id(self):
        response = self.client.get(
            reverse('userHistory', args=[7]), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 404)

    def test_leaderboard(self):
        response = self.client.get(reverse('leaderboard', args=[
                                   "amounth_won"]), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json[0]['amounth_won'], 100*5)
        self.assertEqual(response_json[0]['user__username'], 'test')

    def test_leaderboard_with_wrong_criteria(self):
        response = self.client.get(reverse('leaderboard', args=[
                                   "wrong_Criteria"]), HTTP_AUTHORIZATION="Token " + str(self.token))
        self.assertEqual(response.status_code, 400)

    def test_rigged_roll_machine(self):

        response = self.client.post(
            reverse('riggedRoll'),
            {'cost': 20, 'password': slot_machine_settings.RIGGED_SPIN_PASSWORD,
                'rigged_reels_symbols': '[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]'},
            HTTP_AUTHORIZATION="Token " + str(self.token))

        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['cost'], 20)
        self.assertEqual(response_json['winings_multiplier'], 100)
        self.assertEqual(response_json['scatter_multiplier'], 0)
        self.assertEqual(response_json['result'], 100*20)

    def test_rigged_roll_with_wrong_password(self):
        response = self.client.post(
            reverse('riggedRoll'),
            {'cost': 20, 'password': 'wrong_password',
             'rigged_reels_symbols': '[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]'},
            HTTP_AUTHORIZATION="Token " + str(self.token))

        self.assertEqual(response.status_code, 400)

    def test_rigged_roll_with_wrong_cost(self):
        response = self.client.post(
            reverse('riggedRoll'),
            {'cost': 0, 'password': slot_machine_settings.RIGGED_SPIN_PASSWORD,
             'rigged_reels_symbols': '[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]'},
            HTTP_AUTHORIZATION="Token " + str(self.token))

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse('riggedRoll'),
            {'cost': -5, 'password': slot_machine_settings.RIGGED_SPIN_PASSWORD,
             'rigged_reels_symbols': '[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]'},
            HTTP_AUTHORIZATION="Token " + str(self.token))

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse('riggedRoll'),
            {'cost': 1001, 'password': slot_machine_settings.RIGGED_SPIN_PASSWORD,
             'rigged_reels_symbols': '[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]'},
            HTTP_AUTHORIZATION="Token " + str(self.token))

        self.assertEqual(response.status_code, 400)
