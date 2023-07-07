@echo off

py editor_xlsx.py
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Finalizado!', 'Relatório de lucratividade', 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);}"