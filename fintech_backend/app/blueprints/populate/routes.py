from flask import Blueprint, jsonify, request, current_app
from app import db
import csv
from app.models import FinancialData
from datetime import datetime
import os


populate_blueprint = Blueprint('Populate', __name__)

@populate_blueprint.route('/populate_data', methods=['GET'])
def populate():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'MOCK_DATA.csv')

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = FinancialData(
                date=datetime.strptime(row['Date'], '%Y-%m-%d'),
                total_revenue=float(row['Total_Revenue']),
                revenue_by_product=row['Revenue_by_Product'],
                revenue_by_service=row['Revenue_by_Service'],
                revenue_by_region=row['Revenue_by_Region'],
                total_expenses=float(row['Total_Expenses']),
                operational_expenses=float(row['Operational_Expenses']),
                salaries=float(row['Salaries']),
                marketing_expenses=float(row['Marketing_Expenses']),
                rd_expenses=float(row['RD_Expenses']),
                miscellaneous_expenses=float(row['Miscellaneous_Expenses']),
                gross_profit=float(row['Gross_Profit']),
                net_profit=float(row['Net_Profit']),
                profit_margin_percentage=float(row['Profit_Margin_Percentage']),
                cash_inflows=float(row['Cash_Inflows']),
                cash_outflows=float(row['Cash_Outflows']),
                net_cash_flow=float(row['Net_Cash_Flow']),
                cash_flow_from_operating_activities=float(row['Cash_Flow_from_Operating_Activities'])
            )
            db.session.add(data)
        db.session.commit()

        print('done')
        return {'value':'done'}

