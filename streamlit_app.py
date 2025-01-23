
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from dateutil.relativedelta import relativedelta

# # st.markdown("""
# # <style>
# # body, html {
# #     direction: RTL;
# #     unicode-bidi: bidi-override;
# #     text-align: right;
# # }
# # p, div, input, label, h1, h2, h3, h4, h5, h6 {
# #     direction: RTL;
# #     unicode-bidi: bidi-override;
# #     text-align: right;
# # }
# # </style>
# # """, unsafe_allow_html=True)


# class StreamlitUI:
#     """
#     Handles the Streamlit interface for user interaction.
#     """

#     @staticmethod
#     def get_user_inputs():
#         """
#         Collects user input via Streamlit UI and returns a dictionary.
#         """
#         with st.form("חישוב פנסיה לשכיר"):
#             salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
#             current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
#             current_age = st.text_input("גיל", placeholder="לדוגמא: 30")
#             retirement_age = st.text_input("גיל פרישה", placeholder="נשים 64, גברים 67")
#             employee_deposit = st.text_input("אחוז הפקדה של העובד",placeholder="בדרך כלל 6% (אפשר להגדיל עד ל-7%)")
#             employer_deposit = st.text_input("אחוז הפקדה של המעסיק",placeholder="בדרך כלל 6.5%")
#             expected_annual_yield = st.text_input("תשואה שנתית צפויה", placeholder="לדוגמה: 4.5%")
            
#             submitted = st.form_submit_button("Submit")

#         if submitted:
#             # if all([salary, current_balance, expected_annual_yield, current_age, retirement_age, employee_deposit, employer_deposit]):
#             if all([salary, current_balance, current_age, retirement_age]):
#                 return {
#                     "salary": float(salary.strip().replace(",", "")),
#                     "current_balance": float(current_balance.strip().replace(",", "")),
#                     "expected_annual_yield": float(expected_annual_yield.strip().replace("%", "")) if expected_annual_yield.strip() else 4.5,
#                     "current_age": int(current_age.strip()),
#                     "retirement_age": int(retirement_age.strip()),
#                     # "employee_deposit": float(employee_deposit.strip()),
#                     # "employer_deposit": float(employer_deposit.strip())
#                     "employee_deposit": float(employee_deposit.strip().replace("%", "")) if employee_deposit.strip() else 6.0,
#                     "employer_deposit": float(employer_deposit.strip().replace("%", "")) if employer_deposit.strip() else 6.5
#                 }




import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# st.title("💰🧮 מחשבון פנסיה לשכירים 💰🧮")
# st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")


class StreamlitUI:
    """
    Handles the Streamlit interface for user interaction.
    """

    @staticmethod
    def get_user_inputs():
        """
        Collects user input via Streamlit UI and returns a dictionary.
        """
        with st.form("חישוב פנסיה לשכיר"):
            salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
            current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
            current_age = st.text_input("גיל *", placeholder="לדוגמא: 30")
            retirement_age = st.text_input("גיל פרישה *", placeholder="נשים 64, גברים 67")
            employee_deposit = st.text_input("אחוז הפקדה של העובד", placeholder="בדרך כלל 6% (אפשר להגדיל עד ל-7%)")
            employer_deposit = st.text_input("אחוז הפקדה של המעסיק", placeholder="בדרך כלל 6.5%")
            expected_annual_yield = st.text_input("תשואה שנתית צפויה", placeholder="לדוגמה: 4.5%")
            
            submitted = st.form_submit_button("חשב")

        if submitted:
            if all([salary, current_balance, current_age, retirement_age]):
                return {
                    "salary": float(salary.strip().replace(",", "")),
                    "current_balance": float(current_balance.strip().replace(",", "")),
                    "expected_annual_yield": float(expected_annual_yield.strip().replace("%", "")) if expected_annual_yield.strip() else 4.5,
                    "current_age": int(current_age.strip()),
                    "retirement_age": int(retirement_age.strip()),
                    "employee_deposit": float(employee_deposit.strip().replace("%", "")) if employee_deposit.strip() else 6.0,
                    "employer_deposit": float(employer_deposit.strip().replace("%", "")) if employer_deposit.strip() else 6.5
                }
            else:
                st.warning("יש למלא את כל הפרטים לפני השליחה")
                return None


class PensionCalculator:
    """
    Handles all calculations related to the pension savings plan.
    """

    def __init__(self, salary, current_balance, expected_annual_yield, 
                 current_age, retirement_age, employee_deposit, employer_deposit):
        self.salary = salary
        self.current_balance = current_balance
        self.expected_annual_yield = expected_annual_yield / 100  # Convert to decimal
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.employee_deposit = employee_deposit / 100  # Convert to decimal
        self.employer_deposit = employer_deposit / 100  # Convert to decimal
        self.start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def get_months_until_retirement(self):
        """
        Calculate the number of months until retirement.
        """
        years_until_retirement = self.retirement_age - self.current_age
        if years_until_retirement < 0:
            raise ValueError("Retirement age must be greater than current age.")
        return years_until_retirement * 12

    def get_dates(self):
        """
        Generate a list of dates until retirement.
        """
        months = self.get_months_until_retirement()
        return [self.start_date + relativedelta(months=+m) for m in range(months)]

    def calculate_monthly_deposit(self):
        """
        Calculate the monthly deposit based on salary and contributions.
        """
        return (self.salary * 0.0833) + (self.salary * self.employee_deposit) + (self.salary * self.employer_deposit)

    def generate_pension_forecast(self):
        """
        Generate a forecast dataframe with future balances.
        """
        dates = self.get_dates()
        df = pd.DataFrame({'date': dates})
        
        monthly_deposit = self.calculate_monthly_deposit()
        df['monthly_deposit'] = monthly_deposit

        monthly_yield = self.expected_annual_yield / 12
        balance = self.current_balance

        balances = []
        for _ in range(len(df)):
            balance = balance * (1 + monthly_yield) + monthly_deposit
            balances.append(balance)

        df['balance'] = balances
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        return df

    def apply_fees(self, df, fee_from_deposit, fee_from_balance):
        """
        Apply deposit and balance fees to the forecast.
        """
        df['fee_from_deposit'] = df['monthly_deposit'] * (fee_from_deposit / 100)
        df['fee_from_balance'] = df['balance'] * (fee_from_balance / 100 / 12)
        df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
        return df


class PensionApp:
    """
    The main application class that integrates UI and calculations.
    """

    def run(self):
        # st.title("חישוב פנסיה לשכיר")
        st.title("💰🧮 מחשבון פנסיה לשכירים 💰🧮")
        st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")
        user_inputs = StreamlitUI.get_user_inputs()

        if user_inputs:
            pension_calculator = PensionCalculator(**user_inputs)
            forecast_df = pension_calculator.generate_pension_forecast()
            fee_columns = forecast_df.filter(like='total_fee').columns
            if not fee_columns.empty:
                forecast_df[fee_columns] = forecast_df[fee_columns].apply(pd.to_numeric, errors='coerce').fillna(float('inf'))
                forecast_df['Lowest Total Fee'] = forecast_df[fee_columns].min(axis=1)
                forecast_df['Best Offer'] = forecast_df[fee_columns].idxmin(axis=1)
            st.write("תוצאות הסימולציה")
            st.dataframe(forecast_df[['date', 'Lowest Total Fee', 'Best Offer']])

if __name__ == "__main__":
    app = PensionApp()
    app.run()
