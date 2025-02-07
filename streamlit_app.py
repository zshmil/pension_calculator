
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from IPython.display import display, HTML, clear_output
import time
import random
import re
import io


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
    """
    Add fee calculations to the given DataFrame.
    This function calculates the fee from monthly deposits and the fee from 
    the current balance, then sums them into a total fee column.
    Args:
        df (pd.DataFrame): The input DataFrame, expected to contain at least:
            - 'monthly_deposit' (float): The monthly deposit amount.
            - 'balance' (float): The current balance of the pension.
        fee_from_deposit (float): Percentage (as a decimal) of the monthly deposit 
            that will be charged as a fee. For example, 0.015 for 1.5%.
        fee_from_balance (float): Percentage (as a decimal) of the balance 
            that will be charged as a fee. For example, 0.005 for 0.5%.
            This value is assumed to be the monthly rate (or already converted 
            to monthly), not annual.
    Returns:
        pd.DataFrame: The same DataFrame with three new columns added:
            - 'fee_from_deposit' (float): Fee charged from the monthly deposit.
            - 'fee_from_balance' (float): Fee charged from the balance.
            - 'total_fee' (float): The sum of the above two fees.
    """
    
    df['fee_from_deposit'] = df['monthly_deposit'] * fee_from_deposit
    df['fee_from_balance'] = df['balance'] * fee_from_balance
    df['total_fee'] = df['fee_from_deposit'] + df['fee_from_balance']
    return df


def get_user_inputs():
    """
    Create and display a form in Streamlit for user pension inputs.
    The form collects various financial and personal details like monthly salary, 
    current balance, age, and deposit percentages. When the user clicks "שלח", 
    it validates required inputs before returning them as a dictionary.
    Returns:
        dict or None: A dictionary of user inputs if the form is submitted and 
        required fields are filled. The dictionary contains:
            - "salary" (float): Monthly gross salary.
            - "current_balance" (float): Current total balance in pension.
            - "current_age" (int): The user's current age.
            - "retirement_age" (int): The user's desired retirement age.
            - "employee_deposit" (float): Percentage of salary the employee contributes.
            - "employer_deposit" (float): Percentage of salary the employer contributes.
            - "severance_pay" (float): Percentage of salary for severance pay.
            - "expected_annual_yield" (float): Expected annual yield, converted to monthly.       
        If not submitted or if required fields are missing, returns None.
    """
    
    with st.form("Pension Inputs", clear_on_submit=True, enter_to_submit=True):
        salary = st.text_input(" שכר חודשי (ברוטו) *", placeholder="לדוגמה: 15,000")
        current_balance = st.text_input("צבירה נוכחית *", placeholder="לדוגמה: 300,000")
        current_age = st.text_input("גיל *", placeholder="לדוגמא: 30")
        retirement_age = st.text_input("גיל פרישה *", placeholder="נשים 64, גברים 67")
        employee_deposit = st.text_input("הפקדות עובד", placeholder="בדרך כלל 6% (אפשר להגדיל עד ל-7%)")
        employer_deposit = st.text_input("הפקדות מעסיק", placeholder="בדרך כלל 6.5%")
        severance_pay = st.text_input("רכיב פיצויים", placeholder="לדוגמה: 8.33%")
        expected_annual_yield = st.text_input("תשואה שנתית צפויה", placeholder="לדוגמה: 4.5%")
        submitted = st.form_submit_button("שלח",icon=":material/send:") #,on_click=click_button)

        if submitted and all([salary, current_balance, current_age, retirement_age]):
            try:
                st.session_state.user_inputs = {"salary": float(salary.strip().replace(",", "")),
                                                "current_balance": float(current_balance.strip().replace(",", "")),
                                                "current_age": int(current_age.strip()),
                                                "retirement_age": int(retirement_age.strip()),
                                                "employee_deposit": float(employee_deposit.strip().replace("%", ""))/100 if employee_deposit.strip() else 0.06,
                                                "employer_deposit": float(employer_deposit.strip().replace("%", ""))/100 if employer_deposit.strip() else 0.065,
                                                "severance_pay": float(severance_pay.strip().replace("%", ""))/100 if severance_pay.strip() else 0.0833,
                                                "expected_annual_yield": float(expected_annual_yield.strip().replace("%", ""))/100/12 if expected_annual_yield.strip() else 0.045/12,
                                               }

                st.success("נתונים לחישוב נקלטו!")
                return st.session_state.get("user_inputs")
            except ValueError:
                st.error("נא להזין ערכים מספריים תקינים.")              
        else:
            st.warning("יש למלא את כל הפרטים לפני השליחה")
            return None


