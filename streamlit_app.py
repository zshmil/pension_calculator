
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

st.title("💰🧮 מחשבון פנסיה לשכיר 💰🧮")
st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")


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

            # Get multiple offers from user
            offers = {}
            st.write("הוסף תוכניות פנסיה עם עמלות שונות")
            add_offer = st.checkbox("הוסף תוכנית פנסיה חדשה")

            while add_offer:
                offer_name = st.text_input("שם התוכנית:")
                fee_from_deposit = st.number_input("עמלה מהפקדה (%):", min_value=0.0, max_value=100.0, value=0.5)
                fee_from_balance = st.number_input("עמלה מהיתרה (%):", min_value=0.0, max_value=100.0, value=0.2)

                if st.button("הוסף תוכנית"):
                    df_with_fees = pension_calculator.apply_fees(forecast_df.copy(), fee_from_deposit, fee_from_balance)
                    offers[offer_name] = df_with_fees[['date', 'fee_from_balance', 'fee_from_deposit', 'total_fee']]
                    st.success(f"תוכנית {offer_name} נוספה בהצלחה!")
            
            # Merge all offers into a single DataFrame
            if offers:
                offer_dfs = [df.set_index('date') for df in offers.values()]
                merged_df = pd.concat([forecast_df.set_index('date')] + offer_dfs, axis=1)
                merged_df.reset_index(inplace=True)
            else:
                merged_df = forecast_df

            st.write("תוצאות הסימולציה")
            st.dataframe(merged_df)

            # Show lowest fee
            merged_df['Lowest Total Fee'] = merged_df.filter(like='total_fee').min(axis=1)
            merged_df['Best Offer'] = merged_df.filter(like='total_fee').idxmin(axis=1)

            st.write("השוואת עמלות בין התוכניות השונות")
            st.dataframe(merged_df[['date', 'Lowest Total Fee', 'Best Offer']])


if __name__ == "__main__":
    app = PensionApp()
    app.run()
