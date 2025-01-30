# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# import time

# start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


# def get_months_until_retirement(current_age, retirement_age):
#     """
#     Calculates the number of months until retirement.
#     """
#     try:
#         years_until_retirement = int(retirement_age) - int(current_age)
#         if years_until_retirement < 0:
#             raise ValueError("Retirement age must be greater than current age.")
#         months = years_until_retirement * 12
#         return months
#     except ValueError:
#         raise ValueError("Invalid input for ages. Please enter integer values.")


# def get_dates(start_date, months):
#     """
#     Generates a list of dates from the start date spanning the number of months.
#     """
#     dates = [start_date + relativedelta(months=+m) for m in range(months)]
#     return dates
   

# def add_monthly_deposit_column(df, salary, employee_deposit, employer_deposit, severance_pay):
#     """
#     Adds a 'monthly_deposit' column based on the salary.
#     """
#     try:
#         monthly_deposit = salary * (employee_deposit + employer_deposit + severance_pay)
#         df['monthly_deposit'] = monthly_deposit
#         return df
#     except ValueError:
#         raise ValueError("Invalid input for salary. Please enter a numeric value.")   


# def add_future_value_column(df, present_value, expected_annual_yield):
#     # monthly_yield = (expected_annual_yield/100)/12
#     monthly_yield = expected_annual_yield
#     future_values = []
#     for monthly_deposit in df['monthly_deposit']:
#         present_value = round(present_value * (1 + monthly_yield) + monthly_deposit,2)
#         future_values.append(present_value)
#     df['balance'] = future_values
#     return df


# def add_fee_columns(df, fee_from_deposit, fee_from_balance):
#     df['fee_from_deposit'] = df['monthly_deposit'] * fee_from_deposit
#     df['fee_from_balance'] = df['balance'] * fee_from_balance
#     df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
#     return df

# # Streamlit UI for Inputs
# # if 'clicked' not in st.session_state:
# #     st.session_state.clicked = False
    

# # def click_button():
# #     st.session_state.clicked = True


# def get_user_inputs():
#     with st.form("Pension Inputs", clear_on_submit=False, enter_to_submit=True):
#         salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
#         current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
#         current_age = st.text_input("גיל *", placeholder="לדוגמא: 30")
#         retirement_age = st.text_input("גיל פרישה *", placeholder="נשים 64, גברים 67")
#         employee_deposit = st.text_input("אחוז הפקדה של העובד", placeholder="בדרך כלל 6% (אפשר להגדיל עד ל-7%)")
#         employer_deposit = st.text_input("אחוז הפקדה של המעסיק", placeholder="בדרך כלל 6.5%")
#         severance_pay = st.text_input("רכיב פיצויים", placeholder="לדוגמה: 8.33%")
#         expected_annual_yield = st.text_input("תשואה שנתית צפויה", placeholder="לדוגמה: 4.5%")
#         submitted = st.form_submit_button("שלח",icon=":material/send:") #,on_click=click_button)

#         if submitted and all([salary, current_balance, current_age, retirement_age]):
#             return {"salary": float(salary.strip().replace(",", "")),
#                     "current_balance": float(current_balance.strip().replace(",", "")),
#                     "current_age": int(current_age.strip()),
#                     "retirement_age": int(retirement_age.strip()),
#                     "employee_deposit": float(employee_deposit.strip().replace("%", ""))/100 if employee_deposit.strip() else 0.06,
#                     "employer_deposit": float(employer_deposit.strip().replace("%", ""))/100 if employer_deposit.strip() else 0.065,
#                     "severance_pay": float(severance_pay.strip().replace("%", ""))/100 if severance_pay.strip() else 0.0833,
#                     "expected_annual_yield": float(expected_annual_yield.strip().replace("%", ""))/100/12 if expected_annual_yield.strip() else 0.045/12,
#                    }
#         else:
#             st.warning("יש למלא את כל הפרטים לפני השליחה")
#             return None

# def get_offer_inputs():
#     num_offers = st.number_input("כמה הצעות תרצה להשוות?", min_value=1, step=1, value=1) #, on_change=click_button)
#     offers = []

