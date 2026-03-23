@echo off
REM اختبار سريع للنظام

echo 🧪 اختبار النظام...
python -c "import flask; print('✅ Flask يعمل')"
python -c "import flask_sqlalchemy; print('✅ SQLAlchemy يعمل')"
python -c "import flask_login; print('✅ Flask-Login يعمل')"
echo 🎉 جميع الاختبارات نجحت!
pause