def confirm_num_offers():
    """
    Displays a form to confirm the number of offers.
    On submission, saves the number and a confirmation flag in st.session_state.
    """
    if "num_offers" not in st.session_state:
        st.session_state.num_offers = 1
    if "num_offers_confirmed" not in st.session_state:
        st.session_state.num_offers_confirmed = False

    with st.form("num_offers_form"):
        st.header("מספר הצעות")
        desired_num_offers = st.number_input("כמה הצעות תרצה להשוות?",
                                             min_value=1,
                                             step=1,
                                             value=st.session_state.num_offers)
        submitted = st.form_submit_button("אשר מספר הצעות", icon=":material/check_circle:")
        if submitted:
            st.session_state.num_offers = desired_num_offers
            st.session_state.num_offers_confirmed = True
            st.success(f"מספר ההצעות הוגדר ל- {st.session_state.num_offers}")


def get_offer_details():
    """
    Displays a form for entering offer details based on the confirmed number of offers.
    On submission, saves the offers to st.session_state["offers"].
    """
    if st.session_state.get("num_offers_confirmed"):
        with st.form("offer_details_form"):
            st.header("פרטי הצעות")
            for i in range(st.session_state.num_offers):
                st.markdown(f"### הצעה {i + 1}")
                st.text_input(f"שם הצעה {i + 1}", key=f"offer_name_{i}")
                st.text_input(f"(%) הצעה - {i + 1} - דמי ניהול מהפקדה", placeholder="לדוגמה: 1.5%", key=f"fee_deposit_{i}")
                st.text_input(f"(%) הצעה - {i + 1} - דמי ניהול מצבירה", placeholder="לדוגמה: 0.5%", key=f"fee_balance_{i}")
            submitted = st.form_submit_button("השווה הצעות", icon=":material/calculate:")
            
        if submitted:
            offers = []
            for i in range(st.session_state.num_offers):
                offer_name = st.session_state.get(f"offer_name_{i}", "").strip()
                deposit_raw = st.session_state.get(f"fee_deposit_{i}", "").strip()
                balance_raw = st.session_state.get(f"fee_balance_{i}", "").strip()

                try:
                    fee_from_deposit = float(deposit_raw.replace("%", "")) / 100 if deposit_raw else None
                except ValueError:
                    fee_from_deposit = None
                try:
                    fee_from_balance = float(balance_raw.replace("%", "")) / 100 / 12 if balance_raw else None
                except ValueError:
                    fee_from_balance = None
                offers.append({
                    "offer_name": offer_name,
                    "fee_from_deposit": fee_from_deposit,
                    "fee_from_balance": fee_from_balance
                })
            st.session_state.offers = offers
            st.success("פרטי ההצעות נקלטו!")
    return st.session_state.get("offers")


def get_base_df(user_inputs):
    """
    Create a base DataFrame for pension calculations.
    This function:
        1. Calculates the number of months from current age to retirement.
        2. Generates a date range for those months.
        3. Adds a 'monthly_deposit' column based on user salary and deposit percentages.
        4. Adds a 'balance' column showing the future value growth each month.
    Args:
        user_inputs (dict): A dictionary of user inputs. Must include:
            - "current_age" (int)
            - "retirement_age" (int)
            - "salary" (float)
            - "employee_deposit" (float)
            - "employer_deposit" (float)
            - "severance_pay" (float)
            - "current_balance" (float)
            - "expected_annual_yield" (float) (monthly yield)
    Returns:
        pd.DataFrame: A DataFrame with at least these columns:
            - 'date' (datetime): The monthly timeline from now to retirement.
            - 'balance' (float): The calculated pension balance for each month.
            - 'monthly_deposit' (float): The deposit added each month.
    """
    
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
    df = df[['date','balance','monthly_deposit']]
    # df = add_monthly_deposit_column(df, 28000, 0.07, 0.065, 0.0833)
    # df = add_future_value_column(df, 750000, 0.07/12)
    # df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df


