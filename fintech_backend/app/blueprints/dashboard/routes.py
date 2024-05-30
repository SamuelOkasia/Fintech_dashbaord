from flask import Blueprint, jsonify, request, current_app
from app.models import FinancialData
from datetime import datetime
from app import db



dashboard_blueprint = Blueprint('Upload', __name__)

@dashboard_blueprint.route('/get_data', methods=['GET'])
def dashboard():
    # Get the current year and the previous year
    current_year = datetime.now().year
    previous_year = current_year - 1

    # Helper function to calculate percentage difference
    def calculate_percentage_difference(current, previous):
        if previous == 0:
            return 0
        return round(((current - previous) / previous) * 100)

    # Query the total revenue for the current year
    total_revenue_current = db.session.query(db.func.sum(FinancialData.total_revenue)).filter(
        db.extract('year', FinancialData.date) == current_year).scalar()

    # Query the total revenue for the previous year
    total_revenue_previous = db.session.query(db.func.sum(FinancialData.total_revenue)).filter(
        db.extract('year', FinancialData.date) == previous_year).scalar()

    # Query the total expenses for the current year
    total_expenses_current = db.session.query(db.func.sum(FinancialData.total_expenses)).filter(
        db.extract('year', FinancialData.date) == current_year).scalar()

    # Query the total expenses for the previous year
    total_expenses_previous = db.session.query(db.func.sum(FinancialData.total_expenses)).filter(
        db.extract('year', FinancialData.date) == previous_year).scalar()

    # Query the net profit for the current year
    net_profit_current = db.session.query(db.func.sum(FinancialData.net_profit)).filter(
        db.extract('year', FinancialData.date) == current_year).scalar()

    # Query the net profit for the previous year
    net_profit_previous = db.session.query(db.func.sum(FinancialData.net_profit)).filter(
        db.extract('year', FinancialData.date) == previous_year).scalar()

    # Query the cash flow for the current year
    cash_flow_current = db.session.query(db.func.sum(FinancialData.net_cash_flow)).filter(
        db.extract('year', FinancialData.date) == current_year).scalar()

    # Query the cash flow for the previous year
    cash_flow_previous = db.session.query(db.func.sum(FinancialData.net_cash_flow)).filter(
        db.extract('year', FinancialData.date) == previous_year).scalar()

    # Calculate percentage differences
    revenue_diff_percentage = calculate_percentage_difference(total_revenue_current, total_revenue_previous)
    expenses_diff_percentage = calculate_percentage_difference(total_expenses_current, total_expenses_previous)
    profit_diff_percentage = calculate_percentage_difference(net_profit_current, net_profit_previous)
    cash_flow_diff_percentage = calculate_percentage_difference(cash_flow_current, cash_flow_previous)

    # Construct the response
    response = {
        'total_revenue': total_revenue_current or 0,
        'total_expenses': total_expenses_current or 0,
        'net_profit': net_profit_current or 0,
        'cash_flow': cash_flow_current or 0,
        'revenue_diff_percentage': revenue_diff_percentage,
        'expenses_diff_percentage': expenses_diff_percentage,
        'profit_diff_percentage': profit_diff_percentage,
        'cash_flow_diff_percentage': cash_flow_diff_percentage
    }

    return jsonify(response)


@dashboard_blueprint.route('/revenue_trend', methods=['GET'])
def revenue_trend():
    current_year = datetime.now().year
    previous_year = current_year - 1

    current_year_data = db.session.query(FinancialData).filter(
        db.extract('year', FinancialData.date) == current_year).all()
    previous_year_data = db.session.query(FinancialData).filter(
        db.extract('year', FinancialData.date) == previous_year).all()

    def get_monthly_totals(data):
        monthly_totals = [0] * 12
        for entry in data:
            month = entry.date.month - 1  # Convert to zero-indexed month
            monthly_totals[month] += entry.total_revenue
        return monthly_totals

    current_year_totals = get_monthly_totals(current_year_data)
    previous_year_totals = get_monthly_totals(previous_year_data)

    response = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December'],
        'currentYear': current_year_totals,
        'previousYear': previous_year_totals
    }

    return jsonify(response)

@dashboard_blueprint.route('/expenses_breakdown', methods=['GET'])
def expenses_breakdown():
    current_year = datetime.now().year

    expenses = db.session.query(
        db.func.sum(FinancialData.operational_expenses).label('Operational Expenses'),
        db.func.sum(FinancialData.salaries).label('Salaries'),
        db.func.sum(FinancialData.marketing_expenses).label('Marketing Expenses'),
        db.func.sum(FinancialData.rd_expenses).label('R&D Expenses'),
        db.func.sum(FinancialData.miscellaneous_expenses).label('Miscellaneous Expenses')
    ).filter(db.extract('year', FinancialData.date) == current_year).first()

    response = [
        {'value': expenses[0] or 0, 'name': 'Operational Expenses'},
        {'value': expenses[1] or 0, 'name': 'Salaries'},
        {'value': expenses[2] or 0, 'name': 'Marketing Expenses'},
        {'value': expenses[3] or 0, 'name': 'R&D Expenses'},
        {'value': expenses[4] or 0, 'name': 'Miscellaneous Expenses'}
    ]

    return jsonify(response)

@dashboard_blueprint.route('/monthly_profits_losses', methods=['GET'])
def monthly_profits_losses():
    current_year = datetime.now().year

    # Query to get monthly net profit and loss for the current year
    monthly_data = db.session.query(
        db.extract('month', FinancialData.date).label('month'),
        db.func.sum(FinancialData.net_profit).label('net_profit')
    ).filter(
        db.extract('year', FinancialData.date) == current_year
    ).group_by(
        db.extract('month', FinancialData.date)
    ).order_by(
        db.extract('month', FinancialData.date)
    ).all()

    labels = ['January', 'February', 'March', 'April', 'May']
    # labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    profits = [0] * 12
    losses = [0] * 12

    for data in monthly_data:
        month_index = int(data.month) - 1
        if data.net_profit >= 0:
            profits[month_index] = data.net_profit
        else:
            losses[month_index] = abs(data.net_profit)

    response = {
        'labels': labels,
        'profits': profits,
        'losses': losses
    }

    return jsonify(response)