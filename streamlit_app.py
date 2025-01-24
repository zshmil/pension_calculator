
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

import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# st.title("💰🧮 מחשבון פנסיה לשכירים 🧮💰")
# st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")


class PensionCalculator:
    @staticmethod
    def get_months_until_retirement(current_age, retirement_age):
        years_until_retirement = int(retirement_age) - int(current_age)
        if years_until_retirement < 0:
            raise ValueError("Retirement age must be greater than current age.")
        return years_until_retirement * 12

    @staticmethod
    def get_dates(start_date, months):
        return [start_date + relativedelta(months=+m) for m in range(months)]

    @staticmethod
    def calculate_monthly_deposit(salary, employee_deposit, employer_deposit):
        return salary * ((severance_pay/100) + (employee_deposit/100) + (employer_deposit/100))

    @staticmethod
    def calculate_balance(df, current_balance, expected_annual_yield):
        monthly_yield = (expected_annual_yield / 100) / 12
        balances = []
        for _, row in df.iterrows():
            current_balance = current_balance * (1 + monthly_yield) + row['monthly_deposit']
            balances.append(current_balance)
        df['balance'] = balances
        return df

    @staticmethod
    def calculate_fees(df, fee_from_deposit, fee_from_balance):
        df['fee_from_deposit'] = df['monthly_deposit'] * fee_from_deposit
        df['fee_from_balance'] = df['balance'] * fee_from_balance
        df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
        return df

class StreamlitUI:
    @staticmethod
    def get_user_inputs():
        """
        Collects user input via Streamlit UI and returns a dictionary.
        """

        with st.form("חישוב פנסיה לשכיר", clear_on_submit=True):
            salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
            current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
            current_age = st.text_input("גיל *", placeholder="לדוגמא: 30")
            retirement_age = st.text_input("גיל פרישה *", placeholder="נשים 64, גברים 67")
            employee_deposit = st.text_input("אחוז הפקדה של העובד", placeholder="בדרך כלל 6% (אפשר להגדיל עד ל-7%)")
            employer_deposit = st.text_input("אחוז הפקדה של המעסיק", placeholder="בדרך כלל 6.5%")
            severance_pay = st.text_input("רכיב פיצויים", placeholder="לדוגמה: 8.33%")
            expected_annual_yield = st.text_input("תשואה שנתית צפויה", placeholder="לדוגמה: 4.5%")
            submitted = st.form_submit_button("הוסף")

        if submitted and all([salary, current_balance, current_age, retirement_age]):
            return {"salary": float(salary.strip().replace(",", "")),
                    "current_balance": float(current_balance.strip().replace(",", "")),
                    "current_age": int(current_age.strip()),
                    "retirement_age": int(retirement_age.strip()),
                    "employee_deposit": float(employee_deposit.strip().replace("%", "")) if employee_deposit.strip() else 6.0,
                    "employer_deposit": float(employer_deposit.strip().replace("%", "")) if employer_deposit.strip() else 6.5,
                    "severance_pay": float(employer_deposit.strip().replace("%", "")) if employer_deposit.strip() else 8.33,
                    "expected_annual_yield": float(expected_annual_yield.strip().replace("%", "")) if expected_annual_yield.strip() else 4.5,
                   }
        else:
            st.warning("יש למלא את כל הפרטים לפני השליחה")
            return None

@staticmethod
def get_offer_inputs():
    if "offer_counter" not in st.session_state:
        st.session_state.offer_counter = 0  # Initialize the counter in session state

    offers = []
    while True:
        # Generate unique keys for each form and its elements
        form_key = f"Offer_Input_Form_{st.session_state.offer_counter}"
        name_key = f"offer_name_{st.session_state.offer_counter}"
        fee_deposit_key = f"fee_deposit_{st.session_state.offer_counter}"
        fee_balance_key = f"fee_balance_{st.session_state.offer_counter}"
        more_offers_key = f"add_offer_{st.session_state.offer_counter}"

        with st.form(form_key, clear_on_submit=True):
            offer_name = st.text_input("שם הצעה", key=name_key)
            fee_from_deposit = st.text_input("(%) דמי ניהול מהפקדה )", placeholder="לדוגמה: 1.5%", key=fee_deposit_key)
            fee_from_balance = st.text_input("(%) דמי ניהול מצבירה", placeholder="לדוגמה: 0.5%", key=fee_balance_key)
            offer_submitted = st.form_submit_button("הוסף הצעה")

            if offer_submitted and offer_name:
                offers.append({
                    "offer_name": offer_name,
                    "fee_from_deposit": float(fee_from_deposit.strip().replace("%", "")) / 100
                    if fee_from_deposit.strip() else 0.06,
                    "fee_from_balance": float(fee_from_balance.strip().replace("%", "")) / 100 / 12
                    if fee_from_balance.strip() else 0.005,
                })
                st.session_state.offer_counter += 1  # Increment after successful submission
                st.success(f"הצעה '{offer_name}' נוספה בהצלחה!")
                continue  # Restart the loop for the next offer

        # Radio button to check if the user wants to add more offers
        more_offers = st.radio("האם יש לך הצעה נוספת?", ["Yes", "No"], key=more_offers_key)
        if more_offers == "No":
            break
    return offers


def main():
    # st.title("Pension Calculator")
    st.title("💰🧮 מחשבון פנסיה לשכירים 🧮💰")
    st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")
    
    # Get user inputs
    user_inputs = StreamlitUI.get_user_inputs()
    if not user_inputs:
        return

    # Get offer inputs
    st.subheader("Enter Offers")
    offers = StreamlitUI.get_offer_inputs()
    if not offers:
        st.warning("Please add at least one offer.")
        return

    # Calculate results
    months_until_retirement = PensionCalculator.get_months_until_retirement(user_inputs['current_age'], user_inputs['retirement_age'])
    dates = PensionCalculator.get_dates(datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0), months_until_retirement)

    base_df = pd.DataFrame({"date": dates})
    base_df['monthly_deposit'] = PensionCalculator.calculate_monthly_deposit(
        user_inputs['salary'], user_inputs['employee_deposit'], user_inputs['employer_deposit']
    )

    base_df = PensionCalculator.calculate_balance(base_df, user_inputs['current_balance'], user_inputs['expected_annual_yield'])

    # Calculate fees for each offer
    results = []
    for offer in offers:
        df = base_df.copy()
        df = PensionCalculator.calculate_fees(df, offer['fee_from_deposit'], offer['fee_from_balance'])
        df['offer_name'] = offer['offer_name']
        results.append(df)

    # Display results
    for result in results:
        st.subheader(f"Results for {result['offer_name'].iloc[0]}")
        st.dataframe(result)

if __name__ == "__main__":
    main()
