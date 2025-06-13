import eel
import platform
import sys
import ctypes
import wmi
import psutil
import os
import winreg # Başlangıç programları için

# Uygulamanın arayüz dosyalarının bulunduğu klasörü belirtiyoruz
eel.init('web')

def is_admin():
    """Yönetici izinlerini kontrol eder."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# --- YENİ: Güvenli ve Şüpheli Konumları Tanımlama ---
# Genellikle güvenli olan sistem yolları
SAFE_PATHS = [
    os.environ.get('SystemRoot', 'C:\\Windows').lower(),
    os.environ.get('ProgramFiles', 'C:\\Program Files').lower(),
    os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)').lower()
]
# Potansiyel olarak şüpheli olan kullanıcı yolları
SUSPICIOUS_PATHS = [
    os.environ.get('AppData', '').lower(),
    os.environ.get('LOCALAPPDATA', '').lower(),
    os.environ.get('Temp', '').lower(),
    os.environ.get('UserProfile', '').lower()
]

@eel.expose
def get_security_status():
    """Güvenlik duvarı ve antivirüs durumunu kontrol eder."""
    status = { 'firewall': 'Bilinmiyor', 'antivirus': 'Bilinmiyor' }
    try:
        w = wmi.WMI(namespace="root/SecurityCenter2")
        
        av_products = w.AntiVirusProduct()
        status['antivirus'] = 'Yüklü değil'
        for product in av_products:
            if product.displayName:
                if product.productState in [397312, 393216]:
                    status['antivirus'] = f"Aktif ({product.displayName})"
                else:
                    status['antivirus'] = f"Pasif ({product.displayName})"
                break
        
        fw_products = w.FirewallProduct()
        status['firewall'] = 'Pasif veya Bilinmiyor'
        for product in fw_products:
             if product.displayName and product.productState == 397312:
                 status['firewall'] = f"Aktif ({product.displayName})"
                 break
        
        if not fw_products:
             status['firewall'] = 'Aktif (Windows Defender)'
            
    except Exception as e:
        print(f"WMI Hatası: {e}")
        status['firewall'] = 'Erişilemedi'
        status['antivirus'] = 'Erişilemedi'
    return status

@eel.expose
def get_running_processes():
    """Çalışan tüm işlemleri listeler ve yollarına göre itibar durumlarını belirler."""
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'exe', 'cpu_percent']):
        try:
            p_info = p.as_dict(attrs=['pid', 'name', 'username', 'memory_info', 'exe', 'cpu_percent'])
            p_info['memory_mb'] = round(p_info['memory_info'].rss / (1024 * 1024), 2) if p_info.get('memory_info') else 0
            
            # --- YENİ: İtibar Durumu Mantığı ---
            p_info['reputation'] = 'Güvenli' # Varsayılan olarak güvenli
            exe_path = (p_info.get('exe') or "").lower()

            if exe_path:
                # Eğer dosya yolu şüpheli bir klasörde başlıyorsa ve sistem dosyası değilse
                is_in_suspicious = any(exe_path.startswith(path) for path in SUSPICIOUS_PATHS if path)
                is_in_safe = any(exe_path.startswith(path) for path in SAFE_PATHS if path)

                if is_in_suspicious and not is_in_safe:
                    p_info['reputation'] = 'Potansiyel Şüpheli'
            else:
                 p_info['reputation'] = 'Bilinmiyor' # Yolu alınamayanlar (genellikle sistemin çekirdek işlemleri)

            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)

@eel.expose
def terminate_process(pid):
    """Verilen PID'ye sahip işlemi sonlandırır."""
    try:
        p = psutil.Process(pid)
        p.terminate() # İşlemi sonlandır
        print(f"[BAŞARI] PID {pid} olan işlem sonlandırıldı.")
        return {"success": True, "message": f"PID {pid} olan işlem sonlandırıldı."}
    except psutil.NoSuchProcess:
        return {"success": False, "message": "İşlem zaten kapatılmış."}
    except psutil.AccessDenied:
        return {"success": False, "message": "Bu işlemi sonlandırmak için yetkiniz yok."}
    except Exception as e:
        return {"success": False, "message": f"Bir hata oluştu: {e}"}

@eel.expose
def get_startup_programs():
    """Windows başlangıcında çalışan programları listeler."""
    startup_programs = []
    key_paths = [
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
    ]
    for hkey, path in key_paths:
        try:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_programs.append({"name": name, "path": value, "enabled": True})
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Başlangıç programları okunurken hata: {e}")
            
    return startup_programs

# Ana program bloğu
if __name__ == "__main__":
    if platform.system() == "Windows" and not is_admin():
        print("\n[HATA] YÖNETİCİ İZNİ GEREKLİ!")
        print("Bu programın sistem bilgilerine erişebilmesi için Yönetici olarak çalıştırılması gerekir.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
            
    eel.start('index.html', size=(1280, 800), port=0)
