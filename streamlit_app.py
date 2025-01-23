
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


# class PensionCalculator:
#     """
#     Handles all calculations related to pension projection and fee calculations.
#     """

#     @staticmethod
#     def get_months_until_retirement(current_age, retirement_age):
#         """
#         Calculates the number of months until retirement.
#         """
#         years_until_retirement = retirement_age - current_age
#         return years_until_retirement * 12

#     @staticmethod
#     def get_dates(start_date, months):
#         """
#         Generates a list of future dates from start date.
#         """
#         return [start_date + relativedelta(months=+m) for m in range(months)]

#     @staticmethod
#     def calculate_monthly_deposit(salary, employee_deposit, employer_deposit):
#         """
#         Calculates the total monthly deposit.
#         """
#         return (salary * 0.0833) + (salary * (employee_deposit / 100)) + (salary * (employer_deposit / 100))

#     @staticmethod
#     def calculate_future_values(df, present_value, annual_yield):
#         """
#         Calculates future values with compound interest.
#         """
#         monthly_yield = (annual_yield / 100) / 12
#         future_values = []
#         for monthly_deposit in df['monthly_deposit']:
#             present_value = present_value * (1 + monthly_yield) + monthly_deposit
#             future_values.append(present_value)
#         df['balance'] = future_values
#         return df

#     @staticmethod
#     def apply_fees(df, fee_from_deposit, fee_from_balance):
#         """
#         Adds fee columns based on balance and deposit.
#         """
#         df['fee_from_deposit'] = df['monthly_deposit'] * (fee_from_deposit / 100)
#         df['fee_from_balance'] = df['balance'] * (fee_from_balance / 100 / 12)
#         df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
#         return df

#     @staticmethod
#     def prepare_final_dataframe(dates, salary, current_balance, annual_yield, employee_deposit, employer_deposit, fee_from_deposit, fee_from_balance):
#         """
#         Generates the complete pension projection DataFrame.
#         """
#         df = pd.DataFrame({'date': dates})
#         df['monthly_deposit'] = PensionCalculator.calculate_monthly_deposit(salary, employee_deposit, employer_deposit)
#         df = PensionCalculator.calculate_future_values(df, current_balance, annual_yield)
#         df = PensionCalculator.apply_fees(df, fee_from_deposit, fee_from_balance)
#         return df

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
#             else:
#                 st.warning("יש למלא את כל הפרטים לפני השליחה")
#                 return None

# class DataFormatter:
#     """
#     Handles formatting operations for the pension data.
#     """

#     @staticmethod
#     def format_currency(df):
#         """
#         Formats all numeric columns to display currency with commas and two decimal places.
#         """
#         for col in df.columns[1:]:
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 df[col] = df[col].apply(lambda x: f"₪{x:,.2f}")
#         return df

#     @staticmethod
#     def reorder_columns(df):
#         """
#         Reorders the columns for better readability.
#         """
#         return df[['date', 'balance', 'monthly_deposit', 'fee_from_balance', 'fee_from_deposit', 'total_fee']]

# # Main Streamlit App
# def main():
#     # st.title("Pension Calculator")
#     st.title("💰🧮 מחשבון פנסיה לשכיר 💰🧮")
#     st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")

#     # Step 1: Get user inputs
#     user_inputs = StreamlitUI.get_user_inputs()

#     if user_inputs:
#         start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#         months_until_retirement = PensionCalculator.get_months_until_retirement(
#             user_inputs["current_age"], user_inputs["retirement_age"]
#         )
#         dates = PensionCalculator.get_dates(start_date, months_until_retirement)

#         # Step 2: Calculate the pension projection
#         df = PensionCalculator.prepare_final_dataframe(
#             dates,
#             user_inputs["salary"],
#             user_inputs["current_balance"],
#             user_inputs["expected_annual_yield"],
#             user_inputs["employee_deposit"],
#             user_inputs["employer_deposit"],
#             0,  # Fee from deposit (default to 0)
#             0   # Fee from balance (default to 0)
#         )

#         # Step 3: Format and display the results
#         df = DataFormatter.reorder_columns(df)
#         df = DataFormatter.format_currency(df)

#         st.write("## תוצאות חישוב פנסיה")
#         st.dataframe(df)

# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

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


class PensionApp:
    """
    The main application class that integrates UI and calculations.
    """

    def run(self):
        st.title("חישוב פנסיה לשכיר")
        user_inputs = StreamlitUI.get_user_inputs()

        if user_inputs:
            # Create an instance of PensionCalculator
            pension_calculator = PensionCalculator(
                salary=user_inputs["salary"],
                current_balance=user_inputs["current_balance"],
                expected_annual_yield=user_inputs["expected_annual_yield"],
                current_age=user_inputs["current_age"],
                retirement_age=user_inputs["retirement_age"],
                employee_deposit=user_inputs["employee_deposit"],
                employer_deposit=user_inputs["employer_deposit"],
            )

            forecast_df = pension_calculator.generate_pension_forecast()

            # Display forecast data
            st.write("תחזית חיסכון פנסיוני")
            st.dataframe(forecast_df)

            # Display summary metrics
            final_balance = forecast_df['balance'].iloc[-1]
            total_contributions = forecast_df['monthly_deposit'].sum()
            st.metric("יתרה צפויה בעת הפרישה", f"₪{final_balance:,.2f}")
            st.metric("סה״כ הפקדות", f"₪{total_contributions:,.2f}")

            # Graph
            st.line_chart(forecast_df.set_index('date')['balance'])

if __name__ == "__main__":
    app = PensionApp()
    app.run()
