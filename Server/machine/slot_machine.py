import random
import machine.slot_machine_settings as slot_machine_settings


class Slot_machine:
    REELS_NUMBER = 5

    def __init__(self, is_rigged=False, rigged_reels_symbols=None):
        self.is_rigged = is_rigged
        self.rigged_reels_symbols = rigged_reels_symbols
        if self.is_rigged:
            self.reels = [
                Reel(slot_machine_settings.BASE_REELS_SYMBOLS[i],
                    is_rigged=is_rigged,
                    rigged_reels_symbols=rigged_reels_symbols[i])
                for i in range(Slot_machine.REELS_NUMBER)
            ]
        else:
            self.reels = [
                Reel(slot_machine_settings.BASE_REELS_SYMBOLS[i])
                for i in range(Slot_machine.REELS_NUMBER)
            ]

    def calculate_streek_for_one_line(self, line):\
        #TODO: calculate the edge case where there are 3 or more wilds in a row
        current_symbol = self.reels[0].result[line[0]]
        streek=0
        for reel, line_row in zip(self.reels, line):
            if (not reel.result[line_row] == current_symbol
                and not current_symbol == slot_machine_settings.WILD_SYMBOL
                and not reel.result[line_row] == slot_machine_settings.WILD_SYMBOL):
                break

            streek += 1
            if reel.result[line_row]!=slot_machine_settings.WILD_SYMBOL:
                current_symbol = reel.result[line_row]
        streek-=1
        
        return streek, current_symbol

    def roll_machine(self):
        for reel in self.reels:
            reel.spin()

        multyplier = 0
        winning_lines=[]

        for line in slot_machine_settings.WINNING_LINES:
            streak, symbol = self.calculate_streek_for_one_line(line)
            multyplier += slot_machine_settings.PAYTABLE[symbol][streak]
            if streak > 1:
                winning_lines.append(line)

        return multyplier, [reel.result for reel in self.reels], winning_lines


class Reel:
    def __init__(self, base_reels_symbols, is_rigged=False, rigged_reels_symbols=None):
        self.base_reels_symbols = base_reels_symbols
        self.is_rigged = is_rigged
        self.rigged_reels_symbols = rigged_reels_symbols
        self.result = None

    def spin(self):
        if self.is_rigged:
            self.result = self.rigged_reels_symbols
            return self.rigged_reels_symbols

        first = random.randint(0, len(self.base_reels_symbols) - 1)
        second = (first + 1) % len(self.base_reels_symbols)
        third = (second + 1) % len(self.base_reels_symbols)
        self.result = [
            self.base_reels_symbols[first],
            self.base_reels_symbols[second],
            self.base_reels_symbols[third],
        ]
        return self.result
