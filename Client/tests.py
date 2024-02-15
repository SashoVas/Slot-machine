import unittest
from unittest.mock import patch, Mock
from reel import Reel
from slot_machine import SlotMachine
from user import User
import pygame


class ReelTestCase(unittest.TestCase):
    def test_spin(self):
        pygame.mixer.init()
        pygame.display.set_mode((800, 600))
        reel1 = Reel(0, 0)
        reel1.spin([1, 2, 3], 3)
        self.assertEqual(reel1.is_spinning, True)
        self.assertEqual(reel1.is_board_full, False)
        self.assertEqual(len(reel1.animation_sprites), 6)
        self.assertEqual(len(reel1.symbol_list), 3)


class SlotMachineTestCase(unittest.TestCase):
    def test_spin(self):
        pygame.mixer.init()
        pygame.display.set_mode((800, 600))
        mock_get_spin_result = Mock(return_value=({'roll_board': [[1, 2, 3], [1, 2, 3], [
                                    1, 2, 3], [1, 2, 3], [1, 2, 3]], 'winning_lines': []}, 10, 200))
        mock_reel_spin = Mock(return_value=True)
        fake_user = User()
        fake_user.bet_amount = 20
        fake_user.balance = 1000

        with (patch.object(SlotMachine, 'get_spin_result', mock_get_spin_result),
              patch.object(Reel, 'spin', mock_reel_spin)):
            slot_machine = SlotMachine(None, fake_user)
            slot_machine.spin(20)
            self.assertEqual(fake_user.balance, 980)
            self.assertEqual(slot_machine.result_of_spin, 200)
            self.assertEqual(slot_machine.to_vizualize_winnings, True)