#     for i in range(num_offers):
#         st.subheader(f"Offer {i + 1}")
#         offer_name = st.text_input(f"Offer Name {i + 1}", key=f"offer_name_{i}")
#         fee_from_deposit = st.text_input("(%) דמי ניהול מהפקדה )", placeholder="לדוגמה: 1.5%") #, key=fee_deposit_key)
#         fee_from_balance = st.text_input("(%) דמי ניהול מצבירה", placeholder="לדוגמה: 0.5%") #, key=fee_balance_key)

#         if offer_name and fee_from_deposit and fee_from_balance:
#             try:
#                 offers.append({
#                     "offer_name": offer_name,
#                     "fee_from_deposit": float(fee_from_deposit.strip().replace("%", ""))/100 if float(fee_from_deposit.strip()) >=1 else fee_from_deposit,
#                     "fee_from_balance": float(fee_from_balance.strip().replace("%", ""))/100/12 if float(fee_from_balance.strip()) else 0
#                 })

#             except ValueError:
#                 st.error(f"Invalid input for fees in Offer {i + 1}. Please enter numeric values.")
#     return offers

# def get_base_df(user_inputs):
#     months = get_months_until_retirement(user_inputs["current_age"], user_inputs["retirement_age"])
#     dates = get_dates(datetime.now().replace(day=1), months)

#     df = pd.DataFrame({"date": dates})
#     df = add_monthly_deposit_column(df, user_inputs["salary"], user_inputs["employee_deposit"], user_inputs["employer_deposit"], user_inputs["severance_pay"])
#     df = add_future_value_column(df, user_inputs["current_balance"], user_inputs["expected_annual_yield"])
#     df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
#     return df


# # def format_date_column(df):
# #     """
# #     Format the 'date' column to YYYY-MM-DD format.
# #     Parameters:
# #     - df (pd.DataFrame): The input DataFrame.
# #     Returns:
# #     - pd.DataFrame: The DataFrame with the formatted 'date' column.
# #     """
# #     df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
# #     return df


# # Main Streamlit App Logic
# def main():
#     # st.title("Pension Calculator")
#     st.title("💰🧮 מחשבון פנסיה לשכירים 🧮💰")
#     st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")
    
#     user_inputs = get_user_inputs()
#     if not user_inputs:
#         return

#     # offers = get_offer_inputs()
#     # if not offers:
#     #     st.warning("יש להוסיף לפחות הצעה אחת.")
#     #     return

#     base_df = get_base_df(user_inputs)

#     # Display Progress Bar
#     progress_text = ".מבצע חישוב, אנא המתן"
#     my_bar = st.progress(0, text=progress_text)
#     for percent_complete in range(100):
#         time.sleep(0.03)
#         my_bar.progress(percent_complete + 1, text=progress_text)
#     time.sleep(1)
#     my_bar.empty()

    
#     # Display results
#     st.subheader("🤑 פנסיה צפויה 🤑")
#     st.dataframe(base_df)

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from IPython.display import display, HTML, clear_output


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
    """
    Adds a 'monthly_deposit' column based on the salary.
    """
    try:
        salary = float(salary)
        employee_deposit = float(employee_deposit)
        employer_deposit = float(employer_deposit)
        severance_pay = float(severance_pay)
        monthly_deposit = salary * (employee_deposit + employer_deposit + severance_pay)
        df['monthly_deposit'] = monthly_deposit
        return df
    except ValueError:
        raise ValueError("Invalid input for salary. Please enter a numeric value.")


def add_future_value_column(df, present_value, expected_annual_yield):
    """
    Calculates the 'balance' column based on monthly yield and deposits.
    """
    # monthly_yield = (expected_annual_yield / 100) / 12
    monthly_yield = expected_annual_yield
    future_values = []
    for monthly_deposit in df['monthly_deposit']:
        present_value = round(present_value * (1 + monthly_yield) + monthly_deposit, 2)
        future_values.append(present_value)
    df['balance'] = future_values
    return df


def add_fee_columns(df, fee_from_deposit, fee_from_balance):
    df['fee_from_deposit'] = df['monthly_deposit'] * fee_from_deposit
    df['fee_from_balance'] = df['balance'] * fee_from_balance
    df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
    return df

# Streamlit UI for Inputs

