@echo off
call env\Scripts\activate.bat
python -m event_ticket_booking
deactivate
pause