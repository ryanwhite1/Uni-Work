"""
Calculate tax payable
"""

__author__ = "Dick Thomas"
__date__ = "21/02/18"

deduction_car_usage = 200
deduction_professional_development = 750
gross_income = 100000
tax_free_threshold = 18200
tax_rate = 0.25


deductions = deduction_car_usage + deduction_professional_development
taxable_income = gross_income - tax_free_threshold - deductions
tax_payable = taxable_income * tax_rate
print("You need to pay $", tax_payable, " as your tax this year.", sep="")
