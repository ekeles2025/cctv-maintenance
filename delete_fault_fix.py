@app.route("/faults/delete/<int:fault_id>", methods=["POST"])
@login_required
def delete_fault(fault_id):
    """Delete a fault"""
    if current_user.role != "admin":
        flash("فقط المدير يمكنه حذف الأعطال ❌", "danger")
        return redirect(url_for("dashboard"))
    
    fault = Fault.query.get_or_404(fault_id)
    
    try:
        # تسجيل معلومات العطل قبل الحذف
        fault_info = f"العطل #{fault.id} - {fault.description[:50]}..."
        logger.info(f"Attempting to delete {fault_info} by user {current_user.username}")
        
        # حذف العطل
        db.session.delete(fault)
        db.session.commit()
        
        logger.info(f"Successfully deleted {fault_info}")
        flash(f"تم حذف العطل #{fault.id} بنجاح ✅ - تم إزالته من صفحة جميع الأعطال", "success")
        
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        logger.error(f"Error deleting fault #{fault_id}: {error_msg}", exc_info=True)
        
        # رسائل خطأ مفصلة حسب نوع الخطأ
        if "foreign key constraint" in error_msg.lower():
            flash(f"لا يمكن حذف العطل لأنه مرتبط ببيانات أخرى. يرجى مراجعة الفني أولاً ❌", "danger")
        elif "no such row" in error_msg.lower():
            flash(f"العطل غير موجود أو تم حذفه بالفعل ❌", "warning")
        else:
            flash(f"حدث خطأ أثناء حذف العطل: {error_msg} ❌", "danger")
    
    return redirect(url_for("all_faults"))
