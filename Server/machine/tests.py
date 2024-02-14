from django.test import TestCase, Client
from machine.slot_machine import Slot_machine, Reel
from unittest.mock import Mock, patch
from machine.models import User, Roll
from machine import slot_machine_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        Token.objects.create(user=User.objects.create(username='test', password='test',balance=1000))
        self.token = Token.objects.get(user__username='test')
        for i in range(5):
            Roll.objects.create(cost=20, user=User.objects.get(username='test'), board_info='[]', winings_multyplier=5, scatter_multiplier=0)

    
    def test_roll_machine(self):
        mock_slot_machine_roll_machine=Mock(return_value=(5,"",[],0,[-1,-1,-1,-1,-1]))
        with patch.object(Slot_machine,'roll_machine',mock_slot_machine_roll_machine):
            response = self.client.post(reverse('roll'), {'cost': 20}, HTTP_AUTHORIZATION ="Token "+ str(self.token))
            self.assertEqual(response.status_code, 200)
            response_json = response.json()
            self.assertEqual(response_json['cost'], 20)
            self.assertEqual(response_json['winings_multyplier'], 5)
            self.assertEqual(response_json['scatter_multiplier'], 0)
            self.assertEqual(response_json['result'], 100)


    def test_user_addMoney(self):
        response = self.client.post(reverse('addMoney'), {'amount': 100}, HTTP_AUTHORIZATION ="Token "+ str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['balance'], 1100)


    def test_user_info(self):
        response = self.client.get(reverse('user'), HTTP_AUTHORIZATION ="Token "+ str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['balance'], 1000)
        self.assertEqual(response_json['username'], 'test')


    def test_user_rollHistory(self):
        response = self.client.get(reverse('rollHistory'), HTTP_AUTHORIZATION ="Token "+ str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        for i in range(5):
            self.assertEqual(response_json[i]['cost'], 20)
            self.assertEqual(response_json[i]['winings_multyplier'], 5)
            self.assertEqual(response_json[i]['scatter_multiplier'], 0)

        
    def test_user_statistics(self):
        response = self.client.get(reverse('statistics'), HTTP_AUTHORIZATION ="Token "+ str(self.token))
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
        response = self.client.get(reverse('userHistory', args=[1]), HTTP_AUTHORIZATION ="Token "+ str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['cost'], 20)
        self.assertEqual(response_json['winings_multyplier'], 5)
        self.assertEqual(response_json['scatter_multiplier'], 0)
        self.assertEqual(response_json['result'], 100)


    def test_leaderboard(self):
        response = self.client.get(reverse('leaderboard', args=["amounth_won"]), HTTP_AUTHORIZATION ="Token "+ str(self.token))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json[0]['amounth_won'], 100*5)
        self.assertEqual(response_json[0]['user__username'], 'test')


