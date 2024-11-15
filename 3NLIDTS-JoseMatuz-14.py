# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 20:49:16 2024

@author: ProtofurOwO
"""


import tkinter as tk
from tkinter import messagebox
import serial 
import time
import threading
import mysql.connector

arduino_port = "COM3"
baud_rate=9600
arduino = None 




def insertarRegistro (lim, tem): 
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Timeshirt#21", 
            database="programacionavanzada" 
        )
        cursor = conexion.cursor()      
        query = "INSERT INTO temperaturas (limite, temperatura)" +"VALUES (%s, %s)"
        valores = (lim, tem)
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Información", "Datos guardados en la base de datos con éxito.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar los datos: {err}")

def guardar():
    lim = tbLimTemp.get()
    tem = lbTemp.cget("text")
    insertarRegistro (lim, tem)
    
def conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)
        lbConection.config(text="Estado: Conectado", fg="green") 
        messagebox.showinfo("Conexión", "Conexión establecida.")
        start_reading()
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino. Verifique la conexion")

def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConection.config(text="Estado: Desconectado", fg="red") 
        messagebox.showinfo("Conexión", "Conexión terminada.")
    else:
        messagebox.showwarning("Advertencia", "No hay conexión activa.")
        


def limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimTemp.get()
            if limite.isdigit(): 
                arduino.write(f"{limite}\n".encode())
                messagebox.showinfo("Enviado", f"Límite de temperatura ({limite}°C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numérico para el límite.")
        except Exception as e:
            messagebox. showerror("Error", f"No se pudo enviar el limite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conéctese al Arduino antes de enviar el límite.")
        

def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip() 
            if "Temperatura" in data:
                temp_value = data.split(":")[1].strip().split(" ")[0] 
                lbTemp.config(text=f"{temp_value} °C")
            time.sleep(1)
        except Exception as e:
            print("Error Leyendo datos: {e}")
            break
        


def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()


root = tk.Tk()
root.title("Interfaz de Monitoreo de Temperatura")
root.geometry("300x350")

lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Arial", 12)) 
lbTitleTemp.pack(pady=10)
lbTemp = tk.Label(root, text="0.0°C", font=("Arial", 24))
lbTemp.pack()
lbConection = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Arial", 10)) 
lbConection.pack(pady=5)
lbLimitTemp = tk. Label(root, text="Límite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimTemp = tk.Entry(root, width=10) 
tbLimTemp.pack(pady=5)
btnEnviar = tk.Button(root, text="Enviar Límite", command=limite, font=("Arial", 10)) 
btnEnviar.pack(pady=5)
btnguardar = tk.Button(root, text="Guardar a base", command=guardar, font=("Arial", 10)) 
btnguardar.pack(pady=5)
btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Arial", 10)) 
btnConectar.pack(pady=5)
btnDesconectar = tk. Button (root, text="Desconectar", command=desconectar, font=("Arial", 10)) 
btnDesconectar.pack (pady=5)

root.mainloop()