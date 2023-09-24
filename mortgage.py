from __future__ import print_function
import sys
import argparse
import decimal

MONTHS_IN_YEAR = 12
DOLLAR_QUANTIZE = decimal.Decimal('.01')


class Mortgage:
    def __init__(self, interest, months, amount):
        self._interest = float(interest)
        self._months = int(months)
        self._amount = amount

    def rate(self):
        return self._interest

    def month_growth(self):
        return 1. + self._interest / MONTHS_IN_YEAR

    def apy(self):
        return self.month_growth() ** MONTHS_IN_YEAR - 1

    def loan_years(self):
        return float(self._months) / MONTHS_IN_YEAR

    def loan_months(self):
        return self._months

    def amount(self):
        return self._amount

    def monthly_payment(self):
        pre_amt = float(self.amount()) * self.rate() / (float(MONTHS_IN_YEAR) * (1.-(1./self.month_growth()) ** self.loan_months()))
        return pre_amt

    def total_value(self, m_payment):
        return m_payment / self.rate() * (float(MONTHS_IN_YEAR) * (1.-(1./self.month_growth()) ** self.loan_months()))

    def annual_payment(self):
        return self.monthly_payment() * MONTHS_IN_YEAR

    def total_payout(self):
        return self.monthly_payment() * self.loan_months()

    def monthly_payment_schedule(self):
        monthly = self.monthly_payment()
        balance = self.amount()
        rate = self.rate()
        while True:
            interest_unrounded = balance * rate / MONTHS_IN_YEAR
            interest = interest_unrounded
            if monthly >= balance + interest:
                balance -= principle
                yield principle, interest, balance
                break
            principle = monthly - interest
            balance -= principle
            yield principle, interest, balance

    def balance_schedule(self):
        monthly = self.monthly_payment()
        balance = self.amount()
        rate = self.rate()
        while True:
            interest_unrounded = balance * rate / MONTHS_IN_YEAR
            interest = interest_unrounded
            if monthly >= balance + interest:
                balance -= principle
                yield balance
                break
            principle = monthly - interest
            balance -= principle
            yield balance