class SlotMachineTestCase(TestCase):
    
    def setUp(self):
        self.machine=Slot_machine()

    def test_slot_machine_calculate_streek_for_one_line_rare(self):
        mock_reel_result=Mock(return_value=[1,1,1])

        with patch.object(Reel,'get_result',mock_reel_result):
            for winning_line in slot_machine_settings.WINNING_LINES:
                result=self.machine.calculate_streek_for_one_line(winning_line)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],1)
                self.assertEqual(result[2],0)
            
            mock_reel_result.return_value=[7,7,7]
            for winning_line in slot_machine_settings.WINNING_LINES:
                result=self.machine.calculate_streek_for_one_line(winning_line)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],7)
                self.assertEqual(result[2],4)

            mock_reel_result.return_value=[1,2,3]
            result=self.machine.calculate_streek_for_one_line(slot_machine_settings.WINNING_LINES[1])
            self.assertEqual(result[0],4)
            self.assertEqual(result[1],1)
            self.assertEqual(result[2],0)

            result=self.machine.calculate_streek_for_one_line(slot_machine_settings.WINNING_LINES[0])
            self.assertEqual(result[0],4)
            self.assertEqual(result[1],2)
            self.assertEqual(result[2],0)

            result=self.machine.calculate_streek_for_one_line(slot_machine_settings.WINNING_LINES[2])
            self.assertEqual(result[0],4)
            self.assertEqual(result[1],3)
            self.assertEqual(result[2],0)

            for winning_line in slot_machine_settings.WINNING_LINES[3:]:
                result=self.machine.calculate_streek_for_one_line(winning_line)
                self.assertLess(result[0],2)
                self.assertLess(result[1],4)
                self.assertEqual(result[2],0)


    def test_slot_machine_calculate_scater_multyplyer(self):
        mock_reel_result=Mock(side_effect=[
            [1,1,1], [1,1,1], [1,1,1], [1,1,1], [1,1,1],
            [8,1,1], [8,1,1], [8,1,1], [8,1,1], [8,1,1],
            [1,8,1], [1,8,1], [1,8,1], [1,8,1], [1,8,1],
            [1,1,8], [1,1,8], [1,1,8], [1,1,8], [1,1,8],
            [8,1,1], [1,8,1], [1,1,8], [1,1,1], [1,1,1],
            [1,1,8], [1,8,1], [8,1,1], [8,1,1], [1,1,1]
            ])

        with patch.object(Reel,'get_result',mock_reel_result):
            result=self.machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[-1,-1,-1,-1,-1])
            self.assertEqual(result[0],0)

            result=self.machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[0,0,0,0,0])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][4])

            result=self.machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[1,1,1,1,1])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][4])

            result=self.machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[2,2,2,2,2])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][4])

            result=self.machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[0,1,2,-1,-1])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][2])

            result=self.machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[2,1,0,0,-1])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][3])


    def test_slot_machine_calculate_streek_for_one_line_for_every_line(self):
        line_tests=[]
        for line in slot_machine_settings.WINNING_LINES:
            first_reel=[8,8,8]
            first_reel[line[0]]=1
            line_tests.append(first_reel)
            for pos in line:
                current_reel=[8,8,8]
                current_reel[pos]=1
                line_tests.append(current_reel)
            
        mock_reel_result=Mock(side_effect=line_tests)
        
        with patch.object(Reel,'get_result',mock_reel_result):
            for line in slot_machine_settings.WINNING_LINES:
                result=self.machine.calculate_streek_for_one_line(line)
                self.assertEqual(result[2],0)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],1)
            

    def test_slot_machine_calculate_streek_for_one_line_only_scatter(self):
        mock_reel_result=Mock(return_value=[8,8,8])
        
        with patch.object(Reel,'get_result',mock_reel_result):
            for line in slot_machine_settings.WINNING_LINES:
                result=self.machine.calculate_streek_for_one_line(line)
                self.assertEqual(result[0],0)
                self.assertEqual(result[1],8)
                self.assertEqual(result[2],0)
            

    def test_slot_machine_calculate_streek_for_one_line_with_wilds(self):
        side_effects=[[7,7,7]]*5+[[1,1,1]]
        side_effects*=20
        mock_reel_result=Mock(side_effect=side_effects)
        
        with patch.object(Reel,'get_result',mock_reel_result):
            for line in slot_machine_settings.WINNING_LINES:
                result=self.machine.calculate_streek_for_one_line(line)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],1)
                self.assertEqual(result[2],3)
        
            side_effects=[[7,7,7]]*4+[[1,1,1]]+[[2,2,2]]
            side_effects*=20
            mock_reel_result.side_effect=side_effects

            for line in slot_machine_settings.WINNING_LINES:
                result=self.machine.calculate_streek_for_one_line(line)
                self.assertEqual(result[0],3)
                self.assertEqual(result[1],1)
                self.assertEqual(result[2],2)


    def test_slot_machine_roll_machine(self):
        mock_calcuate_streek_for_one_line=Mock(return_value=(4,1,0))
        mock_calculate_scater_multyplyer=Mock(return_value=(0,[-1,-1,-1,-1,-1]))
        mock_reel_get_result=Mock(return_value=[1,1,1])
        with (patch.object(Slot_machine,'calculate_streek_for_one_line',mock_calcuate_streek_for_one_line),
              patch.object(Slot_machine,'calculate_scater_multyplyer',mock_calculate_scater_multyplyer),
              patch.object(Reel,'get_result',mock_reel_get_result)):
            
            for symbol in range(1,7):
                mock_calcuate_streek_for_one_line.return_value=(4,symbol,0)
                result=self.machine.roll_machine()
                self.assertEqual(result[0],20*slot_machine_settings.PAYTABLE[symbol][4])
                self.assertEqual(result[1],[[1,1,1]]*5)
                self.assertEqual(result[2],slot_machine_settings.WINNING_LINES)
                self.assertEqual(result[3],0)
                self.assertEqual(result[4],[-1,-1,-1,-1,-1])

            mock_calculate_scater_multyplyer.return_value=(slot_machine_settings.PAYTABLE[8][2],[1,0,1,0,1])

            for symbol in range(1,7):
                mock_calcuate_streek_for_one_line.return_value=(4,symbol,0)
                result=self.machine.roll_machine()
                self.assertEqual(result[0],20*slot_machine_settings.PAYTABLE[symbol][4] + slot_machine_settings.PAYTABLE[8][2])
                self.assertEqual(result[1],[[1,1,1]]*5)
                self.assertEqual(result[2],slot_machine_settings.WINNING_LINES)
                self.assertEqual(result[3],slot_machine_settings.PAYTABLE[8][2])
                self.assertEqual(result[4],[1,0,1,0,1])


    def test_slot_machine_roll_machine_with_wilds(self):
        mock_calcuate_streek_for_one_line=Mock(return_value=(4,1,3))
        mock_calculate_scater_multyplyer=Mock(return_value=(0,[-1,-1,-1,-1,-1]))
        mock_reel_get_result=Mock(return_value=[1,1,1])
        with (patch.object(Slot_machine,'calculate_streek_for_one_line',mock_calcuate_streek_for_one_line),
              patch.object(Slot_machine,'calculate_scater_multyplyer',mock_calculate_scater_multyplyer),
              patch.object(Reel,'get_result',mock_reel_get_result)):
            
            for symbol in range(1,7):
                mock_calcuate_streek_for_one_line.return_value=(4,symbol,3)
                result=self.machine.roll_machine()
                self.assertEqual(result[0],
                                    max(20*slot_machine_settings.PAYTABLE[symbol][4],
                                        slot_machine_settings.PAYTABLE[slot_machine_settings.WILD_SYMBOL][3]*20))
                
                self.assertEqual(result[1],[[1,1,1]]*5)
                self.assertEqual(result[2],slot_machine_settings.WINNING_LINES)
                self.assertEqual(result[3],0)
                self.assertEqual(result[4],[-1,-1,-1,-1,-1])

            mock_calculate_scater_multyplyer.return_value=(slot_machine_settings.PAYTABLE[8][2],[1,0,1,0,1])

            for symbol in range(1,7):
                mock_calcuate_streek_for_one_line.return_value=(4,symbol,3)
                result=self.machine.roll_machine()
                self.assertEqual(result[0],max(
                                20*slot_machine_settings.PAYTABLE[symbol][4] + slot_machine_settings.PAYTABLE[8][2],
                                slot_machine_settings.PAYTABLE[slot_machine_settings.WILD_SYMBOL][3]*20+ slot_machine_settings.PAYTABLE[8][2]) )

                self.assertEqual(result[1],[[1,1,1]]*5)
                self.assertEqual(result[2],slot_machine_settings.WINNING_LINES)
                self.assertEqual(result[3],slot_machine_settings.PAYTABLE[8][2])
                self.assertEqual(result[4],[1,0,1,0,1])

class ReelTestCase(TestCase):
    def test_spin(self):
        reel = Reel([1,2,3,4,5,6])
        mock_randint=Mock(return_value=0)
        with patch('random.randint', mock_randint):
            result=reel.spin()
            self.assertEquals(result, [1,2,3])
            mock_randint.return_value=4
            result=reel.spin()
            self.assertEquals(result, [5,6,1])
            mock_randint.return_value=5
            result=reel.spin()
            self.assertEquals(result, [6,1,2])
