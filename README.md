🛡️ Windows Güvenlik Kalkanı / Windows Security Shield
Python ve modern web teknolojileri (HTML/CSS/JS) kullanılarak geliştirilmiş; Windows sistemlerinin güvenlik durumunu analiz eden, iyileştirmeler öneren ve kullanıcıya tam kontrol sağlayan bir masaüstü uygulaması.


(Uygulamanın ana paneli)
🇹🇷 Türkçe
🚀 Özellikler
* Genel Güvenlik Durumu: Antivirüs ve Güvenlik Duvarı'nın aktif olup olmadığını tek bir panelde gösterir.
* Gelişmiş İşlem Yöneticisi:
   * Çalışan tüm işlemleri PID, isim, kullanıcı, CPU ve Bellek kullanımı gibi detaylarla listeler.
   * İşlemlerin çalıştığı dosya yolunu analiz ederek Potansiyel Şüpheli veya Güvenli olarak sınıflandırır.
   * Tek bir tıkla şüpheli veya istenmeyen işlemleri sonlandırma imkanı sunar.
* Başlangıç Programları Kontrolü: Windows başlangıcında otomatik olarak çalışan programları listeleyerek sistemin açılışını yavaşlatan veya gizlice çalışan yazılımları tespit etmeyi kolaylaştırır.
* Modern Arayüz: Geleneksel Windows araçlarının aksine, modern, akıcı ve anlaşılır bir kullanıcı arayüzü sunar.
🛠️ Kullanılan Teknolojiler
* Backend: Python
* Arayüz (GUI): Eel (HTML, CSS, JavaScript)
* Sistem Erişimi: psutil, wmi, pywin32
* Paketleme: PyInstaller
⚙️ Kurulum ve Çalıştırma
Gereksinimler
1. Python 3.8+: Python'un resmi sitesinden indirip kurun.
2. Yönetici İzinleri: Uygulamanın sistem bilgilerine erişebilmesi için yönetici olarak çalıştırılması zorunludur.
Adımlar
1. Bu depoyu klonlayın veya dosyaları indirin.
2. Terminali açıp projenin ana klasörüne gidin ve gerekli Python kütüphanelerini yükleyin.
pip install eel wmi psutil pywin32

3. Uygulamayı çalıştırmak için run.bat dosyasına çift tıklayın. Bu dosya, gerekli olan yönetici izinlerini otomatik olarak isteyecektir.
📦 .EXE Haline Getirme
Projenin kaynak kodunu tek bir .exe dosyasına dönüştürmek için:
   1. PyInstaller'ı yükleyin: pip install pyinstaller
   2. Proje ana klasöründe yönetici olarak bir terminal açın ve aşağıdaki komutu çalıştırın:
pyinstaller --noconfirm --onefile --windowed --add-data "web;web" main.py

   3. Oluşturulan .exe dosyası dist klasörünün içinde yer alacaktır.
🇬🇧 English
🚀 Features
      * General Security Dashboard: Displays the status of the Antivirus and Firewall in a single panel.
      * Advanced Process Manager:
      * Lists all running processes with details like PID, name, user, CPU, and Memory usage.
      * Analyzes the file path of processes to classify them as Potentially Suspicious or Safe.
      * Provides the ability to terminate suspicious or unwanted processes with a single click.
      * Startup Programs Control: Lists programs that run automatically on Windows startup, making it easy to identify software that slows down the system or runs covertly.
      * Modern UI: Offers a modern, fluid, and intuitive user interface, unlike traditional Windows tools.
🛠️ Tech Stack
      * Backend: Python
      * GUI: Eel (HTML, CSS, JavaScript)
      * System Access: psutil, wmi, pywin32
      * Packaging: PyInstaller
⚙️ Setup and Run
Prerequisites
      1. Python 3.8+: Download and install from python.org.
      2. Administrator Privileges: The application must be run as an administrator to access system information.
Steps
      1. Clone this repository or download the files.
      2. Open a terminal, navigate to the project's root directory, and install the required Python libraries:
pip install eel wmi psutil pywin32

      3. To run the application, double-click the run.bat file. It will automatically request the necessary administrator privileges.
📦 Packaging into .EXE
To convert the source code into a single .exe file:
         1. Install PyInstaller: pip install pyinstaller
         2. Open a terminal with administrator privileges in the project's root directory and run the following command:
pyinstaller --noconfirm --onefile --windowed --add-data "web;web" main.py

         3. The generated .exe file will be located in the dist folder.