def get_offers_lists(offers, base_df):
    """
    Build one DataFrame per offer, appending fee columns to each.
    For each offer, this function makes a copy of `base_df`, calculates fees 
    by calling `add_fee_columns()`, then renames and organizes columns.
    Args:
        offers (list of dict): A list of offers from `get_offer_inputs()`. 
            Each offer must include:
              - "offer_name" (str)
              - "fee_from_deposit" (float)
              - "fee_from_balance" (float)
        base_df (pd.DataFrame): A DataFrame with columns at least:
            - 'date'
            - 'balance'
            - 'monthly_deposit'
    Returns:
        tuple: (dfs, offer_names)
            - dfs (list of pd.DataFrame): One DataFrame per offer, each with 
              'fee_from_balance', 'fee_from_deposit', 'total_fee', plus a 
              MultiIndex column for the offer name.
            - offer_names (list of str): A simple list of offer names.
    """
    
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
    """
    Concatenate fee DataFrames from multiple offers onto the base DataFrame.
    This function calls `get_offers_lists()`, then merges each offer's fee data
    with the original pension data. It returns a combined DataFrame with all 
    relevant columns under a MultiIndex.
    Args:
        offers (list of dict): The list of offer dictionaries.
        base_df (pd.DataFrame): The DataFrame containing base pension info.
    Returns:
        pd.DataFrame: A DataFrame combining the base pension columns and each
        offer’s fee columns side by side, structured with a MultiIndex:
            - The top-level index is the offer name (empty string for the base).
            - The second level are column names ('date', 'balance', 'monthly_deposit', 
              'fee_from_balance', 'fee_from_deposit', 'total_fee', etc.).
    """
    
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
    

def rename_df_columns(df):
    rename_dict = {'date': 'תאריך',
                   'balance': 'צבירה',
                   'monthly_deposit': 'הפקדה חודשית',
                   'fee_from_balance': 'דמי ניהול מצבירה',
                   'fee_from_deposit': 'דמי ניהול מהפקדה',
                   'offer_name': 'שם הצעה'
                  }

    # Rename columns on level=1
    df = df.rename(columns=rename_dict, level=1)
    df = df.rename(columns={'total_fee': 'דמי הניהול הכי נמוכים מבין  כל ההצעות'}, level=1)
    df = df.rename(columns=lambda x: x.replace('total_fee', 'סהכ דמי ניהול'), level=1)
    df = df.rename(columns={'Lowest_total_fee': 'הצעה הזולה ביותר'}, level=0)
    return df



def get_final_df(user_inputs, offers):
    """
    Generate the final DataFrame after combining base pension data with 
    multiple offers and formatting the result.
    Internally, this function:
        1. Builds the base pension DataFrame using user inputs (via `get_base_df()`).
        2. Concatenates fee data for each offer (via `concat_base_and_offers_df()`).
        3. Splits or reorganizes columns (`reorganize_and_split_final_df()`).
        4. Formats currency columns (`format_currency_columns()`).
        5. Unifies total fee columns under a single header (`unify_total_fee_columns()`).
    Returns:
        pd.DataFrame: The final, formatted DataFrame containing all 
        necessary columns for display or further analysis.
    """
    
    base_df = get_base_df(user_inputs)
    # base_df = get_base_df()
    full_df = concat_base_and_offers_df(offers, base_df)
    reorganized_df, total_fee_df = reorganize_and_split_final_df(full_df)
    formated_df = format_currency_columns(reorganized_df)
    # unified_df = unify_total_fee_columns(formated_df, unified_header='Total_Fee_by_company')
    unified_df = unify_total_fee_columns(formated_df, unified_header='סהכ דמי ניהול לפי חברה')
    final_df = rename_df_columns(unified_df)
    return final_df


