# Income
# rental income ~1% of property value
# laundry machine
# storage
# misc

# Expenses
# Tax ~$150/m
# Insurance ~ $100/m
# Utilities - $0 if tenant pays utilities
# Electric, water sewer garbage gas
# HOA - $0 if not in HOA
# Lawn/snow
# Vacancy - % of time the property has no renters
# Repairs
# Capex - big purchases like new roof
# Property management
# Mortgage

# Cash flow = income - expenses

# Cash on cash ROI
# Down payment
# Closing costs
# Rehab budget - clean up before selling
# Misc other

# Annual cash flow / total investment

import tkinter as tk

def decToPercent(decimal):
    return f"{decimal * 100}%"

class FreeInputWidget(tk.Frame):
    def __init__(self, parent, labeltext, inputType, restrictPositive=False, initialValue=""):
        tk.Frame.__init__(self, parent)
        self.inputType = inputType

        def validateFloat(newValue):
            try:
                newValue = float(newValue)
                if restrictPositive:
                    return True and newValue >= 0
                else: return True
            except:
                return False

        def validateInt(newValue):
            try:
                newValue = int(newValue)
                if restrictPositive:
                    return True and newValue >= 0
                else: return True
            except:
                return False

        if inputType == float:  # float
            # self.inputVar = tk.DoubleVar(self, 0.0)
            if initialValue != "":
                self.inputVar = tk.StringVar(self, initialValue)
            else:
                self.inputVar = tk.StringVar(self, "0.0")
            validate = self.register(validateFloat)
        elif inputType == int:  # int
            if initialValue != "":
                self.inputVar = tk.StringVar(self, initialValue)
            else:
                self.inputVar = tk.StringVar(self, "0")
            validate = self.register(validateInt)
        else:  # string
            self.inputVar = tk.StringVar(self, initialValue)
            validate = lambda: True


        self.parent = parent
        self.label = tk.Label(self, text=labeltext, width=20, justify="left", relief="groove", anchor="w")

        self.input = tk.Entry(self, textvariable=self.inputVar, width=25, validate="key", validatecommand=(validate, "%P"), )

        self.label.grid(row=0, column=0)
        self.input.grid(row=0, column=1)

    def value(self):
        return self.inputType(self.inputVar.get())

    def setValue(self, value):
        self.inputVar.set(value)


class SliderWidget(tk.Frame):
    def __init__(self, parent, labeltext, min, max, resolution=0, initialvalue="", tooltip="", link=""):
        if initialvalue =="":
            initialvalue = (min + max) / 2
        if resolution == 0:
            resolution = (max - min) / 100
        tk.Frame.__init__(self, parent)

        self.inputVar = tk.DoubleVar(self, initialvalue)
        self.input = tk.Scale(self, variable=self.inputVar, from_=min, to=max, orient="horizontal", resolution=resolution, length=120, command=self.updateValue) #, command=self.updateValue)
        self.input.set(initialvalue)
        self.label = tk.Label(self, text=labeltext, width=20, justify="left", relief="groove", anchor="w")
        self.label.grid(row=0, column=0)
        self.input.grid(row=0, column=1)

        self.v = initialvalue


    def updateValue(self, *args):
        self.v = self.input.get()

    def value(self):
        return self.v

    def setValue(self, value):
        self.v = value
        self.input.set(value)



