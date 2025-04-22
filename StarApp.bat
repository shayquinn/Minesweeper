::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFAhcTR2RAES0A5EO4f7+086CsUYJW/IDVYbV36eZJeUD71f3SoEiwXVIk8ICCyRbcQKyUiI9p2tRoWGAJ8KOjwbiRUaa2lg+EnU6jmDf7A==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSzk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFAhcTR2RAES0A5EO4f7+086CsUYJW/IDVYbV36eZJeUD71f3SoEiwXVIk8ICCyRbcQKyUiI9p2tRoWGAJ8KOjyLSdW2xwwU1A2AU
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
REM Check if MyVenv already exists
IF NOT EXIST MyVenv\ (
    python -m venv MyVenv
)

start /B "" cmd /C "call .\MyVenv\Scripts\activate && pythonw src\minesweeper.py"
exit