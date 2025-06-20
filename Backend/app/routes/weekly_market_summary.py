from flask import Blueprint, request, jsonify
from app.models.WeeklyMarketSummary import WeeklyMarketSummary
from app import db
from datetime import datetime

weekly_market_summary_bp = Blueprint('weekly_market_summary', __name__)

@weekly_market_summary_bp.route('/weekly_market_summary', methods=['POST'])
def create_summary():
    data = request.get_json()
    try:
        summary = WeeklyMarketSummary(
            county=data['county'],
            week_start_date=datetime.fromisoformat(data['week_start_date']),
            week_end_date=datetime.fromisoformat(data['week_end_date']),
            demand_data=data.get('demand_data'),
            total_sales=data['total_sales'],
            total_units_sold=data['total_units_sold'],
            average_price_per_unit=data['average_price_per_unit']
        )
        db.session.add(summary)
        db.session.commit()
        return jsonify({'message': 'Weekly market summary created', 'id': summary.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@weekly_market_summary_bp.route('/weekly_market_summary/<int:summary_id>', methods=['GET'])
def get_summary(summary_id):
    summary = WeeklyMarketSummary.query.get(summary_id)
    if not summary:
        return jsonify({'error': 'Summary not found'}), 404
    return jsonify({
        'id': summary.id,
        'county': summary.county,
        'week_start_date': summary.week_start_date.isoformat() if summary.week_start_date else None,
        'week_end_date': summary.week_end_date.isoformat() if summary.week_end_date else None,
        'demand_data': summary.demand_data,
        'total_sales': summary.total_sales,
        'total_units_sold': summary.total_units_sold,
        'average_price_per_unit': summary.average_price_per_unit
    }), 200

@weekly_market_summary_bp.route('/weekly_market_summary', methods=['GET'])
def list_summaries():
    summaries = WeeklyMarketSummary.query.all()
    result = []
    for summary in summaries:
        result.append({
            'id': summary.id,
            'county': summary.county,
            'week_start_date': summary.week_start_date.isoformat() if summary.week_start_date else None,
            'week_end_date': summary.week_end_date.isoformat() if summary.week_end_date else None,
            'demand_data': summary.demand_data,
            'total_sales': summary.total_sales,
            'total_units_sold': summary.total_units_sold,
            'average_price_per_unit': summary.average_price_per_unit
        })
    return jsonify(result), 200