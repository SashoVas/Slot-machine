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

    def calculate_streek_for_one_line(self, line):
        current_symbol = self.reels[0].get_result()[line[0]]
        streek = 0
        wilds_count = 0

        for reel, line_row in zip(self.reels, line):
            reel_result = reel.get_result()
            if (not reel_result[line_row] == current_symbol
                and not current_symbol == slot_machine_settings.WILD_SYMBOL
                    and not reel_result[line_row] == slot_machine_settings.WILD_SYMBOL):
                break

            if reel_result[line_row] == slot_machine_settings.SCATTER_SYMBOL:
                break

            streek += 1
            if reel_result[line_row] != slot_machine_settings.WILD_SYMBOL:
                current_symbol = reel_result[line_row]
            elif current_symbol == slot_machine_settings.WILD_SYMBOL:
                wilds_count += 1

        if streek > 0:
            streek -= 1
        if wilds_count > 0:
            wilds_count -= 1

        return streek, current_symbol, wilds_count

    def calculate_scater_multyplyer(self):
        scater_count = 0
        scater_positions = []
        for reel in self.reels:
            scater_positions.append(-1)
            for positions, symbol in enumerate(reel.get_result()):
                if symbol == slot_machine_settings.SCATTER_SYMBOL:
                    scater_count += 1
                    scater_positions[-1] = positions

        if scater_count > 0:
            scater_count -= 1

        return slot_machine_settings.PAYTABLE[slot_machine_settings.SCATTER_SYMBOL][scater_count], scater_positions

    def roll_machine(self):
        for reel in self.reels:
            reel.spin()

        multyplier = 0
        winning_lines = []

        for line in slot_machine_settings.WINNING_LINES:
            streak, symbol, wilds_count = self.calculate_streek_for_one_line(
                line)

            multyplier += max(slot_machine_settings.PAYTABLE[symbol][streak],
                              slot_machine_settings.PAYTABLE[slot_machine_settings.WILD_SYMBOL][wilds_count])
            if streak > 1:
                winning_lines.append(line)

        scater_multyplier, scater_positions = self.calculate_scater_multyplyer()
        multyplier += scater_multyplier

        return multyplier, [reel.get_result() for reel in self.reels], winning_lines, scater_multyplier, scater_positions


class Reel:
    def __init__(self, base_reels_symbols, is_rigged=False, rigged_reels_symbols=None):
        self.base_reels_symbols = base_reels_symbols
        self.is_rigged = is_rigged
        self.rigged_reels_symbols = rigged_reels_symbols
        self.result = None

    def get_result(self):
        return self.result

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
