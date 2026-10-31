@echo off
chcp 65001 >nul
title FoMT Studio - Instalador y Lanzador
cd /d "%~dp0FOMT_Studio"

REM --- Si ya esta instalado, abrir directamente ---
if exist ".venv\Scripts\pythonw.exe" goto abrir

echo ============================================================
echo  Primera vez: instalando FoMT Studio (tarda 2-5 minutos)
echo  Necesita internet. No cierres esta ventana.
echo ============================================================
echo.

REM --- Buscar Python ---
set PYCMD=
where py >nul 2>nul && set PYCMD=py -3
if "%PYCMD%"=="" (
    where python >nul 2>nul && set PYCMD=python
)
if "%PYCMD%"=="" (
    echo [ERROR] No se encontro Python en este equipo.
    echo.
    echo Instalalo desde https://www.python.org/downloads/
    echo IMPORTANTE: marca la casilla "Add python.exe to PATH" al instalar.
    echo Luego vuelve a abrir este archivo.
    echo.
    pause
    exit /b 1
)

%PYCMD% -m venv .venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno. Revisa la guia.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Fallo la descarga de componentes. Revisa tu internet y reintenta.
    pause
    exit /b 1
)

echo.
echo Instalacion completa.

:abrir
start "" ".venv\Scripts\pythonw.exe" main.py
