from flask import Blueprint, render_template, request, redirect, url_for, session
import modules.database as database
from modules.auth import login_required

maintenance_bp = Blueprint('maintenance', __name__, template_folder='templates')

@maintenance_bp.route('/maintenance')
@login_required
def maintenance():
    maintenance_list = database.get().get_all_maintenance()
    bikes = database.get().get_bikes_for_maintenance()
    return render_template('maintenance.html', maintenance=maintenance_list, bikes=bikes)

@maintenance_bp.route('/maintenance/new', methods=['GET', 'POST'])
@login_required
def new_maintenance():
    if request.method == 'POST':
        data = {
            'bike_id': request.form.get('bike_id'),
            'staff_id': session.get("staff_id"),
            'maintenance_date': request.form.get('maintenance_date'),
            'maintenance_type': request.form.get('maintenance_type'),
            'description': request.form.get('description'),
            'outcome': request.form.get('outcome') or 'parts_needed'
        }
        mid = database.get().create_maintenance(data)
        database.get().log_action(session.get("staff_id"), "create", "maintenance", mid)
        return redirect(url_for('maintenance.maintenance_detail', mid=mid))
    
    bikes = database.get().get_bikes_for_maintenance()
    return render_template('forms/maintenance_form.html', bikes=bikes, maintenance=None, selected_bike_id=request.args.get("bike_id"))

@maintenance_bp.route('/maintenance/<int:mid>', methods=['GET', 'POST'])
@login_required
def maintenance_detail(mid):
    if request.method == 'POST':
        data = {
            'bike_id': request.form.get('bike_id'),
            'maintenance_date': request.form.get('maintenance_date'),
            'maintenance_type': request.form.get('maintenance_type'),
            'description': request.form.get('description'),
            'outcome': request.form.get('outcome')
        }
        database.get().update_maintenance(mid, data)
        database.get().log_action(session.get("staff_id"), "update", "maintenance", mid)
        return redirect(url_for('maintenance.maintenance'))
    
    maintenance_record = database.get().get_maintenance(mid)
    bikes = database.get().get_bikes_for_maintenance()
    return render_template('forms/maintenance_form.html', bikes=bikes, maintenance=maintenance_record)