def get_final_total_sum(df):
    cols = df.loc[:, df.columns.get_level_values(0) == 'סהכ דמי ניהול לפי חברה'].iloc[:, :-1]
    cols.columns = cols.columns.map(lambda col: (col[0], col[1].replace('_סהכ דמי ניהול', '')))
    cols_numeric = cols.replace({'₪': '', ',': ''}, regex=True).astype(float)
    sums = cols_numeric.sum(axis=0)
    sums_formatted = sums.apply(lambda x: f'₪{x:,.2f}')
    df_one_line = sums_formatted.to_frame().T
    # df_one_line['צבירה'] = df.loc[:, df.columns.get_level_values(0) == ''].iloc[:, 1].tolist()[-1]
    total_value = df.loc[:, df.columns.get_level_values(0) == ''].iloc[:, 1].tolist()[-1]
    df_one_line.insert(0, 'צבירה', total_value)
    return df_one_line


def add_difference_row(df, coefficient):
    """
    Given a one-row DataFrame with MultiIndex columns like:
        ('צבירה', '')
        ('סהכ דמי ניהול לפי חברה', 'הראל')
        ('סהכ דמי ניהול לפי חברה', 'פניקס')
        ('סהכ דמי ניהול לפי חברה', 'מנורה') 
    This function creates two new rows:
      1. "הפרש" – For each offer column, it computes: (צבירה - offer value)
      2. "תוצאה חלקי {coefficient}" – For each offer column, it computes:
         (צבירה - offer value) divided by the given coefficient.       
    The new rows are appended to the original DataFrame.
    """
    # Assume the DataFrame has only one row; get its index (usually 0)
    row_idx = df.index[0]
    
    # Extract the 'צבירה' value (assumed to be in the column with top-level 'צבירה' and empty second level)
    total_str = df.loc[row_idx, ('צבירה', '')]
    total = float(total_str.replace("₪", "").replace(",", ""))
    
    # Build the "הפרש" row (difference row)
    diff_row = {}
    for col in df.columns:
        if col[0] == 'סהכ דמי ניהול לפי חברה':
            offer_str = df.loc[row_idx, col]
            offer_val = float(offer_str.replace("₪", "").replace(",", ""))
            diff_val = total - offer_val
            diff_row[col] = f'₪{diff_val:,.2f}'
        else:
            diff_row[col] = ''
    diff_df = pd.DataFrame(diff_row, index=["צבירה בניכוי דמי ניהול"])
    
    # Build the division row (result divided by coefficient)
    div_row = {}
    for col in df.columns:
        if col[0] == 'סהכ דמי ניהול לפי חברה':
            offer_str = df.loc[row_idx, col]
            offer_val = float(offer_str.replace("₪", "").replace(",", ""))
            diff_val = total - offer_val
            div_val = diff_val / coefficient
            div_row[col] = f'₪{div_val:,.2f}'
        else:
            div_row[col] = ''
    div_label = 'קצבה צפויה'
    div_df = pd.DataFrame(div_row, index=[div_label])
    
    # Concatenate the original one-row DataFrame with the two new rows
    result_df = pd.concat([df, diff_df, div_df])
    return result_df


def style_lowest_total(df_one_line):
    """
    Styles the entire column(s) that contain the lowest value in the one-line DataFrame.
    Assumes that the DataFrame's cells are formatted as currency strings (e.g., "₪135.15").
    """
    # Convert the first row's values to numeric values for comparison
    numeric_row = df_one_line.iloc[0].replace({'₪': '', ',': ''}, regex=True).astype(float)
    min_val = numeric_row.min()
    
    # Identify the column names (i.e. MultiIndex tuples) that have the minimum value
    lowest_columns = numeric_row[numeric_row == min_val].index.tolist()
    
    # Define a function to style an entire column if its name is in the lowest_columns list
    def highlight_lowest_column(col):
        if col.name in lowest_columns:
            return ['background-color: #99ff33'] * len(col)
        else:
            return [''] * len(col)  
    return df_one_line.style.apply(highlight_lowest_column, axis=0)


def get_bottom_line(df):
    df_one_line = get_final_total_sum(df)
    bottom_line_df = add_difference_row(df_one_line,220)
    bottom_line_df.rename(index={0: 'צבירה ודמי ניהול לפי חברה'}, inplace=True)
    return style_lowest_total(bottom_line_df)