def get_user_inputs():
    with st.form("Pension Inputs", clear_on_submit=False, enter_to_submit=True):
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
                    "fee_from_balance": float(fee_from_balance.strip().replace("%", ""))/100/12 if float(fee_from_balance.strip()) else 0
                })
            except ValueError:
                st.error(f"Invalid input for fees in Offer {i + 1}. Please enter numeric values.")
    return offers


def get_base_df(user_inputs):
    months = get_months_until_retirement(user_inputs["current_age"], user_inputs["retirement_age"])
    dates = get_dates(datetime.now().replace(day=1), months)
    df = pd.DataFrame({"date": dates})
    df = add_monthly_deposit_column(df, user_inputs["salary"], user_inputs["employee_deposit"], user_inputs["employer_deposit"], user_inputs["severance_pay"])
    df = add_future_value_column(df, user_inputs["current_balance"], user_inputs["expected_annual_yield"])
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df


def get_base_df(user_inputs):
    months = get_months_until_retirement(user_inputs["current_age"], user_inputs["retirement_age"])
    # months = get_months_until_retirement(43,67)
    dates = get_dates(start_date, months)
    df = pd.DataFrame({"date": dates})  
    df = add_monthly_deposit_column(df,
                                    user_inputs["salary"], 
                                    user_inputs["employee_deposit"], 
                                    user_inputs["employer_deposit"], 
                                    user_inputs["severance_pay"]
                                   )
    df = add_future_value_column(df, user_inputs["current_balance"], user_inputs["expected_annual_yield"])
    
    # df = add_monthly_deposit_column(df, 28000, 0.07, 0.065, 0.0833)
    # df = add_future_value_column(df, 750000, 0.07/12)
    # df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df


def get_offers_lists(offers, base_df):
    offer_names = []
    dfs = []
    for offer in offers:
        df = base_df.copy()
        df = add_fee_columns(df, offer["fee_from_deposit"], offer["fee_from_balance"])
        df = df[['date', 'fee_from_balance', 'fee_from_deposit', 'total_fee']]  # Select relevant columns
        df = df.set_index('date')  # Set 'date' as the index
        df["offer_name"] = offer["offer_name"]
        # df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        # df.columns = pd.MultiIndex.from_product([[offer_name], df.columns])   
        df.columns = pd.MultiIndex.from_product([df["offer_name"].unique().tolist(), df.columns]) 
        dfs.append(df)
        offer_names.append(offer["offer_name"])
    return dfs, offer_names 


def concat_base_and_offers_df(offers, base_df):
    dfs, offer_names = get_offers_lists(offers, base_df)
    if dfs:
        offers_df = pd.concat(dfs, axis=1)
        offer_cols = [(offer, col) for offer in offer_names for col in ['fee_from_balance', 'fee_from_deposit', 'total_fee']]
        offers_df = offers_df[offer_cols]
        df = pd.concat([base_df.set_index('date'), offers_df], axis=1)
    else:
        df = base_df
    
    base_cols = [('', 'date'), ('', 'balance'), ('', 'monthly_deposit')]
    df = df.reset_index()
    df.columns = pd.MultiIndex.from_tuples(base_cols + offer_cols)
    return df


def add_min_total_fee_column(total_fee_df):
    """
    Adds a new column to the total_fee DataFrame containing the lowest value
    across all `total_fee` columns for each row.
    Parameters:
        total_fee_df (pd.DataFrame): DataFrame containing `total_fee` columns for each offer.
    Returns:
        pd.DataFrame: The modified DataFrame with a new column for the minimum `total_fee` values.
    """
    # Calculate the minimum value across all columns for each row
    total_fee_df[('Lowest_total_fee', 'total_fee')] = total_fee_df.min(axis=1)
    total_fee_df[('Lowest_total_fee', 'offer_name')] = total_fee_df.idxmin(axis=1).apply(lambda x: x[0])
    
    return total_fee_df


