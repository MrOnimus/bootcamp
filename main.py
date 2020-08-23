import math
from random import randint
import matplotlib.pyplot as plt


CHEATED_BY_MONEY = 1
SUCCESS_MONEY = 4
CHEATED_MONEY = 5
BOTH_CHEATED_MONEY = 2

CHURN_RATE = 0.2


class Merchant:

    """Docstring for base class of any merchant type. """

    money = 0

    def __init__(self, money):
        self.money = money

    def cheated_by(self):
        self.money += CHEATED_BY_MONEY

    def success(self):
        self.money += SUCCESS_MONEY

    def cheated(self):
        self.money += CHEATED_MONEY

    def both_cheated(self):
        self.money += BOTH_CHEATED_MONEY


class Altruist(Merchant):

    """Docstring for the man who always does the right thing. """

    def logic(self):
        return 'trade'


class Trickster(Merchant):

    """Docstring for someone who's always cheating. """

    def logic(self):
        return 'trick'


class Gaudy(Merchant):

    """Docstring for gaudy merchant. """

    i = 0
    has_been_tricked = False
    opponent_move = 'trade'

    def logic(self):
        if self.i < 4:
            if self.i == 0 or self.i == 2 or self.i == 3:
                return 'trade'

            if self.i == 1:
                return 'trick'

            self.i += 1

        elif self.have_been_tricked:
            return 'trick'

        elif not self.have_been_tricked:
            return self.opponent_move

    def cheated_by(self):
        self.money += CHEATED_BY_MONEY
        if self.i < 4:
            self.has_been_tricked = True
        else:
            opponent_move = 'trick'

    def success(self):
        self.money += SUCCESS_MONEY
        if self.i >= 4:
            opponent_move = 'trade'

    def both_cheated(self):
        self.money += BOTH_CHEATED_MONEY
        if self.i >= 4:
            opponent_move = 'trick'

    def cheated(self):
        self.money += CHEATED_MONEY
        if self.i >= 4:
            opponent_move = 'trade'


class Random(Merchant):

    """Docstring for merchant, who behaves randomly. """

    def logic(self):
        if randint(0, 1) == 0:
            return 'trade'
        else:
            return 'trick'


class Vindictive(Merchant):

    """Docstring for vindictive merchant. """

    has_been_tricked = False

    def cheated_by(self):
        self.money += CHEATED_BY_MONEY
        self.has_been_tricked = True

    def logic(self):
        if self.has_been_tricked:
            return 'trick'
        else:
            return 'trade'


class Slyster(Merchant):

    """Docstring for slyster merchant. """

    opponent_move = 'trade'

    def cheated_by(self):
        self.money += CHEATED_BY_MONEY
        opponent_move = 'trick'

    def success(self):
        self.money += SUCCESS_MONEY
        opponent_move = 'trade'

    def both_cheated(self):
        self.money += BOTH_CHEATED_MONEY
        opponent_move = 'trick'

    def cheated(self):
        self.money += CHEATED_MONEY
        opponent_move = 'trade'

    def logic(self):
        return self.opponent_move


class Testing(Merchant):

    """ Docstring for my own test merchant. """

    i = 0
    has_been_tricked = False
    irascibility = 5

    def cheated_by(self):
        self.money += CHEATED_BY_MONEY
        self.i = 0
        self.irascibility = 10 - self.i
        self.has_been_tricked = True

    def both_cheated(self):
        self.money += BOTH_CHEATED_MONEY
        self.i = 0
        self.irascibility = 10 - self.i

    def logic(self):
        if self.has_been_tricked and self.i < self.irascibility:
            return 'trick'
        else:
            self.i += 1
            return 'trade'


def merchant_error(solution):
    if randint(1, 100) <= 5:
        if solution == 'trade':
            return 'trick'
        elif solution == 'trick':
            return 'trade'
        else:
            raise('ERROR: Incorrect solution.')
    return solution


def trade_process(merchant, partner):
    merchant_solution = merchant_error(merchant.logic())
    partner_solution = merchant_error(partner.logic())

    if merchant_solution == 'trade' and partner_solution == 'trade':
        merchant.success()
        partner.success()

    elif merchant_solution == 'trade' and partner_solution == 'trick':
        merchant.cheated_by()
        partner.cheated()

    elif merchant_solution == 'trick' and partner_solution == 'trade':
        merchant.cheated()
        partner.cheated_by()

    elif merchant_solution == 'trick' and partner_solution == 'trick':
        merchant.both_cheated()
        partner.both_cheated()

    else:
        raise('ERROR: Incorrect solution.')


def epoch(merchants):
    for merchant_id in range(len(merchants) - 1):
        deals_amount = randint(5, 10)
        for partner_id in range(merchant_id + 1, len(merchants)):
            for deal_i in range(deals_amount):
                merchant = merchants[merchant_id]
                partner = merchants[partner_id]
                trade_process(merchant, partner)


def kick_N_merchants(N, merchants):
    merchants.sort(key=lambda merchant: merchant.money, reverse=True)
    kicker = slice(0, len(merchants) - N)
    return merchants[kicker]


def add_N_new_merchants(N, merchants):
    for i in range(N):
        merchants.append(type(merchants[i])(money=0))


def print_state(epoch, merchants):
    merchants.sort(key=lambda merchant: merchant.money)
    print("----------------- EPOCH {index} -----------------".format(
        index=epoch + 1
    ))
    for i in range(len(merchants)):
        print("{index} merchant is {name}, and has {money}$.".format(
            index=i + 1,
            name=type(merchants[i]).__name__,
            money=merchants[i].money
        ))
    print()


def analytics(merchants):
    money_data = {}
    demographics = {}
    total = 0

    for merchant in merchants:
        if type(merchant).__name__ in money_data:
            money_data[type(merchant).__name__] += merchant.money
        else:
            money_data[type(merchant).__name__] = merchant.money

        if type(merchant).__name__ in demographics:
            demographics[type(merchant).__name__] += 1
        else:
            demographics[type(merchant).__name__] = 1

        total += merchant.money

    print("---------------- ANALYTICS ----------------")
    print("Total money:")
    for key in money_data:
        print("{name}s collected {part}% of all money in the game.".format(
            name=key,
            part=round(money_data[key] / total * 100, 2)
        ))
    print()
    print("Amount of people:")
    for key in demographics:
        print("{name} takes {part}% of all population in the game.".format(
            name=key,
            part=demographics[key]
        ))
    print()
    print("Average amount of money per class:")
    for key in money_data:
        print("{name} in average have {money}$.".format(
            name=key,
            money=round(money_data[key] / demographics[key])
        ))
    print()

    plt.pie(money_data.values(), labels=money_data.keys(),
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    altruists = [Altruist(money=0) for i in range(10)]
    tricksters = [Trickster(money=0) for i in range(10)]
    gaudies = [Gaudy(money=0) for i in range(10)]
    randoms = [Random(money=0) for i in range(10)]
    vindictives = [Vindictive(money=0) for i in range(10)]
    slysters = [Slyster(money=0) for i in range(10)]
    tests = [Testing(money=0) for i in range(10)]

    merchants = altruists + tricksters + gaudies + \
        randoms + vindictives + slysters + tests

    print('How many epoch do you want to happen?', end=' ')
    try:
        epochs_amount = int(input())
    except Exception as e:
        raise('ERROR: Invalid number.')

    N = math.floor(len(merchants) * CHURN_RATE)
    for i in range(epochs_amount):
        epoch(merchants)

        print_state(i, merchants)

        merchants = kick_N_merchants(N, merchants)

        add_N_new_merchants(N, merchants)

    analytics(merchants)
