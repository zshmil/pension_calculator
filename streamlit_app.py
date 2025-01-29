import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_months_until_retirement(current_age, retirement_age):
    """
    Calculates the number of months until retirement.
    """
    try:
        years_until_retirement = int(retirement_age) - int(current_age)
        if years_until_retirement < 0:
            raise ValueError("Retirement age must be greater than current age.")
        months = years_until_retirement * 12
        return months
    except ValueError:
        raise ValueError("Invalid input for ages. Please enter integer values.")


def get_dates(start_date, months):
    """
    Generates a list of dates from the start date spanning the number of months.
    """
    dates = [start_date + relativedelta(months=+m) for m in range(months)]
    return dates
   

def add_monthly_deposit_column(df, salary, employee_deposit, employer_deposit, severance_pay):
    # monthly_deposit = (salary * severance_pay) + (salary * employee_deposit) + (salary * employer_deposit)
    monthly_deposit = salary * (employee_deposit + employer_deposit + severance_pay)
    df['monthly_deposit'] = monthly_deposit
    return df


def add_future_value_column(df, present_value, expected_annual_yield):
    # monthly_yield = (expected_annual_yield/100)/12
    monthly_yield = expected_annual_yield
    future_values = []
    for monthly_deposit in df['monthly_deposit']:
        present_value = round(present_value * (1 + monthly_yield) + monthly_deposit,2)
        future_values.append(present_value)
    df['balance'] = future_values
    return df


def add_fee_columns(df, fee_from_deposit, fee_from_balance):
    df['fee_from_deposit'] = df['monthly_deposit'] * fee_from_deposit
    df['fee_from_balance'] = df['balance'] * fee_from_balance
    df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
    return df

# Streamlit UI for Inputs
# if 'clicked' not in st.session_state:
#     st.session_state.clicked = False
    

# def click_button():
#     st.session_state.clicked = True


def get_user_inputs():
    with st.form("Pension Inputs", clear_on_submit=True):
        salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
        current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
        current_age = st.text_input("גיל *", placeholder="לדוגמא: 30")
        retirement_age = st.text_input("גיל פרישה *", placeholder="נשים 64, גברים 67")
        employee_deposit = st.text_input("אחוז הפקדה של העובד", placeholder="בדרך כלל 6% (אפשר להגדיל עד ל-7%)")
        employer_deposit = st.text_input("אחוז הפקדה של המעסיק", placeholder="בדרך כלל 6.5%")
        severance_pay = st.text_input("רכיב פיצויים", placeholder="לדוגמה: 8.33%")
        expected_annual_yield = st.text_input("תשואה שנתית צפויה", placeholder="לדוגמה: 4.5%")
        submitted = st.form_submit_button("שלח",icon=":material/send:") #,on_click=click_button)

        if submitted and all([salary, current_balance, current_age, retirement_age]):
            return {"salary": float(salary.strip().replace(",", "")),
                    "current_balance": float(current_balance.strip().replace(",", "")),
                    "current_age": int(current_age.strip()),
                    "retirement_age": int(retirement_age.strip()),
                    "employee_deposit": float(employee_deposit.strip().replace("%", ""))/100 if employee_deposit.strip() else 0.06,
                    "employer_deposit": float(employer_deposit.strip().replace("%", ""))/100 if employer_deposit.strip() else 0.065,
                    "severance_pay": float(severance_pay.strip().replace("%", ""))/100 if severance_pay.strip() else 0.0833,
                    "expected_annual_yield": float(expected_annual_yield.strip().replace("%", ""))/100/12 if expected_annual_yield.strip() else 0.045/12,
                   }
        else:
            st.warning("יש למלא את כל הפרטים לפני השליחה")
            return None

def get_offer_inputs():
    num_offers = st.number_input("כמה הצעות תרצה להשוות?", min_value=1, step=1, value=1) #, on_change=click_button)
    offers = []

    for i in range(num_offers):
        st.subheader(f"Offer {i + 1}")
        offer_name = st.text_input(f"Offer Name {i + 1}", key=f"offer_name_{i}")
        fee_from_deposit = st.text_input("(%) דמי ניהול מהפקדה )", placeholder="לדוגמה: 1.5%") #, key=fee_deposit_key)
        fee_from_balance = st.text_input("(%) דמי ניהול מצבירה", placeholder="לדוגמה: 0.5%") #, key=fee_balance_key)

        if offer_name and fee_from_deposit and fee_from_balance:
            try:
                offers.append({
                    "offer_name": offer_name,
                    "fee_from_deposit": float(fee_from_deposit.strip().replace("%", ""))/100 if float(fee_from_deposit.strip()) >=1 else fee_from_deposit,
                    "fee_from_balance": float(fee_from_balance.strip().replace("%", ""))/12 if float(fee_from_balance.strip()) else 0
                })

            except ValueError:
                st.error(f"Invalid input for fees in Offer {i + 1}. Please enter numeric values.")
    return offers

# def format_date_column(df):
#     """
#     Format the 'date' column to YYYY-MM-DD format.
#     Parameters:
#     - df (pd.DataFrame): The input DataFrame.
#     Returns:
#     - pd.DataFrame: The DataFrame with the formatted 'date' column.
#     """
#     df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
#     return df
    

# Main Streamlit App Logic
def main():
    # st.title("Pension Calculator")
    st.title("💰🧮 מחשבון פנסיה לשכירים 🧮💰")
    st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")
    user_inputs = get_user_inputs()
    if not user_inputs:
        return

    # offers = get_offer_inputs()
    # if not offers:
    #     st.warning("יש להוסיף לפחות הצעה אחת.")
    #     return

    # Perform calculations
    months = get_months_until_retirement(user_inputs["current_age"], user_inputs["retirement_age"])
    dates = get_dates(datetime.now().replace(day=1), months)

    base_df = pd.DataFrame({"date": dates})
    base_df = add_monthly_deposit_column(base_df, user_inputs["salary"], user_inputs["employee_deposit"], user_inputs["employer_deposit"], user_inputs["severance_pay"])
    base_df = add_future_value_column(base_df, user_inputs["current_balance"], user_inputs["expected_annual_yield"])
    base_df['date'] = pd.to_datetime(base_df['date']).dt.strftime('%Y-%m-%d')

    # dfs = []
    # for offer in offers:
    #     df = base_df.copy()
    #     df = add_fee_columns(df, offer["fee_from_deposit"], offer["fee_from_balance"])
    #     df["offer_name"] = offer["offer_name"]
    #     dfs.append(df.set_index("date"))

    # # Combine all DataFrames
    # final_df = pd.concat(dfs, axis=1, keys=[offer["offer_name"] for offer in offers])

    progress_text = ".מבצע חישוב, אנא המתן"
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.03)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    # Display results
    # st.write_stream(base_df)    
    st.subheader("🤑 פנסיה צפויה 🤑")
    st.dataframe(base_df)

if __name__ == "__main__":
    main()
