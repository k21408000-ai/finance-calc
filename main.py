import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Set background to light gray
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class FinanceCalculatorApp(App):
    def build(self):
        self.title = "Financial & General Calculator"
        
        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Header Title
        header = Label(
            text="Financial & General Calculator",
            font_size='22sp',
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=None,
            height=35
        )
        root.add_widget(header)

        # Navigation Bar (Tabs)
        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=8)
        
        self.btn_gen = Button(text="General", background_color=(0.2, 0.6, 0.8, 1), bold=True)
        self.btn_sip = Button(text="SIP", background_color=(0.5, 0.5, 0.5, 1), bold=True)
        self.btn_swp = Button(text="SWP", background_color=(0.5, 0.5, 0.5, 1), bold=True)

        self.btn_gen.bind(on_release=lambda x: self.switch_tab("General"))
        self.btn_sip.bind(on_release=lambda x: self.switch_tab("SIP"))
        self.btn_swp.bind(on_release=lambda x: self.switch_tab("SWP"))

        nav_layout.add_widget(self.btn_gen)
        nav_layout.add_widget(self.btn_sip)
        nav_layout.add_widget(self.btn_swp)
        root.add_widget(nav_layout)

        # Content Box
        self.content_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.content_box.bind(minimum_height=self.content_box.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.content_box)
        root.add_widget(scroll)

        # Default Tab
        self.switch_tab("General")

        return root

    def switch_tab(self, tab_name):
        self.content_box.clear_widgets()
        
        # Tab Highlighting
        self.btn_gen.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_sip.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_swp.background_color = (0.5, 0.5, 0.5, 1)

        if tab_name == "General":
            self.btn_gen.background_color = (0.2, 0.6, 0.8, 1)
            self.build_general_ui()
        elif tab_name == "SIP":
            self.btn_sip.background_color = (0.2, 0.6, 0.8, 1)
            self.build_sip_ui()
        elif tab_name == "SWP":
            self.btn_swp.background_color = (0.2, 0.6, 0.8, 1)
            self.build_swp_ui()

    # --- GENERAL CALCULATOR (GRID WITH BUTTONS) ---
    def build_general_ui(self):
        # Display Screen
        self.calc_input = TextInput(
            text="",
            readonly=True,
            halign="right",
            font_size='28sp',
            size_hint_y=None,
            height=60,
            multiline=False
        )
        self.content_box.add_widget(self.calc_input)

        # Calculator Grid Layout (5 rows, 4 columns)
        grid = GridLayout(cols=4, spacing=8, size_hint_y=None, height=320)

        buttons = [
            'C', '(', ')', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '⌫', '0', '.', '='
        ]

        for btn_text in buttons:
            # Style operational/action buttons differently from numbers
            if btn_text in ['=', 'C', '⌫']:
                bg_color = (0.8, 0.3, 0.3, 1) if btn_text == 'C' else (0.2, 0.7, 0.3, 1)
            elif btn_text in ['/', '*', '-', '+', '(', ')']:
                bg_color = (0.3, 0.5, 0.7, 1)
            else:
                bg_color = (0.7, 0.7, 0.7, 1)

            btn = Button(
                text=btn_text,
                font_size='20sp',
                bold=True,
                background_color=bg_color
            )
            btn.bind(on_release=self.on_calc_button_press)
            grid.add_widget(btn)

        self.content_box.add_widget(grid)

    def on_calc_button_press(self, instance):
        text = instance.text

        if text == 'C':
            self.calc_input.text = ""
        elif text == '⌫':
            self.calc_input.text = self.calc_input.text[:-1]
        elif text == '=':
            expr = self.calc_input.text.strip()
            if not expr:
                return
            try:
                # Replace visual operators if needed
                sanitized_expr = expr.replace('×', '*').replace('÷', '/')
                res = eval(sanitized_expr, {"__builtins__": None}, {})
                self.calc_input.text = str(round(res, 6))
            except Exception:
                self.calc_input.text = "Error"
        else:
            # If screen previously showed "Error", reset on new button tap
            if self.calc_input.text == "Error":
                self.calc_input.text = ""
            self.calc_input.text += text

    # --- SIP CALCULATOR ---
    def build_sip_ui(self):
        self.sip_monthly = self.create_input("Monthly Investment (₹)")
        self.sip_rate = self.create_input("Expected Return Rate (% p.a.)")
        self.sip_years = self.create_input("Time Period (Years)")
        
        btn = Button(text="Calculate SIP", size_hint_y=None, height=50, background_color=(0.2, 0.7, 0.3, 1), bold=True)
        btn.bind(on_release=self.calculate_sip)
        
        self.sip_result = Label(text="Total Value: ₹0", font_size='16sp', bold=True, color=(0, 0, 0, 1), size_hint_y=None, height=80)

        self.content_box.add_widget(btn)
        self.content_box.add_widget(self.sip_result)

    def calculate_sip(self, instance):
        try:
            P = float(self.sip_monthly.text)
            i = (float(self.sip_rate.text) / 100) / 12
            n = float(self.sip_years.text) * 12
            
            total_value = P * ((((1 + i) ** n) - 1) / i) * (1 + i)
            invested = P * n
            returns = total_value - invested
            
            self.sip_result.text = (
                f"Total Value: ₹{round(total_value, 2):,}\n"
                f"Total Invested: ₹{round(invested, 2):,}\n"
                f"Estimated Returns: ₹{round(returns, 2):,}"
            )
        except Exception:
            self.sip_result.text = "Please enter valid numbers"

    # --- SWP CALCULATOR ---
    def build_swp_ui(self):
        self.swp_total = self.create_input("Total Investment Amount (₹)")
        self.swp_withdraw = self.create_input("Monthly Withdrawal (₹)")
        self.swp_rate = self.create_input("Expected Return Rate (% p.a.)")
        self.swp_years = self.create_input("Time Period (Years)")
        
        btn = Button(text="Calculate SWP", size_hint_y=None, height=50, background_color=(0.2, 0.7, 0.3, 1), bold=True)
        btn.bind(on_release=self.calculate_swp)
        
        self.swp_result = Label(text="Remaining Balance: ₹0", font_size='16sp', bold=True, color=(0, 0, 0, 1), size_hint_y=None, height=50)

        self.content_box.add_widget(btn)
        self.content_box.add_widget(self.swp_result)

    def calculate_swp(self, instance):
        try:
            total = float(self.swp_total.text)
            withdraw = float(self.swp_withdraw.text)
            rate = (float(self.swp_rate.text) / 100) / 12
            months = int(float(self.swp_years.text) * 12)
            
            for _ in range(months):
                total = (total - withdraw) * (1 + rate)
                if total <= 0:
                    break
                
            if total <= 0:
                self.swp_result.text = "Funds exhausted before tenure!"
            else:
                self.swp_result.text = f"Remaining Balance: ₹{round(total, 2):,}"
        except Exception:
            self.swp_result.text = "Please enter valid numbers"

    def create_input(self, hint):
        lbl = Label(text=hint, color=(0.2, 0.2, 0.2, 1), size_hint_y=None, height=25)
        inp = TextInput(hint_text=hint, multiline=False, input_filter='float', size_hint_y=None, height=45, font_size='16sp')
        self.content_box.add_widget(lbl)
        self.content_box.add_widget(inp)
        return inp

if __name__ == "__main__":
    FinanceCalculatorApp().run()