def reorganize_and_split_final_df(df):
    """
    Reorganizes the DataFrame so that:
    1. Each offer retains two columns (excluding `total_fee`).
    2. `total_fee` columns are moved to the end of the DataFrame.
    3. Creates a separate DataFrame containing only `total_fee` columns.
    Parameters:
        final_df (pd.DataFrame): The final DataFrame with MultiIndex columns.
    Returns:
        tuple: A tuple containing:
            - reorganized_df (pd.DataFrame): The DataFrame with `total_fee` moved to the end.
            - total_fee_df (pd.DataFrame): A DataFrame containing only `total_fee` columns, 
                                            renamed for clarity with unique names.
    """
    # Ensure the DataFrame has MultiIndex columns
    if not isinstance(df.columns, pd.MultiIndex):
        raise ValueError("DataFrame must have MultiIndex columns with the first level as offer names.")

    # Extract base columns and offer-specific columns
    base_columns = [col for col in df.columns if col[0] == '']  # Base columns
    offer_columns = [col for col in df.columns if col[0] != '']  # Offer-specific columns

    # Separate `total_fee` columns and other columns for each offer
    total_fee_columns = [col for col in offer_columns if col[1] == 'total_fee']
    other_offer_columns = [col for col in offer_columns if col[1] != 'total_fee']

    # Create a DataFrame for `total_fee` columns and rename them
    total_fee_df = df.loc[:, total_fee_columns]
    total_fee_df.columns = pd.MultiIndex.from_tuples(
        [(offer, f'{offer}_total_fee') for offer, _ in total_fee_columns]
    )

    add_min_total_fee_column(total_fee_df)
    # Reorganize the columns: base columns + other offer columns
    reorganized_columns = base_columns + other_offer_columns
    reorganized_df = df.loc[:, reorganized_columns]

    # Append the renamed `total_fee` columns to the reorganized DataFrame
    reorganized_df = pd.concat([reorganized_df, total_fee_df], axis=1)
    return reorganized_df, total_fee_df


def unify_total_fee_columns(df, unified_header='Total_Fee_by_company'):
    """
    Unify all columns with 'total_fee' in their name under a single column index.

    Parameters:
    - df (pd.DataFrame): The input DataFrame with MultiIndex columns.
    - unified_header (str): The new top-level index for the unified columns.

    Returns:
    - pd.DataFrame: The modified DataFrame with unified total_fee columns.
    """
    # Create a new list of column headers
    new_columns = []
    for col in df.columns:
        if 'total_fee' in col[1]:  # Check if 'total_fee' is in the second-level header
            new_columns.append((unified_header, col[1]))
        else:
            new_columns.append(col)

    # Update the DataFrame with the new columns
    df.columns = pd.MultiIndex.from_tuples(new_columns)
    return df


def format_currency_columns(df):
    """
    Formats all numeric columns in a DataFrame, except the first column (assumed to be a date column),
    by adding a currency symbol and formatting numbers with commas and two decimal places.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        currency_symbol (str): The currency symbol to prepend to the formatted values.

    Returns:
        pd.DataFrame: The DataFrame with formatted numeric columns.
    """
    # Iterate through all columns except the first one
    for col in df.columns[1:]:
        # Skip formatting for non-numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].astype(float).apply(lambda x: f"₪{x:,.2f}")   
    return df


def get_final_df(user_inputs):
    base_df = get_base_df(user_inputs)
    # base_df = get_base_df()
    full_df = concat_base_and_offers_df(offers, base_df)
    reorganized_df, total_fee_df = reorganize_and_split_final_df(full_df)
    formated_df = format_currency_columns(reorganized_df)
    final_df = unify_total_fee_columns(formated_df, unified_header='Total_Fee_by_company')
    return final_df


# Main Streamlit App Logic
def main():
    # st.title("Pension Calculator")
    st.title("💰🧮 מחשבון פנסיה לשכירים 🧮💰")
    st.write("תוצאות המחשבון אינן מהוות המלצה או תחליף לייעוץ.")
    user_inputs = get_user_inputs()
    if not user_inputs:
        return

    offers = get_offer_inputs()
    if not offers:
        st.warning("יש להוסיף לפחות הצעה אחת.")
        return

    df = get_final_df(user_inputs)

    # Display Progress Bar
    progress_text = ".מבצע חישוב, אנא המתן"
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.03)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    
    # Display results
    # st.write_stream(stream_data)    
    st.subheader("פנסיה צפויה")
    st.dataframe(user_inputs)

if __name__ == "__main__":
    main()
    
