from django.test import TestCase
from machine.slot_machine import Slot_machine, Reel
from unittest.mock import Mock, patch, PropertyMock
from machine import slot_machine_settings
# Create your tests here.

class SlotMachineTestCase(TestCase):

    def test_slot_machine_calculate_streek_for_one_line_rare(self):
        machine=Slot_machine()
        mock_reel_result=Mock(return_value=[1,1,1])

        with patch.object(Reel,'get_result',mock_reel_result):
            for winning_line in slot_machine_settings.WINNING_LINES:
                result=machine.calculate_streek_for_one_line(winning_line)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],1)
                self.assertEqual(result[2],0)
            
            mock_reel_result.return_value=[7,7,7]
            for winning_line in slot_machine_settings.WINNING_LINES:
                result=machine.calculate_streek_for_one_line(winning_line)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],7)
                self.assertEqual(result[2],4)

            mock_reel_result.return_value=[1,2,3]
            result=machine.calculate_streek_for_one_line(slot_machine_settings.WINNING_LINES[1])
            self.assertEqual(result[0],4)
            self.assertEqual(result[1],1)
            self.assertEqual(result[2],0)

            result=machine.calculate_streek_for_one_line(slot_machine_settings.WINNING_LINES[0])
            self.assertEqual(result[0],4)
            self.assertEqual(result[1],2)
            self.assertEqual(result[2],0)

            result=machine.calculate_streek_for_one_line(slot_machine_settings.WINNING_LINES[2])
            self.assertEqual(result[0],4)
            self.assertEqual(result[1],3)
            self.assertEqual(result[2],0)

            for winning_line in slot_machine_settings.WINNING_LINES[3:]:
                result=machine.calculate_streek_for_one_line(winning_line)
                self.assertLess(result[0],2)
                self.assertLess(result[1],4)
                self.assertEqual(result[2],0)


    def test_slot_machine_calculate_scater_multyplyer(self):
        machine=Slot_machine()
        mock_reel_result=Mock(side_effect=[
            [1,1,1], [1,1,1], [1,1,1], [1,1,1], [1,1,1],
            [8,1,1], [8,1,1], [8,1,1], [8,1,1], [8,1,1],
            [1,8,1], [1,8,1], [1,8,1], [1,8,1], [1,8,1],
            [1,1,8], [1,1,8], [1,1,8], [1,1,8], [1,1,8],
            [8,1,1], [1,8,1], [1,1,8], [1,1,1], [1,1,1],
            [1,1,8], [1,8,1], [8,1,1], [8,1,1], [1,1,1]
            ])

        with patch.object(Reel,'get_result',mock_reel_result):
            result=machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[-1,-1,-1,-1,-1])
            self.assertEqual(result[0],0)

            result=machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[0,0,0,0,0])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][4])

            result=machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[1,1,1,1,1])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][4])

            result=machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[2,2,2,2,2])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][4])

            result=machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[0,1,2,-1,-1])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][2])

            result=machine.calculate_scater_multyplyer()
            self.assertEqual(result[1],[2,1,0,0,-1])
            self.assertEqual(result[0],slot_machine_settings.PAYTABLE[8][3])


    def test_slot_machine_calcuate_streek_for_one_line_for_every_line(self):
        machine=Slot_machine()

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
                result=machine.calculate_streek_for_one_line(line)
                self.assertEqual(result[2],0)
                self.assertEqual(result[0],4)
                self.assertEqual(result[1],1)
            

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
