from flask import Blueprint, jsonify, request, send_file
from ..services.database import get_db_connection
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime, timedelta

statistic_reports_blueprint = Blueprint('statistic_reports', __name__)

@statistic_reports_blueprint.route('/getWeeklyReviewReport', methods=['GET'])
def get_weekly_review_report():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Calculate the date two months ago from today
    two_months_ago = datetime.now() - timedelta(days=60)

    # SQL query to count reviews per week for the last two months
    query = """
    SELECT YEARWEEK(date) as review_week, COUNT(*) as review_count
    FROM reviews
    WHERE date >= %s
    GROUP BY YEARWEEK(date)
    ORDER BY YEARWEEK(date)
    """

    # Execute the query
    cursor.execute(query, (two_months_ago,))
    
    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

     # Prepare data for plotting
    date_ranges = []
    counts = []
    for result in results:
        year_week = str(result['review_week'])
        year = int(year_week[:4])
        week = int(year_week[4:]) - 1
        week_start = datetime(year, 1, 1) + timedelta(weeks=week)
        if week_start.weekday() > 0:
            week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=6)
        date_range = f"{week_start.strftime('%Y/%m/%d')} - {week_end.strftime('%Y/%m/%d')}"
        date_ranges.append(date_range)
        counts.append(result['review_count'])

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(date_ranges, counts, marker='o')
    plt.title('Number of Reviews Written per Week')
    plt.xlabel('Date Range')
    plt.ylabel('Number of Reviews')

    # Adjust x-axis labels: smaller font and horizontal alignment
    plt.xticks(rotation=0, fontsize=8)  # Change rotation to 0 and adjust font size as needed
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object to send as a response
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Send the image in the response
    return send_file(img, mimetype='image/png')

@statistic_reports_blueprint.route('/getWeeklyCommentReport', methods=['GET'])
def get_weekly_comment_report():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Calculate the date two months ago from today
    two_months_ago = datetime.now() - timedelta(days=60)

    # SQL query to count reviews per week for the last two months
    query = """
    SELECT YEARWEEK(date) as comment_week, COUNT(*) as comment_count
    FROM comments
    WHERE date >= %s
    GROUP BY YEARWEEK(date)
    ORDER BY YEARWEEK(date)
    """

    # Execute the query
    cursor.execute(query, (two_months_ago,))
    
    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

     # Prepare data for plotting
    date_ranges = []
    counts = []
    for result in results:
        year_week = str(result['comment_week'])
        year = int(year_week[:4])
        week = int(year_week[4:]) - 1
        week_start = datetime(year, 1, 1) + timedelta(weeks=week)
        if week_start.weekday() > 0:
            week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=6)
        date_range = f"{week_start.strftime('%Y/%m/%d')} - {week_end.strftime('%Y/%m/%d')}"
        date_ranges.append(date_range)
        counts.append(result['comment_count'])

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(date_ranges, counts, marker='o')
    plt.title('Number of Comments Written per Week')
    plt.xlabel('Date Range')
    plt.ylabel('Number of Comments')

    # Adjust x-axis labels: smaller font and horizontal alignment
    plt.xticks(rotation=0, fontsize=8)  # Change rotation to 0 and adjust font size as needed
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object to send as a response
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Send the image in the response
    return send_file(img, mimetype='image/png')

@statistic_reports_blueprint.route('/getTop3MostActiveUsersReport', methods=['GET'])
def get_top_three_most_active_users_report():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # SQL query to fetch the top 3 users based on total comments and reviews
    query = """
    SELECT u.username, SUM(total_activities) as total_activities
    FROM (
        SELECT user_id, COUNT(*) as total_activities FROM reviews GROUP BY user_id
        UNION ALL
        SELECT user_id, COUNT(*) FROM comments GROUP BY user_id
    ) as combined
    INNER JOIN users u ON combined.user_id = u.user_id
    GROUP BY combined.user_id
    ORDER BY total_activities DESC
    LIMIT 3
    """


    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    db.close()

    # Process the results for plotting
    usernames = [result['username'] for result in results]
    activities = [result['total_activities'] for result in results]

    # Generate the bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(usernames, activities, color='blue')
    plt.title('Top 3 Most Active Users')
    plt.xlabel('Username')
    plt.ylabel('Total Number of Comments and Reviews')

    plt.xticks(usernames)  # Set user IDs as x-axis labels
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Send the image in the response
    return send_file(img, mimetype='image/png')