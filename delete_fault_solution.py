# هذا الملف يحتوي على دالة حذف العطل الصحيحة
# استبدل دالة delete_fault التالفة في app.py بهذه الدالة

@app.route("/faults/delete/<int:fault_id>", methods=["POST"])
@login_required
def delete_fault(fault_id):
    """Delete a fault"""
    if current_user.role != "admin":
        flash("فقط المدير يمكنه حذف الأعطال ❌", "danger")
        return redirect(url_for("dashboard"))
    
    fault = Fault.query.get_or_404(fault_id)
    
    try:
        db.session.delete(fault)
        db.session.commit()
        flash(f"تم حذف العطل #{fault.id} بنجاح ✅", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"حدث خطأ: {str(e)} ❌", "danger")
    
    return redirect(url_for("all_faults"))