@st.cache_data
def convert_df_to_excel(df):
    """
    Export a MultiIndex DataFrame to an Excel file with merged headers for hierarchical column names.
    Parameters:
    - df (pd.DataFrame): The DataFrame to export.
    - file_name (str): The name of the Excel file to save.
    - sheet_name (str): The name of the sheet in the Excel file.
    """
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Write the DataFrame to Excel with merged headers
        df.to_excel(writer,
                    sheet_name='Sheet1',
                    # index=False,
                    merge_cells=True)
    processed_data = output.getvalue()
    return processed_data


def show_download_button(df):
    """
    Displays a download button if the predictions (or final DataFrame) are ready.
    """
    excel_data = convert_df_to_excel(df)
    st.download_button(
        label='שמור תוצאות באקסל', 
        data=excel_data,
        file_name="pension_calculator.xlsx",
        # mime="application/octet-stream"
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        icon=":material/download:"
    )


def get_excpeted_monthly_allowance(df):
    df_one_line = get_final_total_sum(df)
    bottom_line_df = add_difference_row(df_one_line,220)
    bottom_line_df.rename(index={0: 'צבירה ודמי ניהול לפי חברה'}, inplace=True)
    fee_row_numeric = bottom_line_df.iloc[0,1:].replace({'₪': '', ',': ''}, regex=True).astype(float)
    fee = f'₪{fee_row_numeric.min():,.2f}'
    allowance_row_numeric = bottom_line_df.iloc[2,1:].replace({'₪': '', ',': ''}, regex=True).astype(float)
    allowance = f'₪{allowance_row_numeric.max():,.2f}'
    company_name = allowance_row_numeric.idxmax()[1]
    # final_text = f'{company_name} מציעים את ההצעה הזולה ביותר, עם דמי ניהול של {fee} לכל אורך שנות החיסכון, מה שמביא לקצבה צפויה של כ-{allowance}'
    final_text = {'allowance': allowance,
                 'fee': fee,
                  'company_name': company_name}
    return final_text


