@app.route("/faults/delete/<int:fault_id>", methods=["POST"])
@login_required
def delete_fault(fault_id):
    """Delete a fault"""
    if current_user.role != "admin":
        flash("فقط المدير يمكنه حذف الأعطال ❌", "danger")
        return redirect(url_for("dashboard"))
    
    fault = Fault.query.get_or_404(fault_id)
    
    try:
        # Check for any dependencies before deleting
        if fault.bbm_faults:
            error_msg = f"لا يمكن حذف العطل #{fault.id} لأنه مرتبط بأعطال BBM ❌"
            
            # Check if this is an AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                     request.content_type and 'application/json' in request.content_type
            
            if is_ajax:
                return jsonify({"success": False, "message": error_msg})
            else:
                flash(error_msg, "danger")
                return redirect(url_for("all_faults"))
        
        db.session.delete(fault)
        db.session.commit()
        
        success_msg = f"تم حذف العطل #{fault.id} بنجاح ✅"
        
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                 request.content_type and 'application/json' in request.content_type
        
        if is_ajax:
            return jsonify({"success": True, "message": success_msg})
        else:
            flash(success_msg, "success")
            return redirect(url_for("all_faults"))
        
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        
        # Handle specific database errors
        if "FOREIGN KEY constraint" in error_msg:
            error_msg = f"لا يمكن حذف العطل #{fault.id} لأنه مرتبط ببيانات أخرى في النظام ❌"
        elif "no such table" in error_msg:
            error_msg = f"خطأ في قاعدة البيانات: {error_msg} ❌"
        else:
            error_msg = f"حدث خطأ أثناء حذف العطل: {error_msg} ❌"
        
        # Log the error for debugging
        print(f"Error deleting fault {fault_id}: {error_msg}")
        
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                 request.content_type and 'application/json' in request.content_type
        
        if is_ajax:
            return jsonify({"success": False, "message": error_msg})
        else:
            flash(error_msg, "danger")
            return redirect(url_for("all_faults"))