class ROICalculator(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.incomeRow = tk.LabelFrame(self, text="Monthly Income")
        self.expensesRow = tk.LabelFrame(self, text="Monthly Expenses")
        self.ROIRow = tk.LabelFrame(self, text="Return on Investment")
        self.incomeRow.grid(row=1, column=0, sticky="N")
        self.expensesRow.grid(row=2, column=0, sticky="N")
        self.ROIRow.grid(row=3, column=0, sticky="N")


        self.totalPurchasePrice = FreeInputWidget(self, "Total purchase cost", float, True, initialValue=50000)
        self.rent = FreeInputWidget(self.incomeRow, "Rent", float, True, initialValue=2000)
        self.addtlIncome = FreeInputWidget(self.incomeRow, "Additional Income", float, True, initialValue=0)
        self.tax = FreeInputWidget(self.expensesRow, "Taxes", float, True, initialValue=100)
        self.insurance = FreeInputWidget(self.expensesRow, "Insurance", float, True, initialValue=100)
        self.utilities = FreeInputWidget(self.expensesRow, "Utilities", float, True, initialValue=0)
        self.hoaFee = FreeInputWidget(self.expensesRow, "HOA Fee", float, True, initialValue=0)
        self.lawnSnow = FreeInputWidget(self.expensesRow, "Lawncare/snow", float, True, initialValue=0)
        self.vacancyPercent = SliderWidget(self.expensesRow, "Expected vacancy", 0, 100, initialvalue=5)
        self.repairs = FreeInputWidget(self.expensesRow, "Repairs", float, True, initialValue=100)
        self.capEx = FreeInputWidget(self.expensesRow, "Capital expenses", float, True, initialValue=100)
        self.management = FreeInputWidget(self.expensesRow, "Management fees", float, True, initialValue=200)
        self.mortgage = FreeInputWidget(self.expensesRow, "Mortgage payment", float, True, initialValue=860)

        self.cashFlow = FreeInputWidget(self, "Cash flow", float)
        self.cashFlow.input.config(state="disabled")
        self.ROI = FreeInputWidget(self, "Return on investment", float)
        self.ROI.input.config(state="disabled")

        self.rent.pack()
        self.addtlIncome.pack()
        self.tax.pack()
        self.insurance.pack()
        self.utilities.pack()
        self.hoaFee.pack()
        self.lawnSnow.pack()
        self.vacancyPercent.pack()
        self.repairs.pack()
        self.capEx.pack()
        self.management.pack()
        self.mortgage.pack()
        self.totalPurchasePrice.grid(row=0, column=0)
        self.cashFlow.grid(row=4, column=0)
        self.ROI.grid(row=5, column=0)

        self.calcCashOnCashROI()

        self.rent.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.addtlIncome.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.tax.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.insurance.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.utilities.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.hoaFee.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.lawnSnow.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.vacancyPercent.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.repairs.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.capEx.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.management.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.mortgage.inputVar.trace_add("write", self.calcCashOnCashROI)
        self.totalPurchasePrice.inputVar.trace_add("write", self.calcCashOnCashROI)
        
    
    def calcMonthlyIncome(self):
        return self.rent.value() + self.addtlIncome.value()

    def calcMonthlyCosts(self):
        return self.tax.value() + self.insurance.value() + self.utilities.value() + self.hoaFee.value() + self.lawnSnow.value() \
        + self.vacancyPercent.value() * 0.01 * self.rent.value() + self.repairs.value() + self.capEx.value() + self.management.value() + self.mortgage.value()
    
    def calcMonthylCashFlow(self):
        self.cashFlow.setValue(f"{round(self.calcMonthlyIncome() - self.calcMonthlyCosts(), 2)}")
        return self.calcMonthlyIncome() - self.calcMonthlyCosts()

    def calcCashOnCashROI(self, *args):
        totalCost = self.totalPurchasePrice.value()
        cashFlow = self.calcMonthylCashFlow()
        if totalCost == 0:
            self.ROI.setValue("Please set purchase cost.")
        else:
            self.ROI.setValue(decToPercent(cashFlow * 12 / totalCost))
    

def run():
        root = tk.Tk()
        root.title("ROI Calculator")
        baseFrame = tk.Frame(root)
        baseFrame.pack()
        calc = ROICalculator(baseFrame)
        calc.pack()
        root.mainloop()

run()


# class RentalProperty():
#     # thanks Cam
#     Ptax = {
#         "Hawaii": 0.28, 
#         "Alabama": 0.41,
#         "Colorado": 0.51,
#         "Louisiana": 0.55,
#         "District of Columbia": 0.56,
#         "South Carolina": 0.57,
#         "Delaware": 0.57,
#         "West Virginia": 0.58,
#         "Nevada": 0.6,
#         "Wyoming": 0.61,
#         "Arkansas": 0.62,
#         "Utah": 0.63,
#         "Arizona": 0.66,
#         "Idaho": 0.69,
#         "Tennessee": 0.71,
#         "California": 0.76,
#         "New Mexico": 0.8,
#         "Mississippi": 0.81,
#         "Virginia": 0.82,
#         "Montana": 0.84,
#         "North Carolina": 0.84,
#         "Indiana": 0.85,
#         "Kentucky": 0.86,
#         "Florida": 0.89,
#         "Oklahoma": 0.9,
#         "Georgia": 0.92,
#         "Missouri": 0.97,
#         "Oregon": 0.97,
#         "North Dakota": 0.98,
#         "Washington": 0.98,
#         "Maryland": 1.09,
#         "Minnesota": 1.12,
#         "Alaska": 1.19,
#         "Massachusetts": 1.23,
#         "South Dakota": 1.31,
#         "Maine": 1.36,
#         "Kansas": 1.41,
#         "Michigan": 1.54,
#     }
#     def __init__(self, rent, addtlIncome, tax, insurance, utilities, hoaFee, lawnSnow, vacancyPercent, repairs, capEx, management, mortgage, totalPurchasePrice):
#         self.rent = float(rent)
#         self.tax = float(tax)
#         self.insurance = float(insurance)
#         self.utilities = float(utilities)
#         self.hoaFee = float(hoaFee)
#         self.lawnSnow = float(lawnSnow)
#         self.vacancyPercent = float(vacancyPercent)
#         self.repairs = float(repairs)
#         self.capEx = float(capEx)
#         self.management = float(management)
#         self.mortgage = float(mortgage)
#         self.totalPurchasePrice = float(totalPurchasePrice)
#         self.addtlIncome = float(addtlIncome)
    
#     def calcMonthlyIncome(self):
#         return self.rent + self.addtlIncome

#     def calcMonthlyCosts(self):
#         return self.tax + self.insurance + self.utilities + self.hoaFee + self.lawnSnow + self.vacancyPercent * self.rent + self.repairs + self.capEx + self.management + self.mortgage
    
#     def calcMonthylCashFlow(self):
#         return self.calcMonthlyIncome() - self.calcMonthlyCosts()

#     def calcCashOnCashROI(self):
#         return self.calcMonthylCashFlow() * 12 / self.totalPurchasePrice

# prop1 = RentalProperty(2000, 0, 150, 100, 0, 0, 0, 0.05, 100, 100, 200, 860, 50000)
# print("Income:", prop1.calcMonthlyIncome())
# print("Expenses:", prop1.calcMonthlyCosts())
# print("Cash flow:", prop1.calcMonthylCashFlow())
# print("Cash on cash ROI:", decToPercent(prop1.calcCashOnCashROI()))