def styled_subheader_green(text, color="#27ae60", align="right", background="#f0f0f0", font_family="Arial", font_size="1.75em", margin="20px 0 10px 0"):
    """
    Renders text as a styled subheader using HTML.    
    Parameters:
      - text (str): The subheader text.
      - color (str): The text color in hex.
      - align (str): Text alignment.
      - font_family (str): The font family.
      - font_size (str): The font size.
      - margin (str): CSS margin (top, right, bottom, left).
    """
    html_str = f"""
    <h3 style="
        text-align: {align};
        color: {color};
        font-family: {font_family};
        font-size: {font_size};
        margin: {margin};
    ">{text}</h3>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def styled_subheader_black(text, color="black", align="center", font_family="Arial", font_size="1.75em", margin="20px 0 10px 0"):
    """
    Renders text as a styled subheader using HTML.    
    Parameters:
      - text (str): The subheader text.
      - color (str): The text color in hex.
      - align (str): Text alignment.
      - font_family (str): The font family.
      - font_size (str): The font size.
      - margin (str): CSS margin (top, right, bottom, left).
    """
    html_str = f"""
    <h3 style="
        text-align: {align};
        color: {color};
        font-family: {font_family};
        font-size: {font_size};
        margin: {margin};
    ">{text}</h3>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def styled_title(text, color="black", align="right", font_family="Arial", font_size="3em", margin="20px 0 10px 0"):
    """
    Renders text as a styled title using HTML.   
    Parameters:
      - text (str): The title text.
      - color (str): The text color (e.g., 'black' or any valid CSS color).
      - align (str): Text alignment (e.g., 'center', 'left', 'right').
      - font_family (str): The font family (e.g., 'Arial', 'Helvetica').
      - font_size (str): The font size (e.g., '3em', '36px').
      - margin (str): CSS margin (top, right, bottom, left).
    """
    html_str = f"""
    <h1 style="
        text-align: {align};
        color: {color};
        font-family: {font_family};
        font-size: {font_size};
        margin: {margin};
    ">{text}</h1>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def styled_markdown(text, color="black", align="right",  background="#f0f0f0", font_family="Arial (Body CS)", font_size="1.2", margin="10px 0 10px 0"):
    """
    Renders text as a styled title using HTML.
    Parameters:
      - text (str): The title text.
      - color (str): The text color (e.g., 'black' or any valid CSS color).
      - align (str): Text alignment (e.g., 'center', 'left', 'right').
      - font_family (str): The font family (e.g., 'Arial', 'Helvetica').
      - font_size (str): The font size (e.g., '3em', '36px').
      - margin (str): CSS margin (top, right, bottom, left).
    """
    html_str = f"""
    <p style="
        text-align: {align};
        background-color: {background};
        color: {color};
        font-family: {font_family};
        font-size: {font_size};
        margin: {margin};
    ">{text}</p>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def main():
    st.logo('me_linkedin.png')
    st.title("💰🧮 מחשבון פנסיה לשכירים 🧮💰")
    st.divider()
    styled_markdown(''',מחשבון פנסיה לשכירים – כלי פשוט ונוח המאפשר להזין פרטים אישיים כגון שכר, גיל, הפקדות ותשואה צפויה<br>
    .ולחזות את צפי החיסכון הפנסיוני העתידי שלך<br>
    המחשבון מסייע לעשות סדר בהשוואת הצעות שונות ובבחירה בין מספר הצעות שקיבלת (אך אינו מחפש הצעות מול חברות, יש להזין פרטי ההצעות)<br>
    <strong>.המחשבון אינו מהווה המלצה ו/או תחליף לייעוץ מקצועי</strong>''', background="white")
    st.divider()
    
    # Step 1: Get and save user inputs.
    user_inputs = get_user_inputs()
    
    # Once user inputs are saved, proceed.
    if "user_inputs" in st.session_state:
        user_inputs = st.session_state.user_inputs

        styled_markdown(f'''<strong>:הפרטים שהוזנו<br></strong>
    <strong>משכורת:</strong> {st.session_state.user_inputs['salary']:,.0f}₪<br>
    <strong>צבירה:</strong> {st.session_state.user_inputs['current_balance']:,.0f}₪<br>
    <strong>גיל:</strong> {st.session_state.user_inputs['current_age']}<br>
    <strong>גיל פרישה:</strong> {st.session_state.user_inputs['retirement_age']}<br>
    <strong>הפקדות עובד:</strong> {st.session_state.user_inputs['employee_deposit']*100:,.2f}%<br>
    <strong>הפקדות מעסיק:</strong> {st.session_state.user_inputs['employer_deposit']*100:,.2f}%<br>
    <strong>פיצויים:</strong> {st.session_state.user_inputs['severance_pay']*100:,.2f}%<br>
    <strong>תשואה צפויה:</strong> {st.session_state.user_inputs['expected_annual_yield']*100*12:,.2f}%<br>
    ''',  font_size="18px", background="#E8F9EE")

        st.divider()    
        # Step 2: Confirm the number of offers.
        confirm_num_offers()
        
        # Step 3: If the number of offers is confirmed, show the offer details form.
        if st.session_state.get("num_offers_confirmed"):
            styled_markdown('''<strong>:אנא הזן את פרטי ההצעות</strong>''')
            offers = get_offer_details()
            
            # Step 4: If offers are saved, calculate and display the result.
            if "offers" in st.session_state:
                offers = st.session_state.offers
                df = get_final_df(user_inputs, offers)
                # Display Progress Bar #
                progress_text = ".מבצע חישוב, אנא המתן"
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.03)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                st.divider() 
                styled_subheader_black("פנסיה צפויה")
                styled_markdown('''<strong>.תוצאות המחשבון אינן מהוות המלצה ו/או תחליף לייעוץ מקצועי</strong>''')
                st.dataframe(df)
                show_download_button(df)
                st.divider() 
                styled_subheader_black("סהכ דמי ניהול לאורך שנות החיסכון")
                st.dataframe(get_bottom_line(df))
                final_text = get_excpeted_monthly_allowance(df)
                # styled_subheader_green(final_text)
                styled_subheader_green(final_text[company_name])

#                 styled_subheader_green(f'''{final_text[company_name]} מציעים את ההצעה הזולה ביותר, עם דמי ניהול של<br>
# {final_text[fee]} לכל אורך שנות החיסכון, מה שמביא לקצבה צפויה של כ-{final_text[allowance]}
#     ''',  font_size="18px", background="#E8F9EE")
                
if __name__ == "__main__":
    main()
