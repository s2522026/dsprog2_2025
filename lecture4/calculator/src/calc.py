import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=24)
        self.width = 360
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton("AC", self.button_clicked),
                        ExtraActionButton("+/-", self.button_clicked),
                        ExtraActionButton("%", self.button_clicked),
                        ActionButton("/", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton("sin", self.button_clicked),
                        ExtraActionButton("cos", self.button_clicked),
                        ExtraActionButton("tan", self.button_clicked),
                        ExtraActionButton("√", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton("x²", self.button_clicked),
                        ExtraActionButton("log", self.button_clicked),
                        ActionButton("*", self.button_clicked),
                        ActionButton("-", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("7", self.button_clicked),
                        DigitButton("8", self.button_clicked),
                        DigitButton("9", self.button_clicked),
                        ActionButton("+", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("4", self.button_clicked),
                        DigitButton("5", self.button_clicked),
                        DigitButton("6", self.button_clicked),
                        ActionButton("=", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("1", self.button_clicked),
                        DigitButton("2", self.button_clicked),
                        DigitButton("3", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("0", self.button_clicked, expand=2),
                        DigitButton(".", self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data

        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data.isdigit() or data == ".":
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator)
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = 0
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator)
            self.reset()

        elif data == "%":
            self.result.value = self.format_number(
                float(self.result.value) / 100)
            self.reset()

        elif data == "+/-":
            val = float(self.result.value)
            self.result.value = self.format_number(-val)

        elif data in ("sin", "cos", "tan"):
            val = float(self.result.value)
            if data == "sin":
                self.result.value = self.format_number(
                    math.sin(math.radians(val)))
            elif data == "cos":
                self.result.value = self.format_number(
                    math.cos(math.radians(val)))
            elif data == "tan":
                self.result.value = self.format_number(
                    math.tan(math.radians(val)))
            self.reset()

        elif data == "√":
            val = float(self.result.value)
            self.result.value = "Error" if val < 0 else self.format_number(
                math.sqrt(val))
            self.reset()

        elif data == "x²":
            val = float(self.result.value)
            self.result.value = self.format_number(val ** 2)
            self.reset()

        elif data == "log":
            val = float(self.result.value)
            self.result.value = "Error" if val <= 0 else self.format_number(
                math.log10(val))
            self.reset()

        self.update()

    def calculate(self, op1, op2, operator):
        try:
            if operator == "+":
                return self.format_number(op1 + op2)
            if operator == "-":
                return self.format_number(op1 - op2)
            if operator == "*":
                return self.format_number(op1 * op2)
            if operator == "/":
                return "Error" if op2 == 0 else self.format_number(op1 / op2)
        except:
            return "Error"

    def format_number(self, num):
        return int(num) if num == int(num) else round(num, 6)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator"
    page.add(CalculatorApp())


ft.app(main)
