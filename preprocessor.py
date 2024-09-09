import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{2}\s*(?:AM|PM) -'

    # Extract messages and dates using regex
    messages = re.split(pattern, data)
    messages = [message.strip() for message in messages if message.strip()]

    dates = re.findall(pattern, data)
    dates = [date.replace('\u202f', '').strip() for date in dates]

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert 'message_date' to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M%p -', errors='coerce')

    # Rename 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract month, day, hour, and minute before converting 'date' to string
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Convert 'date' back to string format (if needed for display purposes)
    df['date'] = df['date'].dt.strftime('%m/%d/%y, %I:%M %p')

    # Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    # Drop the 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df
